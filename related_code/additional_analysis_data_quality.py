import numpy as np
import pandas as pd
from pdb import set_trace as bp

if __name__ == '__main__':
  dtype = {'Hospital_ID': 'int32',
           'State': 'object',
           'Latitude': 'float32',
           'Longitude': 'float32'}
  df = pd.read_csv('../data/processed/myhospitals-contact-details.csv', usecols=dtype.keys(), dtype=dtype)
  df['State'] = df['State'].str.lower()

  # sample 10 hospitals for each state and territory
  id_act_nt = ((df['State']=='act') | (df['State']=='nt')) # act and nt have less than 10 hospitals
  df_act_nt = df[id_act_nt]
  df = df[~id_act_nt]
  df = df.groupby('State').apply(lambda x: x.sample(n=10, random_state=42)).reset_index(drop=True)
  df = df.append(df_act_nt)

  df.to_csv('./sample_hospitals.csv', index=False)
