import random
import numpy as np
from numpy import *
import math
from random import choice
import statistics

"""
To perform simulations for different values for k and N, Please change the values below.
"""

v = 2
t = 2
k = 5
#N = v**t
N = 4

# print(arr)
"""
    arr[a][b]: [a] is the index of the column, [b] is the index of the row 
"""
#arr = [[1, 0, 1, 0], [1, 1, 0, 0], [0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 1, 0]]
# print(arr)
"""
    List a : The first column
    List b : The second column
"""
def missing_combinations(a: list, b: list):
    number_of_possible_combinations = v**t
    unique_combinations = set({})
    for i in zip(a, b):
        unique_combinations.add(i)
        number_missing_combinations = number_of_possible_combinations - len(unique_combinations)
    return number_missing_combinations
    # print(len(unique_combinations))

    # Find the number of all possible combinations
    # Subtract the length of unique_combinations by 
    # the number of all possible combinations

"""
    The combinations of columns (i,j) is same as (j,i) so eleminating all the duplicates as such in the method below.
"""
def objective_function(array: list,a: int):
    previous_total_missing_combinations = 0
    total_missing_combinations = 0
    for a in range(k-1):
        previous_missing_combinations = 0
        total_number_missing_combinations = 0
        for b in range(k-a):
            b = b+a
            if b!=a:
                number_missing_combinations = missing_combinations(array[a],array[b])
                total_number_missing_combinations = number_missing_combinations + previous_missing_combinations
                previous_missing_combinations = total_number_missing_combinations
        #print(total_number_missing_combinations)
        total_missing_combinations = total_number_missing_combinations + previous_total_missing_combinations
        previous_total_missing_combinations = total_missing_combinations
    return total_missing_combinations

"""
where 'a' is the current state cost and 'b' is the possible future state cost
where 'array1' is the current state matrix and 'array2' is the possible future state matrix
where 'c' is the temperature
"""

def selecting_next_state(array1: list, a: int, array2: list, b: int, c: int):
    delta_E = b - a
    if delta_E < 0:
        array1 = [row.copy() for row in array2]
    elif delta_E > 0:
        rho = math.exp(-delta_E/c)
        rand = np.random.uniform(1,0,1)
        if rand < rho:
            array1 = [row.copy() for row in array2]
        else:
            array1 = [row.copy() for row in array1]
    return array1

def frozen_factor(a: int,b: int):
    number_to_stop = math.factorial(a)/(math.factorial(b)*math.factorial(a-b))
    return number_to_stop

for i in range(30):
    print("")
    arr = [[random.randint(0,2) for m in range(N)] for n in range(k)]
    array_original = [row.copy() for row in arr]
    stop_number = frozen_factor(k,t)
    list_check = []
    T = k
    alpha = 0.99
    ll = 0
    while T > 1*(10**-12):
        # print("new cycle")
        T = alpha*T
        #print(arr)
        original_objective_function_value = objective_function(arr,k)
        # print(original_objective_function_value)
        j = random.randint(0,k)
        #print(j)
        # dict_of_arr_test = {}
        from collections import defaultdict
        dict_of_arr_test = defaultdict(lambda: [])
        test_objective_function_value = []
        for row in range(N):
            arr_test = [row.copy() for row in arr]
            if arr_test[j][row] == 1:
                arr_test[j][row] = 0
                #print(arr_test)
            elif arr_test[j][row] == 0:
                arr_test[j][row] = 1
                #print(arr_test)
            # print(arr_test)
            l = objective_function(arr_test,k)
            #dict_of_arr_test[l] = arr_test
            dict_of_arr_test[l].append(arr_test)
            
        min_test_objective_function = min(dict_of_arr_test.keys())
        #print(min_test_objective_function)
        possible_new_state = dict_of_arr_test[min_test_objective_function][0]
        #print(possible_new_state)
        new_state = selecting_next_state(arr,original_objective_function_value,possible_new_state,min_test_objective_function,T)
        arr = [row.copy() for row in new_state]
        # print(array_original)
        # print(arr)
        #print(min_test_objective_function)
        list_check.append(min_test_objective_function)
        # print(list_check)
        if len(list_check) == stop_number:
            if len(set(list_check)) == 1:
                print("frozen Condition Reached")
                break
            elif len(set(list_check)) != 1:
                list_check.pop(0)
        ll = ll+1
    if min_test_objective_function == 0:
        print("covering array found")
    print("Run Number  -  "+str(i))
    print("Original State")
    print(array_original)
    print("objective Function Value Initial  -  "+str(objective_function(array_original,k)))
    print("Final State")
    print(arr)
    print("objective Function Value Final  -  "+str(min_test_objective_function))
    print("Objective Function Difference Between Initial and Final  -  "+str(objective_function(array_original,k)-min_test_objective_function))
    print("Frozen Factor Stop Condition  -  "+str(stop_number))
    print("Forzen Factor Array  -  " +str(list_check))
    print("Total Number of cycles to reach final state  -  "+str(ll))
    