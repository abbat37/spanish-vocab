# Version Management Implementation Roadmap

**Goal:** Build a production-grade multi-version Flask application with v1 (existing) and v2 (new AI-powered learning flow)

---

## Overview

This roadmap guides you through implementing version management for your Spanish vocabulary app, following patterns used by Stripe, GitHub, and Shopify.

### What You'll Learn
- Version management and API versioning patterns
- Flask Blueprint architecture for scalability
- Database schema evolution and migrations
- LLM integration in production (Claude via Portkey)
- Gradual user migration strategies
- Shared infrastructure patterns

### Timeline
Each phase is designed to be completed in 1-3 development sessions. Total: ~2-3 weeks of learning-focused development.

---

## Current Status

**Completed Phases:** 0, 1, 2, 3, 4 (5 of 8 phases complete)

**Phase 4 Highlights:**
- Implemented bulk word entry with LLM processing
- Used GPT-4o-mini instead of GPT-4o for ~75% cost savings
- Added word normalization (lowercase, singular, masculine forms)
- Implemented 30s timeouts on all API calls
- Two-layer validation system working as designed
- Flash message UX improvements with persistent messages

**Next Up:** Phase 5 - V2 Features Implementation (Create, Study, Revise pages)

---

## Architecture at a Glance

### URL Structure (Final)
```
spanish-vocab.duckdns.org/
├── /                           # → Redirects to /v1/
├── /login                      # Shared auth
├── /register                   # Shared auth
├── /logout                     # Shared auth
├── /v1/                        # Current app
│   ├── /v1/                    # Practice page
│   └── /v1/api/mark-learned    # API
└── /v2/                        # New AI-powered flow
    ├── /v2/dashboard           # Shared dashboard
    ├── /v2/create              # Build word database
    ├── /v2/study               # Flashcard study
    ├── /v2/revise              # AI-powered practice
    └── /v2/api/*               # v2 APIs
```

### Code Structure (Final)
```
app/
├── shared/                     # Shared across versions
│   ├── extensions.py           # db, auth, limiter
│   └── models/user.py          # Shared user model
├── v1/                         # Isolated v1 code
│   ├── models/, routes/, services/
│   └── templates/
├── v2/                         # Isolated v2 code
│   ├── models/, routes/, services/
│   └── templates/
└── routes/auth.py              # Shared auth routes
```

---

## Phases

### ✅ Phase 0: Planning
- [x] Define requirements and architecture
- [x] Choose version management strategy
- [x] Answer design questions
- [x] Create detailed specs

**Status:** COMPLETE

---

### ✅ Phase 1: Restructure for Versioning
**Status:** COMPLETED
**Spec:** [phase-1-version-restructure.md](phase-1-version-restructure.md)
**Completed:** 2026-02-10
**Duration:** 1 session

#### Goals
- Restructure existing app into versioned architecture
- Move current functionality to `/v1/*` URLs
- Extract shared code (auth, db) to `app/shared/`
- Create v2 placeholder at `/v2/*`
- Add version switcher navbar

#### Deliverables
- [x] V1 works at `/v1/*` with all existing features
- [x] Auth routes at root (`/login`, `/register`, `/logout`)
- [x] Root URL redirects to `/v1/`
- [x] V2 placeholder page at `/v2/`
- [x] Version switcher in navbar
- [x] All tests passing
- [x] Production deployment successful

#### Key Files Created/Modified
- Created: `app/shared/extensions.py`
- Created: `app/v1/__init__.py` (blueprint factory)
- Created: `app/v2/__init__.py` (placeholder)
- Created: `app/templates/base.html` (shared navbar)
- Modified: `app/__init__.py` (register versioned blueprints)
- Moved: All existing code to `app/v1/`

#### Learning Focus
- Flask Blueprint URL prefixing
- Shared infrastructure pattern
- Safe code refactoring

---

### ✅ Phase 2: Build V2 Scaffold
**Status:** COMPLETED
**Spec:** [phase-2-v2-scaffold.md](phase-2-v2-scaffold.md)
**Completed:** 2026-02-10
**Duration:** 1 session

