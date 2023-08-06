# DBIS Relational Calculus Exercise Generator

[![pypi](https://img.shields.io/pypi/pyversions/dbis-relational-calculus-exercise-generator)](https://pypi.org/project/dbis-relational-calculus-exercise-generator/)
[![PyPI Status](https://img.shields.io/pypi/v/dbis-relational-calculus-exercise-generator)](https://pypi.org/project/dbis-relational-calculus-exercise-generator/)

This library generates relational calculus exercises based on the [dbis-relational-calculus](https://pypi.org/project/dbis-relational-calculus) library.
# Installation
Install via pip:
```bash
pip install dbis-relational-calculus-exercise-generator
```
Most notably, following required packages are also installed:
 - [dbis-relational-calculus](https://pypi.org/project/dbis-relational-calculus)
 - [dbis-exc-manager](https://pypi.org/project/dbis-exc-manager/)

# Usage
```python
from rc_exercise_generator import generate_exercise

# set the solution, either SQLite query (string), or TupleCalculus / DomainCalculus object
solution_sql_query = "SELECT a, c FROM R;"

from excmanager.Task import Exercise, Task, SubTask
exercise1 = Exercise(1)
task1 = Task(exercise1, "1.1")
subtask1 = SubTask(task1, "a", points=2)
# task description
description = "Select the attributes a and c from the relation R."

generated_cells = generate_exercise(
	subtask1,
	description,
	solution_sql_query,
	correct_attributes_score_perc=0.1,
	calculus_type="tuple" # the student should submit a TupleCalculus solution
)

# generated_cells is a dictionary of cells, which can be used to generate a Jupyter Notebook
# format:
# filename (str) -> cell content (str)
```


## :warning: Guidelines
In order to directly use the generated cells in an exercise Jupyter notebook, one should follow the following guidelines:
 - [tasks](https://pypi.org/project/dbis-exc-manager/) should be named `task1`, `task2`, ...
 - The SQLite Connection has to be made beforehand. This connection should be stored in the variable `sql_con`.

View the [templates](rc_exercise_generator/resources/templates/README.md) and [this test](tests/test_correct.py) for more information on what cells are generated and how one can incorporate them into an exercise Jupyter notebook.


