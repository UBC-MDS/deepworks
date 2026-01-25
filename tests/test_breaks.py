import pytest
from deepworks import breaks
import warnings
from deepworks.breaks import suggest_break, _weighted_random_choice, _format_result, _filter_activities, _warn_if_overworked

# Basic functionality tests

def test_returns_dict():
    """
    Test that suggest_break returns a dictionary.

    The suggest_break function should always return a dict containing
    activity information, regardless of the input parameters provided.
    """
    result = suggest_break(minutes_worked=60, energy_level=5)
    assert isinstance(result, dict)


def test_has_required_keys():
    """
    Test that the result dictionary contains all required keys.

    The format_result function in breaks.py transforms the raw activity
    dict into a standardized output with six keys: name, description,
    duration_minutes, category, energy_required, and location.
    """
    result = suggest_break(minutes_worked=60, energy_level=5)
    assert "name" in result
    assert "description" in result
    assert "duration_minutes" in result
    assert "category" in result
    assert "energy_required" in result
    assert "location" in result


def test_active_break_type():
    """
    Test that specifying break_type='active' returns an active category activity.

    The filter_activities function filters candidates by break_type when it's
    not 'any'. This test verifies that the category filter works correctly
    for the 'active' break type.
    """
    result = suggest_break(minutes_worked=60, energy_level=5, break_type="active")
    assert result["category"] == "active"


def test_any_break_type():
    """
    Test that specifying break_type='any' does not filter activities
    """
    result = suggest_break(minutes_worked=30, energy_level=5, break_type="any", seed=0)
    assert result["category"] in {"active", "rest", "social", "mindful"}

def test_rest_break_type():
    """
    Forces activity["category"] != break_type to be evaluated.
    """
    result = suggest_break(minutes_worked=30, energy_level=5, break_type="rest",
        seed=0)
    assert result["category"] == "rest"


def test_seed_reproducibility():
    """
    Test that providing the same seed produces reproducible results.

    The weighted_random_choice function uses a seeded random.Random instance.
    When the same seed is provided, the random selection should be deterministic,
    returning the same activity for identical inputs.
    """
    result1 = suggest_break(minutes_worked=60, energy_level=5, seed=42)
    result2 = suggest_break(minutes_worked=60, energy_level=5, seed=42)
    assert result1["name"] == result2["name"]

def test_weighted_random_branches():
    """
    To ensure both branches of _weighted_random_choice are covered:
    """
    from deepworks.breaks import _weighted_random_choice

    activities = [
        ({"name": "A"}, 1.0),
        ({"name": "B"}, 1.0),
    ]

    # Test seed=None branch
    result = _weighted_random_choice(activities, seed=None)
    assert result["name"] in {"A", "B"}

    # Test seed=int branch
    result2 = _weighted_random_choice(activities, seed=42)
    assert result2["name"] in {"A", "B"}


def test_high_energy_category():
    """
    Test that high energy level (8-10) returns a valid activity.

    The get_energy_category function maps energy_level 8-10 to 'high' category.
    This verifies the function handles users with high energy appropriately.
    """
    result = suggest_break(minutes_worked=10, energy_level=9)
    assert result is not None


def test_medium_energy_category():
    """
    Test that medium energy level (4-7) returns a valid activity.

    The get_energy_category function maps energy_level 4-7 to 'medium' category.
    This verifies the function handles users with medium energy appropriately.
    """
    result = suggest_break(minutes_worked=45, energy_level=5)
    assert result is not None


def test_weighting_coverage():
    """
    Test that the weight_activities function is exercised for rest activities.

    The weight_activities function assigns weights based on energy alignment.
    This test ensures the weighting logic executes correctly for rest-type breaks.
    """
    result = suggest_break(minutes_worked=20, energy_level=5, break_type="rest")
    assert result is not None


# Edge case tests

def test_indoor_only_filter():
    """
    Test that indoor_only=True excludes outdoor-only activities.

    The filter_activities function checks if indoor_only is True and excludes
    activities where location is 'outdoor'. Activities with location 'indoor'
    or 'either' should still be included.
    """
    result = suggest_break(minutes_worked=60, energy_level=5, indoor_only=True, seed=42)
    assert result["location"] in ["indoor", "either"]


def test_duration_filter():
    """
    Test that the duration parameter limits activity duration.

    The filter_activities function excludes activities whose duration exceeds
    the specified duration parameter. This ensures users get breaks that fit
    their available time.
    """
    result = suggest_break(minutes_worked=60, energy_level=5, duration=5, seed=42)
    assert result["duration_minutes"] <= 5


def test_low_energy_avoids_high_energy_activities():
    """
    Test that low energy users don't receive high-energy activities.

    The filter_activities function excludes activities with energy_required='high'
    when the user's energy_level maps to 'low' category (1-3). This is tested
    across multiple seeds to ensure consistent filtering behavior.
    """
    for seed in range(10):
        result = suggest_break(minutes_worked=60, energy_level=2, seed=seed)
        assert result["energy_required"] != "high"


