# HumanEnerDIA Documentation

This index points to the main HumanEnerDIA documentation for users, operators,
developers, integrators, and release reviewers.

## Start Here

| Need | Read |
|---|---|
| Understand what users can do in the portal | [Business User Guide](./BUSINESS_USER_GUIDE.md) |
| Understand the system architecture | [Technical Architecture Guide](./TECHNICAL_ARCHITECTURE_GUIDE.md) |
| Run and troubleshoot the deployment | [Operations Runbook](./OPERATIONS_RUNBOOK.md) |
| Understand KPIs and calculations | [KPI Reference](./KPI_REFERENCE.md) |
| Understand database tables and aggregates | [Database Schema Reference](./DATABASE_SCHEMA_REFERENCE.md) |
| Check release and delivery status | [Delivery Readiness](./DELIVERY_READINESS.md) |
| Integrate OVOS with the backend API | [ENMS API Documentation for OVOS](./api-documentation/ENMS-API-DOCUMENTATION-FOR-OVOS.md) |
| Package or publish WASABI shop products | [WASABI Shop Docs](./wasabi-shop/) |

## Documentation by Audience

Business and operational users:

- [Business User Guide](./BUSINESS_USER_GUIDE.md)
- [KPI Reference](./KPI_REFERENCE.md)

Technical operators:

- [Operations Runbook](./OPERATIONS_RUNBOOK.md)
- [Technical Architecture Guide](./TECHNICAL_ARCHITECTURE_GUIDE.md)
- [Database Schema Reference](./DATABASE_SCHEMA_REFERENCE.md)

Developers and integrators:

- [Technical Architecture Guide](./TECHNICAL_ARCHITECTURE_GUIDE.md)
- [ENMS API Documentation for OVOS](./api-documentation/ENMS-API-DOCUMENTATION-FOR-OVOS.md)
- [Database Schema Reference](./DATABASE_SCHEMA_REFERENCE.md)

Release and delivery:

- [Delivery Readiness](./DELIVERY_READINESS.md)
- [Documentation Plan](./DOCUMENTATION_PLAN.md)
- [WASABI Release Runbook](./wasabi-shop/HUMANERDIA_WASABI_RELEASE_RUNBOOK.md)
- [Full Stack Installation](./wasabi-shop/HUMANERDIA_FULL_STACK_INSTALLATION.md)

## Important Current Notes

- `query-service` is currently a placeholder and is excluded from release
  readiness expectations.
- `.env` must never be committed.
- The base HumanEnerDIA stack and the companion OVOS stack are distributed as
  separate clean production repositories/artifacts.
- Screenshot placeholders are intentionally left in new docs until final clean
  UI screenshots are captured.

## Screenshot Placeholder Paths

Use these folders for final documentation screenshots:

```text
docs/images/architecture/
docs/images/operations/
docs/images/user-guide/
docs/images/release/
```
