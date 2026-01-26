# Spanish Vocabulary App - Project Constitution

**Version:** 1.0
**Last Updated:** 2026-01-26
**Status:** Active

---

## 🎯 Project Mission

Build a web application for learning Spanish vocabulary through interactive sentence generation and progress tracking, while learning production-grade software engineering practices.

### Primary Goals
1. **Educational Tool**: Help users learn Spanish vocabulary in context
2. **Learning Vehicle**: Serve as a project to learn professional software development practices
3. **Production Quality**: Follow industry standards for code quality, testing, and deployment

---

## 🏗️ Architecture Decisions

### Technology Stack

**Backend Framework: Flask**
- **Why:** Lightweight, easy to learn, sufficient for our needs
- **Why not Django:** Too heavy for this project's scope
- **Trade-off:** Less built-in features, but more control and simplicity

**Database: SQLite (dev) → PostgreSQL (production)**
- **Why SQLite for dev:** File-based, no setup required, fast local development
- **Why PostgreSQL for prod:** Production-ready, handles concurrent users, ACID compliance
- **Why not MongoDB:** Structured data fits relational model better

**ORM: SQLAlchemy**
- **Why:** Industry standard Python ORM, great documentation
- **Why not raw SQL:** Prevents SQL injection, database-agnostic code
- **Trade-off:** Learning curve, but worth the safety and flexibility

**Hosting: Render**
- **Why:** Free tier, auto-deploys from GitHub, simple setup
- **Future:** May migrate to AWS for learning purposes
- **Trade-off:** Cold starts on free tier, but acceptable for learning project

**CI/CD: GitHub Actions**
- **Why:** Free, integrated with GitHub, industry standard
- **Why not Jenkins/CircleCI:** More overhead than needed for solo project

---

## 💻 Coding Standards

### Python Style Guide

**Follow PEP 8** with these specifications:
- Maximum line length: 127 characters (to match flake8 config)
- Use 4 spaces for indentation (never tabs)
- Use snake_case for functions and variables
- Use PascalCase for class names
- Use UPPER_CASE for constants

**Example:**
```python
# Good
def generate_sentences(theme, word_type):
    MAX_SENTENCES = 5
    selected_words = []
    return selected_words

# Bad
def GenerateSentences(Theme, wordType):
    maxSentences = 5
    SelectedWords = []
    return SelectedWords
```

### File Organization

```
project-root/
├── .speckit/          # SpecKit configuration
├── specs/             # Feature specifications
├── .github/           # GitHub Actions workflows
├── tests/             # All test files
├── templates/         # Jinja2 HTML templates
├── static/            # CSS, JS, images (future)
├── app.py             # Main Flask application
├── database.py        # Database models
├── seed_database.py   # Database seeding script
├── requirements.txt   # Python dependencies
└── .env              # Environment variables (not in git)
```

### Import Order

Follow this order (separated by blank lines):
1. Standard library imports
2. Third-party imports
3. Local application imports

**Example:**
```python
import os
import random
from datetime import datetime

from flask import Flask, render_template
from sqlalchemy import func

from database import db, VocabularyWord
```

---

## 🧪 Testing Standards

### Test Coverage Requirements

- **Minimum coverage:** 70% (current: ~85%)
- **Target coverage:** 80%
- **Critical paths:** 100% coverage (authentication, data writes)

### What to Test

**Always test:**
- All routes (status codes, response content)
- Database operations (CRUD)
- Business logic functions
- Edge cases and error handling

**Don't test:**
- Third-party library code
- Configuration files
- Simple getters/setters

### Test File Naming

- Test files: `test_*.py` (pytest discovery)
- Test classes: `Test*` (e.g., `TestRoutes`)
- Test functions: `test_*` (e.g., `test_home_page_loads`)

### Test Structure

Use **Arrange-Act-Assert** pattern:

```python
def test_generate_sentences():
    # Arrange: Set up test data
    theme = 'cooking'
    word_type = 'verb'

    # Act: Execute the function
    result = generate_sentences(theme, word_type)

    # Assert: Verify the result
    assert len(result) <= 5
    assert all('spanish' in s for s in result)
```

---

## 🔄 Git Workflow

### Branch Strategy

**Single developer workflow:**
- **main branch:** Always deployable, protected by CI/CD
- **feature branches (optional):** For experimenting with big features
- **Direct pushes allowed:** To main for small changes (solo project)

**Future team workflow:**
- **main:** Production code only
- **feature branches:** All development work
- **Pull requests:** Required before merging
- **Branch protection:** Enforce passing tests

### Commit Messages

