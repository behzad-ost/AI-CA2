from DFS_Sudoku import solve_dfs
from RBFS_sudoku import solve_RBFS
from BDFS_Sudoku import solve_bt

f = open("sample_test.txt", "r")
data = f.read()
data = data.split(" ")
size = (int)(data[0])

data = data[1]
data = data[1:-1]

data = data.split(",")

board = []
an = 0

for i in range(0, size):
      tmp = []
      for j in range(0, size):
            tmp.append((int)(data[an]))
            an = an + 1
      board.append(tmp)

board = [[0,0,0,8,4,0,6,5,0],
      [0,8,0,0,0,0,0,0,9],
      [0,0,0,0,0,5,2,0,1],
      [0,3,4,0,7,0,5,0,6],
      [0,6,0,2,5,1,0,3,0],
      [5,0,9,0,6,0,7,2,0],
      [1,0,8,5,0,0,0,0,0],
      [6,0,0,0,0,0,0,4,0],
      [0,5,2,0,8,6,0,0,0]]
      
print(board)

solve_dfs(board)
solve_bt(board)
solve_RBFS(board)