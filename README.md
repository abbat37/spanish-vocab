# Spanish Vocabulary Learning App

A production-grade Flask web application for learning Spanish vocabulary through interactive sentence generation and progress tracking.

## Features

- **User Authentication**: Secure account creation with email and password
- **Persistent Progress**: Your learning data is saved to your account, accessible from any device
- Generate practice sentences in Spanish and English based on themes and word types
- Track your learning progress with statistics by theme
- Mark words as learned and monitor your improvement
- Responsive web interface with real-time updates via AJAX
- Full-width dashboard for viewing learning statistics
- Production-ready with HTTPS, database, and automated deployments

## Tech Stack

### Backend
- **Framework**: Flask 3.0.0
- **Database**: PostgreSQL 15 (production) / SQLite (development)
- **ORM**: Flask-SQLAlchemy 3.1.1
- **Server**: Gunicorn 21.2.0 with systemd process management
- **API Validation**: Marshmallow 3.23.2
- **Rate Limiting**: Flask-Limiter 3.8.0
- **Error Tracking**: Sentry SDK 2.19.2
- **Authentication**: Flask-Login 0.6.3
- **Password Hashing**: bcrypt 4.1.2
- **Migrations**: Flask-Migrate 4.0.5 (Alembic)

### Frontend
- **UI**: HTML5, CSS3 (custom responsive design)
- **JavaScript**: Vanilla JS with Fetch API for AJAX
- **Layout**: CSS Grid and Flexbox

### Infrastructure
- **Web Server**: Nginx (reverse proxy with SSL termination)
- **SSL/TLS**: Let's Encrypt (auto-renewal via certbot)
- **Hosting**: AWS EC2
- **Domain**: DuckDNS (free DNS service)
- **CI/CD**: GitHub Actions with automated testing and deployment

### Testing & Quality
- **Testing**: pytest 8.4.2 with pytest-cov 7.0.0
- **Code Quality**: flake8, black (automated in CI/CD)
- **Coverage**: Automated HTML coverage reports

## Project Structure

```
spanish-vocab-app/
├── run.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .gitignore                 # Git ignore rules
├── app/
│   ├── __init__.py            # Application factory
│   ├── config.py              # Configuration management
│   ├── models/                # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── session.py
│   │   └── vocabulary.py
│   ├── routes/                # Blueprint routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── api.py
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── session_service.py
│   │   ├── stats_service.py
│   │   └── sentence_service.py
│   └── utils/                 # Utilities and validators
│       ├── __init__.py
│       └── validators.py
├── templates/
│   ├── index.html             # Main application page
│   ├── login.html             # Login page
│   └── register.html          # Registration page
├── tests/
│   └── test_app.py            # Unit tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions CI/CD pipeline
├── migrations/                # Database migrations
│   └── versions/
├── specs/
│   ├── README.md              # Spec-driven development guide
│   └── postgres-migration.md # PostgreSQL migration spec
└── instance/
    └── spanish_vocab.db       # SQLite database (development only)
```

## Live Deployment

- **Production**: https://spanish-vocab.duckdns.org (AWS EC2)

## Local Development Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git
- PostgreSQL (optional, falls back to SQLite)

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/abbat37/spanish-vocab.git
cd spanish-vocab
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment configuration:
```bash
cp .env.example .env
```

5. Edit [.env](.env) file with your settings:
```
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///spanish_vocab.db  # Or postgresql://...
SENTRY_DSN=your-sentry-dsn  # Optional
```

6. The database will auto-seed on first run! Just start the app:
```bash
python3 run.py
```

7. Open your browser to `http://localhost:8080`

## Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=. --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html  # On Mac/Linux
start htmlcov/index.html  # On Windows
```

## Database

### Schema

```
User
├── id (Primary Key)
├── email (Unique, Indexed)
├── password_hash (bcrypt hashed)
├── created_at (Timestamp)
└── last_login (Timestamp)

VocabularyWord
├── id (Primary Key)
├── theme (e.g., 'cooking', 'work', 'sports', 'restaurant')
├── word_type (e.g., 'verb', 'noun', 'adj')
├── spanish_word
└── english_translation

