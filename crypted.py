from ortools.sat.python import cp_model
#import solution printer
from utils import VarArrayAndObjectiveSolutionPrinter

#PROBLEM : CRYPTARITHMETIC

#PROBLEM DEFINITION

#VARIABLES
#here the variables are all the letters present in the sentences
X = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']

#DOMAINS
#here for each letter except the ones at the beginning of the word, we have 10 values
D = [i for i in range(10)]

#CONSTRAINTS
#integer's sum verify the equation and S and M are non zero-leading numbers
C = ['SEND + MORE = MONEY', 'S != 0', 'M != 0']

#in order to solve the problem with ortools, we have to map each of these components to integers
def CyptedMessage(domains = D): 
    #Creating the model
    model = cp_model.CpModel()

    #Creating the domains for each letter
    base_numbers = len(domains)

    #variables (s and m cannot be 0)
    S = model.NewIntVar(1, base_numbers - 1, 'S') 
    E = model.NewIntVar(0, base_numbers - 1, 'E') 
    N = model.NewIntVar(0, base_numbers - 1, 'N') 
    D = model.NewIntVar(0, base_numbers - 1, 'D') 
    M = model.NewIntVar(1, base_numbers - 1, 'M') 
    O = model.NewIntVar(0, base_numbers - 1, 'O') 
    R = model.NewIntVar(0, base_numbers - 1, 'R') 
    Y = model.NewIntVar(0, base_numbers - 1, 'Y') 

    #Adding constraint that integers verify the equation
    model.Add(
        (D + E)  +  10*(N + R)  +  100*(E + O)  +  1000*(S + M)
        ==
        Y + 10*E + 100*N + 1000*O + 10000*M
    )

    # We need to group variables in a list to use the constraint AllDifferent.
    letters = [S, E, N, D, M, O, R, Y]

    # Verify that we have enough digits.
    assert base_numbers >= len(letters)

    # Define constraints.
    model.AddAllDifferent(letters)

    #Create the solution
    solver = cp_model.CpSolver()
    solution_printer = VarArrayAndObjectiveSolutionPrinter(letters)
    status = solver.SolveWithSolutionCallback(model, solution_printer)

    #formating results
    print('Status = {}'.format(solver.StatusName(status)))
    print('Number of solutions found: {}'.format(solution_printer.solution_count()))


if __name__ == '__main__':
    CyptedMessage()
