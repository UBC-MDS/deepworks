"""Tests for prioritize_tasks function."""

import pytest
import pandas as pd
from deepworks.prioritize import prioritize_tasks


def test_weighted_method_returns_dataframe():
    """
    Test that the weighted method returns a pandas DataFrame.

    The prioritize_tasks function should always return a pandas DataFrame
    regardless of the prioritization method used. This test verifies the
    return type when using the 'weighted' method (the default) with multiple
    tasks containing importance and effort values.
    """
    tasks = [
        {"name": "Task A", "importance": 5, "effort": 2},
        {"name": "Task B", "importance": 3, "effort": 4},
    ]
    result = prioritize_tasks(tasks, method="weighted")
    assert isinstance(result, pd.DataFrame)

def test_weighted_method_has_required_columns():
    """
    Test that the result DataFrame contains all required columns.

    The returned DataFrame should include:
    - 'name': The original task name (required input field)
    - 'priority_score': The calculated weighted score combining importance,
      effort (inverted), and deadline urgency
    - 'rank': The task rank where 1 = highest priority
    """
    tasks = [
        {"name": "Task A", "importance": 5, "effort": 2},
    ]
    result = prioritize_tasks(tasks, method="weighted")
    assert "name" in result.columns
    assert "priority_score" in result.columns
    assert "rank" in result.columns

def test_higher_importance_ranks_higher():
    """
    Test that higher importance values result in higher priority rankings.

    In the weighted method, importance has a default weight of 0.5 (50% of score).
    Tasks with higher importance values (on a 1-5 scale where 5 = most important)
    should receive higher priority scores and thus lower rank numbers
    (rank 1 = highest priority). This test holds effort constant to isolate
    the effect of importance on ranking.
    """
    tasks = [
        {"name": "Low", "importance": 1, "effort": 3},
        {"name": "High", "importance": 5, "effort": 3},
    ]
    result = prioritize_tasks(tasks, method="weighted")
    high_rank = result[result["name"] == "High"]["rank"].values[0]
    low_rank = result[result["name"] == "Low"]["rank"].values[0]
    assert high_rank < low_rank  # Lower rank number = higher priority

def test_deadline_method_returns_dataframe():
    """
    Test that the deadline method returns a pandas DataFrame.

    The 'deadline' method prioritizes tasks solely by deadline proximity,
    ignoring importance and effort values. The score is calculated as
    max(0, 100 - days_until_deadline). This test verifies that the method
    correctly returns a DataFrame when provided with tasks containing
    deadline strings in 'YYYY-MM-DD' format.
    """
    tasks = [
        {"name": "Task A", "deadline": "2026-01-15"},
        {"name": "Task B", "deadline": "2026-01-20"},
    ]
    result = prioritize_tasks(tasks, method="deadline")
    assert isinstance(result, pd.DataFrame)

def test_invalid_date_format_handling():
    """
    Test that invalid date formats are handled gracefully.

    When a deadline string cannot be parsed (e.g., 'not-a-date' instead of
    'YYYY-MM-DD'), the function should not raise an exception. Instead, it
    treats the task as having no deadline, which results in a default urgency
    score of 3 (neutral/middle value) in the weighted method calculation.
    The task should still receive a valid priority_score based on its other
    attributes (importance and effort).
    """
    tasks = [{"name": "Bad Date", "deadline": "not-a-date", "importance": 5}]
    # Current behavior: fails silently and treats as no deadline (score 3 for deadline)
    result = prioritize_tasks(tasks, method="weighted")
    # You might want to assert that a warning is logged or a specific default is used
    assert result.iloc[0]["priority_score"] > 0

def test_out_of_bound_values():
    """
    Test behavior when importance or effort values exceed the expected 1-5 scale.

    The function does not enforce bounds on importance or effort values.
    When values exceed the expected 1-5 range (e.g., importance=100), the
    weighted calculation proceeds without clamping, which can result in
    significantly higher scores (e.g., 100 * 0.5 = 50 for importance alone).
    This test documents the current behavior where out-of-bound values are
    accepted and processed, potentially skewing priority rankings.
    """
    tasks = [
        {"name": "Super Important", "importance": 100, "effort": 1},
        {"name": "Normal", "importance": 5, "effort": 1}
    ]
    result = prioritize_tasks(tasks, method="weighted")
    # Currently, 100 * 0.5 = 50, skewing the results heavily.
    assert result.iloc[0]["priority_score"] > result.iloc[1]["priority_score"]

