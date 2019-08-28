from ortools.sat.python import cp_model
#import solution printer
from utils import VarArrayAndObjectiveSolutionPrinter


#PROBLEM : COLORATION ACCROSS THE MAP OF AUSTRALIA

#PROBLEM DEFINITION

#VARIABLES
#here the variables are all the states among australia
X = ['WA', 'NT', 'Q', 'SA', 'NSW', 'V', 'T']

#DOMAINS
#here for each state, we want a custom color with below-specififed constraints
D = ['red', 'green', 'blue']

#CONSTRAINTS
#none of the adjacent state must have the same color
C = ['SA != WA', 'SA != NT', 'SA != Q', 'SA != NSW', 'SA != V', 'WA != NT', 'Q != NT', 'Q != NSW', 'V != NSW']

#in order to solve the problem with ortools, we have to map each of these components to integers
def AustraliaColoring(domains = D): 
    #Creating the model
    model = cp_model.CpModel()

    #Creating variables
    nums_colors = len(domains)

    WA = model.NewIntVar(0, nums_colors - 1, 'WA') #premiere variable initilisée à rouge(0) qui peut ptrendre 3 valeurs différentes et de nom WA
    NT = model.NewIntVar(0, nums_colors - 1, 'NT')
    Q = model.NewIntVar(0, nums_colors - 1, 'Q')
    SA = model.NewIntVar(0, nums_colors - 1, 'SA')
    NSW = model.NewIntVar(0, nums_colors - 1, 'NSW')
    V = model.NewIntVar(0, nums_colors - 1, 'V')
    T = model.NewIntVar(0, nums_colors - 1, 'T')

    #Adding constraints
    model.Add(SA != WA)
    model.Add(SA != NT)
    model.Add(SA != Q)
    model.Add(SA != NSW)
    model.Add(SA != V)
    model.Add(WA != NT)
    model.Add(Q != NT)
    model.Add(Q != NSW)
    model.Add(V != NSW)

    #Create the solution
    solver = cp_model.CpSolver()
    solution_printer = VarArrayAndObjectiveSolutionPrinter([WA, NT, Q, SA, NSW, V, T])
    status = solver.SolveWithSolutionCallback(model, solution_printer)

    #formatting results
    print('Status = {}'.format(solver.StatusName(status)))
    print('Number of solutions found: {}'.format(solution_printer.solution_count()))


if __name__ == '__main__':
    AustraliaColoring()
