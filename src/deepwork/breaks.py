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
        How long you've been working (in minutes).
    energy_level : int
        Current energy level on a scale of 1-10.
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
    # return {} #stub
    ...
