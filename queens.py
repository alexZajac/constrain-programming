from ortools.sat.python import cp_model
#import diagram queen printer
from utils import DiagramPrinter

#PROBLEM : 8 QUEENS

#PROBLEM DEFINITION

#VARIABLES
#here the variables are all the queens placement ex: at index 0 we have queen0 and it's row-placement is pc0 on the column of the grid
X = ['pc0', 'pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7']

#DOMAINS
#here for each queen there are 8 possible values
D = [i for i in range(8)]

#CONSTRAINTS
#No queens on the same column (already satisfied), no queens on the same row, one queen on each diagonal

#in order to solve the problem with ortools, we have to map each of these components to integers
def EightQueens(domains = D): 
    #Creating the model
    model = cp_model.CpModel()

    #Creating the variables
    grid_size = len(domains)
    queens = [model.NewIntVar(0, grid_size - 1, 'pc{}'.format(i)) for i in range(grid_size)]

    #each row has te be different
    model.AddAllDifferent(queens)

    #each diagonal contains one queen
    #for each column of the grid
    for i in range(grid_size):
        #create ascDiagonal array, and descDiagonal array
        diag1 = []
        diag2 = []
        #for each row in the column
        for j in range(grid_size):
            #diag asc droite, entre 0 et 14 = (7 + 7)
            q1 = model.NewIntVar(0, 2 * grid_size, 'diag1_{}'.format(i))
            #add this value ot diag1
            diag1.append(q1)
            #making sure q1 is equal to the right quantity
            model.Add(q1 == queens[j] + j)

            #diag desc droite
            q2 = model.NewIntVar(-grid_size, grid_size, 'diag2_{}'.format(i))
            #add this value ot diag1
            diag2.append(q2)
            #making sure q2 is equal to the right quantity
            model.Add(q2 == queens[j] - j)
        model.AddAllDifferent(diag1)
        model.AddAllDifferent(diag2)

    #Create the solution
    solver = cp_model.CpSolver()
    solution_printer = DiagramPrinter(queens)
    status = solver.SearchForAllSolutions(model, solution_printer)

    #formating results
    print('Status = {}'.format(solver.StatusName(status)))
    print('Number of solutions found: {}'.format(solution_printer.SolutionCount()))


if __name__ == '__main__':
    EightQueens()
