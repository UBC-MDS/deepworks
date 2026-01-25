"""Tests for plan_pomodoro function."""

import pytest
import pandas as pd
import deepworks.pomodoro as pomodoro_mod
from deepworks.pomodoro import plan_pomodoro


def test_returns_dataframe():
    """
    Test that plan_pomodoro returns a pandas DataFrame.

    The function should always return a pd.DataFrame containing the
    work/break schedule, regardless of the technique or time budget used.
    """
    result = plan_pomodoro(total_minutes=60)
    assert isinstance(result, pd.DataFrame)

def test_has_required_columns():
    """
    Test that the returned DataFrame contains all required columns.

    The schedule DataFrame must include: 'session' (1-based index),
    'type' (work/short_break/long_break), 'duration_minutes' (session length),
    'start_minute' (inclusive start), and 'end_minute' (exclusive end).
    """
    result = plan_pomodoro(total_minutes=60)
    assert "session" in result.columns
    assert "type" in result.columns
    assert "duration_minutes" in result.columns
    assert "start_minute" in result.columns
    assert "end_minute" in result.columns

def test_pomodoro_technique_25_5():
    """
    Test that the 'pomodoro' technique uses 25-minute work sessions.

    The classic Pomodoro Technique preset uses 25-minute work sessions
    with 5-minute short breaks. This verifies the first work session
    has the expected 25-minute duration.
    """
    result = plan_pomodoro(total_minutes=60, technique="pomodoro")
    work_sessions = result[result["type"] == "work"]
    assert work_sessions.iloc[0]["duration_minutes"] == 25

def test_schedule_starts_at_zero():
    """
    Test that the schedule always begins at minute 0.

    The first session in the schedule must have start_minute=0, as the
    schedule represents time from the beginning of the available window.
    The first session is always a work session.
    """
    result = plan_pomodoro(total_minutes=60)
    assert result.iloc[0]["start_minute"] == 0

def test_dataframe_has_metadata():
    """
    Test that the DataFrame includes summary metadata in attrs.

    The returned DataFrame should have metadata attributes containing:
    - total_work_minutes: sum of all work session durations
    - total_break_minutes: sum of all break session durations
    - work_sessions: count of work sessions in the schedule
    """
    result = plan_pomodoro(total_minutes=60)
    assert "total_work_minutes" in result.attrs
    assert "total_break_minutes" in result.attrs
    assert "work_sessions" in result.attrs

def test_52_17_technique():
    """
    Test that the '52-17' technique uses 52-minute work sessions.

    The 52-17 technique preset uses 52-minute work sessions with
    17-minute breaks, based on productivity research. This verifies
    the first work session has the expected 52-minute duration.
    """
    result = plan_pomodoro(total_minutes=120, technique="52-17")
    work_sessions = result[result["type"] == "work"]
    assert work_sessions.iloc[0]["duration_minutes"] == 52

def test_90_20_technique():
    """
    Test that the '90-20' technique uses 90-minute work sessions.

    The 90-20 technique preset uses 90-minute work sessions with
    20-minute short breaks and 30-minute long breaks, aligned with
    ultradian rhythms. This verifies the first work session duration.
    """
    result = plan_pomodoro(total_minutes=180, technique="90-20")
    work_sessions = result[result["type"] == "work"]
    assert work_sessions.iloc[0]["duration_minutes"] == 90

def test_custom_technique():
    """
    Test that the 'custom' technique uses user-specified work/break lengths.

    When technique='custom', the user must provide work_length and short_break
    parameters to define their own schedule. This verifies custom durations
    are correctly applied to work sessions.
    """
    result = plan_pomodoro(
        total_minutes=60,
        technique="custom",
        work_length=20,
        short_break=5
    )
    work_sessions = result[result["type"] == "work"]
    assert work_sessions.iloc[0]["duration_minutes"] == 20

def test_short_time_partial_session():
    """
    Test that sessions are truncated when time budget is insufficient.

    When total_minutes is less than a full work session, the final session
    is truncated to fit exactly within the time budget. Zero-length sessions
    are never created. Here, 15 minutes is less than the 25-minute pomodoro
    work session, so it gets truncated to 15 minutes.
    """
    result = plan_pomodoro(total_minutes=15, technique="pomodoro")
    assert result.iloc[0]["duration_minutes"] == 15

