import numpy as np
import pandas as pd
from pdb import set_trace as bp

if __name__ == '__main__':
  # merge computational blocks (distances between mesh blocks and hospitals)
  chunk0 = pd.read_pickle('../data/processed/duration_mb_hospitals_0_100000.pkl')
  chunk1 = pd.read_pickle('../data/processed/duration_mb_hospitals_100000_200000.pkl')
  chunk2 = pd.read_pickle('../data/processed/duration_mb_hospitals_200000_300000.pkl')
  chunk3 = pd.read_pickle('../data/processed/duration_mb_hospitals_300000_358122.pkl')
  df = pd.concat([chunk0, chunk1, chunk2, chunk3])
  df.to_pickle('../data/processed/duration_mb_hospitals.pkl')

  