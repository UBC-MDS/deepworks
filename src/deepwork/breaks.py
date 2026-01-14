import random
from typing import Optional

VALID_BREAK_TYPES = ["active", "rest", "social", "mindful", "any"]
VALID_DURATIONS = [5, 10, 15, 20]

ACTIVITIES = [
    {"name": "Desk Stretches", "category": "active", "duration": 5, "location": "indoor",
     "energy_required": "low", "description": "Simple stretches you can do at your desk."},
    {"name": "Quick Walk", "category": "active", "duration": 10, "location": "either",
     "energy_required": "medium", "description": "Take a brisk walk around the office."},
    {"name": "Jumping Jacks", "category": "active", "duration": 5, "location": "indoor",
     "energy_required": "high", "description": "Get your blood pumping."},
    {"name": "Power Nap", "category": "rest", "duration": 20, "location": "indoor",
     "energy_required": "low", "description": "Close your eyes and rest."},
    {"name": "Eye Rest", "category": "rest", "duration": 5, "location": "indoor",
     "energy_required": "low", "description": "Look away from screen."},
    {"name": "Chat with Colleague", "category": "social", "duration": 10, "location": "indoor",
     "energy_required": "medium", "description": "Have a quick non-work chat."},
    {"name": "Message a Friend", "category": "social", "duration": 5, "location": "indoor",
     "energy_required": "low", "description": "Send a quick message."},
    {"name": "Deep Breathing", "category": "mindful", "duration": 5, "location": "indoor",
     "energy_required": "low", "description": "Practice 4-7-8 breathing."},
    {"name": "Guided Meditation", "category": "mindful", "duration": 10, "location": "indoor",
     "energy_required": "low", "description": "Follow a short guided meditation."},
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
    if seed is not None:
        random.seed(seed)

    candidates = []
    for activity in ACTIVITIES:
        if break_type != "any" and activity["category"] != break_type:
            continue
        if activity["duration"] > duration:
            continue
        if indoor_only and activity["location"] == "outdoor":
            continue
        candidates.append(activity)
    

    if not candidates:
        candidates = ACTIVITIES

    selected = random.choice(candidates)

    return {
        "name": selected["name"],
        "description": selected["description"],
        "duration_minutes": selected["duration"],
        "category": selected["category"],
        "energy_required": selected["energy_required"],
        "location": selected["location"]
    }
    
