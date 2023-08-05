# FelooPy: An integrated optimization environment for AutoOR in Python

FelooPy (an abbreviation for feasible, logical, optimal, and Python) is a hyper-optimization interface and an integrated optimization environment (IOE) that provides an all-in-one exact and heuristic optimization tool for AutoOR in Python. The motivation behind the development of FelooPy is to move the focus of operations research scientists from coding to modeling, and from modeling to analysis/analytics to automate time-consuming, iterative tasks of optimization model development, debugging, and implementation. FelooPy can currently give you access to more than 172 single-objective heuristic optimization solvers (thanks to `mealpy` interface) and 81 single-objective commercial and open-source exact optimization solvers (thanks to `pyomo`,`pulp`,`ortools`, `gekko`, `cplex`, `gurobi`, `xpress`, `picos`, `pymprog`, `cvxpy`, `cylp`, `linopy`, and `mip` interfaces), all with the same coding syntax! Besides, FelooPy automates common tasks in the optimization process and analytics, by providing tools such as sensitivity analysis, automated encoding/decoding (representation method) for heuristic optimization, timers, and more, all in the Python programming language environment.

## Features

- **Free** and **Open-Source** (FOSS) IOE developed under **MIT** license.
- **Easy** OR model development **workflow**.
- **All-in-One** optimization toolbox.
- Uses **single** optimization programming syntax for **14** **exact** and **heuristic** optimization interfaces in Python.
- Solves an optimization model with **81** exact and **172+5** heuristic optimization solvers (total: **256** optimization algorithms).
- Supports **scalable** optimization for **large-scale** real-world problems.
- Supports **benchmarking** of an optimization problem with various solvers.
- Supports **multi-parameter** sensitivity analysis on a single objective.
- Supports **multi-criteria** and **multi-objective** optimization (coming soon).
- ...