def test_long_break_interval():
    """
    Test that long breaks are inserted after the configured interval.

    For the 'pomodoro' technique, a long break (15 min) occurs after every
    4th work session. With 180 minutes, there should be enough time to
    complete 4 work sessions and trigger at least one long break.
    """
    result = plan_pomodoro(total_minutes=180, technique="pomodoro")
    long_breaks = result[result["type"] == "long_break"]
    assert len(long_breaks) >= 1

def test_total_minutes_not_int_raises_typeerror():
    """
    Test that passing a non-integer total_minutes raises TypeError.

    The total_minutes parameter must be an integer. Passing a string
    (or any non-int type) should raise a TypeError with a descriptive message.
    """
    with pytest.raises(TypeError, match="total_minutes must be an integer"):
        plan_pomodoro(total_minutes="60")

def test_total_minutes_not_positive_raises_valueerror():
    """
    Test that passing zero or negative total_minutes raises ValueError.

    The total_minutes parameter must be greater than 0. Passing zero
    should raise a ValueError indicating the value must be positive.
    """
    with pytest.raises(ValueError, match="must be positive"):
        plan_pomodoro(total_minutes=0)

def test_invalid_technique_raises_valueerror():
    """
    Test that passing an invalid technique name raises ValueError.

    The technique parameter must be one of: 'pomodoro', '52-17', '90-20',
    or 'custom'. Passing an unrecognized technique name should raise
    a ValueError listing the valid options.
    """
    with pytest.raises(ValueError, match="Invalid technique"):
        plan_pomodoro(total_minutes=60, technique="invalid")

def test_custom_missing_params_raises_valueerror():
    """
    Test that custom technique without required parameters raises ValueError.

    When technique='custom', both work_length and short_break parameters
    are required. Omitting these should raise a ValueError explaining
    which parameters are needed.
    """
    with pytest.raises(ValueError, match="requires work_length and short_break"):
        plan_pomodoro(total_minutes=60, technique="custom")

def test_work_length_not_int_raises_typeerror():
    """
    Test that passing a non-integer work_length raises TypeError.

    The work_length parameter must be an integer when provided. Passing
    a float (25.5) should raise a TypeError with a descriptive message.
    Boolean values are also not accepted as integers.
    """
    with pytest.raises(TypeError, match="work_length must be an integer"):
        plan_pomodoro(total_minutes=60, technique="custom", work_length=25.5, short_break=5)

def test_short_break_not_int_raises_typeerror():
    """
    Test that passing a non-integer short_break raises TypeError.

    The short_break parameter must be an integer when provided. Passing
    a string ("5") should raise a TypeError with a descriptive message.
    """
    with pytest.raises(TypeError, match="short_break must be an integer"):
        plan_pomodoro(total_minutes=60, technique="custom", work_length=25, short_break="5")

def test_long_break_not_int_raises_typeerror():
    """
    Test that passing a non-integer long_break raises TypeError.

    The long_break parameter must be an integer when provided. Passing
    a float (15.0) should raise a TypeError with a descriptive message.
    """
    with pytest.raises(TypeError, match="long_break must be an integer"):
        plan_pomodoro(total_minutes=60, technique="pomodoro", long_break=15.0)

def test_long_break_interval_not_int_raises_typeerror():
    """
    Test that passing a non-integer long_break_interval raises TypeError.

    The long_break_interval parameter must be an integer. Passing a float
    (4.0) should raise a TypeError with a descriptive message.
    """
    with pytest.raises(TypeError, match="long_break_interval must be an integer"):
        plan_pomodoro(total_minutes=60, technique="custom", work_length=25, short_break=5, long_break_interval=4.0)

def test_work_length_not_positive_raises_valueerror():
    """
    Test that passing zero or negative work_length raises ValueError.

    The work_length parameter must be greater than 0 when provided.
    Passing zero should raise a ValueError indicating the value must
    be positive.
    """
    with pytest.raises(ValueError, match="work_length must be positive"):
        plan_pomodoro(total_minutes=60, technique="custom", work_length=0, short_break=5)