**Format:**
```
Type: Brief description (50 chars max)

Optional detailed explanation of changes (wrap at 72 chars).
Why this change was made, any important context.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding/updating tests
- `refactor:` Code restructuring
- `chore:` Maintenance tasks

**Examples:**
```
feat: Add user progress tracking

Implements session-based tracking of practiced words and learned status.
Users can now see statistics by theme and total progress.

Closes #15
```

---

## 🚀 Deployment Standards

### Environments

**Local Development:**
- Database: SQLite (file-based)
- Debug mode: ON
- Hot reload: ON
- URL: http://localhost:5000

**Production (Render):**
- Database: PostgreSQL
- Debug mode: OFF
- Server: Gunicorn
- URL: https://spanish-vocab-*.onrender.com

### Deployment Process

**Automated via CI/CD:**
1. Developer pushes to main branch
2. GitHub Actions runs tests
3. If tests pass → Trigger Render deployment
4. If tests fail → Block deployment
5. Render builds and deploys app
6. Monitoring via Render dashboard

### Environment Variables

**Required for all environments:**
- `SECRET_KEY` - Flask session secret
- `FLASK_ENV` - development/production
- `DATABASE_URL` - Database connection string

**Stored in:**
- Local: `.env` file (gitignored)
- Production: Render environment variables
- CI/CD: GitHub Secrets

---

## 📝 Documentation Standards

### Code Documentation

**When to add docstrings:**
- All public functions
- All classes
- Complex algorithms

**Docstring format:**
```python
def generate_sentences(theme, word_type, session_id=None):
    """Generate practice sentences with Spanish vocabulary.

    Args:
        theme (str): Vocabulary theme (cooking, work, sports, restaurant)
        word_type (str): Type of word (verb, noun, adj)
        session_id (str, optional): User session ID for marking learned words

    Returns:
        list: List of sentence dictionaries with spanish/english/word_id keys

    Example:
        >>> generate_sentences('cooking', 'verb')
        [{'spanish': 'Me gusta <mark>cocinar</mark>...', ...}]
    """
```

**When NOT to add comments:**
- Self-explanatory code
- Variable names that are clear
- Standard patterns (don't explain Flask routes)

### README Updates

**Update README when:**
- Adding new features (user-facing)
- Changing setup process
- Adding new dependencies
- Changing deployment process

---

## 🔐 Security Standards

### Sensitive Data

**Never commit:**
- `.env` files
- API keys
- Database passwords
- Session secrets
- OAuth tokens

**Always use:**
- Environment variables for secrets
- GitHub Secrets for CI/CD
- `.gitignore` to exclude sensitive files

### Input Validation

**Always validate:**
- User input from forms
- API request data
- Database query parameters

**Use:**
- SQLAlchemy ORM (prevents SQL injection)
- Flask form validation
- Input sanitization for HTML output

---

## 📊 Quality Gates

### Pre-Commit (Local)

**Before every commit:**
- Tests pass locally: `pytest`
- Code runs without errors
- No obvious bugs

### Pre-Merge (CI/CD)

**Automated checks via GitHub Actions:**
- ✅ All tests pass
- ✅ Code coverage maintained
- ✅ Linting passes (warnings OK)
- ✅ No syntax errors

### Pre-Deploy (CI/CD)

**Before production deployment:**
- ✅ All tests pass
- ✅ Code quality checks pass
- ✅ Main branch only
- ✅ Manual verification if major changes

---

## 🎓 Learning Goals

### Beginner Level (Current Stage)
- [x] Git version control
- [x] Environment variables
- [x] SQLite database
- [x] Unit testing
- [x] CI/CD pipeline
- [x] Cloud deployment
- [x] Spec-driven development

### Intermediate Level (In Progress)
- [ ] PostgreSQL migration
- [ ] Error tracking (Sentry)
- [ ] API design & validation
- [ ] User authentication
- [ ] Application logging

### Professional Level (Future)
- [ ] AWS deployment
- [ ] Docker containerization
- [ ] Monitoring & observability
- [ ] Load testing
- [ ] Security audits

---

## 🔄 Constitution Maintenance

### When to Update

**Update this constitution when:**
- Major technology choices are made
- Coding standards change
- New team members join
- Architecture changes
- New workflows are adopted

### Review Schedule

**Monthly review:** Check if standards still make sense
**After incidents:** Update if gaps exposed
**Learning milestones:** Document new practices

---

## 📚 References

### Essential Reading
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [pytest Documentation](https://docs.pytest.org/)

### Project Documentation
- README.md - Setup and usage instructions
- specs/ - Feature specifications
- tests/ - Test files with examples

---

**End of Constitution**

*This document is a living document and should evolve with the project.*
