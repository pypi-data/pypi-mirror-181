import wall_jumper

matrix = [
    [1, 2, 2, 3],
    [6, 0, 4, 4],
    [7, 8, 9, 4]
]

print(wall_jumper.py_bfs(matrix, (1, 1), (3, 2), 1))