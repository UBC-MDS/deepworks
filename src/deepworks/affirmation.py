"""Affirmation module for deepworks."""

import random
from typing import Optional

VALID_MOODS = ["happy", "stressed", "anxious", "tired", "frustrated", "motivated", "neutral"]
VALID_CATEGORIES = ["motivation", "confidence", "persistence", "self-care", "growth"]

# Affirmation database - developer focused
AFFIRMATIONS = [
    # Motivation - Low Energy
    {"text": "{name}, small commits still move the project forward.", "category": "motivation", "energy": "low"},
    {"text": "Rest is part of the process, {name}.", "category": "motivation", "energy": "low"},
    {"text": "{name}, every bug fixed is progress.", "category": "motivation", "energy": "low"},

    # Motivation - Medium Energy
    {"text": "{name}, you have the skills to solve this.", "category": "motivation", "energy": "medium"},
    {"text": "Your code makes a difference, {name}.", "category": "motivation", "energy": "medium"},
    {"text": "{name}, you've debugged harder problems than this.", "category": "motivation", "energy": "medium"},

    # Motivation - High Energy
    {"text": "{name}, you're on fire! Ship that feature!", "category": "motivation", "energy": "high"},
    {"text": "Channel that energy into clean code, {name}!", "category": "motivation", "energy": "high"},

    # Confidence
    {"text": "{name}, you belong in tech.", "category": "confidence", "energy": "low"},
    {"text": "Trust your debugging instincts, {name}.", "category": "confidence", "energy": "medium"},
    {"text": "{name}, your unique perspective makes the team stronger.", "category": "confidence", "energy": "medium"},
    {"text": "You've got this, {name}!", "category": "confidence", "energy": "high"},

    # Persistence
    {"text": "{name}, even senior devs Google things.", "category": "persistence", "energy": "low"},
    {"text": "The bug will surrender eventually, {name}.", "category": "persistence", "energy": "medium"},
    {"text": "{name}, stuck is temporary. Keep digging.", "category": "persistence", "energy": "medium"},
    {"text": "Persistence beats talent, {name}. Keep going!", "category": "persistence", "energy": "high"},

    # Self-care
    {"text": "{name}, it's okay to step away from the screen.", "category": "self-care", "energy": "low"},
    {"text": "Your worth isn't measured in commits, {name}.", "category": "self-care", "energy": "low"},
    {"text": "{name}, take a break. The code will wait.", "category": "self-care", "energy": "medium"},

    # Growth
    {"text": "{name}, every error is a learning opportunity.", "category": "growth", "energy": "low"},
    {"text": "You're a better developer than you were yesterday, {name}.", "category": "growth", "energy": "medium"},
    {"text": "{name}, embrace the struggle. That's where growth happens.", "category": "growth", "energy": "medium"},
    {"text": "Level up, {name}! Challenge accepted!", "category": "growth", "energy": "high"},
]

# Mood to category mappings
MOOD_CATEGORY_MAP = {
    "happy": ["motivation", "growth"],
    "stressed": ["self-care", "persistence"],
    "anxious": ["confidence", "self-care"],
    "tired": ["self-care", "motivation"],
    "frustrated": ["persistence", "confidence"],
    "motivated": ["motivation", "growth"],
    "neutral": ["motivation", "confidence"]
}


def get_affirmation(
    name: str,
    mood: str,
    energy: int,
    category: Optional[str] = None,
    seed: Optional[int] = None
) -> dict:
    """
    Get a personalized developer affirmation based on mood and energy.
    
    The function uses a weighted random algorithm to select the most appropriate 
    affirmation. It prioritizes matches that align with both the category and the 
    energy level, allowing for variety while maintaining personalization.

    Parameters
    ----------
    name : str
        User's name for personalization.
    mood : str
        Current mood. Valid options: 'happy', 'stressed', 'anxious', 'tired', 
        'frustrated', 'motivated', 'neutral'.
    energy : int
        Energy level on a scale of 1-10.
        - 1-3: Low (calming/reassuring)
        - 4-7: Medium (balanced/steady)
        - 8-10: High (energetic/driving)
    category : str, optional
        Specific category constraint (e.g., 'motivation', 'growth').
        If provided, this overrides the default mood-to-category mapping.
    seed : int, optional
        Random seed for reproducible selection. Uses a local random instance 
        to avoid affecting global state.

    Returns
    -------
    dict
        Affirmation with keys: text, category, mood_alignment.
    """
    _validate_inputs(name, mood, energy, category, seed)

    if seed is not None:
        random.seed(seed)

    display_name = _sanitize_name(name)
    energy_cat = _get_energy_category(energy)
    preferred_categories = _get_preferred_categories(mood, category)

    candidates = _weight_affirmations(preferred_categories, energy_cat)
    selected = _weighted_random_choice(candidates)

    personalized_text = selected["text"].replace("{name}", display_name)
    mood_alignment = _calculate_alignment(selected, preferred_categories, energy_cat)

    return {
        "text": personalized_text,
        "category": selected["category"],
        "mood_alignment": mood_alignment
    }


