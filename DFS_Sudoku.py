import copy
import time

class Problem(object):

    def __init__(self, initial):
        self.initial = initial
        self.type = len(initial)
        self.div = 5 if self.type == 25 else (3 if self.type == 9 else (4 if self.type == 16 else 4))
        self.height = int(self.type/self.div)

    def goal_test(self, state):
        total = sum(range(1, self.type+1))

        for row in range(self.type):
            if (len(state[row]) != self.type) or (sum(state[row]) != total):
                return False;

            column_total = 0
            for column in range(self.type):
                column_total += state[column][row]

            if (column_total != total):
                return False

        for column in range(0,self.type,self.div):
            for row in range(0,self.type,self.height):

                block_total = 0
                for block_row in range(0,self.height):
                    for block_column in range(0,self.div):
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
        in_column = [] # List of valid values in spot's column
        for column_index in range(self.type):
            if state[column_index][column] != 0:
                in_column.append(state[column_index][column])
        options = self.filter_values(options, in_column)
        return options

    def filter_quad(self, options, state, row, column):
        in_block = [] # List of valid values in spot's quadrant
        row_start = int(row/self.height)*self.height
        column_start = int(column/self.div)*self.div
        
        for block_row in range(0, self.height):
            for block_column in range(0,self.div):
                in_block.append(state[row_start + block_row][column_start + block_column])
        options = self.filter_values(options, in_block)
        return options    

    def actions(self, state):
        row,column = self.get_spot(self.type, state) # Get first empty spot on board

        options = self.filter_row(state, row)
        options = self.filter_col(options, state, column)
        options = self.filter_quad(options, state, row, column)

        for number in options:
            new_state = copy.deepcopy(state)
            new_state[row][column] = number
            yield new_state

class Node:

    def __init__(self, state):
        self.state = state

    def expand(self, problem):
        return [Node(state) for state in problem.actions(self.state)]

def DFS(problem):
    start = Node(problem.initial)
    if problem.goal_test(start.state):
        return start.state

    stack = []
    stack.append(start) 

    while stack:
        node = stack.pop()
        if problem.goal_test(node.state):
            return node.state
        stack.extend(node.expand(problem))

    return None

def solve_dfs(board):
    print ("\nSolving with DFS...")
    start_time = time.time()
    problem = Problem(board)
    solution = DFS(problem)
    elapsed_time = time.time() - start_time

    if solution:
        print ("Found solution")
        for row in solution:
            print (row)
    else:
        print ("No possible solutions")

    print ("Time: " + str(elapsed_time))