SentenceTemplate
├── id (Primary Key)
├── theme
├── word_type
├── spanish_template (contains {word} placeholder)
└── english_template (contains {word} placeholder)

UserSession
├── id (Primary Key)
├── session_id (UUID)
├── user_id (Foreign Key to User, nullable for anonymous sessions)
├── created_at (Timestamp)
└── last_active (Timestamp)

WordPractice
├── id (Primary Key)
├── session_id (Foreign Key to UserSession)
├── word_id (Foreign Key to VocabularyWord)
├── theme
├── word_type
├── marked_learned (Boolean)
└── practiced_at (Timestamp)
```

### Database Migration (SQLite → PostgreSQL)

See [specs/postgres-migration.md](specs/postgres-migration.md) for the full migration spec.

## Deployment

### AWS EC2 Production Setup

Our production environment runs on AWS EC2 with the following stack:

**Infrastructure:**
- **EC2 Instance**: t3.micro (free tier)
- **OS**: Ubuntu Server 24.04 LTS
- **Process Manager**: systemd (auto-restart, boot persistence)
- **Web Server**: Nginx (reverse proxy, SSL termination)
- **SSL**: Let's Encrypt (auto-renewal)
- **Database**: PostgreSQL 15
- **Domain**: spanish-vocab.duckdns.org

**Deployment Process:**

1. **Launch EC2 Instance**
   - Instance type: t3.micro
   - Security Groups: SSH (22), HTTP (80), HTTPS (443)
   - Download SSH key pair

2. **Server Setup**
```bash
# SSH into server
ssh -i ~/.ssh/spanish-vocab-key.pem ubuntu@YOUR_IP

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv git postgresql postgresql-contrib nginx certbot python3-certbot-nginx

# Clone repository
git clone https://github.com/abbat37/spanish-vocab.git
cd spanish-vocab

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure PostgreSQL**
```bash
sudo -u postgres psql -c "CREATE DATABASE spanish_vocab;"
sudo -u postgres psql -c "CREATE USER spanish_vocab_user WITH PASSWORD 'your-password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE spanish_vocab TO spanish_vocab_user;"
sudo -u postgres psql -d spanish_vocab -c "GRANT ALL ON SCHEMA public TO spanish_vocab_user;"
```

4. **Create .env file**
```bash
nano .env
# Add:
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-production-secret
DATABASE_URL=postgresql://spanish_vocab_user:your-password@localhost/spanish_vocab
SENTRY_DSN=your-sentry-dsn
```

5. **Setup systemd service**
```bash
sudo nano /etc/systemd/system/spanish-vocab.service
# See deploy.sh for service configuration

sudo systemctl daemon-reload
sudo systemctl start spanish-vocab
sudo systemctl enable spanish-vocab
```

6. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/spanish-vocab
# Add reverse proxy configuration

sudo ln -s /etc/nginx/sites-available/spanish-vocab /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. **Setup HTTPS with Let's Encrypt**
```bash
sudo certbot --nginx -d spanish-vocab.duckdns.org
```

### Automated Deployment

The application automatically deploys to EC2 via GitHub Actions CI/CD pipeline when you push to the main branch. See the CI/CD Pipeline section below for details.

## CI/CD Pipeline

Automated via GitHub Actions ([.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)):

**On every push to main:**
1. **Test Job**: Runs pytest against PostgreSQL
2. **Lint Job**: Checks code quality (flake8, black)
3. **Deploy to EC2**: SSH deployment via automated script

**GitHub Secrets Required:**
- `EC2_SSH_KEY`: Private SSH key for EC2
- `EC2_HOST`: EC2 public IP or domain
- `EC2_USER`: `ubuntu`

**Pipeline Stages:**
```
Push to main
    ↓
Run Tests (PostgreSQL) ──→ Pass ──┐
Run Linting ──→ Pass ──────────────┤
                                   ↓
                            Deploy to EC2 (SSH)
                                   ↓
                            Live in Production!
```

