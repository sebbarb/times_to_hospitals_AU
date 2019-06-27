import numpy as np
import pandas as pd
from tqdm import tqdm
from pdb import set_trace as bp

if __name__ == '__main__':
  # compute distances between sa2 and hospitals
  df = pd.read_pickle('../data/processed/duration_mb_hospitals.pkl')
  num_hospitals = 1011
  frames = []
  for i in tqdm(range(num_hospitals)):
    df['weight'] = df['Person']
    df.loc[df['time_to_' + str(i+1)].isna(), 'weight'] = 0
    df['time_to_' + str(i+1)].fillna(0, inplace=True)
    # compute weighted average of distances
    df_sa2 = df.groupby(['SA2_5DIG16']).apply(lambda x: pd.Series(np.ma.average(x['time_to_' + str(i+1)], weights=x['weight'], axis=0), ['time_to_' + str(i+1)]))
    frames.append(df_sa2)
  df_sa2 = pd.concat(frames, axis=1)
  df_sa2.reset_index(level=0, inplace=True)
  # save
  df_sa2.to_pickle('../data/processed/duration_sa2_hospitals.pkl')
  df_sa2.to_csv('../data/processed/duration_sa2_hospitals.csv', index=False)
  