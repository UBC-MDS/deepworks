"""Pomodoro session planning function for deepwork."""

from typing import Optional
import pandas as pd

def plan_pomodoro(
    total_minutes: int,
    technique: str = "pomodoro",
    work_length: Optional[int] = None,
    short_break: Optional[int] = None,
    long_break: Optional[int] = None,
    long_break_interval: int = 4
) -> pd.DataFrame:
    """
    Calculate a Pomodoro-style work/break schedule within a fixed time budget.

    The schedule always starts with a work session at minute 0 and alternates
    work and break sessions until `total_minutes` is reached. If there is not
    enough time remaining for a full next session, the final session is
    **truncated** to fit exactly within `total_minutes`. Zero-length sessions
    are never included.

    Technique presets set the default work/break lengths:
    - "pomodoro": 25 work, 5 short break
    - "52-17": 52 work, 17 short break
    - "90-20": 90 work, 20 short break
    - "custom": user-specified lengths via `work_length` and `short_break`

    Long breaks: after every `long_break_interval`-th work session, the next break
    is a long break (type "long_break") with duration `long_break` (or
    `short_break` if `long_break` is not provided). Otherwise breaks are short
    (type "short_break"). Long-break settings apply for all techniques.

    Parameters
    ----------
    total_minutes : int
        Total available time in minutes. Must be > 0.
    technique : str, optional
        Preset name: "pomodoro", "52-17", "90-20", or "custom". Default "pomodoro".
    work_length : int, optional
        Work period length in minutes. Required if technique="custom".
    short_break : int, optional
        Short break length in minutes. Required if technique="custom".
    long_break : int, optional
        Long break length in minutes. If None, defaults to `short_break`.
    long_break_interval : int, optional
        Number of work sessions between long breaks. Must be >= 1. Default 4.

    Returns
    -------
    pd.DataFrame
        Schedule with one row per session, in chronological order, with columns:

        - session : int
            1-based sequential session number.
        - type : str
            One of {"work", "short_break", "long_break"}.
        - duration_minutes : int
            Session length in minutes (may be shorter than the preset/parameter
            value only for the final truncated session).
        - start_minute : int
            Inclusive start minute from 0.
        - end_minute : int
            Exclusive end minute; equals start_minute + duration_minutes and
            never exceeds `total_minutes`.

    Raises
    ------
    TypeError
        If any numeric parameter is not an integer (bool is not accepted).
    ValueError
        If `total_minutes` <= 0; if `technique` is invalid; if technique="custom"
        and required parameters are missing; or if any provided duration is <= 0
        or `long_break_interval` < 1.

    Examples
    --------
    >>> schedule = plan_pomodoro(total_minutes=120, technique="pomodoro")
    >>> schedule = plan_pomodoro(total_minutes=60, technique="custom", work_length=20, short_break=5)
    >>> schedule = plan_pomodoro(total_minutes=10, technique="pomodoro")  # final work session truncated to 10
    """

"""Pomodoro session planning module for flowstate."""

import pandas as pd
import warnings
from typing import Optional

VALID_TECHNIQUES = ["pomodoro", "52-17", "90-20", "custom"]

# Preset technique configurations (work_minutes, short_break, long_break, sessions_before_long)
TECHNIQUE_PRESETS = {
    "pomodoro": (25, 5, 15, 4),
    "52-17": (52, 17, 17, 1),  # No long break distinction
    "90-20": (90, 20, 30, 2),
}


def plan_pomodoro(
    total_minutes: int,
    technique: str = "pomodoro",
    work_length: Optional[int] = None,
    short_break: Optional[int] = None,
    long_break: Optional[int] = None,
    long_break_interval: int = 4
) -> pd.DataFrame:
    """
    Calculate a work/break schedule based on total available time.

    [Keep existing docstring...]
    """
    # === Input Validation ===
    if not isinstance(total_minutes, int):
        raise TypeError(f"total_minutes must be an integer, got {type(total_minutes).__name__}")

    if total_minutes <= 0:
        raise ValueError("total_minutes must be positive")

    if technique not in VALID_TECHNIQUES:
        raise ValueError(f"Invalid technique '{technique}'. Must be one of: {', '.join(VALID_TECHNIQUES)}")

    if technique == "custom":
        if work_length is None or short_break is None:
            raise ValueError("Custom technique requires work_length and short_break parameters")

    # Validate optional int parameters if provided
    for name, val in [("work_length", work_length), ("short_break", short_break),
                      ("long_break", long_break), ("long_break_interval", long_break_interval)]:
        if val is not None:
            if not isinstance(val, int):
                raise TypeError(f"{name} must be an integer, got {type(val).__name__}")
            if val <= 0:
                raise ValueError(f"{name} must be positive")

    # === Main Logic ===
    # Get work/break durations based on technique
    if technique == "custom":
        work = work_length
        s_break = short_break
        l_break = long_break if long_break else short_break
    else:
        preset = TECHNIQUE_PRESETS[technique]
        work = work_length if work_length else preset[0]
        s_break = short_break if short_break else preset[1]
        l_break = long_break if long_break else preset[2]
        long_break_interval = preset[3]

    # Warn if total time seems too short
    if total_minutes < work + s_break:
        warnings.warn(
            f"Total time ({total_minutes} min) is less than one work+break cycle ({work + s_break} min).",
            UserWarning
        )

    # Build the schedule
    schedule = []
    current_time = 0
    session_num = 0
    work_session_count = 0

    while current_time < total_minutes:
        # Add work session
        remaining = total_minutes - current_time
        if remaining <= 0:
            break

        work_duration = min(work, remaining)
        session_num += 1
        work_session_count += 1

        schedule.append({
            "session": session_num,
            "type": "work",
            "duration_minutes": work_duration,
            "start_minute": current_time,
            "end_minute": current_time + work_duration
        })
        current_time += work_duration

        # Check if we have time for a break
        remaining = total_minutes - current_time
        if remaining <= 0:
            break

        # Determine break type (long break every N sessions)
        is_long_break = (work_session_count % long_break_interval == 0)
        break_duration = l_break if is_long_break else s_break
        break_type = "long_break" if is_long_break else "short_break"

        break_duration = min(break_duration, remaining)
        session_num += 1

        schedule.append({
            "session": session_num,
            "type": break_type,
            "duration_minutes": break_duration,
            "start_minute": current_time,
            "end_minute": current_time + break_duration
        })
        current_time += break_duration

    df = pd.DataFrame(schedule)

    # Add summary stats as metadata (stored in attrs)
    total_work = df[df["type"] == "work"]["duration_minutes"].sum()
    total_break = df[df["type"].str.contains("break")]["duration_minutes"].sum()
    df.attrs["total_work_minutes"] = int(total_work)
    df.attrs["total_break_minutes"] = int(total_break)
    df.attrs["work_sessions"] = work_session_count

    return df

