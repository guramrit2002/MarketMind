# Coding Standards

> Version: 1.0
> Last Updated: June 2026

---

# Purpose

This document defines the coding standards for MarketMind.

The primary goals are:

- Maintainability
- Readability
- Consistency
- Scalability
- Testability

Every contributor is expected to follow these standards.

---

# Guiding Principles

Code should be:

- Easy to read
- Easy to modify
- Easy to test
- Easy to review
- Easy to debug

Always optimize for maintainability over cleverness.

---

# General Principles

## Follow SOLID

Every feature should follow SOLID principles.

Especially:

- Single Responsibility Principle
- Dependency Inversion Principle

---

## Keep Code Boring

Prefer readable code over clever code.

Avoid unnecessary abstractions.

If someone cannot understand the code within a few minutes,
it is probably too complicated.

---

## Explicit is Better than Implicit

Bad

```python
x = f(a)
```

Good

```python
product_matches = product_match_service.find_matches(product)
```

---

## Small Functions

Functions should generally stay below:

40 lines

Large functions usually indicate multiple responsibilities.

---

## Small Classes

Classes should have one responsibility.

Avoid service classes with thousands of lines.

---

# Naming Conventions

## Variables

Use descriptive names.

Good

```python
conversation
product
matched_listing
confidence_score
```

Bad

```python
obj
tmp
x
data1
```

---

## Boolean Variables

Always start with

```python
is_
has_
can_
should_
```

Example

```python
is_active

has_results

can_retry

should_search
```

---

## Constants

Use uppercase.

```python
MAX_RETRIES = 3

DEFAULT_TIMEOUT = 30
```

---

## Classes

PascalCase

```python
ConversationService

ProductRepository

SearchProvider

PricingEngine
```

---

## Functions

snake_case

```python
create_conversation()

generate_embeddings()

calculate_average_price()
```

---

## Files

snake_case

Good

```
conversation_service.py

pricing_engine.py

product_repository.py
```

---

# Folder Structure

Every domain should contain

```
domain/

entities/

repositories/

services/

exceptions/
```

Infrastructure should never appear inside domain.

---

# Import Order

Always

```python
# Standard Library

import uuid

from datetime import datetime



# Third Party

from fastapi import APIRouter

from sqlalchemy import select



# Local

from app.domain.product import Product
```

Use Ruff to enforce.

---

# Type Hints

Mandatory.

Never omit type hints.

Bad

```python
def create(product):
```

Good

```python
def create(product: Product) -> Product:
```

---

# Docstrings

Public functions require docstrings.

Example

```python
def calculate_average_price(prices: list[float]) -> float:
    """
    Calculate the arithmetic mean of product prices.

    Args:
        prices: List of prices.

    Returns:
        Average price.
    """
```

---

# Comments

Comments explain WHY.

Not WHAT.

Bad

```python
# increment i

i += 1
```

Good

```python
# Skip duplicate marketplace entries.

continue
```

---

# Error Handling

Never

```python
except:
```

Always

```python
except ValidationError as exc:
```

Never ignore exceptions.

Never swallow errors.

Always log.

---

# Logging

Never

```python
print()
```

Use

```python
logger.info()

logger.warning()

logger.error()

logger.exception()
```

Every log should provide context.

Example

```python
logger.info(
    "Product extracted",
    conversation_id=conversation.id,
    product_id=product.id,
)
```

---

# Async Standards

Database

External APIs

LLM Calls

Redis

must all be async.

Never block the event loop.

Avoid

```python
requests.get()
```

Use

```python
httpx.AsyncClient
```

---

# API Standards

Return typed responses.

Never

```python
return {"success": True}
```

Instead

```python
return ConversationResponse(...)
```

---

# Pydantic

Separate

Request models

Response models

Internal models

Never reuse request models as database models.

---

# SQLAlchemy

Always use ORM.

Avoid raw SQL.

Prefer

```python
select(Product)
```

over

```python
SELECT * FROM product
```

---

# Database Transactions

Keep transactions small.

Never perform

LLM calls

HTTP requests

inside transactions.

---

# Dependency Injection

Always depend on interfaces.

Never

```python
ClaudeProvider()
```

inside business logic.

Instead

```python
LLMProvider
```

---

# Repository Pattern

Repositories only talk to database.

Repositories never

- call LLMs
- call APIs
- contain business logic

---

# Services

Services contain business logic.

Services should not know SQL.

---

# Domain Layer

The domain layer

must never import

- FastAPI
- SQLAlchemy ORM models
- Redis
- Celery

It should remain framework-independent.

---

# API Layer

Routes should be thin.

Controller

↓

Service

↓

Repository

Never

Controller

↓

Database

---

# Celery Tasks

Tasks should orchestrate work.

Never contain business logic.

Good

```python
product_service.process(product_id)
```

Bad

500 lines inside Celery task.

---

# LLM Standards

Never call Claude directly.

Always

```
LLMProvider

↓

ClaudeProvider

↓

OpenAIProvider
```

Prompts belong in

```
prompts/
```

Never inline prompts.

---

# Prompt Versioning

Every prompt must include

- version
- owner
- purpose

---

# Magic Values

Never

```python
if score > 0.73
```

Use

```python
MATCH_THRESHOLD = 0.73
```

---

# Configuration

Never hardcode

URLs

Keys

Timeouts

Model Names

Everything belongs in Settings.

---

# Testing

Every new feature requires

Unit Test

Integration Test (if applicable)

Never merge untested code.

---

# File Length

Recommended limits

| Item | Limit |
|------|-------|
| Function | 40 lines |
| Class | 300 lines |
| File | 500 lines |

Split files when necessary.

---

# Cyclomatic Complexity

Avoid deeply nested code.

Instead of

```python
if:
    if:
        if:
            if:
```

Return early.

---

# Early Return

Preferred

```python
if not product:
    return

process(product)
```

instead of

```python
if product:

    process(product)
```

---

# Enums

Use Enum

instead of

magic strings.

Bad

```python
status = "completed"
```

Good

```python
ConversationStatus.COMPLETED
```

---

# UUID

Never expose integer IDs.

Use UUIDs.

---

# Time

Always store timestamps in UTC.

---

# Pagination

Every listing endpoint

must support

- limit
- offset
- sorting

---

# API Versioning

Prefix all APIs

```
/api/v1/
```

---

# Security

Never trust

LLM output

User input

External APIs

Always validate.

---

# Performance

Avoid

N+1 queries.

Use

- selectinload
- joinedload
- batching

Cache expensive operations.

---

# Code Review Checklist

Before opening a PR ensure

- Code compiles
- Ruff passes
- MyPy passes
- Tests pass
- No debug code
- No print statements
- No TODOs
- Documentation updated

---

# Forbidden Practices

Do NOT

- Hardcode secrets
- Hardcode prompts
- Commit .env files
- Ignore exceptions
- Use wildcard imports
- Create God classes
- Duplicate logic
- Skip tests
- Merge failing builds

---

# Formatting Tools

Mandatory

- Ruff
- Black
- MyPy
- Pytest

CI must fail if any check fails.

---

# Git Commit Convention

Use Conventional Commits.

Examples

```
feat: implement conversation state machine

fix: handle missing marketplace URLs

refactor: split search service into providers

docs: update architecture

test: add pricing engine tests

chore: configure ruff
```

---

# Definition of Done

A feature is complete only when:

- Business logic implemented
- Tests added
- Documentation updated
- API documented
- Logging added
- Errors handled
- Types added
- Lint passes
- MyPy passes
- CI passes
- Code reviewed

No feature is considered complete until all of the above are satisfied.