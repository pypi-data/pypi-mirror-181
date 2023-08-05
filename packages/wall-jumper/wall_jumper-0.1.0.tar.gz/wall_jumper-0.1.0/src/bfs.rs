use std::collections::{HashMap, HashSet, VecDeque};

pub struct Matrix {
    data: Vec<Vec<i32>>,
}

impl Matrix{
    pub(crate) fn new() -> Matrix {
        Matrix { data: Vec::new() }
    }

    pub fn add_row(&mut self, row: Vec<i32>) {
        self.data.push(row);
    }

    fn get_movable(&self, x: usize, y: usize, ox: usize, oy: usize, step_size: i32) -> bool {
        let delta = self.get_value(x, y) - self.get_value(ox, oy)+step_size;

        if delta >= 0 {
            return true
        }

        return false
    }

    fn get_value(&self, x: usize, y: usize) -> i32 {
        self.data[y][x]
    }

   /*
    fn set_value(&mut self, x: usize, y: usize, value: i32) {
        self.data[y][x] = value;
    }

    */

    fn width(&self) -> usize {
        self.data[0].len()
    }

    fn height(&self) -> usize {
        self.data.len()
    }
}

pub fn calc_bfs(matrix: Matrix, start: (usize, usize), end: (usize, usize), step_size: i32) -> Vec<(usize, usize)> {
    let mut queue = VecDeque::new();
    let mut visited = HashSet::new();
    let mut parent = HashMap::new();

    queue.push_back(start);
    visited.insert(start);

    while !queue.is_empty() {
        let current = queue.pop_front().unwrap();

        if current == end {
            break;
        }

        let (x, y) = current;

        let mut neighbours = vec![];
            if x != matrix.width() -1 {
                neighbours.push((x+1, y))
            }

            if y != matrix.height() -1 {
                neighbours.push((x, y+1))
            }

            if x != 0 {
                neighbours.push((x - 1, y))
            }

            if y != 0 {
                neighbours.push((x, y - 1))
            }


        for neighbour in neighbours {
            let (nx, ny) = neighbour;

            if nx < matrix.width() && ny < matrix.height() && matrix.get_movable(x, y,nx, ny, step_size) && !visited.contains(&neighbour) {
                queue.push_back(neighbour);
                visited.insert(neighbour);
                parent.insert(neighbour, current);
            }
        }
    }

    let mut path = Vec::new();
    let mut current = end;

    while current != start {
        path.push(current);
        current = parent[&current];
    }

    path.push(start);
    path.reverse();

    path
}

