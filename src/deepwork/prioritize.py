"""Task prioritization function for deepwork."""

import pandas as pd
from typing import Optional

def prioritize_tasks(
    tasks: list[dict],
    method: str = "weighted",
    weights: Optional[dict] = None
) -> pd.DataFrame:
    """
    Rank tasks by priority using different prioritization methods.

    Parameters
    ----------
    tasks : list of dict
        List of task dictionaries. Each task should have:
        - 'name' : str (required)
        - 'deadline' : str, optional (format: 'YYYY-MM-DD')
        - 'effort' : int, optional (1-5 scale)
        - 'importance' : int, optional (1-5 scale)
    method : str, optional
        Prioritization method: 'weighted' or 'deadline'.
        Default is 'weighted'.
    weights : dict, optional
        Custom weights for 'weighted' method. Keys: 'importance', 'effort', 'deadline'.
        Default is {'importance': 0.5, 'effort': 0.3, 'deadline': 0.2}.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: name, priority_score, rank, and original task fields.

    Raises
    ------
    TypeError
        If tasks is not a list or contains non-dict items.
    ValueError
        If tasks is empty, method is invalid, or required fields are missing.

    Examples
    --------
    >>> tasks = [
    ...     {"name": "Fix bug", "importance": 5, "effort": 2},
    ...     {"name": "Write docs", "importance": 3, "effort": 4}
    ... ]
    >>> result = prioritize_tasks(tasks, method="weighted")
    """
    # return pd.DataFrame() # stub
    ...
