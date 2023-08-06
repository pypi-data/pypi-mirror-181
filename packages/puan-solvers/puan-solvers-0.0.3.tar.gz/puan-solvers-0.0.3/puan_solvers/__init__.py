import maz
import operator
import puan.ndarray
import numpy
import typing
import functools
import npycvx
import itertools
from scipy import optimize

def convert_bound_to_constraint(bound: tuple, index: int, num_vars: int) -> numpy.ndarray:
    """
        Converts a variable bound to constraints

        Parameters
        ----------
            bound : ``tuple`` (lower, upper)
                a tuple with the lower and upper bound

            index : ``int``
                index of the variable
            
            num_vars : ``int``
                number of variables 

        Examples
        --------
            >>> convert_bound_to_constraint((-10, 10), 2, 5)
            array([[-10.,   0.,   1.,   0.,   0.],
                   [-10.,   0.,  -1.,   0.,   0.]])

        Returns
        -------
            out : :class:`numpy.ndarray`
        
        Notes
        -----
            A constraint is only created for bounds between the default int bounds.
    """
    res = None
    if bound[0] > puan.default_int_bounds[0]:
        constr = numpy.zeros((1,num_vars))
        constr[0,0] = bound[0]
        constr[0,index] = 1
        res = constr
    
    if bound[1] < puan.default_int_bounds[1]:
        constr = numpy.zeros((1,num_vars))
        constr[0, 0] = -bound[1]
        constr[0, index] = -1
        if res is not None:
            res = numpy.append(res, constr, axis=0)
        else: 
            res = constr
    return res

def convert_variable_bounds_to_constraints(ge_polyhedron: puan.ndarray.ge_polyhedron) -> puan.ndarray.ge_polyhedron:
    """
        Converts variable bounds of a polyhedron to constraints

        Parameters
        ----------
            ge_polyhedron : :class:`puan.ndarray.ge_polyhedron`
                a polyhedron

        Examples
        --------
            >>> import puan
            >>> convert_variable_bounds_to_constraints(
            ...    puan.ndarray.ge_polyhedron([[4, 1, 1]],
            ...         [puan.variable(0, (1,1)),
            ...          puan.variable("x", bounds=(1,4)),
            ...          puan.variable("y")]))
            ge_polyhedron([[ 4,  1,  1],
                           [ 1,  1,  0],
                           [-4, -1,  0]])

        Returns
        -------
            out : :class:`puan.ndarray.ge_polyhedron`
        
        Notes
        -----
            A constraint is only created for integer variables with bounds between the default int bounds.
    """
    return puan.ndarray.ge_polyhedron(
        numpy.vstack(
            [
                ge_polyhedron, 
                *list(
                    filter(
                        lambda x: x is not None,
                        map(
                            lambda x: convert_bound_to_constraint(x[1].bounds.as_tuple(), x[0], ge_polyhedron.variables.shape[0]),
                            filter(
                                lambda x: x[1].bounds.lower != x[1].bounds.upper and x[1].bounds.as_tuple() != (0,1),
                                enumerate(ge_polyhedron.variables)
                            )
                        )
                    )
                )
            ]
        ).reshape((-1, ge_polyhedron.variables.shape[0])),
        variables=ge_polyhedron.variables,
    )