def test_short_break_not_positive_raises_valueerror():
    """
    Test that passing zero or negative short_break raises ValueError.

    The short_break parameter must be greater than 0 when provided.
    Passing a negative value (-1) should raise a ValueError indicating
    the value must be positive.
    """
    with pytest.raises(ValueError, match="short_break must be positive"):
        plan_pomodoro(total_minutes=60, technique="custom", work_length=25, short_break=-1)

def test_long_break_not_positive_raises_valueerror():
    """
    Test that passing zero or negative long_break raises ValueError.

    The long_break parameter must be greater than 0 when provided.
    Passing zero should raise a ValueError indicating the value must
    be positive.
    """
    with pytest.raises(ValueError, match="long_break must be positive"):
        plan_pomodoro(total_minutes=60, technique="pomodoro", long_break=0)

def test_long_break_interval_not_positive_raises_valueerror():
    """
    Test that passing zero or negative long_break_interval raises ValueError.

    The long_break_interval parameter must be at least 1 (meaning a long
    break occurs after at least 1 work session). Passing zero should raise
    a ValueError indicating the value must be positive.
    """
    with pytest.raises(ValueError, match="long_break_interval must be positive"):
        plan_pomodoro(total_minutes=60, technique="custom", work_length=25, short_break=5, long_break_interval=0)

def test_custom_uses_explicit_long_break_and_can_truncate_break():
    """
    Custom technique should use provided long_break (not default to short_break).
    Also validates that a break can be truncated if time runs out mid-break.
    """
    result = plan_pomodoro(
        total_minutes=30,
        technique="custom",
        work_length=10,
        short_break=5,
        long_break=8,
        long_break_interval=1,  # long break after every work session
    )

    assert result.iloc[1]["type"] == "long_break"
    assert result.iloc[1]["duration_minutes"] == 8

    # Total time should never exceed the budget
    assert result["end_minute"].max() == 30

    # With interval=1, breaks should all be long_breaks
    assert (result[result["type"].str.contains("break")]["type"] == "long_break").all()

def test_preset_allows_overrides_for_work_and_breaks():
    """
    Non-custom techniques should allow overriding work_length/short_break/long_break.
    """
    result = plan_pomodoro(
        total_minutes=60,
        technique="pomodoro",
        work_length=10,
        short_break=3,
        long_break=9,
    )

    # First work session should use override (10)
    assert result.iloc[0]["type"] == "work"
    assert result.iloc[0]["duration_minutes"] == 10

    # First break should use override short_break (3)
    assert result.iloc[1]["type"] == "short_break"
    assert result.iloc[1]["duration_minutes"] == 3

def test_empty_schedule_metadata_defaults_to_zero(monkeypatch):
    """
    Force _build_schedule to return an empty schedule to cover the
    defensive else-branch in _create_dataframe_with_metadata.
    """
    def fake_build_schedule(total_minutes, work, short_break, long_break, interval):
        return [], 0  # empty schedule, zero work sessions

    monkeypatch.setattr(pomodoro_mod, "_build_schedule", fake_build_schedule)

    df = pomodoro_mod.plan_pomodoro(total_minutes=10, technique="pomodoro")

    assert df.empty
    assert df.attrs["total_work_minutes"] == 0
    assert df.attrs["total_break_minutes"] == 0
    assert df.attrs["work_sessions"] == 0

def test_schedule_ends_exactly_on_budget_and_triggers_final_loop_break():
    """
    Covers the top-of-loop 'remaining <= 0: break' by making the schedule
    end exactly at total_minutes, so the next loop iteration immediately breaks.
    """
    df = plan_pomodoro(total_minutes=30, technique="pomodoro")

    # Should end exactly at 30 minutes
    assert df.iloc[-1]["end_minute"] == 30

    # Should include exactly: 25 work + 5 short break
    assert df["type"].tolist() == ["work", "short_break"]
    assert df["duration_minutes"].tolist() == [25, 5]

