# MarketMind Development Plan

## Current Status

Project Phase:

🟡 Planning

Current Milestone:

Milestone 1

---

# Milestones

## Milestone 1 — Foundation

Goal

A user can chat with the system and a structured product is extracted.

### Tickets

- [x] MM-001 Project Setup
- [ ] MM-002 Docker
- [ ] MM-003 Config
- [ ] MM-004 Database
- [ ] MM-005 Logging
- [ ] MM-006 Event Infrastructure
- [ ] MM-007 Database Schema
- [ ] MM-013 Conversation Models
- [ ] MM-014 Conversation State Machine
- [ ] MM-015 Conversation Repository
- [ ] MM-016 Conversation APIs
- [ ] MM-017 Conversation Persistence
- [ ] MM-019 LLM Interface
- [ ] MM-020 Claude Adapter
- [ ] MM-022 Response Validation
- [ ] MM-024 Product Extraction Prompt
- [ ] MM-025 Product Extraction Service
- [ ] MM-026 Missing Field Detection
- [ ] MM-027 Clarification Questions
- [ ] MM-028 Product Confirmation

Deliverable

✔ User can complete an AI conversation and receive a structured product.

---

## Milestone 2 — Discovery Pipeline

Goal

Discover products from search engines and marketplaces.

### Tickets

- [ ] MM-029 Product Domain
- [ ] MM-030 Product Repository
- [ ] MM-031 Product APIs
- [ ] MM-033 Search Interface
- [ ] MM-034 Search Provider
- [ ] MM-035 Search Normalization
- [ ] MM-036 Query Builder
- [ ] MM-038 Listing Discovery
- [ ] MM-039 Listing Storage
- [ ] MM-042 Embedding Service
- [ ] MM-043 Vector Search
- [ ] MM-044 Candidate Selection
- [ ] MM-045 Match Classification
- [ ] MM-046 Confidence Scores
- [ ] MM-047 Match Storage

Deliverable

✔ Product listings are discovered and matched.

---

## Milestone 3 — Pricing Intelligence

Goal

Generate pricing insights.

### Tickets

- [ ] MM-049 Lowest Price
- [ ] MM-050 Highest Price
- [ ] MM-051 Average Price
- [ ] MM-052 Recommendation Engine
- [ ] MM-053 Summary Generation
- [ ] MM-054 Persistence

Deliverable

✔ AI pricing report generated.

---

## Milestone 4 — Async Processing

Goal

Background processing.

### Tickets

- [ ] MM-055 Celery
- [ ] MM-056 Extraction Worker
- [ ] MM-057 Discovery Worker
- [ ] MM-058 Matching Worker
- [ ] MM-059 Intelligence Worker

Deliverable

✔ Entire pipeline executes asynchronously.

---

## Milestone 5 — Production

Goal

Deployable production system.

### Tickets

- [ ] MM-065 APIs
- [ ] MM-070 WebSockets
- [ ] MM-073 Validation
- [ ] MM-074 LLM Validation
- [ ] MM-077 Unit Tests
- [ ] MM-078 Integration Tests
- [ ] MM-079 End-to-End Tests
- [ ] MM-080 Matching Evaluation
- [ ] MM-082 CI
- [ ] MM-083 Docker Images
- [ ] MM-084 Deployment
- [ ] MM-085 Monitoring

Deliverable

✔ Production-ready MVP.

---

# Ticket Workflow

Each ticket follows:

Planning

↓

Implementation

↓

Unit Tests

↓

Integration Tests

↓

Code Review

↓

Documentation

↓

Completed

---

# Pull Request Rules

Each PR should:

- Complete one ticket
- Include tests
- Update documentation
- Be under ~500 lines where possible

---

# Definition of Done

A ticket is Done when:

- Implementation complete
- Tests passing
- Review completed
- Documentation updated
- PLAN.md updated

---

# Backlog

Future features

- Authentication
- Multi-user organizations
- Marketplace adapters
- Historical price tracking
- Email reports
- Analytics dashboard
- Multi-language support
