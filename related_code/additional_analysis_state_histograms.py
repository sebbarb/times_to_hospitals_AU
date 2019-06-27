import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pdb import set_trace as bp

if __name__ == '__main__':
  # histograms of distances to hospitals for each Australian state
  dtype = {'MB_CODE16': 'int64',
           'STE_CODE16': 'int32',
           'STE_NAME16': 'object'}
  ste_codes = pd.read_csv('../data/processed/mb_2016_centroids.csv', usecols=dtype.keys(), dtype=dtype)

  df = pd.read_pickle('../data/processed/duration_mb_hospital_shortest.pkl')
  df.dropna(subset=['shortest_time_sec'], inplace=True)
  df = pd.merge(df, ste_codes, how='left', on=['MB_CODE16'])

  cmap = cm.get_cmap('Dark2')
  fig, ax = plt.subplots(nrows=8, sharex=True, sharey=True)
  
  for ste_code in range(1, 9):
    id = ste_code-1
    ax[id].hist(df.loc[df['STE_CODE16']==ste_code, 'shortest_time_min'], bins=50, range=(0,50), density=True, 
                weights=df.loc[df['STE_CODE16']==ste_code, 'Person'],
                color=cmap(id))
    ax[id].annotate(df.loc[df['STE_CODE16']==ste_code, 'STE_NAME16'].iloc[0], xy=(34, 0.04))
    ax[id].spines['right'].set_visible(False)
    ax[id].spines['top'].set_visible(False)
    ax[id].spines['left'].set_visible(False)
    ax[id].get_yaxis().set_visible(False)
  ax[7].set_xlabel('Time to Hospital [min]')
  
  fig.tight_layout()
  plt.savefig('../fig/state_histograms.pdf', bbox_inches='tight')

  