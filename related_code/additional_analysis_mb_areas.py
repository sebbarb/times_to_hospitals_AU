import numpy as np
import pandas as pd
from pdb import set_trace as bp

if __name__ == '__main__':
  dtype = {'MB_CODE_2016': 'int64',
           'Person': 'int32',
           'AREA_ALBERS_SQKM': 'float32'}
  df = pd.read_csv('../data/original/census_2016_mesh_block_counts.csv', usecols=dtype.keys(), dtype=dtype)
  df = df[(df['Person'] > 0) & (df['AREA_ALBERS_SQKM'] > 0)]
  print(df['AREA_ALBERS_SQKM'].min())
  print(df['AREA_ALBERS_SQKM'].median())
  print(df['AREA_ALBERS_SQKM'].max())
  
