import pandas as pd
import time
from tqdm import trange
import numpy as np

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, slope_lim):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    #while len(open_list) > 0:
    for _ in trange(10000):
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue
            
            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]][3] > slope_lim:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            
            # Calc dist to end
            child_obj = maze[child.position[0]][child.position[1]]
            end_obj = maze[end_node.position[0]][end_node.position[1]]
            sum_h = 0
            for i in range(3):
                sum_h += (child_obj[i] - end_obj[i])**2 #does this for each dimension so you get 3d euclidean distance

            # Calc dist between prev node and child
            current_obj = maze[current_node.position[0]][current_node.position[1]]
            sum_g = 0
            for i in range(3):
                sum_g += (current_obj[i] - child_obj[i]) ** 2

            # Create the f, g, and h values
            child.g = current_node.g + sum_g
            child.h = sum_h
            child.f = child.g + child.h

            # Child is already in the open list
            is_continue = False
            for open_node in open_list:
                print(f"ooga {open_node.position} booga {child.position}")
                if child == open_node and child.g > open_node.g:
                    print("ooga")
                    is_continue = True
            if is_continue:
                continue

            # Add the child to the open list
            open_list.append(child)


def main():
    start = time.time()
    with np.load('map.npz') as data:
        maze = data['map']
    elapsed = time.time() - start
    print(f"Loading .csv files: {elapsed}")

    start = (2, 1)
    end = (7, 6)

    path = astar(maze, start, end, 15)
    print(path)


if __name__ == '__main__':
    main()