"""Tests for prioritize_tasks function."""

import pytest
import pandas as pd
from deepwork.prioritize import prioritize_tasks


def test_weighted_method_returns_dataframe():
    """Test that weighted method returns a pandas DataFrame."""
    tasks = [
        {"name": "Task A", "importance": 5, "effort": 2},
        {"name": "Task B", "importance": 3, "effort": 4},
    ]
    result = prioritize_tasks(tasks, method="weighted")
    assert isinstance(result, pd.DataFrame)

def test_weighted_method_has_required_columns():
    """Test that result DataFrame has required columns."""
    tasks = [
        {"name": "Task A", "importance": 5, "effort": 2},
    ]
    result = prioritize_tasks(tasks, method="weighted")
    assert "name" in result.columns
    assert "priority_score" in result.columns
    assert "rank" in result.columns

def test_higher_importance_ranks_higher():
    """Test that higher importance leads to higher priority."""
    tasks = [
        {"name": "Low", "importance": 1, "effort": 3},
        {"name": "High", "importance": 5, "effort": 3},
    ]
    result = prioritize_tasks(tasks, method="weighted")
    high_rank = result[result["name"] == "High"]["rank"].values[0]
    low_rank = result[result["name"] == "Low"]["rank"].values[0]
    assert high_rank < low_rank  # Lower rank number = higher priority

def test_deadline_method_returns_dataframe():
    """Test that deadline method returns a pandas DataFrame."""
    tasks = [
        {"name": "Task A", "deadline": "2026-01-15"},
        {"name": "Task B", "deadline": "2026-01-20"},
    ]
    result = prioritize_tasks(tasks, method="deadline")
    assert isinstance(result, pd.DataFrame)

def test_invalid_date_format_handling():
        """Test that invalid dates are handled gracefully (or raise error if changed)."""
        tasks = [{"name": "Bad Date", "deadline": "not-a-date", "importance": 5}]
        # Current behavior: fails silently and treats as no deadline (score 3 for deadline)
        result = prioritize_tasks(tasks, method="weighted")
        # You might want to assert that a warning is logged or a specific default is used
        assert result.iloc[0]["priority_score"] > 0

def test_out_of_bound_values():
    """Test behavior when inputs exceed 1-5 scale."""
    tasks = [
        {"name": "Super Important", "importance": 100, "effort": 1},
        {"name": "Normal", "importance": 5, "effort": 1}
    ]
    result = prioritize_tasks(tasks, method="weighted")
    # Currently, 100 * 0.5 = 50, skewing the results heavily.
    assert result.iloc[0]["priority_score"] > result.iloc[1]["priority_score"]

def test_empty_input_list():
    """Test that empty list raises ValueError."""
    with pytest.raises(ValueError, match="tasks list cannot be empty"):
        prioritize_tasks([], method="weighted")

def test_single_task():
    """Test with only one task."""
    tasks = [{"name": "Only Task", "importance": 3}]
    result = prioritize_tasks(tasks)
    assert len(result) == 1
    assert result.iloc[0]["rank"] == 1

def test_missing_optional_fields():
    """Test tasks with missing optional fields use defaults."""
    tasks = [{"name": "Minimal Task"}]  # No importance, effort, or deadline
    result = prioritize_tasks(tasks)
    assert len(result) == 1
    assert "priority_score" in result.columns

def test_custom_weights():
    """Test custom weights are applied."""
    tasks = [
        {"name": "A", "importance": 5, "effort": 1},
        {"name": "B", "importance": 1, "effort": 5},
    ]
    # Weight importance heavily
    result = prioritize_tasks(tasks, weights={"importance": 1.0, "effort": 0, "deadline": 0})
    assert result.iloc[0]["name"] == "A"  # Higher importance wins

def test_deadline_method_no_deadline():
    """Test deadline method with tasks that have no deadline."""
    tasks = [{"name": "No Deadline"}]
    result = prioritize_tasks(tasks, method="deadline")
    assert result.iloc[0]["priority_score"] == 0

