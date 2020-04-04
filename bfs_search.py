import csv
import pandas as pd
import numpy as np
import argparse
from matplotlib import pyplot as plt


def visualize_map(map_arr):
    '''
    Function to visualize maze map array.
    Params: map_arr - matrix which contain map
    '''
    plt.imshow(map_arr)
    plt.show()


def find_index(number, map_arr):
    '''
    Function to find index of searching number which represents start or finish. 
        We assume that in array is only one start and finish. 
    Params: number - sought number in array, number representation: Start ---> 2; Finish ---> 3;
        map_arr - array in which we looking for
    Return: tuple with index of start or finish ---> (row, column)
    '''
    for i, row in enumerate(map_arr):
        try:
            list(row).index(number)
            index = (i, list(row).index(number))
        except:
            pass

    return index


def bfs_search(map_arr, start, finish):
    '''
    Function to search path from start to finish using BFS algorithm.
    Params: map_arr - array with maze, in which we are searching the path;
        start - coordinates of start; finish - coordinates of finish
    Return: list with coordinates of path from start to finish
    '''
    h, w = map_arr.shape
    parents = {}
    vertices_to_view = [start]
    vertices_viewed = []

    while len(vertices_to_view) > 0:
        vertex = vertices_to_view.pop(0)

        if vertex in vertices_viewed or map_arr[vertex[0], vertex[1]] == 1:
            continue

        vertices_viewed.append(vertex)

        if vertex == finish:
            break

        neighbours = []

        if vertex[1] + 1 < w:
            neighbours.append((vertex[0], vertex[1] + 1))
        if vertex[0] - 1 > 0:
            neighbours.append((vertex[0] - 1, vertex[1]))
        if vertex[1] - 1 > 0:
            neighbours.append((vertex[0], vertex[1] - 1))
        if vertex[0] + 1 < h:
            neighbours.append((vertex[0] + 1, vertex[1]))

        for neighbour in neighbours:
            if neighbour not in vertices_viewed:
                parents[neighbour] = vertex
                vertices_to_view.append(neighbour)

    parent = finish
    path = [finish]
    while parent != start:
        parent = parents[parent]
        path.append(parent)

    return path


def add_path(map_arr, path):
    '''
    Function change value of coordinates which belong to path.
    Params: map_arr - maze map array; path - list with path coordinates
    '''
    for i in range(1, len(path)-1):
        x, y = path[i]
        map_arr[x, y] = 4


if __name__ == "__main__":
    # reading system command line inputs as input and output csv files paths
    parser = argparse.ArgumentParser(
        description='Script for maze map correct path searching with BSF algorithm.')
    parser.add_argument('--input_csv', type=str, required=True,
                        help='name of csv file with maze map')
    parser.add_argument('--output_csv', default='output.csv',
                        help='name for output csv file with path between start and finish')

    args = parser.parse_args()
    input_csv_path = args.input_csv  
    output_csv_path = args.output_csv 

    # reading input csv file and getting maze map values
    map_df = pd.read_csv(input_csv_path, header=None)
    map_arr = map_df.values

    # visualization of maze map
    # visualize_map(map_arr)

    # finding start and finish coordinates
    start = find_index(number=2, map_arr=map_arr)
    finish = find_index(number=3, map_arr=map_arr)
    print(f"Start point: {start}\nFinish point: {finish}")

    # finding path with bfs algorithm
    path = bfs_search(map_arr, start, finish)
    # print(path)
    print(f'Path length: {len(path)}')

    # add path to maze map
    add_path(map_arr, path)

    # visualization of maze map with path
    visualize_map(map_arr)

    # saving steps from start to finish in csv file
    with open(output_csv_path, 'w', newline='\n') as myfile:
        wr = csv.writer(myfile)
        for move in path:
            wr.writerow(move)