## Database Migrations

This project uses **Flask-Migrate** (Alembic) to manage database schema changes safely.

### Why Migrations Matter

Without migrations, schema changes can break production:
- ❌ SQLAlchemy's `db.create_all()` only creates missing tables
- ❌ It doesn't modify existing tables (e.g., adding columns)
- ✅ Migrations safely update production databases without data loss

### Running Migrations in Production

**For EC2:**
Migrations are applied automatically during deployment via the CI/CD pipeline. The deployment script runs `flask db upgrade` to apply any pending migrations.

**Manual Migration (if needed):**
```bash
# SSH into EC2
ssh -i ~/.ssh/spanish-vocab-key.pem ubuntu@YOUR_IP

# Navigate to app directory
cd ~/spanish-vocab
source venv/bin/activate

# Apply migrations
python3 -m flask db upgrade
```

### Creating New Migrations (For Future Changes)

When you modify database models in `database.py`:

1. **Generate migration:**
   ```bash
   python3 -m flask db migrate -m "Description of changes"
   ```

2. **Review the migration file:**
   - Check `migrations/versions/xxx_description.py`
   - Verify `upgrade()` and `downgrade()` functions
   - Alembic auto-generates but may need tweaks

3. **Test locally:**
   ```bash
   python3 -m flask db upgrade
   ```

4. **Commit migration files:**
   ```bash
   git add migrations/
   git commit -m "Add migration for X"
   git push
   ```

5. **Apply in production:**
   - EC2: Migrations run automatically in deploy script

### Migration Best Practices

- ✅ **Always test locally first** with a copy of production data
- ✅ **Review auto-generated migrations** (Alembic makes mistakes)
- ✅ **Backup database before migrations** (`pg_dump`)
- ✅ **Make migrations reversible** (implement `downgrade()`)
- ✅ **One logical change per migration** (not multiple unrelated changes)
- ❌ **Never edit applied migrations** (create a new one instead)
- ❌ **Never delete migration files** (breaks migration history)

### Common Migration Commands

```bash
# Initialize migrations (already done)
python3 -m flask db init

# Create new migration
python3 -m flask db migrate -m "Add column X to table Y"

# Apply pending migrations
python3 -m flask db upgrade

# Rollback last migration
python3 -m flask db downgrade

# Show current migration
python3 -m flask db current

# Show migration history
python3 -m flask db history
```

## Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Flask session secret | `your-secret-key-here` | Yes |
| `FLASK_ENV` | Environment mode | `development` / `production` | Yes |
| `FLASK_DEBUG` | Debug mode | `True` / `False` | Yes |
| `DATABASE_URL` | Database connection | `postgresql://user:pass@host/db` | Yes |
| `SENTRY_DSN` | Error tracking | `https://...@sentry.io/...` | No |

## Usage

### First-Time User
1. Visit the site and click "Sign up"
2. Create an account with email and password (min 8 characters)
3. You'll be automatically logged in

### Returning User
1. Visit the site and log in with your credentials
2. Your progress is preserved across sessions and devices

### Learning Flow
1. Select a theme (cooking, work, sports, restaurant)
2. Select a word type (verb, noun, adjective)
3. Click "Generate Sentences"
4. Practice reading Spanish sentences with English translations
5. Click "✓ Learned" to mark words as learned
6. View your progress in the dashboard (full-width stats at top)
7. Click "Logout" when done (top-right corner)

## API Endpoints

### `POST /register`
Create a new user account.

**Request:** Form data
- `email`: User email address
- `password`: Password (min 8 characters)
- `confirm_password`: Password confirmation

**Response:** Redirect to index page with success message

### `POST /login`
Authenticate a user.

**Request:** Form data
- `email`: User email address
- `password`: User password

**Response:** Redirect to index page or next parameter

### `GET /logout`
Log out the current user (requires authentication).

**Response:** Redirect to login page

### `POST /api/mark-learned`
Mark a word as learned or unlearned (toggle).

**Request:**
```json
{
  "word_id": 123
}
```

