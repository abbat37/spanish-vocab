# PostgreSQL Migration

**Status:** active
**Author:** Developer
**Created:** 2026-01-26
**Estimated Time:** 3-4 hours

---

## 📋 Context

### Current State
- Using SQLite (file-based database) for both development and production
- SQLite stored in `instance/spanish_vocab.db`
- Works fine for single user, but has limitations

### Problem
SQLite is not production-ready because:
1. **No concurrent writes** - Only one write operation at a time (bottleneck with multiple users)
2. **File corruption risk** - If server crashes during write, database can corrupt
3. **No replication** - Can't back up or replicate data easily
4. **Limited data types** - Lacks advanced features (JSON columns, full-text search)
5. **Not scalable** - Can't distribute across multiple servers

### Solution
Migrate to PostgreSQL for production while keeping SQLite for local development.

---

## 🎯 Goals

### Primary Goals
1. **Use PostgreSQL in production** - Replace SQLite on Render
2. **Keep SQLite for development** - Fast local dev without PostgreSQL setup
3. **Zero data loss** - Preserve all existing vocabulary/template data
4. **Maintain compatibility** - Same code works with both databases

### Success Criteria
- [ ] Local development uses SQLite (`sqlite:///spanish_vocab.db`)
- [ ] Production uses PostgreSQL (from `DATABASE_URL` env var)
- [ ] All tests pass with PostgreSQL
- [ ] CI/CD pipeline tests against PostgreSQL
- [ ] Production deployment uses PostgreSQL
- [ ] Existing data migrated successfully
- [ ] No breaking changes to application code

---

## 🚫 Non-Goals

**What we're NOT doing:**
- ❌ Changing database schema (same tables/columns)
- ❌ Adding new database features
- ❌ Optimizing queries (do separately if needed)
- ❌ Using other databases (MySQL, MongoDB, etc.)
- ❌ Running PostgreSQL locally (SQLite is fine for dev)

---

## 📐 Technical Design

### Database Diagram (Current - No Changes)

```
VocabularyWord
├── id (PK)
├── theme
├── word_type
├── spanish_word
└── english_translation

SentenceTemplate
├── id (PK)
├── theme
├── word_type
├── spanish_template
└── english_template

UserSession
├── id (PK)
├── session_id (unique)
└── created_at

WordPractice
├── id (PK)
├── session_id (FK → UserSession)
├── word_id (FK → VocabularyWord)
├── theme
├── word_type
├── marked_learned
└── practiced_at
```

### Architecture Changes

**Before:**
```python
# app.py - Hardcoded SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spanish_vocab.db'
```

**After:**
```python
# app.py - Dynamic based on environment
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///spanish_vocab.db')

# Handle Render's postgres:// vs postgresql:// URL format
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
```

---

## 📝 Implementation Plan

### Phase 1: Add PostgreSQL Support

**1.1 Install PostgreSQL driver**
```bash
pip install psycopg2-binary
```
- `psycopg2-binary` is the PostgreSQL adapter for Python
- Required for SQLAlchemy to talk to PostgreSQL
- Binary version includes compiled C libraries (easier than psycopg2)

**1.2 Update requirements.txt**
Add: `psycopg2-binary==2.9.9`

**1.3 Update app.py database configuration**
```python
# Get DATABASE_URL from environment, fallback to SQLite
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///spanish_vocab.db')

# Render uses postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
```

**Why this works:**
- Local `.env` has no `DATABASE_URL` → defaults to SQLite
- Production has `DATABASE_URL` env var → uses PostgreSQL
- Same code works for both environments

---

### Phase 2: Set Up Production PostgreSQL

**2.1 Create PostgreSQL database on Render**

In Render dashboard:
1. Click "New +" → "PostgreSQL"
2. Name: `spanish-vocab-db`
3. Database: `spanish_vocab`
4. User: (auto-generated)
5. Region: Same as web service
6. Instance Type: Free

**2.2 Get connection URL**

Render provides Internal Database URL:
```
postgres://user:password@hostname/database_name
```

Example:
```
postgres://spanish_vocab_user:abc123...@dpg-xyz.oregon-postgres.render.com/spanish_vocab
```

**2.3 Connect web service to database**

