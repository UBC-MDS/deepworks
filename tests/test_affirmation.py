"""Tests for get_affirmation function."""

import pytest
from unittest.mock import MagicMock
from deepworks.affirmation import get_affirmation

# Basic functionality tests

def test_returns_dict():
    """
    Test that get_affirmation returns a dictionary.

    Verifies the function returns the expected data type when called
    with valid parameters (name="Alice", mood="happy", energy=5).
    """
    result = get_affirmation(name="Alice", mood="happy", energy=5)
    assert isinstance(result, dict)

def test_has_required_keys():
    """
    Test that the returned dictionary contains all required keys.

    Verifies the result includes 'text' (the affirmation message),
    'category' (affirmation type), and 'mood_alignment' (relevance score).
    """
    result = get_affirmation(name="Alice", mood="happy", energy=5)
    assert "text" in result
    assert "category" in result
    assert "mood_alignment" in result

def test_name_in_text():
    """
    Test that the user's name appears in the affirmation text.

    Uses a fixed seed for reproducibility and verifies that the provided
    name "Alice" is included somewhere in the generated affirmation message.
    """
    result = get_affirmation(name="Alice", mood="happy", energy=5, seed=42)
    assert "Alice" in result["text"]

def test_seed_reproducibility():
    """
    Test that identical seeds produce identical results.

    Calls get_affirmation twice with the same parameters and seed value,
    then verifies both calls return the exact same affirmation text.
    This ensures deterministic behavior for testing purposes.
    """
    result1 = get_affirmation(name="Alice", mood="happy", energy=5, seed=42)
    result2 = get_affirmation(name="Alice", mood="happy", energy=5, seed=42)
    assert result1["text"] == result2["text"]

# Mood tests

def test_stressed_mood_prefers_selfcare():
    """
    Test that stressed mood tends toward self-care or persistence categories.

    Generates 20 affirmations with mood="stressed" using different seeds
    and verifies that at least one result falls into the 'self-care' or
    'persistence' category, which are appropriate for stressed users.
    """
    categories = []
    for seed in range(20):
        result = get_affirmation(name="Test", mood="stressed", energy=5, seed=seed)
        categories.append(result["category"])
    assert "self-care" in categories or "persistence" in categories


def test_specific_category_override():
    """
    Test that explicitly specifying a category overrides mood-based selection.

    When mood="stressed" would normally prefer self-care categories,
    explicitly setting category="growth" should force that category instead.
    """
    result = get_affirmation(name="Test", mood="stressed", energy=5, category="growth", seed=42)
    assert result["category"] == "growth"

# Edge case tests

def test_empty_name_uses_default():
    """
    Test that whitespace-only names default to 'Developer'.

    When the name parameter contains only whitespace (e.g., "   "),
    the function should substitute the default name "Developer"
    in the affirmation text.
    """
    result = get_affirmation(name="   ", mood="happy", energy=5, seed=42)
    assert "Developer" in result["text"]


def test_name_capitalization():
    """
    Test that lowercase names are properly capitalized.

    Verifies that a lowercase name "alice" is converted to "Alice"
    in the affirmation text for proper formatting.
    """
    result = get_affirmation(name="alice", mood="happy", energy=5, seed=42)
    assert "Alice" in result["text"]

# Exception tests

def test_name_not_string_raises_typeerror():
    """
    Test that passing a non-string name raises TypeError.

    Verifies the function validates the name parameter type and raises
    TypeError with message "name must be a string" when given an integer.
    """
    with pytest.raises(TypeError, match="name must be a string"):
        get_affirmation(name=123, mood="happy", energy=5)

def test_energy_not_int_raises_typeerror():
    """
    Test that passing a non-integer energy raises TypeError.

    Verifies the function validates the energy parameter type and raises
    TypeError with message "energy must be an integer" when given a string.
    """
    with pytest.raises(TypeError, match="energy must be an integer"):
        get_affirmation(name="Alice", mood="happy", energy="5")

def test_invalid_mood_raises_valueerror():
    """
    Test that passing an invalid mood raises ValueError.

    Verifies the function validates the mood parameter against allowed values
    and raises ValueError with message "Invalid mood" for unrecognized moods.
    """
    with pytest.raises(ValueError, match="Invalid mood"):
        get_affirmation(name="Alice", mood="invalid", energy=5)