def test_empty_input_list():
    """
    Test that an empty tasks list raises a ValueError.

    The function requires at least one task to prioritize. Passing an empty
    list should raise a ValueError with the message 'tasks list cannot be empty'
    to provide clear feedback about the invalid input.
    """
    with pytest.raises(ValueError, match="tasks list cannot be empty"):
        prioritize_tasks([], method="weighted")

def test_single_task():
    """
    Test that a single task is processed correctly and assigned rank 1.

    When only one task is provided, it should still be processed through the
    prioritization logic and returned in a DataFrame. The single task should
    always receive rank 1 (highest priority) since there are no other tasks
    to compare against.
    """
    tasks = [{"name": "Only Task", "importance": 3}]
    result = prioritize_tasks(tasks)
    assert len(result) == 1
    assert result.iloc[0]["rank"] == 1

def test_missing_optional_fields():
    """
    Test that tasks with missing optional fields use default values.

    Only the 'name' field is required. When optional fields are omitted:
    - importance: defaults to 3 (middle of 1-5 scale)
    - effort: defaults to 3 (middle of 1-5 scale)
    - deadline: defaults to None (receives urgency score of 3 in weighted method)

    The function should successfully calculate a priority_score using these
    defaults without raising any errors.
    """
    tasks = [{"name": "Minimal Task"}]  # No importance, effort, or deadline
    result = prioritize_tasks(tasks)
    assert len(result) == 1
    assert "priority_score" in result.columns

def test_custom_weights():
    """
    Test that custom weights override the default weighting scheme.

    Default weights are: importance=0.5, effort=0.3, deadline=0.2.
    By providing custom weights (e.g., importance=1.0, effort=0, deadline=0),
    the scoring formula changes to prioritize only the specified factor.

    In this test, with 100% weight on importance and 0% on effort/deadline:
    - Task A (importance=5, effort=1): score = 5 * 1.0 = 5.0
    - Task B (importance=1, effort=5): score = 1 * 1.0 = 1.0
    Task A should rank first despite having lower effort.
    """
    tasks = [
        {"name": "A", "importance": 5, "effort": 1},
        {"name": "B", "importance": 1, "effort": 5},
    ]
    # Weight importance heavily
    result = prioritize_tasks(tasks, weights={"importance": 1.0, "effort": 0, "deadline": 0})
    assert result.iloc[0]["name"] == "A"  # Higher importance wins

def test_deadline_method_no_deadline():
    """
    Test that tasks without deadlines receive a score of 0 in deadline method.

    The deadline method calculates priority_score as max(0, 100 - days_until_deadline).
    When a task has no deadline, the days_until_deadline is None, and the
    function assigns a score of 0. This ensures tasks without deadlines are
    deprioritized in favor of time-sensitive tasks when using this method.
    """
    tasks = [{"name": "No Deadline"}]
    result = prioritize_tasks(tasks, method="deadline")
    assert result.iloc[0]["priority_score"] == 0

def test_tasks_not_list_raises_typeerror():
    """
    Test that passing a non-list type for tasks raises a TypeError.

    The tasks parameter must be a list of dictionaries. Passing other types
    (e.g., a string, tuple, or single dict) should raise a TypeError with
    a descriptive message indicating that 'tasks must be a list'.
    """
    with pytest.raises(TypeError, match="tasks must be a list"):
        prioritize_tasks("not a list")

def test_empty_tasks_raises_valueerror():
    """
    Test that an empty tasks list raises a ValueError.

    This test verifies the input validation that prevents processing an empty
    list. The function should raise a ValueError with a message containing
    'cannot be empty' to indicate that at least one task is required for
    prioritization.
    """
    with pytest.raises(ValueError, match="cannot be empty"):
        prioritize_tasks([])

