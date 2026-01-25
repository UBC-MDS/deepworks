# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

##  [Unreleased]

- Upcoming features and fixes:
  - AI integration on GitHub issues

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
