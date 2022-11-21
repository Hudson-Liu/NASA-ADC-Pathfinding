from mpl_toolkits import mplot3d
import pandas as pd
import matplotlib.pyplot as plt
import time
from tqdm import trange
import itertools
import numpy as np
import math
import os

"""
Data will be measured in 2 distinct coordinate systems:
1. Objective coordinates being longitude, latitude, and height
2. Abstract coordinates representing the column and rows of the longitude, latitude, and height table

The first coordinate system will only be used in the actual distance measuring, for movement purposes, abstract whole
number coordiantes will be how everything is measured
"""

start = time.time()
x = pd.read_csv("C:/Users/hudso/Documents/Programming/Unity & C#/NASA ADC/Downloaded_Files/haworth/FY23_ADC_Latitude_Haworth.csv").to_numpy()
y = pd.read_csv("C:/Users/hudso/Documents/Programming/Unity & C#/NASA ADC/Downloaded_Files/haworth/FY23_ADC_Longitude_Haworth.csv").to_numpy()
z = pd.read_csv("C:/Users/hudso/Documents/Programming/Unity & C#/NASA ADC/Downloaded_Files/haworth/FY23_ADC_Height_Haworth.csv").to_numpy()
s = pd.read_csv("C:/Users/hudso/Documents/Programming/Unity & C#/NASA ADC/Downloaded_Files/haworth/FY23_ADC_Slope_Haworth.csv").to_numpy()
vis_map = np.random.randint(low=0, high=2, size=x.shape)#temp placeholder for vis map, 0 = not vis 1 = vis
elapsed = time.time() - start
print(f"Loading .csv files: {elapsed}")

def abstractToQuantitative(point):
    return [x[point[0], point[1]],
            y[point[0], point[1]], 
            z[point[0], point[1]]]

def distanceToPoint(point1, point2):
    # Reference point1 to it's longtiudinal and latitudinal coordinates
    point1_obj = abstractToQuantitative(point1)
    point2_obj = abstractToQuantitative(point2)

    # 3D Distance
    sum_ = 0
    n_dim = 3
    for i in range(n_dim):
        sum_ += (point1_obj[i] - point2_obj[i])**2 #does this for each dimension so you get 3d euclidean distance
    distance = math.sqrt(sum_)
    return distance

def pointsAreEqual(point1, point2, margin=0.1): #this accomodates for the intrinsic inaccuracy of floats
    for i in range(0, 2):
        if (abs(point1[i] - point2[i]) >= margin): #If a single of the x, y, or z coordinates are off then return false
            return False
    return True

def generateNeighbors(current_node):
    """Generates 2D neighbors in a donut pattern"""
    neighbors = []
    
    translator = list(itertools.product([0, 1, -1], repeat=2))[1:] #the slice removes the first entry which is just empty
    for translate in translator:
        neighbors.append([current_node[0] + translate[0], #x
                          current_node[1] + translate[1]])
    return neighbors

def isValidPoint(abstract_coor):
    """Take abstract coordinate and check if corresponding real-world slope is invalid"""
    slope = s[abstract_coor[0], abstract_coor[1]]
    if slope >= 15:
        return False
    return True

