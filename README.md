# deepworks

| | |
| --- | --- |
| Testing | [![CI](https://github.com/UBC-MDS/deepworks/actions/workflows/build.yml/badge.svg)](https://github.com/UBC-MDS/deepworks/actions/workflows/build.yml) [![CD](https://github.com/UBC-MDS/deepworks/actions/workflows/deploy.yml/badge.svg)](https://github.com/UBC-MDS/deepworks/actions/workflows/deploy.yml) [![codecov](https://codecov.io/github/UBC-MDS/deepworks/branch/main/graph/badge.svg?token=0mWtA6XJd5)](https://codecov.io/github/UBC-MDS/deepworks) |
| Package | [![Test PyPI Latest Release](https://img.shields.io/badge/dynamic/json?url=https://test.pypi.org/pypi/deepworks/json&query=$.info.version&label=TestPyPI&color=green)](https://test.pypi.org/project/deepworks/) [![GitHub Release](https://img.shields.io/github/v/release/UBC-MDS/deepworks?color=green)](https://github.com/UBC-MDS/deepworks/releases) [![Python Version](https://img.shields.io/badge/dynamic/json?url=https://test.pypi.org/pypi/deepworks/json&query=$.info.requires_python&label=Python&color=green)](https://test.pypi.org/project/deepworks/) [![Repo Status](https://img.shields.io/badge/repo%20status-Active-brightgreen)](https://github.com/UBC-MDS/deepworks) |
| Meta | [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) [![License - MIT](https://img.shields.io/badge/dynamic/json?url=https://test.pypi.org/pypi/deepworks/json&query=$.info.license&label=License&color=blue)](https://github.com/UBC-MDS/deepworks/blob/main/LICENSE) |

`deepworks` is a Python package for developer productivity that helps developers stay focused and energized throughout the workday. `deepworks` provides tools to plan focus (pomodoro) sessions, prioritize tasks, take effective breaks, and stay motivated with personalized affirmations. The perfect package for developers looking to optimize their workflow.

## Installation

To install the latest release from Test PyPi:

```bash
pip install -i https://test.pypi.org/simple/ deepworks
```

### Functions

This package contains four main functions:

-   **`prioritize_tasks()`**: Rank a list of tasks by priority using different methods including weighted scoring or deadline-based sorting. Returns a DataFrame with priority scores and rankings.

-   **`plan_pomodoro()`**: Calculate a work/break schedule based on your available time and preferred technique (Pomodoro, 52-17, 90-20, or custom). Returns a DataFrame with a complete session schedule.

-   **`suggest_break()`**: Get a recommended break activity based on how long you've worked, your current energy level, and preferences for activity type and duration. Returns a dictionary with activity details and instructions.

-   **`get_affirmation()`**: Receive a personalized developer-focused affirmation based on your current mood and energy level. Returns a dictionary with the affirmation text and metadata.

*This package does not include any datasets and all functions work based on user-provided inputs.*

### Dependencies

`deepworks` requires the following libraries:

-   **Python 3.10+**: Required runtime environment.
-   **Pandas**: Used for data manipulation and the structured table display of schedules and tasks.
-   **pip**: Used for package installation.

## Usage

``` python
from deepworks.affirmation import get_affirmation
from deepworks.pomodoro import plan_pomodoro
from deepworks.prioritize import prioritize_tasks
from deepworks.breaks import suggest_break

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

## Developer Setup

1. To set up the development environment, first install [pipx](https://pipx.pypa.io/) and then [Hatch](https://hatch.pypa.io/):
> For more information on how to use Hatch, check out this tutorial from pyOpenSci [here](https://www.pyopensci.org/python-package-guide/tutorials/get-to-know-hatch.html).

```bash
pip install pipx
pipx install hatch
```

2. Clone the repository:

```bash
git clone https://github.com/UBC-MDS/deepworks
cd deepworks
```

3. Install the package in development mode using Hatch:

```bash
hatch shell
```

This will create a virtual environment and install the package with all dependencies.

If you want to leave the developer environment, simply type the following command:

```bash
exit
```

Alternatively, if you want to install the package on a particular environment run:

```bash
pip install -e .
```

## Testing

To run the tests for this package using Hatch:

```bash
hatch run test:run
```

This runs pytest with coverage reporting in the `test` environment.

## Building Documentation

The documentation is built using [Quarto](https://quarto.org/) and [quartodoc](https://machow.github.io/quartodoc/) through Hatch.

1. Install the [Quarto CLI](https://quarto.org/docs/get-started/):

```bash
pip install quarto-cli
```

2. To preview the documentation locally with live reload:

```bash
hatch run docs:serve
```

3. Build and render the documentation:

```bash
hatch run docs:build
```

The generated documentation will be in the `docs/` directory.

## Deployment

This project uses GitHub Actions for continuous integration and deployment.

### Continuous Integration (`build.yml`)

Runs on pushes and pull requests to `main` and `develop` branches:
- Runs the test suite across Python 3.10, 3.11, 3.12, and 3.13
- Uploads coverage reports to Codecov
- Runs linting and formatting checks with Ruff

### Continuous Deployment (`deploy.yml`)

Runs on new version tags (`v*.*.*`):
- Runs the full test suite and style checks
- Builds the package using Hatch
- Publishes to Test PyPI

### Documentation (`docs-publish.yml`)

Runs on pushes and pull requests to `main`:
- Builds the quartodoc API reference
- Renders the Quarto site
- Publishes to GitHub Pages (`gh-pages` branch)

## Python Ecosystem

`deepworks` combines productivity and wellness features into a single cohesive library. While there are separate packages for individual features like [tomato-timer](https://pypi.org/project/tomato-timer/) for Pomodoro timing and various task management libraries, `deepworks` uniquely integrates focus session planning, task prioritization, break suggestions, and motivational affirmations into one package, specifically designed for developers. This holistic approach helps developers maintain both productivity and well-being without needing multiple tools.

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
