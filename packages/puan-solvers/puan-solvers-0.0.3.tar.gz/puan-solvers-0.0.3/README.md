# Puan Solvers

Wrappers for integer linear programming solvers together with [puan-python](https://github.com/ourstudio-se/puan-python).

### Install
```bash
pip install puan-solvers
```

### Usage
Here is a simple example of creating a model using puan-python and solving using GLPK solver.
```python
import puan_solvers as ps
import puan.logic.plog as pg # <- pip install puan

# Create a model: E.g. exactly one of x, y and z must be selected
model = pg.Xor(*"xyz", variable="A")

# Finds a solution that maximizing objective such that all constraints in model are satisfied
for sol in model.solve([{"x": 1, "y": 2}], solver=ps.glpk_solver):
    print(sol)
```
