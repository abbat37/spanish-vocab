# Spanish Vocabulary Learning App

A Flask web application for learning Spanish vocabulary through interactive sentence generation and progress tracking.

## Features

- Generate practice sentences in Spanish and English based on themes and word types
- Track your learning progress with statistics by theme
- Mark words as learned and monitor your improvement
- Responsive web interface with real-time updates
- Persistent user sessions and progress tracking

## Tech Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLite with Flask-SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Testing**: pytest with coverage reporting
- **Production Server**: Gunicorn

## Project Structure

```
spanish-vocab-app/
├── app.py                 # Main Flask application
├── database.py            # Database models and configuration
├── seed_database.py       # Database seeding script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore rules
├── templates/
│   └── index.html        # Main HTML template
├── tests/
│   └── test_app.py       # Unit tests
└── instance/
    └── spanish_vocab.db  # SQLite database (not in git)
```

## Local Development Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/abbat37/spanish-vocab.git
cd spanish-vocab
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
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
DATABASE_URL=sqlite:///spanish_vocab.db
```

6. Seed the database with vocabulary:
```bash
python3 seed_database.py
```

7. Run the application:
```bash
python3 app.py
```

8. Open your browser to `http://localhost:5000`

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
open htmlcov/index.html  # On Mac
```

## Database

The app uses SQLite for data persistence with the following models:

- **VocabularyWord**: Spanish words with themes and types
- **SentenceTemplate**: Template sentences for word substitution
- **UserSession**: User session tracking
- **WordPractice**: User practice history and learned status

### Database Schema

```
VocabularyWord
├── id (Primary Key)
├── theme (e.g., 'cooking', 'work', 'sports')
├── word_type (e.g., 'verb', 'noun', 'adj')
├── spanish_word
└── english_translation

SentenceTemplate
├── id (Primary Key)
├── theme
├── word_type
├── spanish_template (contains {word} placeholder)
└── english_template (contains {word} placeholder)

WordPractice
├── id (Primary Key)
├── session_id (Foreign Key)
├── word_id (Foreign Key)
├── theme
├── word_type
├── marked_learned (Boolean)
└── practiced_at (Timestamp)
```

## Deployment

### Deploying to Render

1. Create a [Render](https://render.com) account

2. Create a new Web Service:
   - Connect your GitHub repository
   - Select branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance Type: Free

3. Set Environment Variables in Render dashboard:
   ```
   SECRET_KEY=your-production-secret-key
   FLASK_ENV=production
   FLASK_DEBUG=False
   DATABASE_URL=sqlite:///spanish_vocab.db
   ```

4. Deploy! Render will automatically:
   - Install dependencies
   - Start your app with gunicorn
   - Provide a public URL

5. After first deployment, manually seed the database:
   - Use Render Shell to run: `python3 seed_database.py`

### Deploying to Railway

1. Create a [Railway](https://railway.app) account

2. Create new project from GitHub repository

3. Add environment variables:
   ```
   SECRET_KEY=your-production-secret-key
   FLASK_ENV=production
   FLASK_DEBUG=False
   ```

4. Railway will auto-detect Flask and deploy

### Deploying to Fly.io

1. Install flyctl CLI: `https://fly.io/docs/getting-started/installing-flyctl/`

2. Login: `fly auth login`

3. Launch app: `fly launch`

4. Set secrets:
   ```bash
   fly secrets set SECRET_KEY=your-production-secret-key
   fly secrets set FLASK_ENV=production
   ```

5. Deploy: `fly deploy`

## Environment Variables

Required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask session secret key | `your-secret-key-here` |
| `FLASK_ENV` | Environment mode | `development` or `production` |
| `FLASK_DEBUG` | Debug mode flag | `True` or `False` |
| `DATABASE_URL` | Database connection string | `sqlite:///spanish_vocab.db` |

## Usage

1. Select a theme (cooking, work, sports, etc.)
2. Select a word type (verb, noun, adjective)
3. Click "Generate Sentences"
4. Practice reading Spanish sentences and checking English translations
5. Click "Mark as Learned" to track your progress
6. View your statistics at the top of the page

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `pytest`
5. Commit changes: `git commit -m "Add feature"`
6. Push to branch: `git push origin feature-name`
7. Create a Pull Request

## Future Improvements

### Beginner Level (Current)
- ✅ Git version control
- ✅ SQLite database with migrations
- ✅ Environment variables (.env)
- ✅ User progress tracking
- ✅ Unit tests
- ✅ Cloud deployment

### Intermediate Level (Next Phase)
- [ ] CI/CD Pipeline with GitHub Actions
- [ ] PostgreSQL with connection pooling
- [ ] User authentication (login/signup)
- [ ] CSS framework (Tailwind/Bootstrap)
- [ ] Error tracking (Sentry)
- [ ] RESTful API with rate limiting

### Pro Level (Future)
- [ ] Docker containerization
- [ ] Kubernetes orchestration
- [ ] Load balancing and horizontal scaling
- [ ] Redis caching layer
- [ ] Advanced monitoring (New Relic/Datadog)

## License

MIT License - feel free to use this project for learning purposes.

## Acknowledgments

Built as a learning project to understand production web development practices while studying Spanish vocabulary.

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation in `/docs` folder
- Review test files for usage examples

---

Made with ❤️ for Spanish learners and aspiring web developers