**Response:**
```json
{
  "success": true,
  "marked_learned": true,
  "stats": {
    "total_practiced": 50,
    "total_learned": 25,
    "by_theme": {"cooking": 15, "work": 10}
  }
}
```

**Rate Limit:** 10 requests per minute

## Features Roadmap

### ✅ Completed (Current)
- **User Authentication & Authorization** (Session-based with Flask-Login)
- Git version control with GitHub
- CI/CD Pipeline with GitHub Actions
- PostgreSQL production database
- User progress tracking with persistent accounts
- Unit tests with 90%+ coverage
- Cloud deployment (AWS EC2)
- HTTPS with Let's Encrypt
- Nginx reverse proxy
- systemd process management
- Error tracking with Sentry
- API validation with Marshmallow
- Rate limiting on API endpoints
- Auto-seeding database on startup
- Responsive dashboard (full-width)
- Spec-driven development
- Password hashing with bcrypt

### 🚧 Next Phase
- Password reset via email
- Email notifications for progress milestones
- OAuth integration (Sign in with Google/GitHub)
- Spaced repetition algorithm
- Audio pronunciation
- Mobile app (React Native)

### 🔮 Future
- Docker containerization
- Kubernetes orchestration
- Redis caching layer
- Advanced monitoring (Datadog/New Relic)
- Load balancing and horizontal scaling
- Multi-language support (French, Italian, etc.)

## Architecture

### Current Production Stack

```
                    Internet
                       ↓
            ┌──────────────────────┐
            │   DuckDNS (DNS)     │
            │ spanish-vocab.      │
            │  duckdns.org        │
            └──────────────────────┘
                       ↓
            ┌──────────────────────┐
            │ Nginx (Port 80/443)  │
            │ - Reverse Proxy      │
            │ - SSL Termination    │
            │ - Rate Limiting      │
            └──────────────────────┘
                       ↓
            ┌──────────────────────┐
            │ Gunicorn (Port 8000) │
            │ - WSGI Server        │
            │ - 4 Workers          │
            └──────────────────────┘
                       ↓
            ┌──────────────────────┐
            │   Flask App          │
            │ - Routes             │
            │ - Business Logic     │
            │ - API Endpoints      │
            └──────────────────────┘
                       ↓
            ┌──────────────────────┐
            │ PostgreSQL Database  │
            │ - Vocabulary         │
            │ - User Sessions      │
            │ - Practice History   │
            └──────────────────────┘
```

### CI/CD Flow

```
Developer Push
      ↓
GitHub Repository (main branch)
      ↓
GitHub Actions Workflow
      ↓
┌──────────────────────────────┐
│  Run Tests (PostgreSQL)      │
│  Run Linters (flake8, black) │
└──────────────────────────────┘
      ↓ (if pass)
┌──────────────────────────────┐
│  Deploy to EC2 (SSH + script)│
└──────────────────────────────┘
      ↓
Production Live!
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `pytest`
5. Commit changes: `git commit -m "Add feature"`
6. Push to branch: `git push origin feature-name`
7. Create a Pull Request

## Development Practices

- **Spec-Driven Development**: All features documented in `/specs` before coding
- **Test-Driven Development**: Write tests before implementation
- **CI/CD**: Automated testing and deployment on every push
- **Production-First**: Use same stack (PostgreSQL) in dev and prod
- **Security**: HTTPS, rate limiting, input validation, secret management

## License

MIT License - feel free to use this project for learning purposes.

## Acknowledgments

Built as a comprehensive learning project to understand:
- Full-stack web development
- DevOps and cloud deployment
- CI/CD pipelines
- Database design and migrations
- Production best practices
- Spec-driven development

While also learning Spanish vocabulary! 🇪🇸

## Support

For issues or questions:
- Open an issue on GitHub
- Check `/specs` folder for detailed documentation
- Review test files for usage examples
- Read inline code comments

---

**Live Site:** https://spanish-vocab.duckdns.org
**Repository:** https://github.com/abbat37/spanish-vocab

Made with ❤️ for Spanish learners and aspiring web developers