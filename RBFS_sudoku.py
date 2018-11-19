import copy
import time

class Problem(object):

    def __init__(self, initial):
        self.initial = initial
        self.type = len(initial) 
        self.height = int(self.type/3)

    def goal_test(self, state):
        total = sum(range(1, self.type+1))

        for row in range(self.type):
            if (len(state[row]) != self.type) or (sum(state[row]) != total):
                return False

            column_total = 0
            for column in range(self.type):
                column_total += state[column][row]

            if (column_total != total):
                return False

        for column in range(0,self.type,3):
            for row in range(0,self.type,self.height):

                block_total = 0
                for block_row in range(0,self.height):
                    for block_column in range(0,3):
                        block_total += state[row + block_row][column + block_column]

                if (block_total != total):
                    return False

        return True

    def filter_values(self, values, used):
        return [number for number in values if number not in used]

    def get_spot(self, board, state):
        for row in range(board):
            for column in range(board):
                if state[row][column] == 0:
                    return row, column

    def filter_row(self, state, row):
        number_set = range(1, self.type+1)
        in_row = [number for number in state[row] if (number != 0)]
        options = self.filter_values(number_set, in_row)
        return options

    def filter_col(self, options, state, column):
        in_column = []
        for column_index in range(self.type):
            if state[column_index][column] != 0:
                in_column.append(state[column_index][column])
        options = self.filter_values(options, in_column)
        return options

    def filter_quad(self, options, state, row, column):
        in_block = []
        row_start = int(row/self.height)*self.height
        column_start = int(column/3)*3
        
        for block_row in range(0, self.height):
            for block_column in range(0,3):
                in_block.append(state[row_start + block_row][column_start + block_column])
        options = self.filter_values(options, in_block)
        return options    

    def actions(self, state):
        row,column = self.get_spot(self.type, state)

        options = self.filter_row(state, row)
        options = self.filter_col(options, state, column)
        options = self.filter_quad(options, state, row, column)

        for number in options:
            new_state = copy.deepcopy(state)
            new_state[row][column] = number
            yield new_state

class Node:

    def __init__(self, state, g):
        self.state = state
        self.g = g
        self.h = 0
        self.marked = 0
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 0:
                    self.h = self.h + 1

    def expand(self, problem):
        self.marked = 1
        return [Node(state, self.g + 1) for state in problem.actions(self.state)]

    def getAn(self):
        return self.g + self.h
        


def RBFS(problem):
    nodes = []
    start = Node(problem.initial, 0)

    nodes.append(start)
    
    while nodes:
        min_node = nodes[0]
        for node in nodes:
            if node.getAn() < min_node.getAn():
                min_node = node

        if problem.goal_test(min_node.state):
            return min_node.state

        nodes.remove(min_node)
        for node in min_node.expand(problem):
            nodes.append(node) 

    return None

def solve_RBFS(board):
    print ("\nSolving with RBFS ...")
    start_time = time.time()
    problem = Problem(board)
    solution = RBFS(problem)
    elapsed_time = time.time() - start_time

    if solution:
        print ("Found solution")
        for row in solution:
            print (row)
    else:
        print ("No possible solutions")

    print ("Time: " + str(elapsed_time))