def glpk_solver(ge_polyhedron: puan.ndarray.ge_polyhedron, objectives: typing.Iterable[numpy.ndarray], add_integer_constraints: bool = False) -> typing.Iterable[typing.Tuple[numpy.ndarray, int, int]]:
    
    """
        Maximizes objective functions :math:`c \cdot x` such that :math:`Ax \ge b` using `GLPK` solver through npycvx python package. 
        Variable bounds are set in ``ge_polyhedron.variables``, where each variable in :class:`ge_polyhedron` has the attribute ``bounds``.

        Solution status codes:
            - 1: solution is undefined
            - 2: solution is feasible
            - 3: solution is infeasible (will never occur for GLPK in npycvx)
            - 4: no feasible solution exists (will never occur for GLPK in npycvx)
            - 5: solution is optimal
            - 6: solution is unbounded (will never occur for GLPK in npycvx)

        Parameters
        ----------
            ge_polyhedron : :class:`puan.ndarray.ge_polyhedron`
                a polyhedron with greater or equal sign between A and b.

            objectives : Iterable[:class:`numpy.ndarray`]
                an iterable of some kind of numpy ndarrays

            add_integer_constraints : ``bool``
                if polyhedron automatically should add constraints to represent variable's bounds if variable is integer

        Examples
        --------
            >>> import puan, numpy
            >>> polyhedron = puan.ndarray.ge_polyhedron([[1, 1, 1]])
            >>> # no variables given to polyhedron defaults to list of boolean variables
            >>> objectives = numpy.array([[1,1]])
            >>> list(glpk_solver(polyhedron, objectives))
            [(array([1., 1.]), 2.0, 5)]

        Returns
        -------
            out : Iterable[Tuple[:class:`numpy.ndarray`, ``int``, ``int``]]

    """
    if add_integer_constraints:
        extended_polyhedron = convert_variable_bounds_to_constraints(ge_polyhedron)
    else:
        extended_polyhedron = ge_polyhedron

    solver_partial = functools.partial(
        npycvx.solve_lp, 
        *npycvx.convert_numpy(
            extended_polyhedron.A, 
            extended_polyhedron.b,
            set(map(int, extended_polyhedron.A.integer_variable_indices)),
        ), 
        False, # means maximize
    )
    objs1, objs2 = itertools.tee(objectives, 2)
    return itertools.starmap(
        lambda obj, sol_sc: (
            sol_sc[0],
            sol_sc[0].dot(obj) if sol_sc[0] is not None else None,
            sol_sc[1],
        ),
        zip(
            objs2,
            map(
                maz.compose(
                    lambda x_status_code: (
                        x_status_code[1], 
                        5 if x_status_code[0] == 'optimal' else 3,
                    ),
                    solver_partial,
                ),
                objs1
            )
        )
    )

def scipy_solver(ge_polyhedron: puan.ndarray.ge_polyhedron, objectives: typing.Iterable[numpy.ndarray]) -> typing.Iterable[typing.Tuple[numpy.ndarray, int, int]]:
    
    """
        Maximizes objective functions :math:`c \cdot x` such that :math:`Ax \ge b` using `SciPys` solver through the SciPy python package. 
        Variable bounds are set in ``ge_polyhedron.variables``, where each variable in :class:`ge_polyhedron` has the attribute ``bounds``.

        Solution status codes:
            - 1: solution is undefined (will never occur for scipy)
            - 2: solution is feasible (will never occur for scipy)
            - 3: solution is infeasible
            - 4: no feasible solution exists
            - 5: solution is optimal
            - 6: solution is unbounded

        Parameters
        ----------
            ge_polyhedron : :class:`puan.ndarray.ge_polyhedron`
                a polyhedron with greater or equal sign between A and b.

            objectives : Iterable[:class:`numpy.ndarray`]
                an iterable of some kind of numpy ndarrays

        Notes
        -----
            Status of solution from SciPy solver has been compromised: 
                - Status code 1 ("Iteration or time limit reached") from SciPy is status code 4 ("no feasible solution exists").
                - Status code 4 ("The HiGHS solver ran into a problem") from SciPy is status code 4 ("no feasible solution exists").

        Returns
        -------
            out : Iterable[Tuple[:class:`numpy.ndarray`, ``int``, ``int``]]

    """

    status_code_map = {
        0: 5,
        1: 4,
        2: 3,
        3: 6,
        4: 4
    }
    return map(
        lambda x: (
            x.x, 
            int(x.fun)*-1 if x.fun is not None else None, # multiply -1 because scipy is minimizing and we expect maximization
            status_code_map.get(x.status)
        ),
        map(
            functools.partial(
                optimize.linprog,
                A_ub=ge_polyhedron.A * -1, 
                b_ub=ge_polyhedron.b * -1,
                bounds=list(
                    map(
                        maz.compose(
                            operator.methodcaller("as_tuple"),
                            operator.attrgetter("bounds")
                        ),
                        ge_polyhedron.A.variables
                    )
                ),
                method='highs',
                integrality=numpy.ones(
                    ge_polyhedron.A.variables.size, 
                    dtype=int
                ),
            ),
            map(
                # because scipy is minimizing and we expect maximization
                functools.partial(
                    operator.mul,
                    -1
                ),
                objectives,
            ),
        )
    )