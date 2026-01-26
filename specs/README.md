# Project Specifications

This directory contains detailed specifications for features and changes to the Spanish Vocabulary App.

## About Spec-Driven Development

Spec-driven development means writing detailed plans BEFORE writing code. Each spec answers:
- **What** are we building?
- **Why** are we building it?
- **How** will it work?
- **What** could go wrong?

## Spec Status

Specs progress through these statuses:

- **draft** - Work in progress, gathering requirements
- **ready** - Reviewed and ready to implement
- **active** - Currently being implemented
- **done** - Completed and deployed
- **cancelled** - Decided not to build

## Current Specs

| Spec | Status | Priority | Estimated Time |
|------|--------|----------|----------------|
| [PostgreSQL Migration](postgres-migration.md) | draft | High | 3-4 hours |

## How to Use Specs

### For Solo Development

1. **Before coding:** Write or update spec
2. **Review spec:** Read through, think of edge cases
3. **Start coding:** Follow the spec's implementation plan
4. **Update status:** Mark as `active` when you start
5. **Check success criteria:** Verify each checkbox
6. **Mark done:** Update status to `done` when complete

### Creating a New Spec

Copy this template:

```markdown
# Feature Name

**Status:** draft
**Author:** [Your name]
**Created:** [Date]
**Estimated Time:** [Hours]

## Context
[Why are we doing this? What's the problem?]

## Goals
[What are we trying to achieve?]

## Non-Goals
[What are we explicitly NOT doing?]

## Implementation Plan
[Step-by-step how to build this]

## Edge Cases
[What could go wrong? How to handle it?]

## Testing Plan
[How to verify it works?]

## Success Criteria
- [ ] Checklist of requirements
- [ ] Each must be completed
- [ ] To mark spec as done

## Dependencies
[What must be done first?]

## References
[Links to docs, related specs, etc.]
```

## Benefits of Specs

**Clarity:** Everyone knows what's being built
**Speed:** Less time debugging, more time coding
**Quality:** Think through edge cases before coding
**Documentation:** Specs become permanent records

## Related Documents

- [Constitution](.speckit/constitution.md) - Project standards and practices
- [README](../README.md) - Project overview and setup