def _validate_inputs(
    name: str,
    mood: str,
    energy: int,
    category: Optional[str],
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
    if not isinstance(name, str):
        raise TypeError(f"name must be a string, got {type(name).__name__}")

    if not isinstance(mood, str):
        raise TypeError(f"mood must be a string, got {type(mood).__name__}")

    if mood.lower() not in VALID_MOODS:
        raise ValueError(f"Invalid mood '{mood}'. Must be one of: {', '.join(VALID_MOODS)}")

    if not isinstance(energy, int) or isinstance(energy, bool):
        raise TypeError(f"energy must be an integer, got {type(energy).__name__}")

    if energy < 1 or energy > 10:
        raise ValueError("energy must be between 1 and 10")

    if category is not None:
        if not isinstance(category, str):
            raise TypeError(f"category must be a string, got {type(category).__name__}")
        if category.lower() not in VALID_CATEGORIES:
            raise ValueError(f"Invalid category '{category}'. Must be one of: {', '.join(VALID_CATEGORIES)}")

    if seed is not None and not isinstance(seed, int):
        raise TypeError(f"seed must be an integer, got {type(seed).__name__}")


def _sanitize_name(name: str) -> str:
    """
    Sanitize and format the user's name.

    Parameters
    ----------
    name : str
        Raw name input.

    Returns
    -------
    str
        Formatted name or 'Developer' if empty.
    """
    stripped = name.strip()
    return stripped.title() if stripped else "Developer"


def _get_energy_category(energy: int) -> str:
    """
    Convert numeric energy level to category.

    Parameters
    ----------
    energy : int
        Energy level from 1-10.

    Returns
    -------
    str
        Energy category: 'low', 'medium', or 'high'.
    """
    if energy <= 3:
        return "low"
    elif energy <= 7:
        return "medium"
    else:
        return "high"


def _get_preferred_categories(mood: str, category: Optional[str]) -> list[str]:
    """
    Get preferred affirmation categories based on mood.

    Parameters
    ----------
    mood : str
        User's current mood.
    category : str or None
        Explicit category override.

    Returns
    -------
    list of str
        Ordered list of preferred categories.
    """
    if category:
        return [category.lower()]
    return MOOD_CATEGORY_MAP.get(mood.lower(), ["motivation"])


def _weight_affirmations(
    preferred_categories: list[str],
    energy_cat: str
) -> list[tuple[dict, float]]:
    """
    Weight affirmations based on category and energy match.

    Parameters
    ----------
    preferred_categories : list of str
        Preferred categories in order of preference.
    energy_cat : str
        User's energy category.

    Returns
    -------
    list of tuple
        List of (affirmation, weight) tuples.
    """
    candidates = []
    energy_order = ["low", "medium", "high"]

    for affirmation in AFFIRMATIONS:
        weight = 1.0

        # Category match weighting
        if affirmation["category"] in preferred_categories:
            idx = preferred_categories.index(affirmation["category"])
            weight *= (3.0 if idx == 0 else 2.0)
        else:
            weight *= 0.5

        # Energy match weighting
        if affirmation["energy"] == energy_cat:
            weight *= 2.0
        elif abs(energy_order.index(affirmation["energy"]) - energy_order.index(energy_cat)) == 1:
            weight *= 1.5

        candidates.append((affirmation, weight))

    return candidates if candidates else [(a, 1.0) for a in AFFIRMATIONS]


def _weighted_random_choice(candidates: list[tuple[dict, float]]) -> dict:
    """
    Select an affirmation using weighted random selection.

    Parameters
    ----------
    candidates : list of tuple
        List of (affirmation, weight) tuples.

    Returns
    -------
    dict
        Selected affirmation.
    """
    total = sum(w for _, w in candidates)
    r = random.uniform(0, total)

    cumulative = 0
    for affirmation, weight in candidates:
        cumulative += weight
        if r <= cumulative:
            return affirmation

    return candidates[-1][0]


def _calculate_alignment(
    selected: dict,
    preferred_categories: list[str],
    energy_cat: str
) -> float:
    """
    Calculate how well the affirmation aligns with user's mood/energy.

    Parameters
    ----------
    selected : dict
        The selected affirmation.
    preferred_categories : list of str
        User's preferred categories.
    energy_cat : str
        User's energy category.

    Returns
    -------
    float
        Alignment score between 0.0 and 1.0.
    """
    score = 0.5  # Base score
    if selected["category"] in preferred_categories:
        score += 0.3
    if selected["energy"] == energy_cat:
        score += 0.2
    return round(min(score, 1.0), 2)