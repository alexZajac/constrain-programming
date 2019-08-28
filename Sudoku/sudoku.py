from ortools.sat.python import cp_model
from random import shuffle
from constants import Get_empty_cells


#defining a class Sudoku
class Sudoku:

    def __init__(self, size = 9, initial_board=[]):

        #if the size is valid to make regions (i.e.)
        if int(size**0.5)**2 != size:
            raise Exception('Impossible size')
        self.size = size

        #if the programs has to create it automatically, we initialize it to 0 cells
        if len(initial_board) == 0:
            self.grid = [[0] * size for i in range(size)]
        elif len(initial_board) == size:
            self.grid = initial_board
        
        #creates model and its variables
        self.model = cp_model.CpModel()
        self.model_variables = []
        self.solution_count = 0
        
    def Add_variables(self):
        """Here we will transform our default grid to a sudoku grid solvable with ORtools
        empty values have a range (1,9) and non-empty are constants"""
        for i in range(self.size):
            row = []
            for j in range(self.size):
                # empty cell
                if(self.grid[i][j] == 0):
                    value = self.model.NewIntVar(1, self.size, '{}, {}'.format(i, j))
                else:
                # the value is constant
                    value = self.model.NewIntVar(self.grid[i][j], self.grid[i][j], '{}, {}'.format(i, j))
                row.append(value)
            self.model_variables.append(row)

    def Add_constraints(self):
        """Here we will add our constraint on the model"""
        #all values have to be different in rows
        for row in self.model_variables:
            self.model.AddAllDifferent(row)
        
        #all values have to be different in columns
        #we create a copy of our grid which is its transposed version (the map function maps the zip object result to a list)
        column_grid = list(map(list, zip(*self.model_variables)))
        for column in column_grid:
            self.model.AddAllDifferent(column)
        
        #all values have to be different in cells
        #we create a copy of our grid in which each list is a cells in the original sudoku
        cell_grid = [
            [
                self.model_variables[i][j], self.model_variables[i][j+1], self.model_variables[i][j+2],
                self.model_variables[i+1][j], self.model_variables[i+1][j+1], self.model_variables[i+1][j+2],
                self.model_variables[i+2][j], self.model_variables[i+2][j+1], self.model_variables[i+2][j+2]
            ] 
            for i in range(0, self.size-2, 3) 
            for j in range(0, self.size-2, 3)
        ]

        for cell in cell_grid:
            self.model.AddAllDifferent(cell)

    def Solve(self, should_print=True, solution_limit=100):
        """Here we will solve our problem with the constraint solver"""
        # add variables and constraint
        self.Add_variables()
        self.Add_constraints()
        # Create the solution
        solver = cp_model.CpSolver()

        # printing each new solution if needed
        if(should_print):
            solution_printer = Sudoku_Solution_Printer(self.model_variables, solution_limit)
        else:
            solution_printer = Empty_printer(self.model_variables, solution_limit)

        # displaying the status and setting solution count
        status = solver.SearchForAllSolutions(self.model, solution_printer)
        self.solution_count = solution_printer.solution_count()
        
        # formating results
        if(should_print):
            print('Status = {}'.format(solver.StatusName(status)))
            print('Number of solutions found: {}'.format(solution_printer.solution_count()))

def Get_random_valid_grid(size):
    """Returns a single valid raw grid out of 9! possible combiantions"""
    #getting size values and shuffling them
    values_to_set = [i for i in range(size)]
    shuffle(values_to_set)
    #assigning them to a size x size board on the main descending diagonal, by doing so, the initialization of the grid is random and valid
    grid = [[0] * size for _ in range(size)]
    k=0
    for i in range(size):
        for j in range(size):
            #diagonal
            if(i == j):
                grid[i][j] = values_to_set[k]
                k += 1
    
    return grid

def Display_grid(grid, difficulty):
    """Displays model grid"""
    print("Voici la grille de niveau {} générée : \n".format(difficulty))
    for row in grid:
        print([value for value in row])
    
def Get_solvable_grid(difficulty, size=9):
    """Here we will automatically generate a solvable-by-human Sudoku grid as a parameter
    of the difficulty, we cannot guarantee uniqueness of the solution for hardest level"""
    #solving a randomly-initialzed valid grid
    random_valid_grid = Get_random_valid_grid(size)
    s = Sudoku(initial_board=random_valid_grid)
    s.Add_variables()
    s.Add_constraints()
    solver = cp_model.CpSolver()
    status = solver.Solve(s.model)

    #if it's solved
    if(status == cp_model.FEASIBLE or status == cp_model.OPTIMAL):

        # there are size^2 elements, and we will remove enough random elements so that it fits the difficulty
        num_empty_cells = Get_empty_cells(difficulty, size)
        # we get a raw grid from the model solution
        valid_grid = [[solver.Value(value) for value in row] for row in s.model_variables]

        #we make a list of all possible 81 positions
        positions = [[i, j] for i in range(size) for j in range(size)]
        #we shuffle it randomly
        shuffle(positions)

        #we will remove num_empty_cells elements from the valid grid
        k = 0
        cells_removed = 0
        
        while True:
            #if the difficulty is the highest we have no ohter choice than to remove the number of cells asked
            #without guaranteeing the uniqueness of the solution
            if(difficulty == 'he<ll'):
                if(k < num_empty_cells):
                    rnd_pos = positions[k]
                    valid_grid[rnd_pos[0]][rnd_pos[1]] = 0
                    k += 1
                else: 
                    break
            else:
                #if position is valid in positions and we didn't remove enough cells
                if (cells_removed < num_empty_cells and k < len(positions)):
                    #removing one value from the grid and keeping its value in tmp
                    rnd_pos = positions[k]
                    valid_grid[rnd_pos[0]][rnd_pos[1]], tmp = 0, valid_grid[rnd_pos[0]][rnd_pos[1]]

                    #trying to solve it with our new grid
                    test_sudoku = Sudoku(initial_board=valid_grid)
                    test_sudoku.Solve(should_print=False)

                    #if solved with more than one solution, we reassign tmp to its original position and retry with next value
                    if(test_sudoku.solution_count != 1):
                        valid_grid[rnd_pos[0]][rnd_pos[1]] = tmp
                    else: 
                        cells_removed += 1
                    k += 1
                
                #we traversed all the list without removing enough elements, recall recursively the method
                elif(cells_removed < num_empty_cells and k >= len(positions)): 
                    return Get_solvable_grid(difficulty)
                    
                #we removed necessary number of cells
                elif(cells_removed == num_empty_cells):
                    break
   
    #return result
    return valid_grid


#class for sudoku printing
class Sudoku_Solution_Printer(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solution_limit = limit
    
    def on_solution_callback(self):
        print('Solution {}\n'.format(self.__solution_count + 1))

        for row in self.__variables:
            print([self.Value(value) for value in row])
        print("\n\n")
        self.__solution_count += 1
        if self.__solution_count >= self.__solution_limit:
            print('Stop search after {} solutions'.format(self.__solution_limit))
            self.StopSearch()
    
    def solution_count(self):
        return self.__solution_count

#no callback class
class Empty_printer(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solution_limit = limit
    
    def on_solution_callback(self):
        self.__solution_count += 1
        if self.__solution_count >= self.__solution_limit:
            print('Stop search after {} solutions'.format(self.__solution_limit))
            self.StopSearch()
    
    def solution_count(self):
        return self.__solution_count
    




