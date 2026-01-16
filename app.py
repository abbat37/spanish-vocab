from flask import Flask, render_template, request
import random
import os
from dotenv import load_dotenv
from database import db, init_db, VocabularyWord, SentenceTemplate

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure app from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-fallback')
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False') == 'True'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///spanish_vocab.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)


def generate_sentences(theme, word_type):
    """Generate 5 sentences with new Spanish words from database"""
    # Query vocabulary words from database
    words = VocabularyWord.query.filter_by(theme=theme, word_type=word_type).all()

    if not words:
        return []

    # Query sentence templates from database
    templates = SentenceTemplate.query.filter_by(theme=theme, word_type=word_type).all()

    if not templates:
        return []

    # Select 5 random words
    selected_words = random.sample(words, min(5, len(words)))

    # Select 5 random templates (or reuse if less than 5)
    selected_templates = random.sample(templates, min(5, len(templates)))

    sentences = []
    for i, word in enumerate(selected_words):
        # Get the template (cycle through if we have fewer templates than words)
        template = selected_templates[i % len(selected_templates)]

        # Create Spanish sentence
        spanish_sentence = template.spanish_template.replace(
            '{word}',
            f'<mark>{word.spanish_word}</mark>'
        )

        # Create English sentence
        english_sentence = template.english_template.replace(
            '{word}',
            f'<mark>{word.english_translation}</mark>'
        )

        sentences.append({
            'spanish': spanish_sentence,
            'english': english_sentence,
            'word_id': word.id
        })

    return sentences


@app.after_request
def add_header(response):
    """Add headers to prevent caching during development"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    sentences = []
    theme = ''
    word_type = ''

    if request.method == 'POST':
        theme = request.form.get('theme', '').lower()
        word_type = request.form.get('word_type', '').lower()

        if theme and word_type:
            sentences = generate_sentences(theme, word_type)

    return render_template('index.html', sentences=sentences, theme=theme, word_type=word_type)

if __name__ == '__main__':
    app.run(debug=True)
