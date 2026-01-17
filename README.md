# deepwork

|  |  |
|------------------------------------|------------------------------------|
| Package | [![PyPI Version](https://img.shields.io/badge/PyPI-v0.1.0-lightgrey.svg)](#) [![Python Versions](https://img.shields.io/badge/Python-3.10%2B-lightgrey.svg)](#) |
| Meta | [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) |

`deepwork` is a Python package for developer productivity that helps developers stay focused and energized throughout the workday. `deepwork` provides tools to plan focus (pomodoro) sessions, prioritize tasks, take effective breaks, and stay motivated with personalized affirmations. The perfect package for developers looking to optimize their workflow.

## Get Started
> To install the latest release (latest tag) from GitHub, run the following:
``` bash
$ pip install git+https://github.com/UBC-MDS/deepwork@main
```

### Functions

This package contains four main functions:

-   **`prioritize_tasks()`**: Rank a list of tasks by priority using different methods including weighted scoring or deadline-based sorting. Returns a DataFrame with priority scores and rankings.

-   **`plan_pomodoro()`**: Calculate a work/break schedule based on your available time and preferred technique (Pomodoro, 52-17, 90-20, or custom). Returns a DataFrame with a complete session schedule.

-   **`suggest_break()`**: Get a recommended break activity based on how long you've worked, your current energy level, and preferences for activity type and duration. Returns a dictionary with activity details and instructions.

-   **`get_affirmation()`**: Receive a personalized developer-focused affirmation based on your current mood and energy level. Returns a dictionary with the affirmation text and metadata.

*This package does not include any datasets and all functions work based on user-provided inputs.*

### Dependencies

`deepwork` requires the following libraries:

-   **Python 3.10+**: Required runtime environment.
-   **Pandas**: Used for data manipulation and the structured table display of schedules and tasks.
-   **pip**: Used for package installation.

## Usage

``` python
from deepwork.affirmation import get_affirmation
from deepwork.pomodoro import plan_pomodoro
from deepwork.prioritize import prioritize_tasks
from deepwork.breaks import suggest_break

# Get a motivational affirmation
affirmation = get_affirmation(name="Alice", mood="stressed", energy=4)
print(affirmation['text'])

# Plan a 2-hour focus session
schedule = plan_pomodoro(total_minutes=120, technique="pomodoro")
print(schedule)

# Prioritize your tasks
tasks = [
    {"name": "Fix bug", "deadline": "2026-01-10", "effort": 2, "importance": 5},
    {"name": "Write docs", "deadline": "2026-01-15", "effort": 3, "importance": 3},
]
ranked = prioritize_tasks(tasks, method="weighted")
print(ranked)

# Get a break suggestion after working
activity = suggest_break(minutes_worked=90, energy_level=4, break_type="active")
print(activity['name'], "-", activity['description'])
```

## Testing

To run the tests for this package, clone the repository and install it with the test dependencies:

1. Clone the repository:
``` bash
$ git clone https://github.com/UBC-MDS/deepwork
```

2. Install the package with test dependencies:
```bash
$ cd path/to/deepwork
$ pip install -e ".[tests]"
```

3. Run tests accordingly:
```bash
$ pytest tests/ -v --cov=deepwork --cov-branch --cov-report=term-missing # shows a verbose output of tests
```

## Python Ecosystem

`deepwork` combines productivity and wellness features into a single cohesive library. While there are separate packages for individual features like [tomato-timer](https://pypi.org/project/tomato-timer/) for Pomodoro timing and various task management libraries, `deepwork` uniquely integrates focus session planning, task prioritization, break suggestions, and motivational affirmations into one package, specifically designed for developers. This holistic approach helps developers maintain both productivity and well-being without needing multiple tools.

## Contributors

-   Jingbo Wang - @jimmy2026-V
-   Jennifer Onyebuchi - @Jenniferonyebuchi
-   Shanzé Khemani - @shanzekhem
-   Jiro Amato - @jiroamato

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## Copyright

-   Copyright © 2026 Jingbo Wang, Jennifer Onyebuchi, Shanzé Khemani, Jiro Amato.

-   Free software distributed under the [MIT License](./LICENSE).