#### Goals
- Set up v2 route structure (create, study, revise)
- Create basic v2 templates (HTML only, no functionality)
- Wire up navigation between v1 and v2
- Make dashboard accessible from both versions

#### Deliverables
- [x] V2 routes with placeholder content
- [x] Basic HTML templates for create/study/revise
- [x] Dashboard shows combined stats (v1 + v2)
- [x] Navigation works smoothly
- [x] Tailwind CSS styling implemented
- [x] Mobile-responsive design

#### Learning Focus
- Route organization for feature-based architecture
- Template inheritance
- Shared component design

---

### ✅ Phase 3: V2 Database Schema
**Status:** COMPLETED
**Spec:** [phase-3-v2-database-schema.md](phase-3-v2-database-schema.md)
**Completed:** 2026-02-11
**Duration:** 1 session

#### Goals
- Design v2 tables for new data model
- Create database migrations
- Test migrations locally and in production
- Understand schema evolution

#### New Tables
- `v2_words` - User's custom vocabulary
- `v2_generated_examples` - AI-generated sentences
- `v2_practice_attempts` - Practice history with AI feedback

#### Deliverables
- [x] Migration files created
- [x] V2 models implemented
- [x] Migrations tested locally
- [x] Migrations applied in production
- [x] Database backup taken
- [x] Model relationships configured
- [x] Indexes added for performance

#### Learning Focus
- Database schema evolution
- Flask-Migrate best practices
- Production migration strategies

---

### ✅ Phase 4: LLM Integration & Bulk Word Entry
**Status:** COMPLETED
**Spec:** [phase-4-llm-bulk-entry.md](phase-4-llm-bulk-entry.md)
**Completed:** 2026-02-12
**Duration:** 2 sessions

#### Goals
- Integrate OpenAI API for bulk word processing
- Implement word normalization and validation
- Add error handling and timeouts
- Build bulk entry UI with loading states

#### API Integration
- **Provider:** OpenAI GPT-4o-mini (cost-optimized alternative to GPT-4o)
- **Cost savings:** ~75% cheaper than GPT-4o
- **Word normalization:** Lowercase, singular, masculine forms
- **Timeout:** 30s explicit timeouts on all API calls
- **Validation:** Two-layer system (API + database)

#### Deliverables
- [x] OpenAI SDK configured with API keys
- [x] Environment variables for API keys
- [x] LLM service layer with bulk word processing
- [x] Word normalization (lowercase, singular, masculine)
- [x] Two-layer validation system working
- [x] Error handling with 30s timeouts
- [x] Flash message UX with persistent messages
- [x] Production checklist (8/10 items completed)

#### Learning Focus
- Production LLM integration patterns
- API error handling and retries with explicit timeouts
- Cost optimization strategies (GPT-4o-mini vs GPT-4o)
- Word normalization for language learning
- Flash message patterns for better UX

---

### 📋 Phase 5: V2 Features Implementation
**Status:** Spec needed
**Duration:** 3-4 sessions

#### Goals
Implement the three main v2 features:

##### 5.1: Create Page
- Add/edit words with Spanish/English translations
- Tag words by type (verb, noun, adj) and themes
- Pre-generate AI examples for each word
- Filter and search word database

##### 5.2: Study Page
- Show flashcards with word + AI-generated examples
- Mark words as "learned"
- Regenerate examples button (new AI generation)
- Next button for random word selection

##### 5.3: Revise Page
- Prompt user to use learned words in sentences
- AI feedback on correctness and suggestions
- Tip button (show Spanish translation)
- Track practice attempts

#### Deliverables
- [ ] Create page fully functional
- [ ] Study page fully functional
- [ ] Revise page fully functional
- [ ] All v2 APIs working
- [ ] Frontend JavaScript for interactivity
- [ ] Mobile-responsive design

#### Learning Focus
- CRUD operations with Flask
- AJAX requests with Fetch API
- AI-powered UX patterns
- State management in web apps

---

