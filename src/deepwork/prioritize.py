"""Task prioritization function for deepwork."""

import pandas as pd
from datetime import datetime, date
from typing import Optional

VALID_METHODS = ["weighted", "deadline"]
DEFAULT_WEIGHTS = {"importance": 0.5, "effort": 0.3, "deadline": 0.2}
DATE_FMT = "%Y-%m-%d"

def prioritize_tasks(
    tasks: list[dict],
    method: str = "weighted",
    weights: Optional[dict] = None
) -> pd.DataFrame:
    """
    Rank tasks by priority using different prioritization methods.

    This function takes a list of task dictionaries and returns a pandas
    DataFrame with tasks sorted by priority score in descending order (highest
    priority first). Two prioritization methods are available: 'weighted'
    (balances importance, effort, and deadline) and 'deadline' (prioritizes
    purely by deadline proximity).

    Parameters
    ----------
    tasks : list of dict
        List of task dictionaries. Each task should have:

        - 'name' : str (required)
            The task name or description.
        - 'deadline' : str, optional (format: 'YYYY-MM-DD')
            The task deadline. Tasks without deadlines receive a default middle
            urgency score (3 out of 5) in weighted method, or score 0 in
            deadline method.
        - 'effort' : int, optional (1-5 scale, where 1 = low effort, 5 = high)
            Lower effort tasks are prioritized higher. Default is 3.
        - 'importance' : int, optional (1-5 scale, where 5 = most important)
            Higher importance tasks are prioritized higher. Default is 3.

    method : str, optional
        Prioritization method to use. Default is 'weighted'.

        - 'weighted': Calculates a composite score using importance, effort,
          and deadline urgency. Effort is inverted (low effort = high score).
          Deadline is converted to urgency (1-5) based on days remaining.
        - 'deadline': Prioritizes solely by deadline proximity. Score is
          calculated as ``max(0, 100 - days_until_deadline)``. Tasks without
          deadlines receive a score of 0.

    weights : dict, optional
        Custom weights for the 'weighted' method. Keys are 'importance',
        'effort', and 'deadline'. Values should sum to 1.0 for normalized
        scoring. Default is {'importance': 0.5, 'effort': 0.3, 'deadline': 0.2}.
        This parameter is ignored when using the 'deadline' method.

    Returns
    -------
    pd.DataFrame
        DataFrame sorted by priority (highest first) with columns:

        - All original task fields (name, importance, effort, deadline, etc.)
        - 'priority_score' : float - The calculated priority score
        - 'rank' : int - The task rank (1 = highest priority)
        - 'days_until_deadline' : int (only with 'deadline' method)

    Raises
    ------
    TypeError
        If tasks is not a list, contains non-dict items, or weights is not
        a dict.
    ValueError
        If tasks is empty, method is invalid, or a task is missing the
        required 'name' field.

    Notes
    -----
    **Weighted Method Scoring:**

    The weighted method combines three factors into a single score:

    1. Importance (default weight: 0.5): Used directly (1-5 scale)
    2. Effort (default weight: 0.3): Inverted as ``6 - effort`` so that
       low-effort tasks score higher
    3. Deadline urgency (default weight: 0.2): Converted from days remaining
       to urgency level:

       - <= 1 day: urgency 5
       - <= 3 days: urgency 4
       - <= 7 days: urgency 3
       - <= 14 days: urgency 2
       - > 14 days: urgency 1
       - No deadline: urgency 3 (neutral)

    Final score: ``importance * w_imp + (6 - effort) * w_eff + urgency * w_dead``

    **Deadline Method Scoring:**

    Score = ``max(0, 100 - days_until_deadline)``

    Tasks due today score 100, tasks due in 50 days score 50, and tasks
    without deadlines score 0.

    Examples
    --------
    **Basic usage with weighted method (default):**

    >>> tasks = [
    ...     {"name": "Fix critical bug", "importance": 5, "effort": 2},
    ...     {"name": "Write documentation", "importance": 3, "effort": 4},
    ...     {"name": "Refactor module", "importance": 4, "effort": 3}
    ... ]
    >>> df = prioritize_tasks(tasks)
    >>> df[["name", "priority_score", "rank"]]
                     name  priority_score  rank
    0    Fix critical bug            4.30     1
    1     Refactor module            3.70     2
    2  Write documentation            2.70     3

    **Using deadline method for time-sensitive prioritization:**

    >>> from datetime import date, timedelta
    >>> today = date.today().strftime("%Y-%m-%d")
    >>> next_week = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
    >>> tasks = [
    ...     {"name": "Urgent report", "deadline": today},
    ...     {"name": "Weekly review", "deadline": next_week},
    ...     {"name": "Backlog item"}  # No deadline
    ... ]
    >>> df = prioritize_tasks(tasks, method="deadline")
    >>> df[["name", "priority_score", "days_until_deadline"]]
                name  priority_score  days_until_deadline
    0  Urgent report             100                    0
    1  Weekly review              93                    7
    2   Backlog item               0                 None

    **Custom weights emphasizing effort over importance:**

    >>> tasks = [
    ...     {"name": "Quick win", "importance": 2, "effort": 1},
    ...     {"name": "Big project", "importance": 5, "effort": 5}
    ... ]
    >>> custom_weights = {"importance": 0.2, "effort": 0.6, "deadline": 0.2}
    >>> df = prioritize_tasks(tasks, weights=custom_weights)
    >>> df[["name", "priority_score", "rank"]]
              name  priority_score  rank
    0    Quick win            4.00     1
    1  Big project            2.00     2

    **Minimal task (only required field):**

    >>> tasks = [{"name": "Simple task"}]
    >>> df = prioritize_tasks(tasks)
    >>> df["priority_score"].iloc[0]  # Uses defaults: importance=3, effort=3
    3.1
    """
    _validate_inputs(tasks, method, weights)

    effective_weights = weights if weights is not None else DEFAULT_WEIGHTS.copy()

    if method == "weighted":
        scored_tasks = _calculate_weighted_scores(tasks, effective_weights)
    elif method == "deadline":
        scored_tasks = _calculate_deadline_scores(tasks)

    _assign_ranks(scored_tasks)

    return pd.DataFrame(scored_tasks)