def generatePath(start, end, iterations, slope_w, vis_w, short_w, elev_w): #jump_dist is how far the astrobee can move per iteration of A*, this is essentially a measure of resolution
    #Scaling values to 0-1 for f cost calculation, s=scaled w=weight
    slope_s = slope_w * 1
    vis_s = vis_w * 1
    short_s = (short_w * 2)
    elev_s = elev_w * 1

    #initialize vars
    open_list = [[start, distanceToPoint(start, end), 0, [0,0], distanceToPoint(start, end)]] #[[[coordinate], f_cost, g_cost, parent, h_cost]]
    closed = []
    selected_node = []
    profiling = 0 #use this for profiling code
    min = 1500
    max = 0
    for _ in trange(iterations, desc="Iterations of A* Algorithm"):
        # Finds the index of the best open_list node with the least f_cost
        best_f = open_list[0][1]
        best_h = open_list[0][4]
        best_index = 0
        for index in range(len(open_list)):
            if open_list[index][1] < best_f:
                best_f = open_list[index][1]
                best_h = open_list[index][4]
                best_index = index
            elif open_list[index][1] == best_f:
                if open_list[index][4] < best_h:
                    best_f = open_list[index][1]
                    best_h = open_list[index][4]#best_h isn't actually necessarily the best h_cost, but instead just the h_cost of the best f_cost
                    best_index = index

        #Appends this node to closed and removes it from open_list
        selected_node = open_list[best_index]
        open_list.pop(best_index)
        closed.append(selected_node)

        #Tests if selected node is goal
        if pointsAreEqual(selected_node[0], end):
            break #if it has reached the goal, stop the algorithm
            
        #Generate children of current node (neighbors of current node)
        neighbors = generateNeighbors(selected_node[0])
        for child in neighbors:
            valid_node = True
            
            #Calculates g, h, and f cost
            child_g = distanceToPoint(child, start)
            #child_g = selected_node[2] + distanceToPoint(child, selected_node[0]) #this is the equivalent new way of doing the old way
            child_h = distanceToPoint(child, end)
            # Shortest dist + minimize slope + vis to earth + least elev change
            if child_g + child_h < min:
                min = child_g + child_h
            if child_g + child_h > max:
                max = child_g + child_h
            # Find out what value shortest dist is when short_w = 2, then make all the other factors equal that same value when weight is 2
            child_f = child_g + child_h
            """
            child_f = (
                slope_s * s[child[0], child[1]] + 
                vis_s * vis_map[child[0], child[1]] + 
                short_w * (child_g + child_h) + 
                elev_s * abs(z[child[0], child[1]] - z[selected_node[0][0], selected_node[0][1]])
            )
            """
            # Check if it's slope is below 15 degrees
            if not isValidPoint(child):
                valid_node = False

            #Check if child is on closed
            # THIS IS CAUSING THE O(n) TIME COMPLEXITY
            for point in closed:
                if pointsAreEqual(child, point[0]):
                    valid_node = False #Skip the point and move onto the next one

            #Check if the child is on open_list already
            remove_index = 0
            remove = False
            for index in range(len(open_list)):
                if pointsAreEqual(child, open_list[index][0]):
                    if child_g <= open_list[index][2]: #If the new g cost is better than the previoius g cost, remove the old one so we can append the new one
                        remove_index = index #THIS HAS TO BE THE LAST STATEMENT BEFFORE THE VARIABLE IS APPENDED
                        remove = True
                    else:
                        valid_node = False
            if remove:
                open_list.pop(remove_index)
            
            #Appends child to open_list
            if valid_node:
                open_list.append([child, child_f, child_g, selected_node[0], child_h]) #both the coordinates and the f_cost
   
    #Find the closest waypoint to end and backtrace from there
    lowest_h = closed[0][4]
    selected_node = closed[0]
    i = 0
    for point in closed:
        if point[4] < lowest_h:
            lowest_h = point[4]
            selected_node = closed[i]
        i+=1
    path = backtracing(start, closed, selected_node)
    
    #Create a duplicate-removed version of closed
    closed_points = [i[0] for i in closed]
    plottable = []
    for point1 in closed_points:
        dont_append = False
        for end in path:
            if pointsAreEqual(point1, end) or pointsAreEqual(point1, start):
                dont_append = True
        if not dont_append:
            plottable.append(point1) #plottable is a verison of closed without any of the duplicates of path
            
    return closed, plottable, path

def backtracing(start, closed, selected_node):
    #Performs backtracing and appends list of parents toward final goal
    path = []
    while True: #For all the nodes of the path
        for point in closed: #Find the current node's parent
            if pointsAreEqual(point[0], selected_node[3]):
                selected_node = point
                break
        if pointsAreEqual(start, selected_node[0]): #check if the parent is the starting node
            return path
        path.append(selected_node[0])

closed, plottable, path = generatePath([0, 0], [20, 20], 10000, 2, 2, 2, 2)

# This is for visualization only not actually necessary
closed_qua = [abstractToQuantitative(point[0]) for point in closed]
path_qua = [abstractToQuantitative(point) for point in path]

np.savez("data", closed_abst=closed, closed_qua=closed_qua, path_abst=path, path_qua=path_qua)

"""STILL NEED TO ADD REMOVE ALL POINTS > 15 DEGREE SLOPE ALSO TAKE THIS RUN IT RANDOMLY 100x"""

"""Input will need to be abstract coordinates to the neural network, e.g. [0, 1], [4, 5], output will be a path also in abstract coords"""

"""
os.chdir("/content/gdrive/My Drive/")
for angle in range(0, 360):
    ax.view_init(30, angle)
    plt.draw()
    plt.savefig(f'bar_{angle}.png')
print(closed_quantitative)
"""