In your web service environment variables:
- Variable: `DATABASE_URL`
- Value: [Internal Database URL from step 2.2]

**Why Internal URL:**
- Faster (same datacenter)
- Free (no bandwidth charges)
- More secure (not exposed to internet)

---

### Phase 3: Database Migrations with Alembic

**3.1 Install Alembic**
```bash
pip install alembic
```

**What is Alembic?**
- Database migration tool for SQLAlchemy
- Tracks schema changes over time
- Allows upgrading/downgrading database schema
- Like "Git for your database schema"

**3.2 Initialize Alembic**
```bash
alembic init migrations
```

This creates:
```
migrations/
├── versions/        # Migration scripts go here
├── env.py          # Alembic configuration
├── script.py.mako  # Template for new migrations
└── README

alembic.ini          # Alembic settings file
```

**3.3 Configure Alembic**

Edit `alembic.ini`:
```ini
# Line ~55 - Point to your database
sqlalchemy.url = sqlite:///spanish_vocab.db
```

Edit `migrations/env.py`:
```python
# Import your models
from app import app
from database import db

# Set target metadata
target_metadata = db.metadata

# Use app's database URL
config.set_main_option('sqlalchemy.url',
                       app.config['SQLALCHEMY_DATABASE_URI'])
```

**3.4 Generate initial migration**
```bash
alembic revision --autogenerate -m "Initial schema"
```

This creates a migration file that:
- Detects your current models
- Generates CREATE TABLE statements
- Can apply to empty PostgreSQL database

**3.5 Apply migration**
```bash
alembic upgrade head
```

This runs the migration to create all tables.

---

### Phase 4: Update CI/CD for PostgreSQL

**4.1 Update GitHub Actions workflow**

Add PostgreSQL service to test job:

```yaml
test:
  runs-on: ubuntu-latest

  services:
    postgres:
      image: postgres:15
      env:
        POSTGRES_PASSWORD: postgres
        POSTGRES_DB: test_db
      options: >-
        --health-cmd pg_isready
        --health-interval 10s
        --health-timeout 5s
        --health-retries 5
      ports:
        - 5432:5432

  steps:
    # ... existing steps ...

    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
      run: |
        pytest --cov=. --cov-report=term-missing -v
```

**What this does:**
- Spins up PostgreSQL 15 in Docker container
- Waits for it to be ready (health checks)
- Exposes on port 5432
- Runs tests against PostgreSQL (not SQLite)
- Catches PostgreSQL-specific issues before deployment

---

### Phase 5: Deploy to Production

**5.1 Deploy sequence**

When you push to main:
1. GitHub Actions runs tests against PostgreSQL ✓
2. Tests pass → Trigger Render deployment ✓
3. Render deploys new code with PostgreSQL support ✓
4. App connects to PostgreSQL database ✓
5. Auto-seeding runs if database empty ✓

**5.2 Verify deployment**
- Check Render logs for database connection
- Visit app URL, generate sentences
- Verify data persists across requests
- Check PostgreSQL dashboard for active connections

---

## 🧪 Testing Plan

### Unit Tests
```bash
# Test locally with SQLite (existing behavior)
pytest

# Test locally with PostgreSQL (if you want)
export DATABASE_URL=postgresql://localhost/test_db
pytest
```

### Integration Tests

**Test scenarios:**
1. **Fresh database**
   - Deploy to new PostgreSQL
   - Verify auto-seeding works
   - Generate sentences, check data persists

2. **Data persistence**
   - Mark words as learned
   - Restart app
   - Verify marked words still learned

3. **Concurrent access** (manual test)
   - Open app in 2 browser tabs
   - Both generate sentences simultaneously
   - Verify no errors

### CI/CD Tests

**Automated in GitHub Actions:**
- All unit tests run against PostgreSQL
- Tests must pass before deployment
- Catches issues before production

---

## ⚠️ Edge Cases & Error Handling

### Edge Case 1: Database Connection Fails

**Scenario:** PostgreSQL is down or URL is wrong

**Current behavior:**
```python
# App crashes on startup
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db.init_app(app)
db.create_all()  # ← Crashes here if DB down
```

**Solution:** Add connection error handling
```python
try:
    with app.app_context():
        db.create_all()
        print("✅ Database connected successfully")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("Check DATABASE_URL environment variable")
    sys.exit(1)
```

