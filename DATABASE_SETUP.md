# Database Setup Guide

## First Time Setup

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Initialize and seed the database:**
   ```bash
   python3 seed_database.py
   ```
   This will create the SQLite database and populate it with vocabulary words and sentence templates.

3. **Run the application:**
   ```bash
   python3 app.py
   ```
   Then open http://127.0.0.1:5000 in your browser.

## Database Location

The SQLite database is stored at: `instance/spanish_vocab.db`

This file is automatically excluded from Git via `.gitignore`.

## Resetting the Database

To clear and reseed the database, simply run:
```bash
python3 seed_database.py
```

When prompted, type "yes" to confirm you want to clear existing data.

## Database Schema

### VocabularyWord Table
- `id`: Primary key
- `theme`: cooking, work, sports, restaurant
- `word_type`: verb, noun, adj
- `spanish_word`: Spanish vocabulary word
- `english_translation`: English translation
- `created_at`: Timestamp

### SentenceTemplate Table
- `id`: Primary key
- `theme`: cooking, work, sports, restaurant
- `word_type`: verb, noun, adj
- `spanish_template`: Spanish sentence template with {word} placeholder
- `english_template`: English sentence template with {word} placeholder
- `created_at`: Timestamp
