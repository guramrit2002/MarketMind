# Git Conventions

> Version: 1.0
> Last Updated: June 2026

---

# Purpose

This document defines the Git workflow, branching strategy, commit conventions, pull request process, release strategy, and collaboration rules for MarketMind.

The goals are:

- Maintain a clean commit history
- Enable safe collaboration
- Reduce merge conflicts
- Simplify code reviews
- Make releases predictable
- Ensure traceability between code and tickets

---

# Git Workflow

We follow a simplified GitFlow model.

```

Production
▲
│
main
▲
│
develop
▲
│
feature/*
│
bugfix/*
│
hotfix/*
│
release/*

```

---

# Branches

## main

Purpose

Production-ready code.

Rules

- Always deployable
- Protected branch
- No direct commits
- No force push
- Only merged via Pull Request

---

## develop

Purpose

Integration branch.

Rules

- All completed features merge here first.
- CI must pass.
- Always stable enough for QA.

---

## feature

Purpose

New functionality.

Naming

```

feature/MM-001-project-setup

feature/MM-025-product-extraction

feature/MM-041-vector-search

```

Rules

- Created from develop
- Merged back into develop
- Deleted after merge

---

## bugfix

Purpose

Fix bugs found during development.

Naming

```

bugfix/MM-067-pagination

bugfix/MM-080-null-pricing

```

---

## hotfix

Purpose

Emergency production fixes.

Naming

```

hotfix/MM-201-auth-failure

```

Rules

- Created from main
- Merged into both

main

develop

---

## release

Purpose

Prepare production deployment.

Naming

```

release/v1.0.0

release/v1.1.0

```

Allowed Changes

- Documentation
- Version bump
- Minor bug fixes
- Release notes

No new features.

---

# Branch Lifecycle

```

develop

↓

feature/MM-025

↓

commit

↓

push

↓

Pull Request

↓

Review

↓

CI

↓

Merge

↓

Delete Branch

```

---

# Ticket Mapping

Every branch must reference a ticket.

Example

```

MM-025

↓

feature/MM-025-product-extraction

```

Every commit

Every PR

Every merge

should reference the ticket.

---

# Commit Strategy

Commit often.

Each commit should represent one logical change.

Bad

```

Implemented extraction
Fixed API
Updated docs
Refactored repository

```

Good

```

feat: add product extraction service

test: add extraction service tests

docs: update extraction flow

```

---

# Commit Messages

We use Conventional Commits.

Format

```

<type>: <description>

```

---

# Commit Types

Feature

```

feat:

```

Bug

```

fix:

```

Refactor

```

refactor:

```

Documentation

```

docs:

```

Tests

```

test:

```

CI

```

ci:

```

Dependencies

```

build:

```

Maintenance

```

chore:

```

Performance

```

perf:

```

Style

```

style:

```

Revert

```

revert:

```

---

# Good Examples

```

feat: implement conversation state machine

fix: handle empty marketplace response

refactor: split pricing service

test: add vector search tests

docs: update architecture

ci: configure GitHub Actions

```

---

# Bad Examples

```

updated code

fixes

work

changes

done

latest

```

Never use meaningless commit messages.

---

# Commit Size

Preferred

50–300 lines

Maximum

~500 lines

Huge commits are difficult to review.

---

# Pull Requests

Every feature goes through a Pull Request.

Never push directly to

main

develop

---

# Pull Request Title

Use

```

MM-025 Product Extraction Service

MM-041 Product Matching Engine

```

---

# Pull Request Description

Template

```

## Summary

Brief description.

---

## Ticket

MM-025

---

## Changes

- Added service
- Added repository
- Added tests

---

## Testing

- Unit tests
- Integration tests

---

## Checklist

- [ ] Tests passing
- [ ] Documentation updated
- [ ] PLAN updated
- [ ] CI passing

```

---

# Pull Request Size

Preferred

<500 lines

Maximum

~1000 lines

Split larger work.

---

# Code Review

Every PR requires at least one approval.

Review should verify

- Correctness
- Readability
- Tests
- Architecture
- Performance
- Security

---

# Merge Strategy

Use

Squash Merge

Reason

Keeps history clean.

One feature

↓

One commit

---

# Merge Commit Format

```

feat: MM-025 Product Extraction Service

```

---

# Rebasing

Before opening a PR

```

git fetch origin

git rebase origin/develop

```

Avoid unnecessary merge commits.

---

# Resolving Conflicts

Rules

- Pull latest develop
- Rebase
- Resolve locally
- Run tests
- Push

Never resolve conflicts in GitHub UI unless trivial.

---

# Force Push

Allowed only on

your own feature branch

Never

main

Never

develop

Never

release

---

# Tags

Every production release gets a tag.

Examples

```

v0.1.0

v0.2.0

v1.0.0

v1.1.2

```

Follow Semantic Versioning.

---

# Semantic Versioning

```

MAJOR.MINOR.PATCH

```

Example

```

1.4.2

```

Major

Breaking changes.

Minor

New features.

Patch

Bug fixes.

---

# Release Process

```

develop

↓

release/v1.0.0

↓

QA

↓

main

↓

tag

↓

deploy

↓

merge back into develop

```

---

# Emergency Hotfix

```

main

↓

hotfix/MM-201

↓

main

↓

deploy

↓

merge into develop

```

---

# Git Ignore

Never commit

```

.env

.idea

.vscode/settings.json

__pycache__

.pytest_cache

.coverage

*.log

*.sqlite3

```

---

# Binary Files

Avoid committing

- Videos
- Screenshots
- ZIP files
- Large datasets

Store them externally.

---

# Secrets

Never commit

- API Keys
- Tokens
- Passwords
- Certificates

Use environment variables.

---

# Large Refactoring

Separate refactoring from feature work.

Bad

```

Refactor 40 files

+

Implement feature

```

Good

PR 1

Refactor

PR 2

Feature

---

# Feature Development Workflow

```

git checkout develop

↓

git pull

↓

git checkout -b feature/MM-025-product-extraction

↓

Implement

↓

git add .

↓

git commit

↓

git push

↓

Open Pull Request

↓

Review

↓

Merge

↓

Delete Branch

```

---

# Before Every Commit

Run

```

ruff check .

black .

mypy .

pytest
```

No commit should break the build.

---

# Before Opening a Pull Request

Verify

- Project builds
- Tests pass
- Ruff passes
- MyPy passes
- Documentation updated
- PLAN.md updated
- No TODOs
- No print statements
- No commented code

---

# Protected Branch Rules

For

main

- No direct push
- No force push
- PR required
- CI required
- Review required

For

develop

- PR required
- CI required
- At least one approval

---

# Git Aliases (Recommended)

```

git config --global alias.st status

git config --global alias.co checkout

git config --global alias.br branch

git config --global alias.cm commit

git config --global alias.lg "log --graph --oneline --decorate"

git config --global alias.last "log -1 HEAD"

```

---

# Definition of Done (Git)

A ticket is considered complete only when:

- Feature branch created from `develop`
- Commits follow Conventional Commits
- Branch rebased with latest `develop`
- All CI checks pass
- Pull Request approved
- Squash merged into `develop`
- Feature branch deleted
- Ticket status updated
- `PLAN.md` updated
- Release notes updated if user-facing behavior changed

---

# Golden Rules

1. Never commit directly to `main`.
2. Never force push shared branches.
3. One ticket = one feature branch.
4. One Pull Request should address one logical feature or fix.
5. Keep commits small and meaningful.
6. Rebase before requesting review.
7. Ensure the repository is always in a buildable state.
8. Treat Git history as a permanent project record—write commits that explain *why* the change exists, not just *what* changed.