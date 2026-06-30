# MarketMind

## Overview

MarketMind is an AI-powered pricing intelligence platform that helps businesses understand where their products are listed across the internet, identify equivalent products, and generate pricing recommendations.

This repository contains the backend service responsible for:

- Conversational product collection
- Product extraction using LLMs
- Marketplace discovery
- Product matching
- Pricing intelligence
- REST APIs
- Background workers

The goal is to build a production-quality backend that is scalable, maintainable, observable, and easily extensible.

---

# Core Principles

This project values:

1. Clean Architecture
2. Domain Driven Design
3. SOLID Principles
4. Type Safety
5. Testability
6. Small Pull Requests
7. Production Ready Code

Never sacrifice maintainability for speed.

---

# Architecture

The project follows Hexagonal Architecture.

```
app/

    api/
    domain/
    application/
    infrastructure/
    workers/
    shared/
```

Dependencies must always point inward.

Infrastructure should never leak into the domain.

Business logic belongs inside domain/application.

---

# Coding Standards

Always:

- use type hints
- use async/await
- use Pydantic v2
- use SQLAlchemy 2.x
- keep functions under ~40 lines where practical
- keep classes focused
- prefer composition over inheritance
- avoid global state
- write self-documenting code

Avoid:

- God classes
- circular imports
- duplicated logic
- hardcoded prompts
- magic strings
- huge service files

---

# Project Workflow

Before implementing any feature:

1. Understand the ticket.
2. Understand dependencies.
3. Produce a short implementation plan.
4. Implement.
5. Add tests.
6. Self review.
7. Update PLAN.md.

---

# Ticket Rules

Every implementation should correspond to one ticket.

Never implement multiple unrelated tickets together.

Each PR should ideally close one ticket.

---

# AI Guidelines

LLMs are adapters.

Business logic must NEVER depend directly on Claude/OpenAI.

Always expose an interface like:

```

LLMProvider

```

Implementations:

- ClaudeProvider
- OpenAIProvider

Prompts must be stored separately.

Prompt templates should never be embedded inside business logic.

---

# Error Handling

Never swallow exceptions.

Always:

- log
- raise meaningful exceptions
- return typed errors

---

# Logging

Every request should contain:

- request id
- conversation id
- execution time

Background workers must log:

- start
- finish
- retries
- failures

---

# Database

Use:

- PostgreSQL
- pgvector
- Alembic

Never write raw SQL unless necessary.

Prefer SQLAlchemy ORM.

---

# API Standards

REST first.

Return typed responses.

Use proper HTTP status codes.

No generic dictionaries.

---

# Testing

Every ticket should include:

- unit tests
- integration tests (when applicable)

Aim for meaningful coverage.

---

# Background Jobs

Long-running operations must never block API requests.

Use Celery workers.

Examples:

- Search
- Matching
- Embedding generation
- Pricing computation

---

# Performance

Prefer:

- async IO
- batching
- caching
- pagination

Avoid N+1 queries.

---

# Documentation

Whenever a significant architectural decision is made:

Update:

- PLAN.md
- README.md (if needed)

Create and Update Global for summarizing this whole claude session

---

# When Unsure

If implementation choices are unclear:

Do not guess.

Provide:

- assumptions
- alternatives
- recommendation

before implementing.

---

# Definition of Done

A ticket is complete only if:

- Code compiles
- Tests pass
- Lint passes
- Types pass
- Documentation updated
- PLAN.md updated
