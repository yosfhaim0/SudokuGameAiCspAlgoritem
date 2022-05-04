# SUDOKU
import math
import copy

# yosef haim amrusi 314897208

# board - The variables' value are in a list of the (N*N)*(N*N) board cells
#            (a vector represenring a mat.).
# an empty cell contains 0.
#
# d - The domains are a list of lists - the domain of every var.
#
# The state is a list of 2 lists: the vars. and the domains.
import CSPSolver

N = 0


def create(fpath="sudoku.txt"):
    global N
    board = read_board_from_file(fpath)
    lenOfBoard = len(board)
    N = int(lenOfBoard ** 0.25)
    ##########################
    # Create a domain for each value
    domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    domains = []
    for i in range(lenOfBoard):
        domains += [copy.deepcopy(domain)]
    p = [board, domains]
    # For each location you will propagate the constraints
    for v in range(lenOfBoard):
        CSPSolver.propagate_constraints(p, v)
    ###########################
    return p


def read_board_from_file(fpath):
    f = open(fpath, "r")
    board = []
    s = f.readline()
    while s != "":
        for i in s.split():
            board += [int(i)]
        s = f.readline()
    f.close()
    return board


def domain(problem, v):
    # Returns the domain of v
    return problem[1][v][:]


def domain_size(problem, v):
    # Returns the domain size of v
    return len(problem[1][v])


def assign_val(problem, v, x):
    # Assigns x in var. v
    problem[0][v] = x


def get_val(problem, v):
    # Returns the val. of v
    return problem[0][v]


def erase_from_domain(problem, v, x):
    # Erases x from the domain of v
    problem[1][v].remove(x)


def get_list_of_free_vars(problem):
    # Returns a list of vars. that were not assigned a val.
    l = []
    for i in range(len(problem[0])):
        if problem[0][i] == 0:
            l += [i]
    return l


def is_solved(problem):
    # Returns True iff the problem is solved
    for i in range(len(problem[0])):
        if problem[0][i] == 0:
            return False
    return True

#A function that returns the square belongs to a specific location
# return the (squareColum, squareRow)
# squareColum= 0...2  index of the Square
def square(problem, v):
    n = len(problem[0]) ** 0.25
    squareColum = (v % N ** 2) // N
    squareRow = (v // N ** 2) // N
    return squareColum, squareRow


# Returns True iff v1=x1 and v2=x2 is consistent with all constraints
def is_consistent(problem, v1, v2, x1, x2):
    # your code here
    # v1 and v2 there are the location
    # If the value is different can not be a problem
    if x1 != x2:
        return True
    # If one of the values 0 also can not be a problem
    if x1 == 0 or x2 == 0:
        return True
    # If the locations are equal
    if v1 == v2:
        return True
    # The values are equal and none of them are 0 so if they are in the same row or
    # column or square they break the constraint
    if v1 % N ** 2 == v2 % N ** 2 or v1 // N ** 2 == v2 // N ** 2 or square(problem, v1) == square(problem, v2):
        return False
    # Otherwise they do not affect each other at all
    return True


def list_of_influenced_vars(problem, v):
    # Returns a list of free vars. whose domain will be
    # influenced by assigning a val. to v
    r = list(range(N ** 4))
    r.remove(v)
    l = []
    for i in r:
        if problem[0][i] == 0 and not is_consistent(problem, v, i, 1, 1):
            l += [i]
    return l


def present(problem):
    # #i add chack if solve for me
    # if not chackIfSolve(problem):
    #     print("ERROR!!!")
    #     return
    for i in range(len(problem[0])):
        if i % (N * N) == 0:
            print()
        x = str(problem[0][i])
        pad = (math.ceil(math.log(N * N, 10)) - len(x))
        print(pad * " ", x, end="")
    print()

# def chackIfSolve(p):
#     if not is_solved(p):
#         return False
#     for v1 in range(len(p[0])):
#         for v2 in range(len(p[0])):
#             if not is_consistent(p,v1,v2,p[0][v1],p[0][v2]):
#                 return False
#     return True
