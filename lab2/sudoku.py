#!/usr/bin/env python3

import argparse
import itertools
import math
import sys

from utils import save_dimacs_cnf, solve
from math import sqrt


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Solve Sudoku problems.')
    parser.add_argument("board", help="A string encoding the Sudoku board, with all rows concatenated,"
                                      " and 0s where no number has been placed yet.")
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Do not print any output.')
    parser.add_argument('-c', '--count', action='store_true',
                        help='Count the number of solutions.')
    return parser.parse_args(argv)


def print_solution(solution):
    """ Print a (hopefully solved) Sudoku board represented as a list of 81 integers in visual form. """
    #print(f'Solution: {"".join(map(str, solution))}')
    print("Solution: {}".format({"".join(map(str, solution))}))
    print('Solution in board form:')
    Board(solution).print_board()


# def compute_solution(sat_assignment, variables, size):
def compute_solution(sat_assignment, size):
    solution = []
    
    for l in range(size*size):
        i= int(l/size) +1
        j= l%size +1

        found=False
        k=1        
        while(not found):
            if sat_assignment.get(generateVariableID(i, j, k, size))==1 :
                found=True
            else:
                k+=1
        
        if found: 
            solution.append(k)
        else:
            print("The solution mapping has failed")
            return []            



    return solution


def generate_theory(board, verbose):
    """ Generate the propositional theory that corresponds to the given board. """
    size = board.size()
    clauses = []

    #variables = {} ##not used

    # Generate clauses

    for K in range(1, size+1):
        # ROW clauses
        for I in range(1, size+1):
            # Clause: The number k must appear at least once in row I
            clause = []
            for j in range(1, size+1):
                clause.append(generateVariableID(I, j, K, size))

            clauses.append(clause)

            # Clause: The number k is allowed to appear at most once in row I
            for j in range(1, size):
                for l in range(j+1, size+1):

                    clauses.append(
                        [-generateVariableID(I, j, K, size), -generateVariableID(I, l, K, size)])

        # COLUMN clauses
        for J in range(1, size+1):
            # Clause: The number k must appear at least once in col J
            clause = []
            for i in range(1, size+1):
                clause.append(generateVariableID(i, J, K, size))

            clauses.append(clause)

            # Clause: The number k is allowed to appear at most once in col J
            for i in range(1, size):
                for l in range(i+1, size+1):

                    clauses.append(
                        [-generateVariableID(i, J, K, size), -generateVariableID(l, J, K, size)])

        # SUBMATRIX clauses
        for S in range(0, size):
            # Clause: The number k must appear at least once in submatrix S
            clause = []
            for l in range(0, size):
                i,j= subMatrixToGlobalCoord(S,l,size)

                clause.append(generateVariableID(i, j, K, size))

            clauses.append(clause)

            # Clause: The number k is allowed to appear at most once in submatrix S
            for l in range(0, size-1):
                i, j = subMatrixToGlobalCoord(S, l, size)
                for m in range(l+1, size):
                    n, o = subMatrixToGlobalCoord(S, m, size)
                    clauses.append(
                        [-generateVariableID(i, j, K, size), -generateVariableID(n, o, K, size)])

    ##Clause: In each cell one number at most is allowed to appear
    for I in range(1, size+1):
        for J in range(1, size+1):
            for k in range(1, size):
                for l in range(k+1, size+1) :
                    clauses.append(
                        [-generateVariableID(I, J, k, size), -generateVariableID(I, J, l, size)])
                        
    ##Include all the known truth values to the clauses
    for x,y in board.all_coordinates():
        value = board.value(x, y)
        if value != 0:
            clauses.append([generateVariableID(x+1,y+1,value,size)])
   #return clauses, variables, size
    return clauses, size

def generateVariableID(i, j, k, n):
    """ Generate a numerical id for a state variable of the form (Pijk) for convinience when using SAT solver """
    return round(1 + pow(n, 2)*(k-1) + pow(n, 1)*(i-1) + pow(n, 0)*(j-1))


def subMatrixToGlobalCoord(S, l, n):
    """ Transform submatrix coordinates (S=submatrix id, l= local position in submatrix) to global board coordinates i,j """
    b=int(sqrt(n))
    i = int(l/b) + b*int(S/b) + 1
    j = l%b + b*(S%b) + 1

    return i,j

def count_number_solutions(board, verbose=False):
    count = 0

    # TODO

    print("Number of solutions: {}".format(count))


def find_one_solution(board, verbose=False):
    # clauses, variables, size = generate_theory(board, verbose)
    clauses, size = generate_theory(board, verbose)
    # return solve_sat_problem(clauses, "theory.cnf", size, variables, verbose)
    return solve_sat_problem(clauses, "theory.cnf", size, verbose)


# def solve_sat_problem(clauses, filename, size, variables, verbose):
def solve_sat_problem(clauses, filename, size, verbose):
    # save_dimacs_cnf(variables, clauses, filename, verbose)
    numvars=pow(size,3)
    save_dimacs_cnf(numvars,clauses, filename, verbose)
    result, sat_assignment = solve(filename, verbose)
    if result != "SAT":
        if verbose:
            print("The given board is not solvable")
        return None
    # solution = compute_solution(sat_assignment, variables, size)
    solution = compute_solution(sat_assignment,size)
    if verbose:
        print_solution(solution)
    return sat_assignment


class Board(object):
    """ A Sudoku board of size 9x9, possibly with some pre-filled values. """

    def __init__(self, string):
        """ Create a Board object from a single-string representation with 81 chars in the .[1-9]
         range, where a char '.' means that the position is empty, and a digit in [1-9] means that
         the position is pre-filled with that value. """
        size = math.sqrt(len(string))
        if not size.is_integer():
            raise RuntimeError(
                "The specified board has length {} and does not seem to be square".format(len(string)))
        self.data = [0 if x == '.' else int(x) for x in string]
        self.size_ = int(size)

    def size(self):
        """ Return the size of the board, e.g. 9 if the board is a 9x9 board. """
        return self.size_

    def value(self, x, y):
        """ Return the number at row x and column y, or a zero if no number is initially assigned to
         that position. """
        return self.data[x*self.size_ + y]

    def all_coordinates(self):
        """ Return all possible coordinates in the board. """
        return ((x, y) for x, y in itertools.product(range(self.size_), repeat=2))

    def print_board(self):
        """ Print the board in "matrix" form. """
        assert self.size_ == 9
        for i in range(self.size_):
            base = i * self.size_
            row = self.data[base:base + 3] + ['|'] + self.data[base +
                                                               3:base + 6] + ['|'] + self.data[base + 6:base + 9]
            print(" ".join(map(str, row)))
            if (i + 1) % 3 == 0:
                print("")  # Just an empty line


def main(argv):
    args = parse_arguments(argv)
    board = Board(args.board)

    if args.count:
        count_number_solutions(board, verbose=False)
    else:
        find_one_solution(board, verbose=not args.quiet)


if __name__ == "__main__":
    main(sys.argv[1:])
