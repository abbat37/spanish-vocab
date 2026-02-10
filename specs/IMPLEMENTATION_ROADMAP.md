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

### ✅ Phase 0: Planning (Current)
- [x] Define requirements and architecture
- [x] Choose version management strategy
- [x] Answer design questions
- [x] Create detailed specs

**Status:** COMPLETE

---

### 📋 Phase 1: Restructure for Versioning
**Status:** Ready to implement
**Spec:** [phase-1-version-restructure.md](phase-1-version-restructure.md)
**Duration:** 1-2 sessions

#### Goals
- Restructure existing app into versioned architecture
- Move current functionality to `/v1/*` URLs
- Extract shared code (auth, db) to `app/shared/`
- Create v2 placeholder at `/v2/*`
- Add version switcher navbar

#### Deliverables
- [ ] V1 works at `/v1/*` with all existing features
- [ ] Auth routes at root (`/login`, `/register`, `/logout`)
- [ ] Root URL redirects to `/v1/`
- [ ] V2 placeholder page at `/v2/`
- [ ] Version switcher in navbar
- [ ] All tests passing
- [ ] Production deployment successful

#### Key Files to Create/Modify
- Create: `app/shared/extensions.py`
- Create: `app/v1/__init__.py` (blueprint factory)
- Create: `app/v2/__init__.py` (placeholder)
- Create: `app/templates/base.html` (shared navbar)
- Modify: `app/__init__.py` (register versioned blueprints)
- Move: All existing code to `app/v1/`

#### Learning Focus
- Flask Blueprint URL prefixing
- Shared infrastructure pattern
- Safe code refactoring

---

### 📋 Phase 2: Build V2 Scaffold
**Status:** Spec needed (will create after Phase 1)
**Duration:** 1 session

#### Goals
- Set up v2 route structure (create, study, revise)
- Create basic v2 templates (HTML only, no functionality)
- Wire up navigation between v1 and v2
- Make dashboard accessible from both versions

#### Deliverables
- [ ] V2 routes with placeholder content
- [ ] Basic HTML templates for create/study/revise
- [ ] Dashboard shows combined stats (v1 + v2)
- [ ] Navigation works smoothly

#### Learning Focus
- Route organization for feature-based architecture
- Template inheritance
- Shared component design

---

### 📋 Phase 3: V2 Database Schema
**Status:** Spec needed
**Duration:** 1-2 sessions

#### Goals
- Design v2 tables for new data model
- Create database migrations
- Test migrations locally and in production
- Understand schema evolution

#### New Tables
- `v2_words` - User's custom vocabulary
- `v2_generated_examples` - AI-generated sentences
- `v2_learned_words` - Learning progress
- `v2_practice_attempts` - Practice history with feedback

#### Deliverables
- [ ] Migration files created
- [ ] V2 models implemented
- [ ] Migrations tested locally
- [ ] Migrations applied in production
- [ ] Database backup taken

#### Learning Focus
- Database schema evolution
- Flask-Migrate best practices
- Production migration strategies

---

### 📋 Phase 4: LLM Integration
**Status:** Spec needed
**Duration:** 2 sessions

#### Goals
- Integrate Claude API via Portkey SDK
- Implement sentence generation
- Implement AI feedback generation
- Add error handling and rate limiting

#### API Integration
- **Provider:** Anthropic Claude (via Portkey)
- **SDK:** `portkey-ai` Python package
- **Features:** Cost tracking, rate limiting, logging, retries

#### Deliverables
- [ ] Portkey SDK installed and configured
- [ ] Environment variables for API keys
- [ ] LLM service layer implemented
- [ ] Sentence generation working (3+ sentences, 5-7 words)
- [ ] Feedback generation working
- [ ] Error handling for API failures
- [ ] Rate limiting to control costs

#### Learning Focus
- Production LLM integration patterns
- API error handling and retries
- Cost management strategies
- Prompt engineering basics

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
