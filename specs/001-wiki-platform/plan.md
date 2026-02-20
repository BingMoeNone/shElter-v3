# Implementation Plan: Wiki Platform

**Branch**: `001-wiki-platform` | **Date**: 2026-02-17 | **Spec**: [link](./spec.md)
**Input**: Feature specification from `/specs/001-wiki-platform/spec.md`

## Summary

Implementation of a wiki platform with Vue 3 + TypeScript frontend, FastAPI backend, and PostgreSQL database. The system will support article creation/publishing, user profiles, social connections, and content discovery. All components will include upgrade interfaces to support future technology migrations.

**Current Status**: v3.1.0 - Security Enhanced Version

### Recent Updates (v3.1.0 - 2026-02-17)
- Upgraded JWT from HS256 to RS256 encryption
- Added Rate Limiting (slowapi)
- Added unified response format
- Added security headers middleware
- Added upgrade guide documentation

## Technical Context

**Language/Version**: Vue 3 + TypeScript 5.x (frontend), Python 3.11+ (backend)
**Primary Dependencies**: Vue 3 + TypeScript for frontend, FastAPI for backend, PostgreSQL for storage
**Storage**: PostgreSQL 15+ with support for JSON fields for flexible data modeling
**Testing**: Vitest + Vue Test Utils for frontend, pytest for backend, Playwright for E2E tests
**Target Platform**: Web application (responsive design for desktop and mobile browsers)
**Project Type**: Web application with separate frontend and backend projects
**Performance Goals**: Support 10,000+ articles with search results under 2 seconds, handle 1000 concurrent users
**Constraints**: Real-time collaborative editing support, responsive UI, SEO-friendly content delivery
**Scale/Scope**: Target 10,000+ articles, 50,000+ registered users, 99.9% uptime

## Security Architecture

### Authentication Flow
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   FastAPI   │────▶│  Database   │
│  (Vue 3)    │◀────│  Backend    │◀────│(PostgreSQL) │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                    │
       │  1. Login         │                    │
       │──────────────────▶│                    │
       │                   │  2. Validate      │
       │                   │──────────────────▶│
       │                   │◀──────────────────│
       │                   │                    │
       │  3. JWT (RS256)   │                    │
       │◀──────────────────│                    │
       │                   │                    │
       │  4. Access API    │                    │
       │──────────────────▶│                    │
```

### Rate Limiting Strategy
| Endpoint | Limit | Purpose |
|----------|-------|---------|
| `/auth/login` | 10/min | Prevent brute force |
| `/auth/register` | 5/min | Prevent spam |
| `/auth/refresh` | 10/min | Token refresh |
| Other API | 60/min | General protection |

### Security Headers
All responses include:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000`
- `Referrer-Policy: strict-origin-when-cross-origin`

## Constitution Check

### Pre-Design Verification:
- [x] Specification-first development approach followed and documented (spec.md complete)
- [x] Template-driven architecture principles applied consistently (using plan template)
- [x] Automated workflow integration planned for all features (PowerShell scripts included)
- [x] Test-driven development approach incorporated in plan (Vitest, pytest, Playwright included)
- [x] Agent-centric design considerations addressed (Speckit agents used for planning)
- [x] Development standards compliance verified (TypeScript, consistent naming planned)
- [x] Quality assurance requirements defined and achievable (unit, integration, E2E tests planned)

### Post-Design Verification:
- [x] Data models align with specification requirements (data-model.md complete)
- [x] API contracts support all functional requirements (contracts/api.yaml complete)
- [x] Upgrade interfaces implemented at key technology points
- [x] Architecture supports performance goals from spec
- [x] Security and privacy requirements addressed in design
- [x] Security requirements from constitution met (RS256, Rate Limiting, Headers)

## Project Structure

### Documentation (this feature)

```
specs/001-wiki-platform/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
├── tasks.md             # Phase 2 output
├── STATUS.md            # Project status
└── spec.md              # Feature specification
```

### Source Code (repository root)

```
shElter-v3/
├── backend/
│   ├── src/
│   │   ├── api/              # API route definitions
│   │   ├── auth/             # JWT authentication (RS256)
│   │   ├── core/             # Core modules
│   │   │   ├── response.py   # Unified response format
│   │   │   └── security.py   # Rate limiter
│   │   ├── models/           # SQLAlchemy ORM models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── utils/            # Utilities
│   │   └── main.py           # Application entry
│   ├── keys/                 # RSA keys (RS256)
│   ├── alembic/              # Database migrations
│   ├── tests/                # Tests
│   ├── requirements.txt      # Python dependencies
│   ├── generate_keys.py      # RSA key generator
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Vue components
│   │   ├── views/            # Page views
│   │   ├── services/         # API services
│   │   ├── stores/           # Pinia stores
│   │   ├── router/           # Vue Router
│   │   └── App.vue
│   ├── package.json
│   └── Dockerfile
│
├── specs/                    # Specification documents
├── UPGRADE_GUIDE.md         # Security upgrade guide
├── SECURITY_AUDIT_REPORT.md # Security audit
└── docker-compose.yml       # Orchestration
```

**Structure Decision**: Web application with separate frontend (Vue 3 + TS) and backend (FastAPI) projects to enable independent scaling and development. Frontend communicates with backend via REST API. Both include upgrade interfaces to support future technology migrations.

## Complexity Tracking

| Complexity | Justification |
|------------|---------------|
| Separate projects | Scalability and team specialization |
| RSA encryption | Enhanced security (vs HS256) |
| Rate limiting | Security compliance |
| Upgrade interfaces | Future technology migration |

## Security Implementation Details

### JWT RS256 Upgrade
- Generated RSA-2048 key pair
- Private key: `backend/keys/private_key.pem`
- Public key: `backend/keys/public_key.pem`
- Key generation: `python generate_keys.py`

### Unified Response Format
```python
{
    "data": {...},
    "message": "操作成功",
    "status": 200,
    "timestamp": "2026-02-17T10:00:00Z",
    "error_code": None
}
```

### API Response Time Targets
- Authentication: < 200ms
- Article CRUD: < 300ms
- Search: < 500ms
- File Upload: < 2s

## Dependencies

### Backend (v3.1.0)
| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.109.0 | Web framework |
| sqlalchemy | 2.0.25 | ORM |
| python-jose | 3.3.0 | JWT (RS256) |
| slowapi | 0.1.9 | Rate limiting |
| bcrypt | 4.x | Password hashing |
| alembic | 1.13.1 | Migrations |

### Frontend
| Package | Version | Purpose |
|---------|---------|---------|
| vue | 3.x | UI framework |
| pinia | 2.x | State management |
| vue-router | 4.x | Routing |
| axios | 1.x | HTTP client |
| typescript | 5.x | Type safety |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release |
| 3.0.0 | 2026-02-15 | v3 integration |
| 3.1.0 | 2026-02-17 | Security enhancements (RS256, Rate Limiting) |

## Next Steps

1. Run `python generate_keys.py` to generate RSA keys
2. Update `.env` with RS256 configuration
3. Run `pip install -r requirements.txt`
4. Run database migrations
5. Start services with `docker-compose up`

**Plan Version**: 3.1.0 | **Last Updated**: 2026-02-17