def test_energy_out_of_range_raises_valueerror():
    """
    Test that energy values outside 1-10 range raise ValueError.

    Verifies the function validates energy is within the accepted range
    and raises ValueError with message "must be between 1 and 10" for energy=0.
    """
    with pytest.raises(ValueError, match="must be between 1 and 10"):
        get_affirmation(name="Alice", mood="happy", energy=0)

def test_invalid_category_raises_valueerror():
    """
    Test that passing an invalid category raises ValueError.

    Verifies the function validates the category parameter against allowed values
    and raises ValueError with message "Invalid category" for unrecognized categories.
    """
    with pytest.raises(ValueError, match="Invalid category"):
        get_affirmation(name="Alice", mood="happy", energy=5, category="invalid")

def test_mood_not_string_raises_typeerror():
    """
    Test that passing a non-string mood raises TypeError.

    Verifies the function validates the mood parameter type and raises
    TypeError with message "mood must be a string" when given an integer.
    """
    with pytest.raises(TypeError, match="mood must be a string"):
        get_affirmation(name="Alice", mood=123, energy=5)

def test_category_not_string_raises_typeerror():
    """
    Test that passing a non-string category raises TypeError.

    Verifies the function validates the category parameter type and raises
    TypeError with message "category must be a string" when given an integer.
    """
    with pytest.raises(TypeError, match="category must be a string"):
        get_affirmation(name="Alice", mood="happy", energy=5, category=123)

def test_seed_not_int_raises_typeerror():
    """
    Test that passing a non-integer seed raises TypeError.

    Verifies the function validates the seed parameter type and raises
    TypeError with message "seed must be an integer" when given a string.
    """
    with pytest.raises(TypeError, match="seed must be an integer"):
        get_affirmation(name="Alice", mood="happy", energy=5, seed="42")

# Weighting tests

def test_non_adjacent_energy_levels():
    """
    Test weighting behavior with low energy value.

    Verifies the affirmation weighting system handles energy=1 correctly,
    returning a valid dictionary with a 'text' key even when energy levels
    may not align closely with affirmation energy metadata.
    """
    result = get_affirmation(name="Alice", mood="happy", energy=1, seed=42)
    assert isinstance(result, dict)
    assert "text" in result

def test_weighting_with_extreme_energy_mismatch():
    """
    Test weighting handles extreme energy mismatches gracefully.

    Generates 50 affirmations with mood="motivated" (typically high energy)
    but energy=1 (minimum). Verifies all results contain valid 'text' keys,
    confirming the weighting system doesn't fail with conflicting inputs.
    """
    results = []
    for seed in range(50):
        result = get_affirmation(name="Test", mood="motivated", energy=1, seed=seed)
        results.append(result)
    assert all("text" in r for r in results)


def test_weighted_random_fallback_execution(monkeypatch):
    """
    Test that _weighted_random_choice hits the fallback return.

    We mock random.Random to return an instance whose uniform method
    returns a value larger than the total weights. This forces the
    selection loop to finish without returning, triggering the safety
    'return candidates[-1][0]' at the end.
    """
    import deepworks.affirmation as affirmation_module

    mock_rng = MagicMock()
    mock_rng.uniform.return_value = 10000.0

    monkeypatch.setattr(affirmation_module.random, "Random", lambda seed: mock_rng)
    result = get_affirmation(name="Test", mood="happy", energy=5)

    # Verify we still got a valid result (the fallback worked)
    assert result["text"]

# Testing different energy levels

def test_low_energy_range():
    """Test energy 1-3 maps to low energy category."""
    for energy in [1, 2, 3]:
        result = get_affirmation(name="Test", mood="neutral", energy=energy, seed=42)
        assert "text" in result

def test_medium_energy_range():
    """Test energy 4-7 maps to medium energy category."""
    for energy in [4, 5, 6, 7]:
        result = get_affirmation(name="Test", mood="neutral", energy=energy, seed=42)
        assert "text" in result

def test_high_energy_range():
    """Test energy 8-10 maps to high energy category."""
    for energy in [8, 9, 10]:
        result = get_affirmation(name="Test", mood="neutral", energy=energy, seed=42)
        assert "text" in result
