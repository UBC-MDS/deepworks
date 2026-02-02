---
title: "Retrospective"
---

# Retrospective

This portion discusses the development tools, GitHub infrastructure, and organizational practices we learned and applied throughout this project, as well as recommendations for scaling up.

## Project Analytics & Data-Driven Retrospective

### Team Workload Distribution

Based on our [Team Workload View](https://github.com/orgs/UBC-MDS/projects/353/views/10):

| Contributor | Issues Assigned |
|-------------|-----------------|
| @jiroamato | 61 |
| @shanzekhem | 41 |
| @Jenniferonyebuchi | 33 |
| @jimmy2026-V | 33 |

**Analysis:** While the raw numbers show variation, this reflects the nature of different tasks rather than unequal contribution. @jiroamato took on many smaller coordination and integration tasks (such as testing workflows), while the rest of the team members handled larger, more complex features. Otherwise, team members shared responsibility equally for major milestone deliverables, with pull requests showing collaborative co-assignment during integration phases.

### Burn-up Chart Analysis

Based on our [Burn-up Chart](https://github.com/orgs/UBC-MDS/projects/353/insights/8):

| Contributor | M1 | M2 | M3 | M4 | Total |
|-------------|----|----|----|----|-------|
| Jenniferonyebuchi | 7 | 4 | 8 | 14 | 33 |
| jimmy2026-V | 7 | 4 | 8 | 14 | 33 |
| jiroamato | 8 | 9 | 14 | 30 | 61 |
| shanzekhem | 7 | 5 | 9 | 20 | 41 |
| **Total** | **29** | **22** | **39** | **78** | **168** |

**Velocity Trend:** Total issues completed increased from 29 in Milestone 1 to 78 in Milestone 4, representing sustained project acceleration and completion momentum. M4 had the highest volume due to the addition of AI workflows, peer review feedback, documentation improvements, and final polish tasks.

### Status Overview

Based on our [Status Chart](https://github.com/orgs/UBC-MDS/projects/353/insights/6):

- **Milestones 1-4**: 100% completion (all tasks closed)

### Pull Request Contributions

Based on our [PR per Contributor](https://github.com/orgs/UBC-MDS/projects/353/insights/4) view, the team collectively completed **49 merged pull requests** across four milestones. All team members contributed PRs covering feature implementations, documentation, bug fixes, and CI/CD improvements.

## Retrospective Discussion: DAKI Framework

Using the **DAKI (Drop, Add, Keep, Improve)** framework to reflect on our practices:

### Drop

- **Real-life communication dependency:** Reliance on real-life meetings could be reduced with better async/digital practices

### Add

- **CODEOWNERS file:** Would have auto-assigned reviewers by file path, reducing "who should review this?" questions
- **Stale issue automation:** GitHub Actions like `actions/stale` to auto-close inactive issues
- **Automated labeling:** `actions/labeler` to tag PRs based on changed files

### Keep

- **Sprint-based milestones:** Master issues with linked sub-issues provided clear scope and traceability
- **CI/CD pipelines:** Automated testing and deployment caught issues early
- **AI-powered workflows:** Gemini-based PR reviews and docstring checks improved quality
- **Code coverage tracking:** Codecov integration ensured test quality

### Improve

- **Issue templates:** More structured bug reports with required fields would reduce back-and-forth
- **Draft PRs:** Better use of draft status to signal "work in progress"
- **Earlier documentation:** Writing docs alongside code rather than after

## Planning Accuracy & Bottlenecks

**Planning Observations:**

- M1 and M2 had relatively balanced scope (29 and 22 issues)
- M3 (CI/CD setup) required more issues (39) due to debugging workflows
- M4 had the highest count (78) due to comprehensive peer review feedback integration

**Bottleneck Analysis:**

- PR reviews occasionally created small queues
- GitHub Actions debugging required more iterations than anticipated
- Integration testing across Python versions (3.10-3.13) caught edge cases late

**Bus Factor Consideration:**

Looking at workload distribution, if the contributor with the highest ticket count became unavailable, the project could have faced delays. Mitigation strategies include:

- Comprehensive documentation
- Code review ensuring multiple people understand each area

## Project Dimensions: Communication Load & Criticality

Following Alistair Cockburn's framework (from the Agile Manifesto), we recognize that project methodology should match two key dimensions:

### Communication Load

Our team of 4 required structured coordination tools:

- **GitHub Issues & Milestones** replaced informal verbal agreements
- **Project Boards** provided visibility into what everyone was working on
- **PR-based workflow** forced explicit code review and knowledge sharing

As teams grow, "shouting across the room" stops working—tools must compensate for the inability to hold the entire project state in one person's head.

### Criticality

As a package deployed to PyPI for public use:

- **CI matrix testing** across Python 3.10-3.13 mitigates "it works on my machine" issues
- **Codecov integration** ensures we don't ship untested code paths
- **Trusted publishing** to PyPI ensures the repository code matches what users install

Higher criticality justifies heavier infrastructure, not to "be good programmers," but to mitigate risk.

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

- **AI Critic (PR)**: Uses to review pull request changes for quality, correctness, and maintainability - [example outout in #108](https://github.com/UBC-MDS/deepworks/pull/108#issuecomment-3827676383)
- **AI Docstring Detective**: Analyzes docstrings from a novice user's perspective to ensure clarity - [example output in #109](https://github.com/UBC-MDS/deepworks/pull/109#issuecomment-3832175512)
- **AI Tutorial Generator**: Generates tutorials based on code changes - [example output in #108](https://github.com/UBC-MDS/deepworks/pull/108#issuecomment-3827676410)
- **AI Critic (Issues)**: Reviews and provides feedback on new issues - [example output in #68](https://github.com/UBC-MDS/deepworks/issues/68#issuecomment-3814188038)

### Code Coverage with Codecov

Integration with [Codecov](https://codecov.io/) provides:

- Coverage reports on every PR - [example output in #109](https://github.com/UBC-MDS/deepworks/pull/109#issuecomment-3827863018)
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
- **Cross-team visibility**: All contributors can see what others are working on, reducing duplication and improving collaboration

## Scaling Recommendations

If we were to scale up this or another project, we would implement the following tools, infrastructure, and practices. The level of formality should match project needs—a 48-hour hackathon doesn't need the same rigor as production tax software.

### Formality Scaling Framework

Drawing from course learnings, here's how formality scales across project dimensions. We assess our **current formality level** and identify **next steps** for scaling.

#### Verification Strategy (Local → Distributed)

| Formality | Practice | Our Implementation | Status |
|-----------|----------|-------------------|--------|
| Low | Run `pytest` locally | Initial development | Past |
| Medium | CI on standard runner | `build.yml` on Ubuntu | Past |
| **High** | **Matrix testing + coverage gates** | **Python 3.10-3.13, Codecov 80% threshold** | **Current** |

**Current Level: High** — We have matrix testing across 4 Python versions with coverage enforcement.

**Next Level:** Add OS matrix (Ubuntu, macOS, Windows), performance regression testing with `pytest-benchmark`, and mutation testing to verify test quality.

#### Release Management (Manual → Automated)

| Formality | Practice | Our Implementation | Status |
|-----------|----------|-------------------|--------|
| Low | Zip and share | N/A | Past |
| Medium | Semantic versioning + GitHub Releases | `hatch-vcs` for git tags | Past |
| **High** | **CD pipelines with trusted publishing** | **`deploy.yml` to Test PyPI via OIDC** | **Current** |

**Current Level: High** — We use trusted publishing (OIDC) to Test PyPI without secret API keys.

**Next Level:** Add staged deployments (Test PyPI → PyPI) with manual approval gates, automatic changelog generation from conventional commits using `action-gh-release`, and signed releases with Sigstore.

#### Workflow & Planning (Ad-hoc → Transparent)

| Formality | Practice | Our Implementation | Status |
|-----------|----------|-------------------|--------|
| Low | Chat to decide tasks | Early discussions | Past |
| Medium | Issues + Kanban board | GitHub Projects | Past |
| **High** | **Analytics, templates, CONTRIBUTING.md** | **Project Insights, contribution guidelines** | **Current** |

**Current Level: High** — We have project analytics, structured contribution guidelines, and milestone-based planning.

**Next Level:** Add CODEOWNERS for automatic reviewer assignment, YAML-based issue templates with required fields, `actions/stale` for automatic issue cleanup, and `actions/labeler` for automatic PR categorization.

#### Code Review & Collaboration

| Formality | Practice | Our Implementation | Status |
|-----------|----------|-------------------|--------|
| Low | Informal review or none | N/A | Past |
| **Medium** | **PR reviews** | **Required reviews, status checks** | **Current** |
| High | CODEOWNERS + multiple approvers + AI assist | AI-powered reviews (partial) | → Next |

**Current Level: Medium-High** — We require PR reviews and have AI-powered review assistance, but lack CODEOWNERS.

**Next Level:** Add CODEOWNERS file mapping code areas to specific reviewers, require 2+ approvals for `main`, and integrate AI suggestions more deeply into the review workflow.

### Summary: Current Project Formality

| Dimension | Current Level |
|-----------|---------------|
| Verification | High |
| Release Management | High |
| Workflow & Planning | High |
| Code Review | Medium-High |

**Overall Assessment:** This project operates at **high formality** appropriate for an open-source package deployed to PyPI. The main gap is in code review automation (CODEOWNERS, multi-approver requirements).

### Recommended GitHub Actions for Scale

These actions provide high value for growing projects:

**Quality & Compliance ("The Gatekeepers"):**

- [Super-Linter](https://github.com/super-linter/super-linter): Checks Python, Markdown, YAML, Dockerfiles in one pass
- [Codecov Action](https://github.com/codecov/codecov-action): PR comments showing coverage impact (we use this)

**Release & Deployment ("The Time Savers"):**

- [PyPI Publish](https://github.com/pypa/gh-action-pypi-publish): Trusted publishing without secret API keys (we use this)
- [GH Release](https://github.com/softprops/action-gh-release): Auto-generate releases from git tags

**Project Hygiene ("The Janitors"):**

- [Stale](https://github.com/actions/stale): Auto-close inactive issues/PRs
- [Labeler](https://github.com/actions/labeler): Auto-label based on changed files

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
- **Draft Pull Requests** to signal "work in progress" and prevent premature reviews

### GenAI Integration for Development

Our project already leverages AI-powered workflows. For scaling, we recommend:

**Code Quality:**

- AI-powered PR reviews (we use Gemini 2.5 Flash via `ai-critic.yml`)
- Docstring quality analysis from novice user perspective (`ai-docstring-detective.yml`)
- Automated tutorial generation from code changes (`ai-tutorial.yml`)

**Interaction Rules for GenAI Tools:**

- AI suggestions should be reviewed by humans before merging
- AI-generated code must pass all existing tests and linting
- AI should augment, not replace, code review discussions
- Document when AI tools are used (e.g., `Co-Authored-By` in commits)

### Monitoring and Observability

- **Download statistics** tracking from PyPI (like downloads)
- **Performance monitoring** to track response times and resource usage

### Security Practices

- **Signed commits** with GPG for authenticity verification
- **Regular dependency audits** with automated alerts
- **Secret scanning** to prevent credential leaks
