"""Trov services — business logic layer.

Each service handles a domain:
- ratings: structured, immutable rating system (the moat)
- matching: hybrid search (pgvector + structured filters)
- profiles: candidate profile CRUD + embedding
- alerts: saved search alerts
- stats: kill-criteria metrics
- users: user management
"""
