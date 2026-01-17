"""Tests for prioritize_tasks function."""

import pytest
import pandas as pd
from deepwork.prioritize import prioritize_tasks


class TestPrioritizeTasksBasic:
    """Basic functionality tests for prioritize_tasks."""

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