def test_task_not_dict_raises_typeerror():
    """
    Test that non-dictionary items in the tasks list raise a TypeError.

    Each item in the tasks list must be a dictionary containing at least a
    'name' key. If any item is not a dictionary (e.g., a string or integer),
    the function should raise a TypeError indicating that the task 'must be
    a dict'.
    """
    with pytest.raises(TypeError, match="must be a dict"):
        prioritize_tasks(["not a dict"])

def test_missing_name_raises_valueerror():
    """
    Test that a task dictionary missing the required 'name' field raises ValueError.

    The 'name' field is the only required field for each task dictionary.
    Tasks may omit importance, effort, and deadline (which have defaults),
    but must always include a 'name'. A ValueError with message "missing
    required field 'name'" should be raised when this validation fails.
    """
    with pytest.raises(ValueError, match="missing required field 'name'"):
        prioritize_tasks([{"importance": 5}])

def test_invalid_method_raises_valueerror():
    """
    Test that an invalid prioritization method raises a ValueError.

    Only two methods are supported: 'weighted' and 'deadline'. Passing any
    other string (e.g., 'invalid', 'priority', etc.) should raise a ValueError
    with a message containing 'Invalid method' and listing the valid options.
    """
    with pytest.raises(ValueError, match="Invalid method"):
        prioritize_tasks([{"name": "Task"}], method="invalid")


def test_invalid_weights_type_raises_typeerror():
    """
    Test that passing a non-dictionary type for weights raises a TypeError.

    The weights parameter, when provided, must be a dictionary with keys
    'importance', 'effort', and/or 'deadline' mapping to numeric weights.
    Passing other types (e.g., a string or list) should raise a TypeError
    with the message 'weights must be a dict'.
    """
    with pytest.raises(TypeError, match="weights must be a dict"):
        prioritize_tasks([{"name": "Task"}], weights="not a dict")


def test_urgency_level_one_day_deadline():
    """
    Test that deadlines <= 1 day away receive urgency level 5 (highest).

    The weighted method converts days remaining to urgency levels:
    - <= 1 day: urgency 5 (most urgent)

    With default weights (importance=0.5, effort=0.3, deadline=0.2) and
    task values (importance=3, effort=3, deadline=tomorrow):
    - importance_score = 3 * 0.5 = 1.5
    - effort_score = (6 - 3) * 0.3 = 0.9  (effort is inverted)
    - deadline_score = 5 * 0.2 = 1.0
    - Total = 1.5 + 0.9 + 1.0 = 3.4
    """
    from datetime import date, timedelta
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    tasks = [{"name": "Urgent", "deadline": tomorrow, "importance": 3, "effort": 3}]
    result = prioritize_tasks(tasks, method="weighted")
    # With urgency 5: score = 3*0.5 + 3*0.3 + 5*0.2 = 1.5 + 0.9 + 1.0 = 3.4
    # effort_score = 6 - 3 = 3, so: 3*0.5 + 3*0.3 + 5*0.2 = 1.5 + 0.9 + 1.0 = 3.4
    assert result.iloc[0]["priority_score"] == 3.4


def test_urgency_level_three_days_deadline():
    """
    Test that deadlines <= 3 days away receive urgency level 4.

    The weighted method converts days remaining to urgency levels:
    - <= 3 days (but > 1 day): urgency 4

    With default weights (importance=0.5, effort=0.3, deadline=0.2) and
    task values (importance=3, effort=3, deadline=3 days from now):
    - importance_score = 3 * 0.5 = 1.5
    - effort_score = (6 - 3) * 0.3 = 0.9  (effort is inverted)
    - deadline_score = 4 * 0.2 = 0.8
    - Total = 1.5 + 0.9 + 0.8 = 3.2
    """
    from datetime import date, timedelta
    three_days = (date.today() + timedelta(days=3)).strftime("%Y-%m-%d")
    tasks = [{"name": "Soon", "deadline": three_days, "importance": 3, "effort": 3}]
    result = prioritize_tasks(tasks, method="weighted")
    # urgency 4: score = 3*0.5 + 3*0.3 + 4*0.2 = 1.5 + 0.9 + 0.8 = 3.2
    assert result.iloc[0]["priority_score"] == 3.2


