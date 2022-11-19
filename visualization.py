import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

start = time.time()
x = pd.read_csv("C:/Users/hudso/Documents/Programming/Unity & C#/NASA ADC/Downloaded_Files/haworth/FY23_ADC_Latitude_Haworth.csv").to_numpy()
y = pd.read_csv("C:/Users/hudso/Documents/Programming/Unity & C#/NASA ADC/Downloaded_Files/haworth/FY23_ADC_Longitude_Haworth.csv").to_numpy()
z = pd.read_csv("C:/Users/hudso/Documents/Programming/Unity & C#/NASA ADC/Downloaded_Files/haworth/FY23_ADC_Height_Haworth.csv").to_numpy()
s = pd.read_csv("C:/Users/hudso/Documents/Programming/Unity & C#/NASA ADC/Downloaded_Files/haworth/FY23_ADC_Slope_Haworth.csv").to_numpy()
elapsed = time.time() - start
print(f"Loading .csv files: {elapsed}")

closed_abst, closed_qua, path_abst, path_qua = np.load("data")

#Print Visualizations
fig = plt.figure()
ax = plt.axes(projection='3d')

#Visualize terrain
ax.scatter3D(x, y, z, c=z, cmap="hsv")
plt.show()
input("Press Enter to Generate Next Image")

#Visualize terrain w/o invalid spots


#Visualize all searched points
ax.scatter3D(
    [i[0] for i in closed_qua], 
    [i[1] for i in closed_qua], 
    [i[2] for i in closed_qua], 
    c=[i[2] for i in closed_qua], 
    cmap='hsv')
plt.show()
for angle in range(0, 360):
    ax.view_init(30, angle)
    plt.draw()
    plt.savefig(f'path_{angle}.png')
input("Press Enter to Generate Next Image")

#Visualize path itself
ax.scatter3D(
    [i[0] for i in path_qua],
    [i[1] for i in path_qua], 
    [i[2] for i in path_qua], 
    c=[i[2] for i in path_qua], 
    cmap='inferno')
plt.show()
for angle in range(0, 360):
    ax.view_init(30, angle)
    plt.draw()
    plt.savefig(f'path_{angle}.png')
input("Press Enter to Generate Next Image")

