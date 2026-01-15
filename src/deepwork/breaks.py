import random
import warnings 
from typing import Optional

VALID_BREAK_TYPES = ["active", "rest", "social", "mindful", "any"]
VALID_DURATIONS = [5, 10, 15, 20]

ACTIVITIES = [
    # Active activities
    {"name": "Desk Stretches", "category": "active", "duration": 5, "location": "indoor",
     "energy_required": "low", "description": "Simple stretches you can do at your desk to relieve tension."},
    {"name": "Quick Walk", "category": "active", "duration": 10, "location": "either",
     "energy_required": "medium", "description": "Take a brisk walk around the office or outside."},
    {"name": "Jumping Jacks", "category": "active", "duration": 5, "location": "indoor",
     "energy_required": "high", "description": "Get your blood pumping with some jumping jacks."},
    {"name": "Stair Climb", "category": "active", "duration": 10, "location": "indoor",
     "energy_required": "high", "description": "Walk up and down stairs to boost energy."},
    {"name": "Outdoor Walk", "category": "active", "duration": 15, "location": "outdoor",
     "energy_required": "medium", "description": "Take a refreshing walk outside in fresh air."},

    # Rest activities
    {"name": "Power Nap", "category": "rest", "duration": 20, "location": "indoor",
     "energy_required": "low", "description": "Close your eyes and rest for a quick recharge."},
    {"name": "Eye Rest", "category": "rest", "duration": 5, "location": "indoor",
     "energy_required": "low", "description": "Look away from screen, focus on distant objects."},
    {"name": "Quiet Sitting", "category": "rest", "duration": 10, "location": "indoor",
     "energy_required": "low", "description": "Sit quietly without any stimulation."},

    # Social activities
    {"name": "Chat with Colleague", "category": "social", "duration": 10, "location": "indoor",
     "energy_required": "medium", "description": "Have a quick non-work chat with a coworker."},
    {"name": "Message a Friend", "category": "social", "duration": 5, "location": "indoor",
     "energy_required": "low", "description": "Send a quick message to someone you care about."},
    {"name": "Coffee Break", "category": "social", "duration": 15, "location": "either",
     "energy_required": "medium", "description": "Grab a coffee and chat with someone."},

    # Mindful activities
    {"name": "Deep Breathing", "category": "mindful", "duration": 5, "location": "indoor",
     "energy_required": "low", "description": "Practice 4-7-8 breathing or box breathing."},
    {"name": "Guided Meditation", "category": "mindful", "duration": 10, "location": "indoor",
     "energy_required": "low", "description": "Follow a short guided meditation."},
    {"name": "Mindful Walking", "category": "mindful", "duration": 15, "location": "either",
     "energy_required": "medium", "description": "Walk slowly and focus on each step."},
    {"name": "Gratitude Reflection", "category": "mindful", "duration": 5, "location": "indoor",
     "energy_required": "low", "description": "Think of three things you're grateful for."},
]

def suggest_break(
    minutes_worked: int,
    energy_level: int,
    break_type: str = "any",
    duration: int = 5,
    indoor_only: bool = False,
    seed: Optional[int] = None
) -> dict:
    """
    Suggest a break activity based on current state and preferences.

    Parameters
    ----------
    minutes_worked : int
        How long you've been working (in minutes). This will influence the length of the suggested break.
    energy_level : int
        Your current energy level on a scale of 1-10.
    break_type : str, optional
        Preferred break type: 'active', 'rest', 'social', 'mindful', or 'any'.
        Default is 'any'.
    duration : int, optional
        Desired break duration: 5, 10, 15, or 20 minutes. Default is 5.
    indoor_only : bool, optional
        If True, only suggest indoor activities. Default is False.
    seed : int, optional
        Random seed for reproducible selection.

    Returns
    -------
    dict
        Activity dictionary with keys: name, description, duration_minutes,
        category, energy_required, location.

    Raises
    ------
    TypeError
        If minutes_worked, energy_level, or duration are not integers.
    ValueError
        If energy_level not in 1-10, break_type invalid, or duration invalid.

    Examples
    --------
    >>> activity = suggest_break(minutes_worked=90, energy_level=4, break_type="active")
    >>> print(activity['name'])
    """
     # Input Validation
    if not isinstance(minutes_worked, int):
        raise TypeError(f"minutes_worked must be an integer, got {type(minutes_worked).__name__}")

    if not isinstance(energy_level, int):
        raise TypeError(f"energy_level must be an integer, got {type(energy_level).__name__}")

    if energy_level < 1 or energy_level > 10:
        raise ValueError("energy_level must be between 1 and 10")

    if break_type not in VALID_BREAK_TYPES:
        raise ValueError(f"Invalid break_type '{break_type}'. Must be one of: {', '.join(VALID_BREAK_TYPES)}")

    if duration not in VALID_DURATIONS:
        raise ValueError(f"Invalid duration '{duration}'. Must be one of: {VALID_DURATIONS}")

    if not isinstance(indoor_only, bool):
        raise TypeError(f"indoor_only must be a boolean, got {type(indoor_only).__name__}")

    if seed is not None and not isinstance(seed, int):
        raise TypeError(f"seed must be an integer, got {type(seed).__name__}")

    # Main Logic 
    if seed is not None:
        random.seed(seed)

    # Warn if worked too long without break
    if minutes_worked > 120:
        warnings.warn(
            f"You've worked {minutes_worked} minutes. Consider taking a longer break!",
            UserWarning
        )

    # Determine energy category
    if energy_level <= 3:
        energy_cat = "low"
    elif energy_level <= 7:
        energy_cat = "medium"
    else:
        energy_cat = "high"

    # Filter activities
    candidates = []
    for activity in ACTIVITIES:
        # Filter by break type
        if break_type != "any" and activity["category"] != break_type:
            continue

        # Filter by duration
        if activity["duration"] > duration:
            continue

        # Filter by indoor constraint
        if indoor_only and activity["location"] == "outdoor":
            continue

        # Filter by energy (low energy person shouldn't do high energy activities)
        if energy_cat == "low" and activity["energy_required"] == "high":
            continue

        candidates.append(activity)

    # If no exact matches, relax constraints
    if not candidates:
        for activity in ACTIVITIES:
            if break_type != "any" and activity["category"] != break_type:
                continue
            if indoor_only and activity["location"] == "outdoor":
                continue
            candidates.append(activity)

    if not candidates:
        candidates = ACTIVITIES  # Fallback to all activities

    # Weight by energy alignment and work duration
    weighted = []
    for activity in candidates:
        weight = 1.0

        # Boost weight for energy-appropriate activities
        if activity["energy_required"] == energy_cat:
            weight *= 2.0

        # After long work sessions, boost restful activities
        if minutes_worked > 90:
            if activity["category"] in ["rest", "mindful"]:
                weight *= 1.5

        weighted.append((activity, weight))

    # Weighted random selection
    total = sum(w for _, w in weighted)
    r = random.uniform(0, total)

    cumulative = 0
    selected = weighted[-1][0]
    for activity, weight in weighted:
        cumulative += weight
        if r <= cumulative:
            selected = activity
            break

    return {
        "name": selected["name"],
        "description": selected["description"],
        "duration_minutes": selected["duration"],
        "category": selected["category"],
        "energy_required": selected["energy_required"],
        "location": selected["location"]
    } 
