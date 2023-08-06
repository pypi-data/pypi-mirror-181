import numpy as np
import puan
import puan_solvers

def test_convert_variable_bounds_to_constraints():
    variables = [
        puan.variable(0, (1,1)),
        puan.variable("a", (-10,10)),
        puan.variable("b", (-5,-2)),
        puan.variable("c", (10,20)),
        puan.variable("d", (0,10)),
    ]
    polyhedron = puan.ndarray.ge_polyhedron([
        [-3, 0, 1, 0, 0],
        [-3, 0, 0, 0,-1],
    ], variables=variables)
    actual = puan_solvers.convert_variable_bounds_to_constraints(polyhedron)
    expected = np.array(
        [
            [ -3.,  0.,  1.,  0.,  0.],
            [ -3.,  0.,  0.,  0., -1.],
            [-10.,  1.,  0.,  0.,  0.],
            [-10., -1.,  0.,  0.,  0.],
            [ -5.,  0.,  1.,  0.,  0.],
            [  2.,  0., -1.,  0.,  0.],
            [ 10.,  0.,  0.,  1.,  0.],
            [-20.,  0.,  0., -1.,  0.],
            [  0.,  0.,  0.,  0.,  1.],
            [-10.,  0.,  0.,  0., -1.],
        ])
    assert np.array_equal(actual, expected)

    variables = [
        puan.variable(0, (1,1)),
        puan.variable("a", (0,1)),
        puan.variable("b", dtype="bool"),
        puan.variable("c", dtype="int")
    ]
    polyhedron = puan.ndarray.ge_polyhedron([
        [-3, 0, 1,  0],
        [-3, 0, 0, -1],
    ], variables=variables)
    actual = puan_solvers.convert_variable_bounds_to_constraints(polyhedron)
    expected = np.array(
        [
            [ -3.,  0.,  1.,  0.],
            [ -3.,  0.,  0., -1.]
        ])
    assert np.array_equal(actual, expected)

def test_solvers():

    tests = [
        (
            puan.ndarray.ge_polyhedron([[1, 1, 1]]),
            (
                [
                    np.array([1,1]),
                    np.array([-1,-1])
                ],
                [
                    (
                        [[1,1]],
                        2,
                        5
                    ),
                    (
                        [[1,0],[0,1]],
                        -1,
                        5
                    ),
                ]
            )
        ),
        (
            puan.ndarray.ge_polyhedron([[3, 1, 1]]),
            (
                [
                    np.array([1,1])
                ],
                [
                    (
                        [None],
                        None,
                        3
                    ),
                ]
            )
        ),
    ]
    for solver in [puan_solvers.glpk_solver, puan_solvers.scipy_solver]:
        for polyhedron, (objectives, expected) in tests:
            for (asolution, aobjective, astatus_code), (esolutions, eobjective, estatus_code) in zip(solver(polyhedron, iter(objectives)), expected):
                assert (asolution.tolist() if isinstance(asolution, np.ndarray) else None) in esolutions
                assert aobjective == eobjective
                assert astatus_code == estatus_code

    polyhedron = puan.ndarray.ge_polyhedron([[-3, -1, 0], [-2, -1, 1]], variables=[puan.variable(0, (1,1)), puan.variable('x', (0,5)), puan.variable('y')]) 
    objectives = np.array([[1,1],[-1,-1]])
    expected = [
        (
            np.array([3,1]),
            4,
            5
        ),
        (
            np.array([0,0]),
            0,
            5
        ),
    ]
    for (actual_solution, actual_objective, actual_status_code), (expected_solution, expected_objective, expected_status_code) in zip(puan_solvers.glpk_solver(polyhedron, objectives, True), expected):
        assert (actual_solution == expected_solution).all()
        assert actual_objective == expected_objective
        assert actual_status_code == expected_status_code
