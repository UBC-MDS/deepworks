"""Tests for get_affirmation function."""

import pytest
from deepwork.affirmation import get_affirmation


class TestGetAffirmationBasic:
    """Basic functionality tests for get_affirmation."""

    def test_returns_dict(self):
        """Test that function returns a dictionary."""
        result = get_affirmation(name="Alice", mood="happy", energy=5)
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        """Test that result dict has required keys."""
        result = get_affirmation(name="Alice", mood="happy", energy=5)
        assert "text" in result
        assert "category" in result
        assert "mood_alignment" in result

    def test_name_in_text(self):
        """Test that name appears in affirmation text."""
        result = get_affirmation(name="Alice", mood="happy", energy=5, seed=42)
        assert "Alice" in result["text"]

    def test_seed_reproducibility(self):
        """Test that same seed produces same result."""
        result1 = get_affirmation(name="Alice", mood="happy", energy=5, seed=42)
        result2 = get_affirmation(name="Alice", mood="happy", energy=5, seed=42)
        assert result1["text"] == result2["text"]