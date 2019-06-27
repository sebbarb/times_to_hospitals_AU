import numpy as np
import pandas as pd
from pdb import set_trace as bp

if __name__ == '__main__':
  # compute shortest time to hospital for each mesh block
  df = pd.read_pickle('../data/processed/duration_mb_hospitals.pkl')
  df['shortest_time_sec'] = df.loc[:, df.columns.str.startswith('time_to_')].min(axis=1)
  df['shortest_time_min'] = np.ceil(df['shortest_time_sec']/60)
  df = df.loc[:, ~df.columns.str.startswith('time_to_')]
  df.to_pickle('../data/processed/duration_mb_hospital_shortest.pkl')
  df.to_csv('../data/processed/duration_mb_hospital_shortest.csv', index=False)

  # compute shortest time to hospital for each SA2
  # df = pd.read_pickle('../data/processed/duration_mb_hospital_shortest.pkl')
  # weights for weighted averages of shortest distances
  df['weight'] = df['Person']
  df.loc[df['shortest_time_sec'].isna(), 'weight'] = 0
  df['shortest_time_sec'].fillna(0, inplace=True)
  # compute weighted average of distances
  df_sa2 = df.groupby(['SA2_5DIG16']).apply(lambda x: pd.Series(np.ma.average(x['shortest_time_sec'], weights=x['weight'], axis=0), ['shortest_time_sec']))
  df_sa2.reset_index(level=0, inplace=True)
  df_sa2['shortest_time_min'] = np.ceil(df_sa2['shortest_time_sec']/60)
  # save
  df_sa2.to_pickle('../data/processed/duration_sa2_hospital_shortest.pkl')
  df_sa2.to_csv('../data/processed/duration_sa2_hospital_shortest.csv', index=False)
  