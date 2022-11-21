import time
import pandas as pd
import numpy as np
from tqdm import tqdm

start = time.time()
x = np.ravel(pd.read_csv("C:/Users/hudso/Documents/Programming/Unity & C#/NASA ADC/Downloaded_Files/haworth/FY23_ADC_Latitude_Haworth.csv").to_numpy())
y = np.ravel(pd.read_csv("C:/Users/hudso/Documents/Programming/Unity & C#/NASA ADC/Downloaded_Files/haworth/FY23_ADC_Longitude_Haworth.csv").to_numpy())
z = np.ravel(pd.read_csv("C:/Users/hudso/Documents/Programming/Unity & C#/NASA ADC/Downloaded_Files/haworth/FY23_ADC_Height_Haworth.csv").to_numpy())
st = pd.read_csv("C:/Users/hudso/Documents/Programming/Unity & C#/NASA ADC/Downloaded_Files/haworth/FY23_ADC_Slope_Haworth.csv").to_numpy()
s = np.ravel(st)
vis_map = np.ravel(np.random.randint(low=0, high=2, size=st.shape))#temp placeholder for vis map, 0 = not vis 1 = vis
row_len = np.size(st, axis = 1)
elapsed = time.time() - start
print(f"Loading .csv files: {elapsed}")

start = time.time()
stacked = np.vstack((x, y, z, s, vis_map))
elapsed = time.time() - start
print(f"Stacking array: {elapsed}")

start = time.time()
map = stacked.T
map = np.reshape(map, (np.size(map, axis=0) // row_len, row_len, 5))
elapsed = time.time() - start
print(f"Slicing Array into Columns: {elapsed}")

np.savez_compressed("map", map=map)
"""
a = []
for row in tqdm(range(len(s))):
    b = []
    \"""for col in tqdm(range(len(s[0])), leave=False):
        b.append([x[row][col], y[row][col], z[row][col], s[row][col], vis_map[row][col]])
    a.append(b)\"""
    np.vstack[x[row], y[row], z[row], s[row]]
a = np.array(a)
"""
