"""Tests for prioritize_tasks function."""

import pytest
import pandas as pd
from deepwork.prioritize import prioritize_tasks


def test_weighted_method_returns_dataframe(self):
    """Test that weighted method returns a pandas DataFrame."""
    tasks = [
        {"name": "Task A", "importance": 5, "effort": 2},
        {"name": "Task B", "importance": 3, "effort": 4},
    ]
    result = prioritize_tasks(tasks, method="weighted")
    assert isinstance(result, pd.DataFrame)

def test_weighted_method_has_required_columns(self):
    """Test that result DataFrame has required columns."""
    tasks = [
        {"name": "Task A", "importance": 5, "effort": 2},
    ]
    result = prioritize_tasks(tasks, method="weighted")
    assert "name" in result.columns
    assert "priority_score" in result.columns
    assert "rank" in result.columns

def test_higher_importance_ranks_higher(self):
    """Test that higher importance leads to higher priority."""
    tasks = [
        {"name": "Low", "importance": 1, "effort": 3},
        {"name": "High", "importance": 5, "effort": 3},
    ]
    result = prioritize_tasks(tasks, method="weighted")
    high_rank = result[result["name"] == "High"]["rank"].values[0]
    low_rank = result[result["name"] == "Low"]["rank"].values[0]
    assert high_rank < low_rank  # Lower rank number = higher priority

def test_deadline_method_returns_dataframe(self):
    """Test that deadline method returns a pandas DataFrame."""
    tasks = [
        {"name": "Task A", "deadline": "2026-01-15"},
        {"name": "Task B", "deadline": "2026-01-20"},
    ]
    result = prioritize_tasks(tasks, method="deadline")
    assert isinstance(result, pd.DataFrame)

def test_invalid_date_format_handling(self):
        """Test that invalid dates are handled gracefully (or raise error if changed)."""
        tasks = [{"name": "Bad Date", "deadline": "not-a-date", "importance": 5}]
        # Current behavior: fails silently and treats as no deadline (score 3 for deadline)
        result = prioritize_tasks(tasks, method="weighted")
        # You might want to assert that a warning is logged or a specific default is used
        assert result.iloc[0]["priority_score"] > 0

def test_out_of_bound_values(self):
    """Test behavior when inputs exceed 1-5 scale."""
    tasks = [
        {"name": "Super Important", "importance": 100, "effort": 1},
        {"name": "Normal", "importance": 5, "effort": 1}
    ]
    result = prioritize_tasks(tasks, method="weighted")
    # Currently, 100 * 0.5 = 50, skewing the results heavily.
    assert result.iloc[0]["priority_score"] > result.iloc[1]["priority_score"]

def test_empty_input_list(self):
    """Test that empty list raises ValueError."""
    with pytest.raises(ValueError, match="tasks list cannot be empty"):
        prioritize_tasks([], method="weighted")

def test_single_task(self):
    """Test with only one task."""
    tasks = [{"name": "Only Task", "importance": 3}]
    result = prioritize_tasks(tasks)
    assert len(result) == 1
    assert result.iloc[0]["rank"] == 1

def test_missing_optional_fields(self):
    """Test tasks with missing optional fields use defaults."""
    tasks = [{"name": "Minimal Task"}]  # No importance, effort, or deadline
    result = prioritize_tasks(tasks)
    assert len(result) == 1
    assert "priority_score" in result.columns

def test_custom_weights(self):
    """Test custom weights are applied."""
    tasks = [
        {"name": "A", "importance": 5, "effort": 1},
        {"name": "B", "importance": 1, "effort": 5},
    ]
    # Weight importance heavily
    result = prioritize_tasks(tasks, weights={"importance": 1.0, "effort": 0, "deadline": 0})
    assert result.iloc[0]["name"] == "A"  # Higher importance wins

def test_deadline_method_no_deadline(self):
    """Test deadline method with tasks that have no deadline."""
    tasks = [{"name": "No Deadline"}]
    result = prioritize_tasks(tasks, method="deadline")
    assert result.iloc[0]["priority_score"] == 0

def test_tasks_not_list_raises_typeerror(self):
    """Test that non-list tasks raises TypeError."""
    with pytest.raises(TypeError, match="tasks must be a list"):
        prioritize_tasks("not a list")

def test_empty_tasks_raises_valueerror(self):
    """Test that empty tasks list raises ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        prioritize_tasks([])

def test_task_not_dict_raises_typeerror(self):
    """Test that non-dict task item raises TypeError."""
    with pytest.raises(TypeError, match="must be a dict"):
        prioritize_tasks(["not a dict"])

def test_missing_name_raises_valueerror(self):
    """Test that task without name raises ValueError."""
    with pytest.raises(ValueError, match="missing required field 'name'"):
        prioritize_tasks([{"importance": 5}])

def test_invalid_method_raises_valueerror(self):
    """Test that invalid method raises ValueError."""
    with pytest.raises(ValueError, match="Invalid method"):
        prioritize_tasks([{"name": "Task"}], method="invalid")