"""Tests for get_affirmation function."""

import pytest
from deepwork.affirmation import get_affirmation


# Basic functionality tests

def test_returns_dict():
    """Test that function returns a dictionary."""
    result = get_affirmation(name="Alice", mood="happy", energy=5)
    assert isinstance(result, dict)

def test_has_required_keys():
    """Test that result dict has required keys."""
    result = get_affirmation(name="Alice", mood="happy", energy=5)
    assert "text" in result
    assert "category" in result
    assert "mood_alignment" in result

def test_name_in_text():
    """Test that name appears in affirmation text."""
    result = get_affirmation(name="Alice", mood="happy", energy=5, seed=42)
    assert "Alice" in result["text"]

def test_seed_reproducibility():
    """Test that same seed produces same result."""
    result1 = get_affirmation(name="Alice", mood="happy", energy=5, seed=42)
    result2 = get_affirmation(name="Alice", mood="happy", energy=5, seed=42)
    assert result1["text"] == result2["text"]

# Mood tests

def test_stressed_mood_prefers_selfcare():
    """Test that stressed mood prefers self-care or persistence categories."""
    categories = []
    for seed in range(20):
        result = get_affirmation(name="Test", mood="stressed", energy=5, seed=seed)
        categories.append(result["category"])
    assert "self-care" in categories or "persistence" in categories


def test_specific_category_override():
    """Test that explicit category overrides mood-based selection."""
    result = get_affirmation(name="Test", mood="stressed", energy=5, category="growth", seed=42)
    assert result["category"] == "growth"

# Edge case tests

def test_empty_name_uses_default():
    """Test that empty name defaults to 'Developer'."""
    result = get_affirmation(name="   ", mood="happy", energy=5, seed=42)
    assert "Developer" in result["text"]


def test_name_capitalization():
    """Test that name is properly capitalized."""
    result = get_affirmation(name="alice", mood="happy", energy=5, seed=42)
    assert "Alice" in result["text"]

# Exception tests

def test_name_not_string_raises_typeerror():
    """Test that non-string name raises TypeError."""
    with pytest.raises(TypeError, match="name must be a string"):
        get_affirmation(name=123, mood="happy", energy=5)

def test_energy_not_int_raises_typeerror():
    """Test that non-integer energy raises TypeError."""
    with pytest.raises(TypeError, match="energy must be an integer"):
        get_affirmation(name="Alice", mood="happy", energy="5")

def test_invalid_mood_raises_valueerror():
    """Test that invalid mood raises ValueError."""
    with pytest.raises(ValueError, match="Invalid mood"):
        get_affirmation(name="Alice", mood="invalid", energy=5)

def test_energy_out_of_range_raises_valueerror():
    """Test that energy outside 1-10 raises ValueError."""
    with pytest.raises(ValueError, match="must be between 1 and 10"):
        get_affirmation(name="Alice", mood="happy", energy=0)

def test_invalid_category_raises_valueerror():
    """Test that invalid category raises ValueError."""
    with pytest.raises(ValueError, match="Invalid category"):
        get_affirmation(name="Alice", mood="happy", energy=5, category="invalid")

def test_mood_not_string_raises_typeerror():
    """Test that non-string mood raises TypeError."""
    with pytest.raises(TypeError, match="mood must be a string"):
        get_affirmation(name="Alice", mood=123, energy=5)

def test_category_not_string_raises_typeerror():
    """Test that non-string category raises TypeError."""
    with pytest.raises(TypeError, match="category must be a string"):
        get_affirmation(name="Alice", mood="happy", energy=5, category=123)

def test_seed_not_int_raises_typeerror():
    """Test that non-integer seed raises TypeError."""
    with pytest.raises(TypeError, match="seed must be an integer"):
        get_affirmation(name="Alice", mood="happy", energy=5, seed="42")

# Energy level tests

def test_low_energy_returns_valid_result():
    """Test that low energy (1-3) returns appropriate affirmation."""
    result = get_affirmation(name="Alice", mood="happy", energy=2, seed=42)
    assert result["text"]
    assert result["category"] in ["motivation", "growth"]

def test_high_energy_returns_valid_result():
    """Test that high energy (8-10) returns appropriate affirmation."""
    result = get_affirmation(name="Alice", mood="motivated", energy=9, seed=42)
    assert result["text"]
    assert result["category"]

def test_energy_boundary_low():
    """Test energy at low boundary (1)."""
    result = get_affirmation(name="Alice", mood="tired", energy=1, seed=42)
    assert isinstance(result, dict)

def test_energy_boundary_high():
    """Test energy at high boundary (10)."""
    result = get_affirmation(name="Alice", mood="motivated", energy=10, seed=42)
    assert isinstance(result, dict)

# Weighting tests

def test_non_adjacent_energy_levels():
    """Test weighting when energy levels are not adjacent (low vs high)."""
    result = get_affirmation(name="Alice", mood="happy", energy=1, seed=42)
    assert isinstance(result, dict)
    assert "text" in result

def test_weighting_with_extreme_energy_mismatch():
    """Test that weighting handles extreme energy mismatches."""
    results = []
    for seed in range(50):
        result = get_affirmation(name="Test", mood="motivated", energy=1, seed=seed)
        results.append(result)
    assert all("text" in r for r in results)
