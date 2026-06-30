# MarketMind Architecture

> Version: 1.0
> Status: Planning
> Architecture Style: Hexagonal Architecture + Domain Driven Design + Event Driven Workflow

---

# 1. Vision

MarketMind is an AI-powered pricing intelligence platform that enables businesses to:

- Describe their product conversationally.
- Extract structured product information using an LLM.
- Search the internet for equivalent products.
- Match products using semantic search and AI reasoning.
- Generate pricing intelligence and recommendations.

The system is designed to be:

- Modular
- Scalable
- Observable
- Testable
- Provider Agnostic
- Production Ready

---

# 2. High Level Architecture

```

```
                    ┌──────────────────┐
                    │    React / Next  │
                    └─────────┬────────┘
                              │
                              │ REST + WebSocket
                              │
                    ┌─────────▼─────────┐
                    │     FastAPI       │
                    └─────────┬─────────┘
                              │
          ┌───────────────────┼────────────────────┐
          │                   │                    │
          ▼                   ▼                    ▼
 Conversation          Product Domain        Search Domain
 Service               Service               Service

          │                   │                    │
          └──────────────┬────┴──────────────┬─────┘
                         ▼                   ▼
                  Matching Engine     Pricing Engine

                         │
                         ▼
                   Celery Workers

                         │
             ┌───────────┼────────────┐
             ▼           ▼            ▼
        PostgreSQL     Redis      LLM Provider
        + pgvector                 (Claude)

```

```

---

# 3. Architecture Principles

The project follows:

- Hexagonal Architecture
- Domain Driven Design
- SOLID Principles
- Repository Pattern
- Dependency Injection
- Event Driven Workflow

The Domain layer must never depend on Infrastructure.

```

Presentation

↓

Application

↓

Domain

↓

Infrastructure

```

Dependencies always point inward.

---

# 4. Folder Structure

```

app/

api/
routes/
schemas/

application/
services/
handlers/
events/

domain/
entities/
repositories/
value_objects/

infrastructure/
database/
repositories/
llm/
search/
cache/

workers/

shared/
config/
exceptions/
logging/
utils/

```

---

# 5. Domains

## Conversation Domain

Responsible for:

- Chat sessions
- Message history
- State transitions
- Clarification questions

Owns:

- Conversation
- Message
- ConversationState

---

## Product Domain

Responsible for:

- Product entity
- Product validation
- Draft products
- Confirmed products

Owns:

- Product
- ProductAttribute

---

## Search Domain

Responsible for:

- Search providers
- Query generation
- Marketplace discovery
- Listing normalization

Owns:

- Listing
- Marketplace
- SearchResult

---

## Matching Domain

Responsible for:

- Embeddings
- Semantic similarity
- AI verification
- Confidence scoring

Owns:

- Match
- MatchReason

---

## Pricing Domain

Responsible for:

- Price aggregation
- Lowest price
- Highest price
- Average price
- Recommendations

Owns:

- PricingReport

---

# 6. Database

Main Database

PostgreSQL

Extensions

- pgvector

Tables

Conversation

Message

Product

Listing

Match

PricingReport

Embedding

AuditLog

---

# 7. Event Flow

The system communicates internally using domain events.

Example:

```

Conversation Finished

↓

Product Extracted

↓

Product Confirmed

↓

Search Requested

↓

Listings Discovered

↓

Embeddings Generated

↓

Products Matched

↓

Pricing Calculated

↓

Report Generated

```

Events should be immutable.

---

# 8. AI Pipeline

```

Conversation

↓

LLM Product Extraction

↓

Missing Field Detection

↓

Clarification Questions

↓

Updated Product

↓

Confirmation

↓

Search

↓

Embedding Generation

↓

Vector Search

↓

LLM Match Verification

↓

Pricing Intelligence

```

The LLM should never be called directly from business logic.

Always use

```

LLMProvider

```

---

# 9. Search Pipeline

```

Product

↓

Query Builder

↓

Search Provider

↓

Results

↓

Normalization

↓

Listing Repository

```

Search Providers must implement:

```

SearchProvider

```

Example:

```

SERPAPIProvider

GoogleProvider

```

---

# 10. Matching Pipeline

```

Listing

↓

Keyword Filter

↓

Embedding

↓

pgvector Search

↓

Top K Candidates

↓

LLM Verification

↓

Confidence Score

↓

Persist Match

```

---

# 11. Pricing Pipeline

```

Matched Products

↓

Extract Prices

↓

Outlier Removal

↓

Statistics

↓

Recommendation Engine

↓

Pricing Report

```

---

# 12. Background Jobs

All expensive operations are asynchronous.

Workers include:

- Search Worker
- Embedding Worker
- Matching Worker
- Pricing Worker

API should never wait for these jobs.

---

# 13. API Design

REST First

```

POST /conversations

POST /messages

GET /products/{id}

GET /listings/{id}

GET /pricing/{id}

```

Responses use Pydantic models.

No raw dictionaries.

---

# 14. WebSocket

WebSocket is used for:

- Chat streaming
- Progress updates
- Worker status

Typical flow

```

Connected

↓

Processing

↓

Searching

↓

Matching

↓

Pricing

↓

Completed

```

---

# 15. Error Handling

Every layer returns typed exceptions.

Infrastructure Exceptions

↓

Application Exceptions

↓

HTTP Exceptions

Never expose stack traces.

---

# 16. Logging

Every request should contain

- Request ID
- Conversation ID
- Execution Time

Workers log

- Started
- Completed
- Failed
- Retry Count

---

# 17. Security

Validate

- Input
- LLM Output
- Database Writes

Never trust external APIs.

Never trust LLM responses.

---

# 18. Testing Strategy

Unit Tests

Domain logic only.

Integration Tests

Repositories

API

Workers

End-to-End Tests

Entire pipeline

Conversation

↓

Extraction

↓

Search

↓

Matching

↓

Pricing

---

# 19. Performance Goals

Target

API latency

< 300 ms (excluding async jobs)

Search

Background

Matching

Background

Pricing

Background

Use

- Async IO
- Redis Cache
- Connection Pooling
- Batch Processing

---

# 20. Future Extensions

Potential additions

- Authentication
- Organizations
- User Roles
- Price History
- Scheduled Monitoring
- Competitor Tracking
- Email Reports
- Marketplace-specific adapters
- Analytics Dashboard
- Multi-language support

---

# 21. Architecture Decision Records (ADRs)

Major architectural decisions should be documented in `DECISIONS.md`.

Examples:

- Why Hexagonal Architecture?
- Why PostgreSQL over MongoDB?
- Why pgvector instead of Pinecone?
- Why Celery over Temporal?
- Why FastAPI instead of Django?

---

# 22. Definition of Architecture Done

A feature is architecturally complete when:

- Domain model is defined.
- Interfaces are implemented.
- Infrastructure is isolated.
- Tests are added.
- Events are documented.
- API is documented.
- PLAN.md is updated.