import sys
import csv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

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
            index = (i,list(row).index(number))
        except:
            pass
        
    return index

def visualize_map(map_arr):
    '''
    Function to visualize array.
    Params: map_arr - matrix which contain map
    '''
    plt.imshow(map_arr)

def check_step(steps, x, y, finish):
    '''
    Function to add new step to list with previous steps and check if new step is finish point.
    Params: steps - list with previous steps; x - row index; y - column index; finish - coordinates of finish point
    Return: steps - updated list with steps; finish_find - bool value, true if new point is finish point, else false
    '''
    finish_find = False
    steps = steps + [(x,y)]
    if (x,y) == finish:
        print("Finish find!")
        finish_find = True
    return steps, finish_find

def check_neighbor(map_arr, steps_list, finish):
    '''
    Function to check neighbours of last step and find possible further steps.
    Params: map_arr - array with maze map; steps_list - list with previous steps coordinates; finish - coordinates of finish point 
    Return: possible_steps - list with possible paths from start point; 
        finish_find - bool value, true if finish point founded, else false, it is responsible for 
        ending searching start-finish path
    '''
    finish_find = False
    possible_steps = []
    x, y = steps_list[-1]
    shape_x, shape_y = map_arr.shape

    if x > 0:
        step_x, step_y = x-1, y
        if (map_arr[step_x][step_y] == 0 or map_arr[step_x][step_y] == 3) and (step_x,step_y) not in steps_list:
            steps, finish_find = check_step(steps_list.copy(), step_x, step_y, finish)
            possible_steps.append(steps)
    if x < (shape_x-1):
        step_x, step_y = x+1, y
        if (map_arr[step_x][step_y] == 0 or map_arr[step_x][step_y] == 3) and (step_x,step_y) not in steps_list:
            steps, finish_find = check_step(steps_list.copy(), step_x, step_y, finish)
            possible_steps.append(steps)
    if y > 0:
        step_x, step_y = x, y-1
        if (map_arr[step_x][step_y] == 0 or map_arr[step_x][step_y] == 3) and (step_x,step_y) not in steps_list:
            steps, finish_find = check_step(steps_list.copy(), step_x, step_y, finish)
            possible_steps.append(steps)
    if y < (shape_y-1):
        step_x, step_y = x, y+1
        if (map_arr[step_x][step_y] == 0 or map_arr[step_x][step_y] == 3) and (step_x,step_y) not in steps_list:
            steps, finish_find = check_step(steps_list.copy(), step_x, step_y, finish)
            possible_steps.append(steps)      

    return possible_steps, finish_find

def choose_min_steps(steps_options, finish):
    '''
    Function to choose path which include finish point coordinate, because it is minimum step way 
        between start and finish.
    Params: steps_options - array with different paths; finish - tuple with finish point coordinates
    Return: the shortest array which contain steps between start and finish
    '''
    for steps in steps_options:
        if finish in steps:
            #print("Shortest path finded: {}".format(steps))
            return steps

def select_path(map_arr, points):
    '''
    Function to select path on map array.
    Params: map_arr - array on which path is selected; points - list of steps' coordinates 
    Return: map_arr - array with changed values on indexes included in points list
    '''
    for index in points[1:-1]:
        map_arr[index[0]][index[1]] = 4 # symbolize path of algorithm, helpful in visualization
        
    return map_arr

if __name__ == "__main__":
    # reading system command line inputs as input and output csv files paths
    input_csv_path = sys.argv[1]
    output_csv_path = sys.argv[2]
    
    # reading input csv file and getting maze map values
    map_df = pd.read_csv(input_csv_path, header=None)
    map_arr = map_df.values

    # visualization of maze map
    #visualize_map(map_arr)

    # finding start and finish coordinates
    start = find_index(number=2, map_arr=map_arr)
    finish = find_index(number=3, map_arr=map_arr)
    #print("Start point: {}\nFinish point: {}".format(start, finish))

    # preparing starting steps' queue for searching
    searching_queue = [[start]]
    finish_find = False

    # main loop of algorithm
    while(~finish_find):
        new_steps = []
        #print("Queue before update: {}".format(searching_queue))
        for i in range(len(searching_queue)):
            steps = searching_queue[i].copy()
            #print("Checked step: {}".format(steps))
            new_step, finish_find = check_neighbor(map_arr, steps, finish)
            new_steps = new_steps + new_step
            if finish_find == True:
                break
            
        searching_queue = new_steps # updating by new possible ways
        #print("Queue after update: {}".format(searching_queue))

        if finish_find == True: # leaving from searching loop
            break 
    
    # extracting shortest correct start-finish path
    correct_path = choose_min_steps(searching_queue, finish)

    # adding correct path values in maze map array
    map_arr_with_path = select_path(map_arr.copy(), correct_path)

    # visualization of maze map with start-finish path
    #visualize_map(map_arr_with_path)

    #print(shortest_path, type(shortest_path))

    # saving steps from start to finish in csv file
    with open(output_csv_path, 'w', newline='\n') as myfile:
        wr = csv.writer(myfile)
        for tup in correct_path:
            wr.writerow(tup)