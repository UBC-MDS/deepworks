---
title: "Retrospective"
---

# Retrospective

This portion discusses the development tools, GitHub infrastructure, and organizational practices we learned and applied throughout this project, as well as recommendations for scaling up.

## Development Tools

### Package Management with Hatch

We use [Hatch](https://hatch.pypa.io/) as our primary build and environment management tool. Hatch provides:

- **Isolated environments** for different tasks (testing, documentation, linting)
- **Reproducible builds** with `hatchling` as the build backend
- **Version control integration** via `hatch-vcs` for automatic versioning from git tags
- **Script management** for common tasks like `hatch run test:run` and `hatch run docs:build`

### Code Quality with Ruff

[Ruff](https://docs.astral.sh/ruff/) handles both linting and formatting:

- Automatic formatting ensures consistent code style
- Integrated into CI pipeline for automated checks

### Testing with Pytest

Our test suite uses [pytest](https://docs.pytest.org/) with several plugins:

- `pytest-cov` for code coverage reporting
- `pytest-randomly` to detect order-dependent tests
- `pytest-xdist` for parallel test execution
- Multi-version testing across Python 3.10, 3.11, 3.12, and 3.13

### Documentation with Quarto and Quartodoc

Documentation is built using:

- [Quarto](https://quarto.org/) for rendering the website
- [Quartodoc](https://machow.github.io/quartodoc/) for automatic API reference generation from docstrings

## GitHub Infrastructure

### Git Workflow

We follow a structured branching strategy based on GitHub Flow:

```
main
 └── develop
      ├── feature/feature-name
      │    └── test/feature-name
      └── fix/bug-name
```

- **`main`**: Stable, production-ready branch; only receives merges from `develop` after milestone completion
- **`develop`**: Integration/staging branch where all features and fixes merge
- **Feature branches**: For new features, branched from `develop`
- **Fix branches**: For bug fixes, branched from `develop`
- **Test branches**: For writing tests, branched from feature branches

Check [here](https://github.com/UBC-MDS/deepworks/network) for a better visualization of the branch structure that we have implemented so far.

### CI/CD Pipelines

Our GitHub Actions workflows automate the development lifecycle:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `build.yml` (CI) | Push/PR to `main`/`develop` | Run tests, coverage, and linting |
| `deploy.yml` (CD) | Version tags (`v*.*.*`) | Build and publish to Test PyPI |
| `docs-publish.yml` | Push to `main` | Build and publish documentation to GitHub Pages |
| `docs-preview.yml` | Pull requests | Deploy preview documentation to Netlify |

### AI-Powered Workflows

We leverage AI in the following workflows using [Google Gemini API](https://ai.google.dev/gemini-api/docs) (Gemini 2.5 Flash):

- **AI Critic (PR)**: Uses to review pull request changes for quality, correctness, and maintainability
- **AI Docstring Detective**: Analyzes docstrings from a novice user's perspective to ensure clarity
- **AI Tutorial Generator**: Generates tutorials based on code changes
- **AI Critic (Issues)**: Reviews and provides feedback on new issues

### Code Coverage with Codecov

Integration with [Codecov](https://codecov.io/) provides:

- Coverage reports on every PR
- Historical tracking of code coverage trends
- Visualization of which lines are tested
- Dynamic badge in `README.md`

## Organizational Practices

### Contributing Guidelines

Our [CONTRIBUTING.md](CONTRIBUTING.md) provides:

- Clear instructions for different contribution types (bugs, features, documentation)
- Git workflow (noted above) practices
- Step-by-step setup guide for local development
- Pull request guidelines and review process
- Semantic commit message conventions

### Code of Conduct

We adopt the Contributor Covenant to maintain a welcoming community for all contributors.

### Semantic Versioning

We follow [Semantic Versioning](https://semver.org/) with automated version extraction from git tags using `hatch-vcs`.

We use the following format `v*.*.*` with the convention of `MAJOR.MINOR.PATCH`.

## Sprint-Based Development with Milestones

We operate in sprints organized around GitHub Milestones:

- **Master milestone issues**: Each milestone begins with a master issue that outlines all deliverables and tasks for the sprint
- **Sub-issues**: Individual tasks are created as sub-issues linked to the master issue, providing clear scope and traceability
- **Contributor assignment**: Each sub-issue is assigned to specific contributors, establishing clear ownership and accountability
- **Progress tracking**: The milestone view provides visibility into sprint progress and remaining work

Examples of master issues in this project:

- [Milestone 1](https://github.com/UBC-MDS/deepworks/issues/1)
- [Milestone 2](https://github.com/UBC-MDS/deepworks/issues/22)
- [Milestone 3](https://github.com/UBC-MDS/deepworks/issues/38)
- [Milestone 4](https://github.com/UBC-MDS/deepworks/issues/68)

### Project Board Management

We leverage GitHub Project Boards to manage our workflow:

- **Kanban-style tracking**: Issues move through columns (e.g., To Do, In Progress, Done) as work progresses
- **Visual overview**: The board provides a clear picture of current sprint status at a glance
- **Prioritization**: Issues can be ordered within columns to indicate priority
- **Cross-team visibility**: All contributors can see what others are working on, reducing duplication and improving collaboration

## Scaling Recommendations

If we were to scale up this or another project, we would implement the following tools, infrastructure, and practices:

### Enhanced Testing Infrastructure

- **Performance benchmarking** with [pytest-benchmark](https://pytest-benchmark.readthedocs.io/) to catch regressions

### Advanced CI/CD

- **Matrix testing** across multiple operating systems (Linux, macOS, Windows)
- **Dependency caching** to speed up workflow execution
- **Staged deployments** (Test PyPI → PyPI) with manual approval gates
- **Release automation** with changelog generation from conventional commits

### Documentation Improvements

- **Versioned documentation** to support multiple release versions

### Team Collaboration

- **Protected branches** requiring multiple approvals for `main`
- **CODEOWNERS** file to automatically assign reviewers by file path
- **Issue and PR templates** for feature requests, releases, and more with automatic labelling
- **Automated labeling** based on file paths and PR content

### Monitoring and Observability

- **Download statistics** tracking from PyPI (like downloads)
- **Performance monitoring** to track response times and resource usage

### Security Practices

- **Signed commits** with GPG for authenticity verification
- **Regular dependency audits** with automated alerts
- **Secret scanning** to prevent credential leaks
