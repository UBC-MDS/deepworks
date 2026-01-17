import random
import warnings 
from typing import Optional

VALID_BREAK_TYPES = ["active", "rest", "social", "mindful", "any"]
VALID_DURATIONS = [5, 10, 15, 20]

# Database 
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
    validate_inputs(minutes_worked, energy_level, break_type, duration, indoor_only, seed)

    warn_if_overworked(minutes_worked)

    energy_cat = get_energy_category(energy_level)
    candidates = filter_activities(break_type, duration, indoor_only, energy_cat)
    weighted = weight_activities(candidates, energy_cat, minutes_worked)
    selected = weighted_random_choice(weighted, seed)

    return format_result(selected)

def validate_inputs(
    minutes_worked: int,
    energy_level: int,
    break_type: str,
    duration: int,
    indoor_only: bool,
    seed: Optional[int]
) -> None:
    """
    Validate all input parameters.

    Raises
    ------
    TypeError
        If parameters have incorrect types.
    ValueError
        If parameters have invalid values.
    """
    if not isinstance(minutes_worked, int):
        raise TypeError(f"minutes_worked must be an integer, got {type(minutes_worked).__name__}")

    if minutes_worked < 0:
        raise ValueError("minutes_worked cannot be negative")

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

def warn_if_overworked(minutes_worked: int) -> None:
    """
    Warn if user has worked too long without a break.

    Parameters
    ----------
    minutes_worked : int
        Minutes worked since last break.
    """
    if minutes_worked > 120:
        warnings.warn(
            f"You've worked {minutes_worked} minutes. Consider taking a longer break!",
            UserWarning
        )

def get_energy_category(energy_level: int) -> str:
    """
    Convert numeric energy level to category.

    Parameters
    ----------
    energy_level : int
        Energy level from 1-10.

    Returns
    -------
    str
        Energy category: 'low', 'medium', or 'high'.
    """
    if energy_level <= 3:
        return "low"
    elif energy_level <= 7:
        return "medium"
    else:
        return "high"

def filter_activities(
    break_type: str,
    duration: int,
    indoor_only: bool,
    energy_cat: str
) -> list[dict]:
    """
    Filter activities based on constraints.

    Parameters
    ----------
    break_type : str
        Desired break type or 'any'.
    duration : int
        Maximum activity duration.
    indoor_only : bool
        Whether to exclude outdoor activities.
    energy_cat : str
        User's energy category.

    Returns
    -------
    list of dict
        Filtered activity list.
    """
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
        # Filter by energy
        if energy_cat == "low" and activity["energy_required"] == "high":
            continue
        candidates.append(activity)

    # Fallback to relax duration constraint if no matches
    if not candidates:
        for activity in ACTIVITIES:
            if break_type != "any" and activity["category"] != break_type:
                continue
            if indoor_only and activity["location"] == "outdoor":
                continue
            if energy_cat == "low" and activity["energy_required"] == "high":
                continue
            candidates.append(activity)

    if not candidates:
        candidates = list(ACTIVITIES)

    return candidates

def weight_activities(
    candidates: list[dict],
    energy_cat: str,
    minutes_worked: int
) -> list[tuple[dict, float]]:
    """
    Assign weights to activities based on energy alignment and work duration.

    Parameters
    ----------
    candidates : list of dict
        Filtered activities to weight.
    energy_cat : str
        User's energy category.
    minutes_worked : int
        How long user has been working.

    Returns
    -------
    list of tuple
        List of (activity, weight) tuples.
    """
    weighted = []
    for activity in candidates:
        weight = 1.0
        # Boost weight for activities
        if activity["energy_required"] == energy_cat:
            weight *= 2.0
        # Boost restful activities if long work session
        if minutes_worked > 90:
            if activity["category"] in ["rest", "mindful"]:
                weight *= 1.5
        weighted.append((activity, weight))
    return weighted

def weighted_random_choice(weighted: list[tuple[dict, float]], seed: Optional[int]) -> dict:
    """
    Select an activity using weighted random selection.

    Parameters
    ----------
    weighted : list of tuple
        List of (activity, weight) tuples.

    Returns
    -------
    dict
        Selected activity.
    """
    rng = random.Random(seed)
    activities, weights = zip(*weighted)
    return rng.choices(activities, weights=weights, k=1)[0]

def format_result(activity: dict) -> dict:
    """
    Format the selected activity for return.

    Parameters
    ----------
    activity : dict
        The selected activity.

    Returns
    -------
    dict
        Formatted activity dictionary.
    """
    return {
        "name": activity["name"],
        "description": activity["description"],
        "duration_minutes": activity["duration"],
        "category": activity["category"],
        "energy_required": activity["energy_required"],
        "location": activity["location"]
    }
    
        
