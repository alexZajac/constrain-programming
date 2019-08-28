from ortools.sat.python import cp_model


#custom class for printing solutions
class VarArrayAndObjectiveSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        print('Solution %i' % self.__solution_count)
        print('  objective value = %i' % self.ObjectiveValue())
        for v in self.__variables:
            print('  %s = %i' % (v, self.Value(v)), end=' ')
        print()
        self.__solution_count += 1

    def solution_count(self):
        return self.__solution_count


#QUEENS

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
  """Print intermediate solutions."""

  def __init__(self, variables):
    cp_model.CpSolverSolutionCallback.__init__(self)
    self.__variables = variables
    self.__solution_count = 0

  def OnSolutionCallback(self):
    self.__solution_count += 1
    for v in self.__variables:
      print('%s = %i' % (v, self.Value(v)), end = ' ')
    print()

  def SolutionCount(self):
    return self.__solution_count


class DiagramPrinter(cp_model.CpSolverSolutionCallback):
  def __init__(self, variables):
    cp_model.CpSolverSolutionCallback.__init__(self)
    self.__variables = variables
    self.__solution_count = 0

  def OnSolutionCallback(self):
    self.__solution_count += 1
    print("Solution : {}".format(self.__solution_count))

    for v in self.__variables:
      queen_col = int(self.Value(v))
      board_size = len(self.__variables)
      # Print row with queen.
      for j in range(board_size):
        if j == queen_col:
          # There is a queen in column j, row i.
          print("Q", end=" ")
        else:
          print("_", end=" ")
      print()
    print()

  def SolutionCount(self):
    return self.__solution_count

