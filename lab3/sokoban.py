#!/usr/bin/env python3

import argparse
import sys, os
import re

def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Solve Sudoku problems.')
    parser.add_argument("-i", help="Path to the file with the Sokoban instance.")
    return parser.parse_args(argv)

class SokobanGame(object):
    """ A Sokoban Game. """
    def __init__(self, string):
        """ Create a Sokoban game object from a string representation such as the one defined in
            http://sokobano.de/wiki/index.php?title=Level_format
        """
        lines = string.split('\n')
        self.h, self.w = len(lines), max(len(x) for x in lines)
        self.player = None
        self.walls = set()
        self.boxes = set()
        self.goals = set()
        for y, line in enumerate(lines, 0):
            for x, char in enumerate(line, 0):
                if char == '#':  # Wall
                    self.walls.add((x,y))
                elif char == '@':  # Player
                    assert self.player is None
                    self.player = (x,y)
                elif char == '+':  # Player on goal square
                    assert self.player is None
                    self.player = (x,y)
                    self.goals.add((x,y))
                elif char == '$':  # Box
                    self.boxes.add((x,y))
                elif char == '*':  # Box on goal square
                    self.boxes.add((x,y))
                    self.goals.add((x,y))
                elif char == '.':  # Goal square
                    self.goals.add((x,y))
                elif char == ' ':  # Space
                    pass  # No need to do anything
                else:
                    raise ValueError(f'Unknown character "{char}"')

    def is_wall(self, x, y):
        """ Whether the given coordinate is a wall. """
        return (x, y) in self.walls

    def is_box(self, x, y):
        """ Whether the given coordinate has a box. """
        return (x, y) in self.boxes

    def is_goal(self, x, y):
        """ Whether the given coordinate is a goal location. """
        return (x, y) in self.goals


def intToLoc(i,j):
    return "x%sy%s " % (i, j)

def getAdjacent(i, j, dir):
    if (dir == "n"):
        return (i, j-1)
    elif (dir == "s"):
        return (i, j+1)
    elif (dir == "w"):
        return (i-1, j)
    elif (dir == "e"):
        return (i+1, j)
    else:
        print("ERROR in direction")

DIR = ["n", "s", "e", "w"]

def getProblemInstance(board):
    resultingInstance = "(define (problem sokoban-easy) (:domain sokoban)\n(:objects \n"
    
    """objects"""
    # first, make all locations
    locations = ""
    for y in range(0,board.h):
        for x in range(0, board.w):
            locations += intToLoc(x, y)
        locations += "\n"
    locations += " - location\n"
    resultingInstance += locations

    # second, add teleporter, end objects & open init
    resultingInstance += "tele - teleporter\n)\n\n(:init \n"
    
    """ init """
    # specify agent position
    resultingInstance += "(at-agent " + intToLoc(board.player[0], board.player[1]) + ")\n"

    # specify target positions
    targets = ""
    for goal in board.goals:
        targets += "(is-target " + intToLoc(goal[0], goal[1]) + ")\n"
    resultingInstance += targets

    # get walls
    walls = ""
    for wall in board.walls:
        walls += "(is-wall " + intToLoc(wall[0], wall[1]) + ")\n"
    resultingInstance += walls

    # set boxes
    boxes = ""
    for box in board.boxes:
        boxes += "(is-box " + intToLoc(box[0], box[1]) + ")\n"
        if (board.is_goal(box[0], box[1])):
            boxes += "(target-satisfied " + intToLoc(box[0], box[1]) + ")\n"
    resultingInstance += boxes

    # set connections
    connections_h = ""
    connections_v = ""
    for y in range(0, board.h):
        for x in range(0, board.w):
            if board.is_wall(x,y):
                continue
            # check for each part each direction (n, e, s, w)
            for dir in DIR:
                adj = getAdjacent(x,y,dir)
                if (board.is_wall(adj[0], adj[1])):
                    continue
                # check boundaries
                if (adj[0] < 0 or adj[1] < 0 or adj[0] >= board.w or adj[1] >= board.h):
                    continue
                if (dir == "n" or dir == "s"):
                    connections_v += "(connected-v " + intToLoc(x, y) + " " + intToLoc(adj[0], adj[1]) + ")\n"
                    #connections_v += "(connected-v " + intToLoc(adj[0], adj[1]) + " " + intToLoc(i, j) + ")\n"
                else:
                    connections_h += "(connected-h " + intToLoc(x, y) + " " + intToLoc(adj[0], adj[1]) + ")\n"
                    #connections_h += "(connected-h " + intToLoc(adj[0], adj[1]) + " " + intToLoc(i, j) + ")\n"
    resultingInstance += ";horizontal\n" + connections_h
    resultingInstance += ";vertical\n" + connections_v

    """ goals """
    resultingInstance += ")\n\n(:goal (and \n"
    goals = ""
    for goal in board.goals:
        goals += "(target-satisfied " + intToLoc(goal[0], goal[1]) + ")\n"
    resultingInstance += goals + "))\n)"

    return resultingInstance

def main(argv):
    args = parse_arguments(argv)
    with open(args.i, 'r') as file:
        board = SokobanGame(file.read().rstrip('\n'))
    # TODO - Some of the things that you need to do:
    #  1. (Previously) Have a domain.pddl file somewhere in disk that represents the Sokoban actions and predicates.
    #  2. Generate an instance.pddl file from the given board, and save it to disk.
    #  3. Invoke some classical planner to solve the generated instance.
    #  3. Check the output and print the plan into the screen in some readable form.
    
    resultingInstance = getProblemInstance(board)

    """ solve """
    f = open('problem-out.pddl', "w")
    f.write(resultingInstance)
    f.close()

    os.system("python ./downward/fast-downward.py domain.pddl problem-out.pddl --search astar(lmcut())")

    """ read solution """
    f = open('sas_plan', 'r')
    lines = f.read().split("\n")
    prettyPrintSolution(lines)


def extractCoords(string):
    result = []
    numbers = re.findall(r'\d+', string)
    for i in range(0, len(numbers), 2):
        coords = (numbers[i], numbers[i+1])
        result.append(coords)
    return result

def getDirection(string):
    coords = extractCoords(string)
    x1,y1 = coords[0]
    x2,y2 = coords[1]
    if (x1 < x2):
        return "Move right\n"
    elif (x1 > x2):
        return "Move left\n"
    elif (y1 < y2):
        return "Move down\n"
    elif (y1 > y2):
        return "Move up\n"

"""
(teleport x4y4 x3y3 tele)
(move-box-vertical x3y3 x3y4 x3y5)
(move-horizontal x3y4 x2y4)
(move-box-vertical x2y4 x2y5 x2y6)
(move-vertical x2y5 x2y4)
(move-horizontal x2y4 x3y4)
(move-horizontal x3y4 x4y4)
"""
def prettyPrintSolution(solution):
    prettySol = ""
    for line in solution:
        if "move-horizontal" in line or "move-box-horizontal" in line:
            prettySol += getDirection(line)
        elif "move-vertical" in line or "move-box-vertical" in line:
            prettySol += getDirection(line)
        elif "teleport" in line:
            coords = extractCoords(line)
            x,y = coords[1]
            prettySol += "Teleport to position (%s, %s)\n" % (x, y)
        elif "cost" in line:
            prettySol += line[2:-12]
    print(prettySol)

if __name__ == "__main__":
    main(sys.argv[1:])