**Why this matters:**
- Fails fast with clear error message
- Prevents confusing errors later
- Easier to debug in production

---

### Edge Case 2: Render Uses Wrong URL Format

**Scenario:** Render provides `postgres://` but SQLAlchemy needs `postgresql://`

**Problem:**
```
postgres://user:pass@host/db     ← Render format
postgresql://user:pass@host/db   ← SQLAlchemy format
```

**Solution:** Already handled in implementation plan
```python
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
```

---

### Edge Case 3: Migration Fails Mid-Way

**Scenario:** Alembic migration crashes partway through

**Problem:** Database in inconsistent state

**Solution:** Alembic uses transactions
```python
# migrations/env.py
def run_migrations_online():
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            transaction_per_migration=True  # ← Each migration is atomic
        )
```

**Recovery:**
- Check migration status: `alembic current`
- Rollback if needed: `alembic downgrade -1`
- Fix issue and re-run: `alembic upgrade head`

---

### Edge Case 4: SQLite Specific Features

**Scenario:** Code uses SQLite-specific features

**Check for:**
- Date/time functions (different in PostgreSQL)
- String operations (case sensitivity differs)
- Auto-increment (works differently)

**Solution:** Use SQLAlchemy abstractions
- ✅ `func.now()` instead of `CURRENT_TIMESTAMP`
- ✅ `func.lower(column)` instead of `LOWER(column)`
- ✅ SQLAlchemy handles auto-increment

---

## 📊 Rollback Plan

### If Deployment Fails

**Immediate rollback:**
1. In Render dashboard → "Manual Deploy"
2. Select previous deployment
3. Click "Deploy"
4. App rolls back to SQLite version

**Or via Git:**
```bash
git revert HEAD
git push origin main
# CI/CD auto-deploys previous version
```

### If Data Issues

**PostgreSQL has data issues:**
- Keep SQLite backup locally
- Can export/import data if needed
- Use `pg_dump` for PostgreSQL backups

---

## 🎯 Success Metrics

### Performance Metrics

**Response time:**
- SQLite: ~50ms per request
- PostgreSQL: ~50-100ms per request (acceptable)

**Concurrent users:**
- SQLite: 1 concurrent write
- PostgreSQL: 100+ concurrent writes

### Quality Metrics

**Test coverage:**
- Maintain 70%+ coverage
- All tests pass with PostgreSQL

**Deployment:**
- Zero downtime deployment
- No manual intervention needed

---

## 📚 Dependencies

### Must Complete First
- [x] CI/CD pipeline (for testing)
- [x] Test suite (to verify migration works)
- [x] Auto-seeding (to populate new database)

### Blocks Future Work
- [ ] User authentication (needs PostgreSQL features)
- [ ] Advanced search (PostgreSQL full-text search)
- [ ] Analytics (PostgreSQL aggregate functions)

---

## 🚀 Launch Checklist

Before marking this spec as `done`:

- [ ] psycopg2-binary added to requirements.txt
- [ ] app.py updated with dynamic DATABASE_URL
- [ ] PostgreSQL created on Render
- [ ] DATABASE_URL environment variable set
- [ ] Alembic installed and configured
- [ ] Initial migration generated
- [ ] CI/CD updated to test against PostgreSQL
- [ ] All tests pass in CI/CD
- [ ] Deployed to production successfully
- [ ] Production app connects to PostgreSQL
- [ ] Data seeded in PostgreSQL
- [ ] App works end-to-end in production
- [ ] Constitution updated (if needed)

---

## 📖 References

- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Render PostgreSQL Guide](https://render.com/docs/databases)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

---

## 📝 Notes

### Learning Objectives
- Understand why PostgreSQL vs SQLite
- Learn database migrations with Alembic
- Practice environment-specific configuration
- Experience production database setup

### Questions to Answer
- How do migrations work?
- What's the difference between postgres:// and postgresql://?
- Why use transactions for migrations?
- How does SQLAlchemy abstract database differences?

---

**Status Transitions:**
- `draft` → Ready to review and start implementation
- `ready` → Reviewed and approved, ready to code
- `active` → Currently implementing
- `done` → Completed and deployed
