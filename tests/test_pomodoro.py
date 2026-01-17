"""Tests for plan_pomodoro function."""

import pytest
import pandas as pd
from deepwork.pomodoro import plan_pomodoro


def test_returns_dataframe():
    """Test that function returns a pandas DataFrame."""
    result = plan_pomodoro(total_minutes=60)
    assert isinstance(result, pd.DataFrame)

def test_has_required_columns():
    """Test that result DataFrame has required columns."""
    result = plan_pomodoro(total_minutes=60)
    assert "session" in result.columns
    assert "type" in result.columns
    assert "duration_minutes" in result.columns
    assert "start_minute" in result.columns
    assert "end_minute" in result.columns

def test_pomodoro_technique_25_5():
    """Test default pomodoro technique creates 25-min work sessions."""
    result = plan_pomodoro(total_minutes=60, technique="pomodoro")
    work_sessions = result[result["type"] == "work"]
    assert work_sessions.iloc[0]["duration_minutes"] == 25

def test_schedule_starts_at_zero():
    """Test that schedule starts at minute 0."""
    result = plan_pomodoro(total_minutes=60)
    assert result.iloc[0]["start_minute"] == 0

def test_dataframe_has_metadata():
    """Test that DataFrame has summary metadata."""
    result = plan_pomodoro(total_minutes=60)
    assert "total_work_minutes" in result.attrs
    assert "total_break_minutes" in result.attrs
    assert "work_sessions" in result.attrs

def test_52_17_technique():
    """Test 52-17 technique creates 52-min work sessions."""
    result = plan_pomodoro(total_minutes=120, technique="52-17")
    work_sessions = result[result["type"] == "work"]
    assert work_sessions.iloc[0]["duration_minutes"] == 52

def test_90_20_technique():
    """Test 90-20 technique creates 90-min work sessions."""
    result = plan_pomodoro(total_minutes=180, technique="90-20")
    work_sessions = result[result["type"] == "work"]
    assert work_sessions.iloc[0]["duration_minutes"] == 90

def test_custom_technique():
    """Test custom technique with user-defined intervals."""
    result = plan_pomodoro(
        total_minutes=60,
        technique="custom",
        work_length=20,
        short_break=5
    )
    work_sessions = result[result["type"] == "work"]
    assert work_sessions.iloc[0]["duration_minutes"] == 20

def test_short_time_partial_session():
    """Test that short time creates partial work session."""
    result = plan_pomodoro(total_minutes=15, technique="pomodoro")
    assert result.iloc[0]["duration_minutes"] == 15

def test_long_break_interval():
    """Test that long breaks occur at correct intervals."""
    result = plan_pomodoro(total_minutes=180, technique="pomodoro")
    long_breaks = result[result["type"] == "long_break"]
    assert len(long_breaks) >= 1

def test_total_minutes_not_int_raises_typeerror():
    with pytest.raises(TypeError, match="total_minutes must be an integer"):
        plan_pomodoro(total_minutes="60")

def test_total_minutes_not_positive_raises_valueerror():
    with pytest.raises(ValueError, match="must be positive"):
        plan_pomodoro(total_minutes=0)

def test_invalid_technique_raises_valueerror():
    with pytest.raises(ValueError, match="Invalid technique"):
        plan_pomodoro(total_minutes=60, technique="invalid")

def test_custom_missing_params_raises_valueerror():
    with pytest.raises(ValueError, match="requires work_length and short_break"):
        plan_pomodoro(total_minutes=60, technique="custom")

def test_work_length_not_int_raises_typeerror():
    """Test that non-integer work_length raises TypeError."""
    with pytest.raises(TypeError, match="work_length must be an integer"):
        plan_pomodoro(total_minutes=60, technique="custom", work_length=25.5, short_break=5)

def test_short_break_not_int_raises_typeerror():
    """Test that non-integer short_break raises TypeError."""
    with pytest.raises(TypeError, match="short_break must be an integer"):
        plan_pomodoro(total_minutes=60, technique="custom", work_length=25, short_break="5")

def test_long_break_not_int_raises_typeerror():
    """Test that non-integer long_break raises TypeError."""
    with pytest.raises(TypeError, match="long_break must be an integer"):
        plan_pomodoro(total_minutes=60, technique="pomodoro", long_break=15.0)

def test_long_break_interval_not_int_raises_typeerror():
    """Test that non-integer long_break_interval raises TypeError."""
    with pytest.raises(TypeError, match="long_break_interval must be an integer"):
        plan_pomodoro(total_minutes=60, technique="custom", work_length=25, short_break=5, long_break_interval=4.0)

def test_work_length_not_positive_raises_valueerror():
    """Test that non-positive work_length raises ValueError."""
    with pytest.raises(ValueError, match="work_length must be positive"):
        plan_pomodoro(total_minutes=60, technique="custom", work_length=0, short_break=5)

def test_short_break_not_positive_raises_valueerror():
    """Test that non-positive short_break raises ValueError."""
    with pytest.raises(ValueError, match="short_break must be positive"):
        plan_pomodoro(total_minutes=60, technique="custom", work_length=25, short_break=-1)

def test_long_break_not_positive_raises_valueerror():
    """Test that non-positive long_break raises ValueError."""
    with pytest.raises(ValueError, match="long_break must be positive"):
        plan_pomodoro(total_minutes=60, technique="pomodoro", long_break=0)

def test_long_break_interval_not_positive_raises_valueerror():
    """Test that non-positive long_break_interval raises ValueError."""
    with pytest.raises(ValueError, match="long_break_interval must be positive"):
        plan_pomodoro(total_minutes=60, technique="custom", work_length=25, short_break=5, long_break_interval=0)