### 📋 Phase 6: Polish & Optimization
**Status:** Spec needed
**Duration:** 1-2 sessions

#### Goals
- Add comprehensive tests for v1 and v2
- Optimize LLM usage (caching, batch generation)
- Performance improvements
- Error tracking with Sentry
- Documentation updates

#### Deliverables
- [ ] Test coverage >90%
- [ ] LLM cost optimization implemented
- [ ] Performance profiling done
- [ ] Sentry alerts configured
- [ ] README updated with v2 docs
- [ ] User guide created

#### Learning Focus
- Testing strategies for versioned apps
- LLM cost optimization
- Production monitoring

---

### 📋 Phase 7: Production Launch & Gradual Migration
**Status:** Spec needed
**Duration:** 1 session

#### Goals
- Deploy v2 to production
- Monitor user adoption
- Gather feedback
- Plan v1 deprecation (if desired)

#### Launch Strategy
1. Soft launch: V2 accessible via navbar link
2. Monitor: Track usage, errors, costs
3. Iterate: Fix bugs and improve UX
4. Promote: Make v2 the default (change root redirect)
5. Sunset: Eventually deprecate v1 (optional)

#### Deliverables
- [ ] V2 live in production
- [ ] Monitoring dashboard set up
- [ ] User feedback mechanism
- [ ] Decision made on v1 deprecation

#### Learning Focus
- Gradual rollout strategies
- Production monitoring
- User adoption patterns
- Feature deprecation best practices

---

## Key Design Decisions

### 1. Version Management Strategy
**Chosen:** Path-based routing (`/v1/*` and `/v2/*`)
**Why:**
- Single codebase, single deployment
- Existing CI/CD works as-is
- Easy to test locally
- Follows Stripe/GitHub patterns

### 2. Database Strategy
**Chosen:** Shared database with new tables for v2
**Why:**
- Unified auth (one account, works for both versions)
- Easy to add cross-version features later
- Simpler infrastructure

### 3. Data Migration
**Chosen:** No migration from v1 to v2
**Why:**
- V2 is a fresh start (different learning methodology)
- Simpler implementation
- Users can still access v1 data

### 4. LLM Provider
**Chosen:** Claude via Portkey SDK
**Why:**
- You already have API key
- Portkey adds analytics and cost tracking
- Better at following structured generation prompts
- More cost-effective than GPT-4 for this use case

---

## Success Metrics

### Technical Goals
- Both versions running simultaneously in production
- <1% error rate for LLM API calls
- All tests passing with >90% coverage
- Page load times <2 seconds

### Learning Goals
- Understand version management patterns used by real companies
- Master Flask Blueprints and application factory
- Gain experience with production LLM integration
- Learn database migration strategies

### User Experience Goals
- Seamless switching between v1 and v2
- Clear communication about version differences
- No data loss or service interruption
- Smooth AI-powered learning experience

---

## Next Steps

1. **Review Phase 1 Spec:** Read [phase-1-version-restructure.md](phase-1-version-restructure.md)
2. **Ask Questions:** Clarify anything unclear before starting
3. **Create Git Branch:** `git checkout -b phase-1-version-restructure`
4. **Start Implementation:** Follow the spec step-by-step
5. **Test Thoroughly:** Use the testing checklist in the spec
6. **Deploy:** Push to main, let CI/CD deploy

---

## Resources

### Flask Documentation
- [Blueprints](https://flask.palletsprojects.com/en/2.3.x/blueprints/)
- [Application Factory](https://flask.palletsprojects.com/en/2.3.x/patterns/appfactories/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)

### Real-World Examples
- [Stripe API Versioning](https://stripe.com/docs/api/versioning)
- [GitHub API Versions](https://docs.github.com/en/rest/overview/api-versions)

### LLM Integration
- [Anthropic Claude API](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [Portkey Documentation](https://portkey.ai/docs)

---

**Questions or Need Help?**

Review the detailed spec for Phase 1, or ask for clarification on any aspect of the implementation plan.

Ready to start Phase 1? Let me know and I'll help you through each step! 🚀
