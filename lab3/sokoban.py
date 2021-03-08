#!/usr/bin/env python3

import argparse
import sys
import codecs
import os
import re


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Solve Sudoku problems.')
    parser.add_argument(
        "-i", help="Path to the file with the Sokoban instance.")
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
        for i, line in enumerate(lines, 0):
            for j, char in enumerate(line, 0):
                if char == '#':  # Wall
                    self.walls.add((i, j))
                elif char == '@':  # Player
                    assert self.player is None

                    self.player = (i, j)
                elif char == '+':  # Player on goal square
                    assert self.player is None
                    self.player = (i, j)
                    self.goals.add((i, j))
                elif char == '$':  # Box
                    self.boxes.add((i, j))
                elif char == '*':  # Box on goal square
                    self.boxes.add((i, j))
                    self.goals.add((i, j))
                elif char == '.':  # Goal square
                    self.goals.add((i, j))
                elif char == ' ':  # Space
                    pass  # No need to do anything
                else:
                    print("unknown: ")
                    # raise ValueError(f'Unknown character "{char}"')

    def is_wall(self, x, y):
        """ Whether the given coordinate is a wall. """
        return (x, y) in self.walls

    def is_box(self, x, y):
        """ Whether the given coordinate has a box. """
        return (x, y) in self.boxes

    def is_goal(self, x, y):
        """ Whether the given coordinate is a goal location. """
        return (x, y) in self.goals


class pddlConverter(object):
    def __init__(self):
        self.problem_objects = []
        self.init_state = []
        self.goal_state = []

    def generateAt(self, name, loc):
        self.init_state.append("(at "+name+" "+loc+")")

    def generateAdjH(self, loc1, loc2):
        self.init_state.append("(adj_horizontal "+loc1+" "+loc2+")")

    def generateAdjV(self, loc1, loc2):
        self.init_state.append("(adj_vertical "+loc1+" "+loc2+")")

    # def generatePushable(self, name):
    #     self.init_state.append("(pushable "+name+")")

    def generateOccupied(self, loc):
        self.init_state.append("(occupied "+loc+")")

    # def generateAlive(self, name):
    #     self.init_state.append("(alive "+name+")")

    def generateTeleportAvaliable(self, name):
        self.init_state.append("(teleport_avaliable "+name+")")

    def writeBox(self, x, y):
        name = "box-"+str(x)+"-"+str(y)
        loc = "sq-"+str(x)+"-"+str(y)

        self.problem_objects.append(name+" - box")

        self.generateAt(name, loc)
        self.generateOccupied(loc)
        # self.generatePushable(name)

    def writeSquare(self, x, y):
        name = "sq-"+str(x)+"-"+str(y)
        self.problem_objects.append(name+" - location")

    # def writeWall(self, x, y):
    #     loc = "sq-"+str(x)+"-"+str(y)
    #     self.generateOccupied(loc)

    def writeGoal(self, x, y):
        loc = "sq-"+str(x)+"-"+str(y)
        self.goal_state.append("(occupied "+loc+")")

    def writeAgent(self, x, y):
        # One single agent is assumed
        name = "agent"
        loc = "sq-"+str(x)+"-"+str(y)
        self.problem_objects.append(name+" - agent")
        # self.generateAlive(name)
        self.generateTeleportAvaliable(name)
        self.generateAt(name, loc)

    def writeAdjH(self, x1, y1, x2, y2):
        loc1 = "sq-"+str(x1)+"-"+str(y1)
        loc2 = "sq-"+str(x2)+"-"+str(y2)
        self.generateAdjH(loc1, loc2)

    def writeAdjV(self, x1, y1, x2, y2):
        loc1 = "sq-"+str(x1)+"-"+str(y1)
        loc2 = "sq-"+str(x2)+"-"+str(y2)
        self.generateAdjV(loc1, loc2)