def test_tasks_not_list_raises_typeerror():
    """Test that non-list tasks raises TypeError."""
    with pytest.raises(TypeError, match="tasks must be a list"):
        prioritize_tasks("not a list")

def test_empty_tasks_raises_valueerror():
    """Test that empty tasks list raises ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        prioritize_tasks([])

def test_task_not_dict_raises_typeerror():
    """Test that non-dict task item raises TypeError."""
    with pytest.raises(TypeError, match="must be a dict"):
        prioritize_tasks(["not a dict"])

def test_missing_name_raises_valueerror():
    """Test that task without name raises ValueError."""
    with pytest.raises(ValueError, match="missing required field 'name'"):
        prioritize_tasks([{"importance": 5}])

def test_invalid_method_raises_valueerror():
    """Test that invalid method raises ValueError."""
    with pytest.raises(ValueError, match="Invalid method"):
        prioritize_tasks([{"name": "Task"}], method="invalid")


def test_invalid_weights_type_raises_typeerror():
    """Test that non-dict weights raises TypeError."""
    with pytest.raises(TypeError, match="weights must be a dict"):
        prioritize_tasks([{"name": "Task"}], weights="not a dict")


def test_urgency_level_one_day_deadline():
    """Test urgency level 5 for deadline <= 1 day away."""
    from datetime import date, timedelta
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    tasks = [{"name": "Urgent", "deadline": tomorrow, "importance": 3, "effort": 3}]
    result = prioritize_tasks(tasks, method="weighted")
    # With urgency 5: score = 3*0.5 + 3*0.3 + 5*0.2 = 1.5 + 0.9 + 1.0 = 3.4
    # effort_score = 6 - 3 = 3, so: 3*0.5 + 3*0.3 + 5*0.2 = 1.5 + 0.9 + 1.0 = 3.4
    assert result.iloc[0]["priority_score"] == 3.4


def test_urgency_level_three_days_deadline():
    """Test urgency level 4 for deadline <= 3 days away."""
    from datetime import date, timedelta
    three_days = (date.today() + timedelta(days=3)).strftime("%Y-%m-%d")
    tasks = [{"name": "Soon", "deadline": three_days, "importance": 3, "effort": 3}]
    result = prioritize_tasks(tasks, method="weighted")
    # urgency 4: score = 3*0.5 + 3*0.3 + 4*0.2 = 1.5 + 0.9 + 0.8 = 3.2
    assert result.iloc[0]["priority_score"] == 3.2


def test_urgency_level_seven_days_deadline():
    """Test urgency level 3 for deadline <= 7 days away."""
    from datetime import date, timedelta
    one_week = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
    tasks = [{"name": "This Week", "deadline": one_week, "importance": 3, "effort": 3}]
    result = prioritize_tasks(tasks, method="weighted")
    # urgency 3: score = 3*0.5 + 3*0.3 + 3*0.2 = 1.5 + 0.9 + 0.6 = 3.0
    assert result.iloc[0]["priority_score"] == 3.0


def test_urgency_level_fourteen_days_deadline():
    """Test urgency level 2 for deadline <= 14 days away."""
    from datetime import date, timedelta
    two_weeks = (date.today() + timedelta(days=14)).strftime("%Y-%m-%d")
    tasks = [{"name": "Two Weeks", "deadline": two_weeks, "importance": 3, "effort": 3}]
    result = prioritize_tasks(tasks, method="weighted")
    # urgency 2: score = 3*0.5 + 3*0.3 + 2*0.2 = 1.5 + 0.9 + 0.4 = 2.8
    assert result.iloc[0]["priority_score"] == 2.8


def test_urgency_level_beyond_fourteen_days_deadline():
    """Test urgency level 1 for deadline > 14 days away."""
    from datetime import date, timedelta
    far_future = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
    tasks = [{"name": "Later", "deadline": far_future, "importance": 3, "effort": 3}]
    result = prioritize_tasks(tasks, method="weighted")
    # urgency 1: score = 3*0.5 + 3*0.3 + 1*0.2 = 1.5 + 0.9 + 0.2 = 2.6
    assert result.iloc[0]["priority_score"] == 2.6