def test_urgency_level_seven_days_deadline():
    """
    Test that deadlines <= 7 days away receive urgency level 3.

    The weighted method converts days remaining to urgency levels:
    - <= 7 days (but > 3 days): urgency 3

    With default weights (importance=0.5, effort=0.3, deadline=0.2) and
    task values (importance=3, effort=3, deadline=7 days from now):
    - importance_score = 3 * 0.5 = 1.5
    - effort_score = (6 - 3) * 0.3 = 0.9  (effort is inverted)
    - deadline_score = 3 * 0.2 = 0.6
    - Total = 1.5 + 0.9 + 0.6 = 3.0
    """
    from datetime import date, timedelta
    one_week = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
    tasks = [{"name": "This Week", "deadline": one_week, "importance": 3, "effort": 3}]
    result = prioritize_tasks(tasks, method="weighted")
    # urgency 3: score = 3*0.5 + 3*0.3 + 3*0.2 = 1.5 + 0.9 + 0.6 = 3.0
    assert result.iloc[0]["priority_score"] == 3.0


def test_urgency_level_fourteen_days_deadline():
    """
    Test that deadlines <= 14 days away receive urgency level 2.

    The weighted method converts days remaining to urgency levels:
    - <= 14 days (but > 7 days): urgency 2

    With default weights (importance=0.5, effort=0.3, deadline=0.2) and
    task values (importance=3, effort=3, deadline=14 days from now):
    - importance_score = 3 * 0.5 = 1.5
    - effort_score = (6 - 3) * 0.3 = 0.9  (effort is inverted)
    - deadline_score = 2 * 0.2 = 0.4
    - Total = 1.5 + 0.9 + 0.4 = 2.8
    """
    from datetime import date, timedelta
    two_weeks = (date.today() + timedelta(days=14)).strftime("%Y-%m-%d")
    tasks = [{"name": "Two Weeks", "deadline": two_weeks, "importance": 3, "effort": 3}]
    result = prioritize_tasks(tasks, method="weighted")
    # urgency 2: score = 3*0.5 + 3*0.3 + 2*0.2 = 1.5 + 0.9 + 0.4 = 2.8
    assert result.iloc[0]["priority_score"] == 2.8


def test_urgency_level_beyond_fourteen_days_deadline():
    """
    Test that deadlines > 14 days away receive urgency level 1 (lowest).

    The weighted method converts days remaining to urgency levels:
    - > 14 days: urgency 1 (least urgent)

    With default weights (importance=0.5, effort=0.3, deadline=0.2) and
    task values (importance=3, effort=3, deadline=30 days from now):
    - importance_score = 3 * 0.5 = 1.5
    - effort_score = (6 - 3) * 0.3 = 0.9  (effort is inverted)
    - deadline_score = 1 * 0.2 = 0.2
    - Total = 1.5 + 0.9 + 0.2 = 2.6
    """
    from datetime import date, timedelta
    far_future = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
    tasks = [{"name": "Later", "deadline": far_future, "importance": 3, "effort": 3}]
    result = prioritize_tasks(tasks, method="weighted")
    # urgency 1: score = 3*0.5 + 3*0.3 + 1*0.2 = 1.5 + 0.9 + 0.2 = 2.6
    assert result.iloc[0]["priority_score"] == 2.6


def test_lower_effort_ranks_higher():
    """
    Test that lower effort values result in higher priority rankings.

    In the weighted method, effort is inverted as (6 - effort) so that
    low-effort tasks are prioritized over high-effort tasks. With equal
    importance and no deadline, a task with effort=1 should rank higher
    than a task with effort=5.
    """
    tasks = [
        {"name": "Hard", "importance": 3, "effort": 5},
        {"name": "Easy", "importance": 3, "effort": 1},
    ]
    result = prioritize_tasks(tasks, method="weighted")
    easy_rank = result[result["name"] == "Easy"]["rank"].values[0]
    hard_rank = result[result["name"] == "Hard"]["rank"].values[0]
    assert easy_rank < hard_rank  # Lower rank number = higher priority