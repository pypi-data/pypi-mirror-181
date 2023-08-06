from __future__ import annotations

from typeguard import typechecked

from relational_calculus.domain_calculus import DomainCalculus
from relational_calculus.tuple_calculus import TupleCalculus
from excmanager.Task import SubTask
from jinja2 import Environment, FileSystemLoader

from pathlib import Path


@typechecked
def generate_exercise(
    subtask: SubTask,
    description: str,
    expression: TupleCalculus | DomainCalculus | str,
    *,
    correct_attributes_score_perc: float = 0.1,
    calculus_type: str = "tuple",
) -> dict[str, str]:
    """
    Generate an exercise for the given subtask.

    Parameters
    ----------
    subtask : SubTask
        The subtask to generate the exercise for.
    description : str
        The description of the exercise.
    expression : TupleCalculus | DomainCalculus | str
        The relational calculus expression to generate the exercise for. If the expression is a string, it is assumed that the string is a valid SQLite query.
    correct_attributes_score_perc : float, optional
        The percentage of the score that is given for correct attributes, by default 0.1
    calculus_type : str, optional
        The type of the relational calculus expression.
        Either "tuple" or "domain":
        - if "expression" is a string (SQLite query), this parameter is "tuple" by default
        - if "expression" is a TupleCalculus or DomainCalculus object, this parameter is "tuple" or "domain" respectively

    Returns
    -------
    dict[str, str]
        A dictionary with the following keys
        - "title.md": The title of the exercise
        - "task.md": The task of the exercise
        - "submission.py": The submission code cell
        - "solution.py": The solution code cell
    """
    # create the data for jinja2
    data = dict()
    # subtask - view https://github.com/rwth-acis/dbis-exercise-manager
    task_num = subtask.task.task
    if "." in task_num:
        task_num = task_num.split(".")[0]
    data["subtask"] = {
        "task": {
            "task": task_num,
        },
        "subtask": subtask.subtask,
        "points": subtask.points,
    }
    # description
    data["description"] = description
    # relational calculus expression
    correct_solution = ""
    if isinstance(expression, TupleCalculus):
        correct_solution = expression.to_sql()
    elif isinstance(expression, DomainCalculus):
        correct_solution = expression.to_sql()
    else:
        assert isinstance(expression, str)
        correct_solution = expression
    data["correct_solution"] = correct_solution
    # correct_attributes_score_perc
    data["correct_attributes_score_perc"] = correct_attributes_score_perc
    # import statements (tuple calculus or domain calculus)
    assert calculus_type in [
        "tuple",
        "domain",
    ], "calculus_type must be either 'tuple' or 'domain'"
    if isinstance(expression, TupleCalculus):
        calculus_type = "tuple"
    elif isinstance(expression, DomainCalculus):
        calculus_type = "domain"
    if calculus_type == "tuple":
        data["import_statement"] = "from relational_calculus.tuple_calculus import *"
    elif calculus_type == "domain":
        data["import_statement"] = "from relational_calculus.domain_calculus import *"

    # load the templates from resources / templates
    abs_path = Path(__file__).parent.resolve() / "resources/templates"
    abs_path = str(abs_path)
    env = Environment(loader=FileSystemLoader(abs_path))
    # render the templates
    # title.md.jinja2
    title_md = env.get_template("title.md.jinja2").render(data)
    # task.md.jinja2
    task_md = env.get_template("task.md.jinja2").render(data)
    # submission.py.jinja2
    submission_py = env.get_template("submission.py.jinja2").render(data)
    # solution.py.jinja2
    solution_py = env.get_template("solution.py.jinja2").render(data)

    # return the rendered templates
    return {
        "title.md": title_md,
        "task.md": task_md,
        "submission.py": submission_py,
        "solution.py": solution_py,
    }
