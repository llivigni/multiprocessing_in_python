#!/usr/bin/env python3
"""
=============================================================================
Title           : Logan_LiVigni_R11800181_final_project.py
Description     : This program executes the first 100 steps of a modified
                : cellular life simulator using multiprocessing.
Author          : llivigni (R#11800181)
Date            : 12/02/2024
Version         : 1.0
Usage           : python3 Logan_LiVigni_R11800181_final_project.py -i inputFile.txt -o outputFile.txt -p
Notes           : Used the replit in Lecture 09 as an example.
Python Version  : 3.1.2
=============================================================================
"""

import argparse
import sys
from pathlib import Path
from multiprocessing import Pool

# List containing the 8 possible neighboring directions
DIRECTIONS = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]

# Function to check if a number is prime or not
def is_prime(num):
    if num <= 1:                # Any negative #, 0, and 1 is not prime
        return False
    elif num == 2:              # Check two before num % 2, because 2 is prime but 2 % 2 = 0
        return True
    elif num % 2 == 0:          # Any number that is / 2 that gives no remainder is not prime
        return False
    for i in range(3, num):     # If there is a number from 3 to num-1 that gives a remainder of 0
        if num % i == 0:        # when divided, the number is not prime
            return False

    return True
# Function to determine if a number is a power of two
# Ex: 64/2 = 32/2 = 16/2 = 8/2 = 4/2 = 2/2 = 1 done (power of two!)
def is_power_of_two(num):
    if num == 0:                # 0 not a power of 2
        return False

    while num != 1:             # Loop until num = 1
        if num % 2 != 0:        # Any number that has a remainder when divided by two is not a power of two
            return False
        num = num // 2          # Divide num by 2 and keep iterating through the loop

    return True

def iterate(matrixData):                # matrixData contains: matrix_data_list and row
    matrix_data_list = matrixData[0]
    row = matrixData[1]
    num_of_rows = matrixData[2]
    num_of_cols = matrixData[3]

    copy_row=list(matrix_data_list[row])    # Create a copy of the row from the input matrix list

    for col in range(num_of_cols):                 # Loop through each column in the matrix
        sum_neighbor = 0
        for neighbor_row, neighbor_col in DIRECTIONS:     # Loop through each direction in the list
            neighbor_cell_row = row + neighbor_row              # [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
            neighbor_cell_col = col + neighbor_col              # Up, up-right, right, down-right, down, down-left, left, up-left

            if 0 <= neighbor_cell_row < num_of_rows and 0 <= neighbor_cell_col < num_of_cols:           # Bounds checking
                    neighbor_cell = matrix_data_list[neighbor_cell_row][neighbor_cell_col]     # Access the neighbor cell in the matrix

                    # Stage 1.3.1 - Symbols
                    if neighbor_cell == 'O':     # Healthy O cell = +2
                        sum_neighbor += 2
                    elif neighbor_cell == 'o':   # Weakened O cell = +1
                        sum_neighbor += 1
                    elif neighbor_cell == '.':   # Dead cell = 0
                        sum_neighbor += 0
                    elif neighbor_cell == 'x':   # Weakened X cell = -1
                        sum_neighbor -= 1
                    elif neighbor_cell == 'X':   # Healthy X cell = -2
                        sum_neighbor -= 2

        current_cell = copy_row[col]        # Get value of current cell in the copied row

        # Stage 1.3.2 - Iterative rules
        if current_cell == 'O':
            if is_power_of_two(sum_neighbor):       # '.' if sum is a power of 2
                copy_row[col] = '.'
            elif sum_neighbor < 10:                 # 'o' if sum is less than 10
                copy_row[col] = 'o'
            else:
                copy_row[col] = 'O'
        elif current_cell == 'o':
            if sum_neighbor <= 0:                   # '.' if sum is less than/equal to 0
                copy_row[col] = '.'
            elif sum_neighbor >= 8:                 # 'O' if sum is greater than/equal to 8
                copy_row[col] = 'O'
            else:
                copy_row[col] = 'o'
        elif current_cell == '.':
            if is_prime(sum_neighbor):              # 'o' if sum is a prime number
                copy_row[col] = 'o'
            elif is_prime(abs(sum_neighbor)):       # 'x' if |sum| is a prime number
                copy_row[col] = 'x'
            else:
                copy_row[col] = '.'
        elif current_cell == 'x':
            if sum_neighbor >= 1:                   # '.' if sum is greater than/equal to 1
                copy_row[col] = '.'
            elif sum_neighbor <= -8:                # 'X' if sum is less than/equal to -8
                copy_row[col] = 'X'
            else:
                copy_row[col] = 'x'
        elif current_cell == 'X':
            if is_power_of_two(abs(sum_neighbor)):  # '.' if |sum| is a power of two
                copy_row[col] = '.'
            elif sum_neighbor > -10:                # 'x' if sum is greater than -10
                copy_row[col] = 'x'
            else:
                copy_row[col] = 'X'


    return ''.join(copy_row)            # Combine all the updated cells into a string


def main():
    print("Project :: R11800181")

    # Stage 1.1 - Data Retrieval
    parser = argparse.ArgumentParser(description = "Allowed arguments")

    # Command line arguments
    # -i <path_to_input_file>
    parser.add_argument('-i', action="store", dest="Input_File", required=True, help="This option retrieves the file path to the starting cellular matrix.")
    # -o <path_to_output_file>
    parser.add_argument('-o', action="store", dest="Output_File", required=True, help="This option retrieves the file path for the final output file.")
    # -p <int>
    parser.add_argument('-p', action="store", dest="Processes", type=int, default=1, help="This option retrieves the file path for the final output file.")

    args = parser.parse_args()

    # Get the file paths of input/output files
    path_to_input_file = Path(args.Input_File)
    path_to_output_file = Path(args.Output_File)

    # Get the directory for path_to_output_file
    directory = path_to_output_file.parent

    # Validation, entire file path must exist
    if not path_to_input_file:
        print("Error - cannot open input file.")
        sys.exit(1)
    # Validation, directories in the file path must exist
    if not directory:
        print("Error - directories in the file path must exist")
        sys.exit(1)
    # Validation, processes must be greater than or equal to 1
    if args.Processes < 1:
        print("Error - number of processes must be 1 or greater.")
        sys.exit(1)

    # Stage 1.2.1 - Reading the Matrix File
    with open(args.Input_File, "r") as Input_File:
        matrix_data_list = Input_File.read().splitlines()   # Open the input file and convert the matrix to a list

    num_of_rows = len(matrix_data_list)     # Calculate the number of rows in the matrix
    num_of_cols = len(matrix_data_list[0])  # Calculate the number of columns in the matrix

    # Stage 1.3 - Matrix Processing
    # Stage 2.1 - Concurrency using Multiprocessing
    processPool = Pool(processes=args.Processes)        # Process pool allows us to create pool of worker processes
    for step in range(100):                             # Simulate time steps 0-100
        poolData = list()
        for row in range(len(matrix_data_list)):
            matrixData = [matrix_data_list, row, num_of_rows, num_of_cols]        # Pack matrixData list with original matrix and row number, number of rows/cols
            poolData.append(matrixData)                 # Append matrixData to aggregate list

        matrix_data_list = processPool.map(iterate, poolData)       # Map function to perform scatter/gather operation

    # Stage 1.2.2 - Writing the Matrix File
    with open(args.Output_File, "w") as Output_File:
        for row in matrix_data_list:
            Output_File.write(''.join(row) + '\n')  # ''.join(row) + '\n' will make the matrix style format

if __name__ == "__main__":
    main()