def getProblemInstance(board):

    converter = pddlConverter()
    for x in range(board.h):
        for y in range(board.w):

            if(board.is_wall(x, y)):
                    # converter.writeWall(x, y)
                    continue
            else:
                converter.writeSquare(x, y)
                if((not board.is_wall(x, y+1)) and (y+1 < board.w)):
                    converter.writeAdjH(x, y, x, y+1)
                    converter.writeAdjH(x, y+1, x, y)
                if((not board.is_wall(x+1, y)) and (x+1 < board.h)):
                    converter.writeAdjV(x, y, x+1, y)
                    converter.writeAdjV(x+1, y, x, y)
                if board.is_box(x, y):
                    converter.writeBox(x, y)
                elif board.is_goal(x, y):
                    converter.writeGoal(x, y)
                elif x == board.player[0] and y == board.player[1]:
                    converter.writeAgent(x, y)
                else:
                    continue

    problem_instance="(define (problem SokobanProblem) \n (:domain TeleportingSokobanDomain)\n" # Write problem header
    problem_instance+="(:objects \n"  # objects header
    for obj in converter.problem_objects:
            problem_instance+=obj  # objects
            problem_instance+="\n"
    problem_instance+=") \n"  # objects closure

    problem_instance+="(:init \n" # init header
    for state in converter.init_state:
            problem_instance+=state  # initial states
            problem_instance += "\n"
    problem_instance+=") \n"  # init closure

    problem_instance+="(:goal \n (and \n" #goal header
    for goal in converter.goal_state: 
            problem_instance+=goal  # goal states
            problem_instance += "\n"
    problem_instance+=") \n ) \n"  # goal closure

    problem_instance+="\n)" # Write problem closure
    return problem_instance


def extractCoords(string):
    result = []
    numbers = re.findall(r'\d+', string)
    for i in range(0, len(numbers), 2):
        coords = (numbers[i], numbers[i+1])
        result.append(coords)
    return result


def getDirection(string):
    coords = extractCoords(string)
    if len(coords)==4:
        x1, y1 = coords[1]
        x2, y2 = coords[2]
    else:
        x1, y1 = coords[0]
        x2, y2 = coords[1]
    
    
    if (x1 < x2):
        return "Move right\n"
    elif (x1 > x2):
        return "Move left\n"
    elif (y1 < y2):
        return "Move down\n"
    elif (y1 > y2):
        return "Move up\n"

def prettySolution(solution):
    prettySol = ""    
    for line in solution:
        # print(line)
        if "move_horizontal" in line or "push_horizontal" in line:
            prettySol += getDirection(line)
        elif "move_vertical" in line or "push_vertical" in line:
            prettySol += getDirection(line)
        elif "teleport" in line:
            coords = extractCoords(line)
            x,y = coords[1]
            prettySol += "Teleport to position (%s, %s)\n" % (x, y)
        elif "cost" in line:
            prettySol += line[2:-12]
    return prettySol


def main(argv):
    args = parse_arguments(argv)

    with codecs.open("benchmarks/sasquatch/level50.sok", 'r', "utf-8") as file:
        board = SokobanGame(file.read().rstrip('\n'))

    # TODO - Some of the things that you need to do:
    #  1. (Previously) Have a domain.pddl file somewhere in disk that represents the Sokoban actions and predicates.
    #  2. Generate an instance.pddl file from the given board, and save it to disk.
    #  3. Invoke some classical planner to solve the generated instance.
    #  3. Check the output and print the plan into the screen in some readable form.
    
    filename = "sokoban_problem.pddl"
    resultingInstance = getProblemInstance(board)

    """ solve """
    f = open(filename, "w")
    f.write(resultingInstance)
    f.close()

    os.system("sudo docker run --rm -v /home/magi.dalmau/Documents/git/miis-autonomous-systems-20-21/lab3:/lab3 aibasel/downward --plan-file /lab3/sas_plan --alias seq-sat-lama-2011 --overall-time-limit 60  /lab3/teleporting_sokoban_domain.pddl /lab3/sokoban_problem.pddl")


    """ read solution """
    f = open('sas_plan', 'r')
    lines = f.read().split("\n")
    f.close()
    prettySol = prettySolution(lines)
    print(prettySol)

    """ save solution """
    f = open('final-plan.txt', 'w')
    f.write(prettySol)
    f.close()


if __name__ == "__main__":
    main(sys.argv[1:])
