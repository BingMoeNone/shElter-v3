<!-- SYNC IMPACT REPORT

Version change: 1.0.0 ?1.1.0

Modified principles: Core Principles, Development Standards

Added sections: Security Requirements, Upgrade Path Compliance

Removed sections: None

Templates requiring updates: spec.md, plan.md

Follow-up TODOs: Update security audit documentation

-->



# shElter-v3 Constitution



## Core Principles



### I. Specification-First Development

All development begins with a clear, detailed specification that defines the problem, requirements, and acceptance criteria before any implementation work begins. Specifications must be reviewed and approved by stakeholders before implementation proceeds.



### II. Template-Driven Architecture

Leverage standardized templates for all project components including plans, specs, tasks, and agent configurations. Templates ensure consistency, reduce boilerplate, and maintain architectural integrity across the codebase.



### III. Automated Workflow Integration

Every feature and process must integrate with automated workflows using PowerShell scripts and command-line interfaces. Automation reduces manual errors, ensures consistency, and enables scalable development practices.



### IV. Test-Driven Development (NON-NEGOTIABLE)

TDD is mandatory: Specifications and tests are written first, validated to fail appropriately, then implementation follows. The Red-Green-Refactor cycle is strictly enforced to ensure code quality and correctness.



### V. Agent-Centric Design

Design systems with intelligent agents that can handle specific responsibilities (analysis, planning, implementation, etc.) through well-defined interfaces and clear separation of concerns.



### VI. Security-First Development

Security is not an afterthought - all features must be designed with security considerations from the start. This includes:

- Authentication and authorization by default

- Input validation and sanitization

- Rate limiting on public endpoints

- HTTPS only in production

- Regular security audits



## Security Requirements



### Authentication

- JWT-based authentication with RS256 encryption

- Access tokens + Refresh token pattern

- Token expiration: Access 30min, Refresh 7-30 days

- Secure cookie storage (HttpOnly, Secure, SameSite)



### Authorization

- Role-Based Access Control (RBAC)

- Role hierarchy: admin > moderator > user > guest

- Permission checks on all protected endpoints



### Rate Limiting

- Login: 10 requests/minute

- Register: 5 requests/minute

- Token refresh: 10 requests/minute

- General API: 60 requests/minute



### Security Headers

All responses must include:

- X-Content-Type-Options: nosniff

- X-Frame-Options: DENY

- X-XSS-Protection: 1; mode=block

- Strict-Transport-Security: max-age=31536000

- Referrer-Policy: strict-origin-when-cross-origin



### Data Protection

- Passwords: bcrypt hashing (cost factor 12+)

- Sensitive data: encrypted at rest

- API responses: no sensitive data leakage



## Development Standards



All code must follow consistent formatting and naming conventions. Documentation is required for all public interfaces and complex logic. Code reviews must verify compliance with all constitutional principles before merge approval.



### Virtual Environment Management



- **Python**: Use `uv` as the primary virtual environment and dependency manager

- **Command Usage**: 

  - Install dependencies: `uv pip install -r requirements.txt`

  - Run development server: `uv run python -m uvicorn src.main:app --reload`

  - Run commands: `uv run <command>`



### Code Quality Standards

| Category | Requirement |

|----------|-------------|

| TypeScript | Strict mode enabled, no `any` |

| Python | Type hints, PEP 8 compliance |

| Vue 3 | Composition API, TypeScript |

| API | OpenAPI 3.0 specification |



### File Naming Conventions

| Type | Convention | Example |

|------|------------|---------|

| Components | PascalCase | `UserProfile.vue` |

| API Routes | snake_case | `user_auth.py` |

| Models | PascalCase | `UserModel.py` |

| Tests | snake_case | `test_user_auth.py` |



### Documentation Requirements

- All public functions: docstring

- API endpoints: OpenAPI annotations

- Complex logic: inline comments

- Security-sensitive code: security notes



## Quality Assurance



Continuous integration pipeline validates all changes against specifications. Automated testing at unit, integration, and end-to-end levels ensures system reliability. Performance benchmarks are maintained and monitored for all critical paths.



### Testing Requirements

| Level | Coverage Target | Tools |

|-------|-----------------|-------|

| Unit | 80%+ | pytest, Vitest |

| Integration | 60%+ | pytest, Vitest |

| E2E | Critical paths | Playwright |



### Performance Standards

| Metric | Target |

|--------|--------|

| API Response | < 200ms (p95) |

| Page Load | < 2s |

| Search | < 500ms |

| Build Time | < 60s |



## Governance



This constitution supersedes all other development practices. Amendments require formal documentation, team approval, and migration planning. All pull requests and code reviews must verify constitutional compliance. Complexity must be justified with clear benefits outweighing maintenance costs. Use the Speckit framework guidance for runtime development decisions.



## Upgrade Path Compliance



When implementing changes that affect security, architecture, or core functionality:



1. **Security Updates** (MANDATORY)

   - Update UPGRADE_GUIDE.md

   - Document breaking changes

   - Provide rollback instructions



2. **Architecture Changes**

   - Update data-model.md

   - Update API contracts

   - Update plan.md



3. **Feature Changes**

   - Update spec.md

   - Update tasks.md

   - Update STATUS.md



## Version Information



**Version**: 1.1.0 | **Ratified**: 2026-02-12 | **Last Amended**: 2026-02-17



### Version History

| Version | Date | Changes |

|---------|------|---------|

| 1.0.0 | 2026-02-12 | Initial constitution |

| 1.1.0 | 2026-02-17 | Added security requirements, upgrade path compliance |

