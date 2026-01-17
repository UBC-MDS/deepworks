# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - (2026-01-16)

- Upcoming features and fixes:

### Added
- Initial `plan_pomodoro()` implementation for generating Pomodoro-style work/break schedules.
- Initial test suite for `plan_pomodoro()`.
- Additional edge case coverage in tests (e.g., short total time / truncation scenarios).
- Input validation for function arguments (type checks, required parameters for `custom`, positive durations, valid technique values).

### Changed
- Updated `pomodoro.py` docstring to document presets, truncation behavior, parameters, return schema, and errors.
- Refactored and consolidated `plan_pomodoro()` using helper functions for better organization and maintainability.

## [0.1.0] - (2026-01-10)

- ## First release:

- Draft a team work contract
- Create project structure for the software package
- Write function specifications and documentation
