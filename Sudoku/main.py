from random import shuffle
from sudoku import Sudoku, Get_solvable_grid, Display_grid
from constants import Get_empty_cells, sudoku_beginner, sudoku_easy, sudoku_medium, sudoku_hard, sudoku_hell
#PROBLEM : SUDOKU

#PROBLEM DEFINITION
# Please note that all variables below are not used in the program but displayed as examples

#VARIABLES
# first, we can define a sudoku grid as an array, in which each element is an array (cell) of n=9 integers (between 1 and 9)
# here all the variables are the unknown numbers in sudoku grid i.e. X(i,j) for i in all columns and j in all rows, whatever the sudoku board size has
grid = [[1,8,7,2,6,5,3,4,9], [4,9,1,8,7,2,6,5,3,], ..., []]
X = ['grid[i, j] for i in grid for j in grid[i]']

#DOMAINS
#here for each variable there are 9 possible values 
D = [i for i in range(9)]

#CONSTRAINTS
#No same integer on the same row of the whole grid, neither on the same line nor in the same cell
C = ['all x(i,j) != for fixed i', 'all x(i,j) != for fixed j', 'all x(i,j) != for cell (i, j) -> (i+2, j+2)']


#MAIN
def Main():
    # hard coded grid solving
    # for hell level, the number of solutions is extremly high
    print("\n\n Grid resolution : \n\n")
    s1 = Sudoku(initial_board=sudoku_hell)
    s1.Solve(solution_limit=20)

    print("\n\n Grid generation : \n\n")
    # automatic grid generation and solving with difficulty parameter oneOf(beginner, easy, medium, hard, hell)
    difficulty = 'hell'
    automatic_grid = Get_solvable_grid(difficulty)
    Display_grid(automatic_grid, difficulty)    
    print("\nRésolution du Sudoku : \n")
    s2 = Sudoku(initial_board=automatic_grid)
    s2.Solve(solution_limit=20)


if __name__ == '__main__':
    Main()
    