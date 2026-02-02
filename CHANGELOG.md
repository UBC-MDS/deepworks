# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.0.0] - (2026-01-31)

### Peer Review Fixes

- Include function outputs in the `Usage` section in `README.md` - #95
- Add emails in the authors matrix in `pyproject.toml` - #96
- Add missing badge for documentation building workflow - #97
- Add more clarity in `README.md` especially in the pomodoro section - #98

### Added

- Workflow improvements:
  - `ai-critic-pr` workflow for AI-powered PR reviews (`.github/workflows/ai-critic-pr.yml`)
  - `ai-critic-issue` workflow for AI-powered issue analysis (`.github/workflows/ai-critic-issue.yml`)
  - `ai-docstring-detective` workflow for detecting missing docstrings (`.github/workflows/ai-docstring-detective.yml`)
  - `ai-tutorial-gen` workflow for AI-generated tutorials (`.github/workflows/ai-tutorial-gen.yml`)
  - `docs-preview` for previewing documentation in PR's (`.github/workflows/docs-preview.yml`)
- Added `raw-options` to `pyproject.toml` to avoid versioning issues in deployment
- Interactive tutorial (`tutorial.qmd`) demonstrating all package functions with executable Python cells
- Jupyter dependency to docs optional dependencies for executable documentation code cells
- Tutorial link added to documentation navbar
- CC-BY-4.0 license for documentation
- Added `RETROSPECTIVE.md` to the quarto website for project reflection

### Changed

- Updated `CONTRIBUTING.md` with clear git workflow and branch structure diagram
- Updated `CONTRIBUTING.md` with developer setup instructions using Hatch
- Improved `README.md` with updated usage examples and test case for a single module
- Updated dynamic badges in `README.md` for CI/CD
- Function changes:
  - `plan_pomodoro()`: Simplified function to return plain DataFrame without metadata attributes (`.attrs`), removed `_create_dataframe_with_metadata()` function, and changed `_build_schedule()` to return only the schedule list
  - `suggest_break()`: Refactored `_filter_activities()` to use list comprehensions with the new `_matches_filters()` helper for cleaner and more readable code
  - `get_affirmation()`:
    - `ENERGY_ORDER` module-level constant for energy level ordering (previously defined locally in `_weight_affirmations`)
    - Random seed isolation: Changed from `random.seed(seed)` to `rng = random.Random(seed)` to prevent polluting global random state when using the seed parameter
  - `prioritize_tasks()`: `_calculate_weighted_scores()` now uses `DEFAULT_WEIGHTS` constant instead of hardcoded fallback values (0.5, 0.3, 0.2)
- Updated docstring for each function to have more detailed parameter descriptions, expanded return value documentation, and updated examples

## [v1.0.2] - (2026-01-26)

### Changed

- Changed pip installation command to `pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ deepworks` in `README.md` in order to include Pandas in the pip installation from Test PyPi

## [v1.0.1] - (2026-01-25)

### Fixed

- Rendering issues of dynamic badges due to `$` in query parameter when rendered in quartodoc

## [v1.0.0] - (2026-01-25)

### Added

- CI integration via GitHub Workflows (`.github/workflows/build.yml`)
- CD integration via GitHub Workflows (`.github/workflows/deploy.yml`)
- Documentation build and deployment via GitHub Workflows (`.github/workflows/docs-publish.yml`)
- Dynamic badges on `README.md`
- Rendered documentation for the repo using [quartodoc](https://machow.github.io/quartodoc/) through Hatch
- Publish on PyPi  

### Changed

- Renamed package from `deepwork` to `deepworks` to avoid naming conflicts when publishign to PyPi
- Added additional unit tests, minor improvements and created a more in depth documentation for the following:
  - `suggest_break`
  - `get_affirmation`
  - `plan_pomodoro()`
  - `prioritize_tasks()`
- Added the following sections on `README.md`:
  - Developer Setup
  - Building Documentation
  - Deployment
- New semantic versioning that follows `v*.*.*` convention
- Removed the following workflows:
  - `docs.yml`
  - `release.yml`
  - `test.yml`
  - `dependabot.yml`

## [0.0.2] - (2026-01-17)

### Added

- Added pandas dependency to pyproject.toml
- `suggest_break` function that recommends break activities based on work duration and preferences (break type, duration, location, energy level)
- `get_affirmation` function that returns motivational affirmations based on energy level and task type
- `plan_pomodoro()` implementation for generating Pomodoro-style work/break schedules.
- `prioritize_tasks()` function for ranking tasks by priority (either by importance or deadline)
- Comprehensive test suite for `suggest_break`, `get_affirmation`, `plan_pomodoro`
- Added `Testing` portion to the README.md
- Added a brief description of the package in `src/deepwork/__init__.py`

### Changed

- Updated all docstring to be more comprehensive and include examples of usage.
- Added `--cov-branch` flag under the [tool.hatch.envs.test.scripts] matrix in the `pyproject.toml` file

## [0.0.1] - (2026-01-10)

- First release:
  - Create project structure for the software package
  - Write function specifications and documentation