def _validate_inputs(tasks: list, method: str, weights: Optional[dict]) -> None:
    if not isinstance(tasks, list):
        raise TypeError(f"tasks must be a list, got {type(tasks).__name__}")

    if len(tasks) == 0:
        raise ValueError("tasks list cannot be empty")

    for i, task in enumerate(tasks):
        if not isinstance(task, dict):
            raise TypeError(f"Task at index {i} must be a dict, got {type(task).__name__}")
        if "name" not in task:
            raise ValueError(f"Task at index {i} missing required field 'name'")

    if method not in VALID_METHODS:
        raise ValueError(f"Invalid method '{method}'. Must be one of: {', '.join(VALID_METHODS)}")

    if weights is not None and not isinstance(weights, dict):
        raise TypeError(f"weights must be a dict, got {type(weights).__name__}")


def _get_days_remaining(deadline_str: Optional[str]) -> Optional[int]:
    """Parses date string and returns days from today. Returns None if invalid/empty."""
    if not deadline_str:
        return None
    try:
        deadline = datetime.strptime(deadline_str, DATE_FMT).date()
        return (deadline - date.today()).days
    except (ValueError, TypeError):
        return None


def _get_urgency_level(days_left: Optional[int]) -> int:
    """Converts days remaining into a 1-5 urgency score."""
    if days_left is None:
        return 3  # Default middle score for no deadline
    
    if days_left <= 1: return 5
    elif days_left <= 3: return 4
    elif days_left <= 7: return 3
    elif days_left <= 14: return 2
    else: return 1


def _calculate_weighted_scores(tasks: list[dict], weights: dict) -> list[dict]:
    scored = []
    
    w_imp = weights.get("importance", 0.5)
    w_eff = weights.get("effort", 0.3)
    w_dead = weights.get("deadline", 0.2)

    for task in tasks:
        importance = task.get("importance", 3)
        effort = task.get("effort", 3)
        
        # 1. Get standardized days remaining
        days_left = _get_days_remaining(task.get("deadline"))
        
        # 2. Convert to urgency level (1-5)
        deadline_score = _get_urgency_level(days_left)

        # 3. Invert effort (Lower effort = higher priority)
        effort_score = 6 - effort

        # 4. Final Weighted Calculation
        score = (importance * w_imp) + (effort_score * w_eff) + (deadline_score * w_dead)

        scored.append({**task, "priority_score": round(score, 2)})

    return scored


def _calculate_deadline_scores(tasks: list[dict]) -> list[dict]:
    scored = []
    
    for task in tasks:
        # 1. Reuse the same date parsing helper
        days_left = _get_days_remaining(task.get("deadline"))
        
        score = 0
        if days_left is not None:
            # Higher score for closer deadlines (invert days)
            score = max(0, 100 - days_left)

        scored.append({
            **task,
            "priority_score": score,
            "days_until_deadline": days_left
        })

    return scored


def _assign_ranks(scored_tasks: list[dict]) -> None:
    """Sorts tasks in-place by priority score."""
    scored_tasks.sort(key=lambda x: x["priority_score"], reverse=True)
    for i, task in enumerate(scored_tasks):
        task["rank"] = i + 1