mod bfs;

use pyo3::prelude::*;
use crate::bfs::{calc_bfs, Matrix};


#[pyfunction]
fn py_bfs(py_matrix: Vec<Vec<i32>>, start_pos: (i32, i32), end_pos: (i32, i32), step_size: i32) -> Vec<(usize, usize)> {
    let mut matrix = Matrix::new();
    for row in py_matrix {
        matrix.add_row(row);
    }

    calc_bfs(matrix, (start_pos.0 as usize, start_pos.1 as usize), (end_pos.0 as usize, end_pos.1 as usize), step_size)
}

/// A Python module implemented in Rust.
#[pymodule]
fn wall_jumper(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_bfs, m)?)?;
    Ok(())
}

//Setup tests
#[cfg(test)]
mod tests {
    use crate::bfs::{calc_bfs, Matrix};

    #[test]
    fn test_pathfinding() {
        let mut matrix = Matrix::new();
        matrix.add_row(vec![0, 1, 2]);
        matrix.add_row(vec![5, 4, 3]);
        matrix.add_row(vec![6, 7, 8]);

        let path = calc_bfs(matrix, (0, 0), (2, 2), 1);

        assert_eq!(path, vec![(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2)]);
    }
}
