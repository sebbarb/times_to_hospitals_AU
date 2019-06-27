import numpy as np
import pandas as pd
import re
import requests as req
from tqdm import tqdm
from pdb import set_trace as bp

if __name__ == '__main__':
  # compute distances between mesh blocks and hospitals
  dtype = {'MB_CODE16': 'int64',
           'SA2_5DIG16': 'int32',
           'xcoord': 'float32',
           'ycoord': 'float32'}
  mb_2016_centroids = pd.read_csv('../data/processed/mb_2016_centroids.csv', usecols=dtype.keys(), dtype=dtype)

  dtype = {'MB_CODE_2016': 'int64',
           'Person': 'int32'}
  census_2016_mesh_block_counts = pd.read_csv('../data/original/census_2016_mesh_block_counts.csv', usecols=dtype.keys(), dtype=dtype)
  census_2016_mesh_block_counts.rename(columns={'MB_CODE_2016': 'MB_CODE16'}, inplace=True)

  dtype = {'Hospital_ID': 'int32',
           'Latitude': 'float32',
           'Longitude': 'float32'}
  hospitals = pd.read_csv('../data/processed/myhospitals-contact-details.csv', usecols=dtype.keys(), dtype=dtype)

  # add counts
  df = pd.merge(mb_2016_centroids, census_2016_mesh_block_counts, how='left', on='MB_CODE16')
  
  # create string of hospital longitude1,latitude1;longitude2,latitude2;...
  hospital_coordinates = ','.join(map(str, hospitals[['Longitude', 'Latitude']].values.flatten()))
  hospital_coordinates = re.sub('(,[^,]*),', r'\1;', hospital_coordinates)

  # fill distances to hospitals
  num_hospitals = hospitals['Hospital_ID'].max()
  start = '"durations":[[0,'
  end = ']]}'
  chunk = 0 # chunk of data to process
  if chunk == 0:
    df_start, df_end = 0,      100000
  elif chunk == 1:
    df_start, df_end = 100000, 200000
  elif chunk == 2:
    df_start, df_end = 200000, 300000
  elif chunk == 3:
    df_start, df_end = 300000, df.shape[0]
  print([df_start, df_end])
  df = df.iloc[df_start:df_end]
  duration_array = np.full([df.shape[0], num_hospitals], np.nan)
  for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    if (row['Person'] > 0) and (not np.isnan(row['xcoord'])):
      # compute durations
      url = 'http://127.0.0.1:5000/table/v1/driving/' + str(row['xcoord']) + ',' + str(row['ycoord']) + ';' + hospital_coordinates + '?sources=0'
      response = req.get(url)
      
      # extract durations list
      s = response.text
      durations = s[s.find(start)+len(start):s.rfind(end)].split(',')
  
      # fill row
      for hosp in range(num_hospitals):
        try:
          duration_array[index-df_start, hosp] = float(durations[hosp])
        except:
          pass

  # create columns with distances to hospitals
  for i in tqdm(range(num_hospitals)):
    df['time_to_' + str(i+1)] = duration_array[:, i]
      
  # save
  df.to_pickle('../data/processed/duration_mb_hospitals_' + str(df_start) + '_' + str(df_end) + '.pkl')

  
  