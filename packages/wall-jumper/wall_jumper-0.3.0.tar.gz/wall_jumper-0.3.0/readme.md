# Wall-jumper

A python library written in rust for the very specific purpose of finding a path through a height map (with a given max step height).

## Installation

```bash
pip install wall-jumper
```


## Usage

```python
import wall_jumper

start_pos = (1, 1)
end_pos = (3, 2)
step_height = 1

matrix = [
    [1, 1, 2, 3],
    [6, 0, 4, 4],
    [7, 8, 9, 4]
]

path = wall_jumper.find_path(matrix, start_pos, end_pos, step_height) 

print(path)
```
