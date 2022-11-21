import numpy as np

a = np.ravel([[1,2,3,4],[3,4,5,6],[1,2,3,4],[3,4,5,6]])
b = np.ravel([[1,2,3,4],[3,4,5,6],[1,2,3,4],[3,4,5,6]])
c = np.ravel([[1,2,3,4],[3,4,5,6],[1,2,3,4],[3,4,5,6]])
row_len = 4
stacked = np.vstack((a,b,c))
map = stacked.T
map = np.reshape(map, (np.size(map, axis=0) // row_len, row_len, 3))
print("helo")