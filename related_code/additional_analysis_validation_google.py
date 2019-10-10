import numpy as np
import pandas as pd
from tqdm import tqdm
import requests as req
import statsmodels.stats.api as sms
from pdb import set_trace as bp

if __name__ == '__main__':
  # validate distances using google maps
  # get 1000 sample shortest distances for each state

  # for each mesh block, shortest time to hospital and hospital id
  df = pd.read_pickle('../data/processed/duration_mb_hospitals.pkl')
  df['shortest_time_sec'] = df.loc[:, df.columns.str.startswith('time_to_')].min(axis=1)
  df['Hospital_ID'] = df.loc[:, df.columns.str.startswith('time_to_')].idxmin(axis=1)
  df = df.loc[:, ~df.columns.str.startswith('time_to_')]
  df.dropna(inplace=True)
  df['Hospital_ID'] = df['Hospital_ID'].str.lstrip('time_to_').astype(int)

  # merge state codes
  dtype = {'MB_CODE16': 'int64',
           'STE_CODE16': 'int32',
           'STE_NAME16': 'object'}
  ste_codes = pd.read_csv('../data/processed/mb_2016_centroids.csv', usecols=dtype.keys(), dtype=dtype)
  df = pd.merge(df, ste_codes, how='left', on=['MB_CODE16'])
  
  # merge hospital coordinates
  dtype = {'Hospital_ID': 'int32',
           'Latitude': 'float32',
           'Longitude': 'float32'}
  hospitals = pd.read_csv('../data/processed/myhospitals-contact-details.csv', usecols=dtype.keys(), dtype=dtype)
  hospitals.rename(columns={'Latitude': 'Hospital_Latitude', 'Longitude': 'Hospital_Longitude'}, inplace=True)
  df = pd.merge(df, hospitals, how='left', on=['Hospital_ID'])
  
  # sample 1000 MBs for each state
  df = df[df['STE_CODE16'] < 9] #remove Other Territories
  df = df.groupby('STE_CODE16').apply(lambda x: x.sample(n=1000, random_state=42)).reset_index(drop=True)
  
  # iterate over rows, get travel time from google maps
  start = '<duration>\n<value>'
  end = '</value>'
  duration_array = np.full(df.shape[0], np.nan)
  for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    # compute durations
    url = 'https://maps.googleapis.com/maps/api/distancematrix/xml?origins=' + str(row['ycoord']) + ',' + str(row['xcoord']) + '&destinations=' + str(row['Hospital_Latitude']) + ',' + str(row['Hospital_Longitude']) + '&key=xyz'
    response = req.get(url)
    
    # extract duration
    resp = response.text.replace(' ','')
    try:
      duration_array[index] = float(resp[resp.find(start)+len(start):resp.find(end)])
    except:
      pass

  df['shortest_time_sec_google'] = duration_array
  
  # save
  df.to_pickle('../data/processed/validation_google.pkl')
  
  # load
  df = pd.read_pickle('../data/processed/validation_google.pkl')
  df.dropna(inplace=True)
  df['diff'] = df['shortest_time_sec_google'] - df['shortest_time_sec']
  for ste in range(1, 9):
    df_ste = df[df['STE_CODE16']==ste]
    print(df_ste['STE_NAME16'].iloc[0])
    print([np.round(df_ste['diff'].mean()), np.round(sms.DescrStatsW(df_ste['diff']).tconfint_mean())])
  print('Overall')
  print([np.round(df['diff'].mean()), np.round(sms.DescrStatsW(df['diff']).tconfint_mean())])
        
