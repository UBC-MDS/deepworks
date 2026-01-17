import pytest
from deepwork.breaks import suggest_break, ACTIVITIES, format_result


# Basic functionality tests

def test_returns_dict():
    """Test that function returns a dictionary."""
    result = suggest_break(minutes_worked=60, energy_level=5)
    assert isinstance(result, dict)


def test_has_required_keys():
    """Test that result dict has required keys."""
    result = suggest_break(minutes_worked=60, energy_level=5)
    assert "name" in result
    assert "description" in result
    assert "duration_minutes" in result
    assert "category" in result
    assert "energy_required" in result
    assert "location" in result


def test_active_break_type():
    """Test that active break type returns active activity."""
    result = suggest_break(minutes_worked=60, energy_level=5, break_type="active")
    assert result["category"] == "active"


def test_seed_reproducibility():
    """Test that same seed produces same result."""
    result1 = suggest_break(minutes_worked=60, energy_level=5, seed=42)
    result2 = suggest_break(minutes_worked=60, energy_level=5, seed=42)
    assert result1["name"] == result2["name"]


def test_high_energy_category():
    result = suggest_break(minutes_worked=10, energy_level=9)
    assert result is not None


def test_medium_energy_category():
    result = suggest_break(minutes_worked=45, energy_level=5)
    assert result is not None


def test_weighting_coverage():
    result = suggest_break(minutes_worked=20, energy_level=5, break_type="rest")
    assert result is not None


# Edge case tests

def test_indoor_only_filter():
    result = suggest_break(minutes_worked=60, energy_level=5, indoor_only=True, seed=42)
    assert result["location"] in ["indoor", "either"]


def test_duration_filter():
    result = suggest_break(minutes_worked=60, energy_level=5, duration=5, seed=42)
    assert result["duration_minutes"] <= 5


def test_low_energy_avoids_high_energy_activities():
    for seed in range(10):
        result = suggest_break(minutes_worked=60, energy_level=2, seed=seed)
        assert result["energy_required"] != "high"


def test_overwork_warning():
    with pytest.warns(UserWarning, match="Consider taking a longer break"):
        suggest_break(minutes_worked=130, energy_level=5)


def test_long_session_weighting():
    result = suggest_break(minutes_worked=100, energy_level=2, break_type="any", seed=1)
    assert result is not None


def test_fallback_with_low_energy():
    result = suggest_break(minutes_worked=30, energy_level=2, break_type="social", duration=5)
    assert result is not None


def test_fallback_with_indoor():
    result = suggest_break(minutes_worked=30, energy_level=5, break_type="active", duration=5, indoor_only=True)
    assert result is not None


def test_indoor_only_filters_outdoor_activity():
    """Test that indoor_only=True filters out outdoor-only activities."""
    result = suggest_break(
        minutes_worked=60,
        energy_level=5,
        break_type="active",
        duration=15,
        indoor_only=True,
        seed=42
    )
    assert result["location"] != "outdoor"


def test_fallback_relaxes_duration_constraint(monkeypatch):
    """Test fallback loop when no activities match duration."""
    mock_activities = [
        {"name": "Long Activity", "category": "active", "duration": 20,
         "location": "indoor", "energy_required": "low",
         "description": "A long activity."},
    ]
    monkeypatch.setattr("deepwork.breaks.ACTIVITIES", mock_activities)

    result = suggest_break(
        minutes_worked=30,
        energy_level=5,
        break_type="active",
        duration=5
    )
    assert result["name"] == "Long Activity"


def test_ultimate_fallback_returns_all_activities(monkeypatch):
    """Test ultimate fallback when no filters match."""
    mock_activities = [
        {"name": "Generic Activity", "category": "rest", "duration": 20,
         "location": "outdoor", "energy_required": "high",
         "description": "An activity that won't match filters."},
    ]
    monkeypatch.setattr("deepwork.breaks.ACTIVITIES", mock_activities)

    result = suggest_break(
        minutes_worked=30,
        energy_level=2,
        break_type="active",
        duration=5,
        indoor_only=True
    )
    assert result["name"] == "Generic Activity"


# Exception tests

def test_minutes_worked_negative_raises_value_error():
    """Test that minutes worked is not a negative number."""
    with pytest.raises(ValueError, match="minutes_worked cannot be negative"):
        suggest_break(minutes_worked=-5, energy_level=5)


def test_empty_break_type_raises_value_error():
    """Test that break type is not an empty string."""
    with pytest.raises(ValueError, match="Invalid break_type"):
        suggest_break(60, 5, break_type="")


def test_minutes_worked_not_int_raises_typeerror():
    with pytest.raises(TypeError, match="minutes_worked must be an integer"):
        suggest_break(minutes_worked="60", energy_level=5)


def test_energy_level_not_int_raises_typeerror():
    with pytest.raises(TypeError, match="energy_level must be an integer"):
        suggest_break(minutes_worked=60, energy_level="5")


def test_energy_level_out_of_range_raises_valueerror():
    with pytest.raises(ValueError, match="must be between 1 and 10"):
        suggest_break(minutes_worked=60, energy_level=11)


def test_invalid_break_type_raises_valueerror():
    with pytest.raises(ValueError, match="Invalid break_type"):
        suggest_break(minutes_worked=60, energy_level=5, break_type="invalid")


def test_invalid_duration_raises_valueerror():
    with pytest.raises(ValueError, match="Invalid duration"):
        suggest_break(minutes_worked=60, energy_level=5, duration=7)


def test_indoor_only_not_bool_raises_typeerror():
    with pytest.raises(TypeError, match="indoor_only must be a boolean"):
        suggest_break(60, 5, indoor_only="True")


def test_seed_not_int_raises_typeerror():
    with pytest.raises(TypeError, match="seed must be an integer"):
        suggest_break(60, 5, seed=1.5)