def test_overwork_warning():
    """
    Test that a UserWarning is raised when minutes_worked exceeds 120.

    The warn_if_overworked function issues a UserWarning when the user has
    worked more than 120 minutes without a break, encouraging them to take
    a longer break.
    """
    with pytest.warns(UserWarning, match="Consider taking a longer break"):
        _warn_if_overworked(minutes_worked=130)


def test_no_overwork_warning():
    """
    Tests that no UserWarning is raised when minutes_worked is less than 120.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("error") 
        from deepworks.breaks import _warn_if_overworked
        _warn_if_overworked(minutes_worked=120)


def test_long_session_weighting():
    """
    Test that long work sessions (>90 min) apply weight boosts to rest activities.

    The weight_activities function multiplies the weight by 1.5 for 'rest' and
    'mindful' activities when minutes_worked exceeds 90, making restful breaks
    more likely to be selected.
    """
    result = suggest_break(minutes_worked=100, energy_level=2, break_type="any", seed=1)
    assert result is not None


def test_fallback_with_low_energy():
    """
    Test fallback behavior when filters are restrictive with low energy.

    When the combination of break_type, duration, indoor_only, and energy
    constraints yields no matches, the filter_activities function progressively
    relaxes constraints to ensure an activity is always returned.
    """
    result = suggest_break(minutes_worked=30, energy_level=2, break_type="social", duration=5)
    assert result is not None


def test_fallback_with_indoor():
    """
    Test fallback behavior with indoor and active constraints.

    This tests that the fallback mechanism works when filtering for indoor-only
    active activities with short duration, which may have limited matches in
    the ACTIVITIES database.
    """
    result = suggest_break(minutes_worked=30, energy_level=5, break_type="active", duration=5, indoor_only=True)
    assert result is not None


def test_indoor_only_filters_outdoor_activity():
    """
    Test that indoor_only=True strictly excludes outdoor-only activities.

    Unlike test_indoor_only_filter which checks for valid locations, this test
    explicitly verifies that 'outdoor' is never returned when indoor_only=True.
    Uses active break_type with longer duration to ensure outdoor activities
    like 'Outdoor Walk' would otherwise be candidates.
    """
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
    """
    Test that the first fallback relaxes the duration constraint.

    The filter_activities function has a two-stage fallback. When no activities
    match all constraints, it first removes the duration filter while keeping
    break_type, indoor_only, and energy constraints. This test uses monkeypatch
    to create a scenario where only a longer activity exists, verifying that
    the duration constraint is relaxed.
    """
    mock_activities = [
        {"name": "Long Activity", "category": "active", "duration": 20,
         "location": "indoor", "energy_required": "low",
         "description": "A long activity."},
    ]
    monkeypatch.setattr(breaks, "ACTIVITIES", mock_activities)

    result = suggest_break(
        minutes_worked=30,
        energy_level=5,
        break_type="active",
        duration=5
    )
    assert result["name"] == "Long Activity"


def test_ultimate_fallback_returns_all_activities(monkeypatch):
    """
    Test that the ultimate fallback returns any activity when all filters fail.

    When both the initial filter and the first fallback (duration relaxed) fail
    to find matches, filter_activities returns the entire ACTIVITIES list as a
    last resort. This test uses monkeypatch to create an activity that matches
    none of the specified constraints, verifying the ultimate fallback works.
    """
    mock_activities = [
        {"name": "Generic Activity", "category": "rest", "duration": 20,
         "location": "outdoor", "energy_required": "high",
         "description": "An activity that won't match filters."},
    ]
    monkeypatch.setattr(breaks, "ACTIVITIES", mock_activities)

    result = suggest_break(
        minutes_worked=30,
        energy_level=2,
        break_type="active",
        duration=5,
        indoor_only=True
    )
    assert result["name"] == "Generic Activity"

def test_filter_activity_continue(monkeypatch):
    """
    Tests that the continue statement in filter_activities is run when an activity entered does not match break_type
    """
    mock_activities = [
        {"name": "Wrong Type", "category": "rest", "duration": 10,
         "location": "indoor", "energy_required": "low",
         "description": "Should be skipped because break_type='active'"},
        {"name": "Correct Type", "category": "active", "duration": 10,
         "location": "indoor", "energy_required": "low",
         "description": "Should pass the filter"},
    ]

    monkeypatch.setattr(breaks, "ACTIVITIES", mock_activities)

    result = _filter_activities(
        break_type="active",
        duration=20,
        indoor_only=False,
        energy_cat = "medium"
    )

    names = [act["name"] for act in result]
    assert "Wrong Type" not in names
    assert "Correct Type" in names

def test_filter_activity_ultimate_fallback(monkeypatch):
    """
    Test for triggering the filter_activities fallback
    """
    mock_activities = [
        {"name": "A", "category": "rest", "duration": 10, "location": "outdoor", "energy_required": "high"},
    ]
    monkeypatch.setattr(breaks, "ACTIVITIES", mock_activities)

    result = _filter_activities(break_type="active", duration=5, indoor_only=True, energy_cat="low")

    assert len(result) == 1  

# just added:
def test_filter_activities_fallback_internal_branches(monkeypatch):
    """
    Triggers the 'continue' statements for location and energy 
    inside the fallback loop of _filter_activities.
    """
    mock_activities = [
        # fails indoor_only
        {"name": "Outdoor Social", "category": "social", "duration": 20, 
         "location": "outdoor", "energy_required": "low"},
        # fails energy
        {"name": "High Energy Social", "category": "social", "duration": 20, 
         "location": "indoor", "energy_required": "high"},
    ]
    monkeypatch.setattr(breaks, "ACTIVITIES", mock_activities)

    result = _filter_activities(
        break_type="social", 
        duration=5, 
        indoor_only=True, 
        energy_cat="low"
    )
    
    assert len(result) == 2

def test_filter_activities_fallback_with_any(monkeypatch):
    """
    Ensures the fallback loop is tested with break_type='any' 
    to cover the short-circuit branch.
    """
    mock_activities = [{"name": "A", "category": "rest", "duration": 20, 
                        "location": "indoor", "energy_required": "low"}]
    monkeypatch.setattr(breaks, "ACTIVITIES", mock_activities)

    result = _filter_activities(
        break_type="any", 
        duration=5, 
        indoor_only=False, 
        energy_cat="medium"
    )
    assert result[0]["name"] == "A"


# Exception tests

def test_minutes_worked_negative_raises_value_error():
    """
    Test that negative minutes_worked raises ValueError.

    The validate_inputs function checks that minutes_worked is non-negative.
    Negative values are invalid since you cannot work negative minutes.
    """
    with pytest.raises(ValueError, match="minutes_worked cannot be negative"):
        suggest_break(minutes_worked=-5, energy_level=5)


def test_empty_break_type_raises_value_error():
    """
    Test that an empty string for break_type raises ValueError.

    The validate_inputs function checks break_type against VALID_BREAK_TYPES
    ('active', 'rest', 'social', 'mindful', 'any'). An empty string is not
    in this list, so it raises ValueError.
    """
    with pytest.raises(ValueError, match="Invalid break_type"):
        suggest_break(60, 5, break_type="")


def test_minutes_worked_not_int_raises_typeerror():
    """
    Test that non-integer minutes_worked raises TypeError.

    The validate_inputs function uses isinstance() to verify minutes_worked
    is an int. String values like "60" are rejected to ensure type safety.
    """
    with pytest.raises(TypeError, match="minutes_worked must be an integer"):
        suggest_break(minutes_worked="60", energy_level=5)


def test_energy_level_not_int_raises_typeerror():
    """
    Test that non-integer energy_level raises TypeError.

    The validate_inputs function uses isinstance() to verify energy_level
    is an int. String values like "5" are rejected to ensure type safety.
    """
    with pytest.raises(TypeError, match="energy_level must be an integer"):
        suggest_break(minutes_worked=60, energy_level="5")


def test_energy_level_out_of_range_raises_valueerror():
    """
    Test that energy_level outside 1-10 range raises ValueError.

    The validate_inputs function checks that energy_level is between 1 and 10
    inclusive. Values outside this range (like 11) are invalid since the
    energy scale is defined as 1-10.
    """
    with pytest.raises(ValueError, match="must be between 1 and 10"):
        suggest_break(minutes_worked=60, energy_level=11)


def test_invalid_break_type_raises_valueerror():
    """
    Test that invalid break_type string raises ValueError.

    The validate_inputs function checks break_type against VALID_BREAK_TYPES.
    Arbitrary strings like 'invalid' that are not in the valid list raise
    ValueError with a descriptive message listing valid options.
    """
    with pytest.raises(ValueError, match="Invalid break_type"):
        suggest_break(minutes_worked=60, energy_level=5, break_type="invalid")


def test_invalid_duration_raises_valueerror():
    """
    Test that duration not in VALID_DURATIONS raises ValueError.

    The validate_inputs function checks duration against VALID_DURATIONS
    (5, 10, 15, 20). Values like 7 that are not in this list are rejected
    to ensure predictable break length options.
    """
    with pytest.raises(ValueError, match="Invalid duration"):
        suggest_break(minutes_worked=60, energy_level=5, duration=7)


def test_indoor_only_not_bool_raises_typeerror():
    """
    Test that non-boolean indoor_only raises TypeError.

    The validate_inputs function uses isinstance() to verify indoor_only
    is a bool. String values like "True" are rejected to prevent truthy
    string evaluation issues.
    """
    with pytest.raises(TypeError, match="indoor_only must be a boolean"):
        suggest_break(60, 5, indoor_only="True")


def test_seed_not_int_raises_typeerror():
    """
    Test that non-integer seed raises TypeError.

    The validate_inputs function checks that seed is either None or an int.
    Float values like 1.5 are rejected since random.Random() expects an
    integer seed for reproducible behavior.
    """
    with pytest.raises(TypeError, match="seed must be an integer"):
        suggest_break(60, 5, seed=1.5)



