"""
Application Entry Point
Run this file to start the Flask development server
"""
import os
from app import create_app

# Create application instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Only used for local development
    # In production, use gunicorn: gunicorn run:app
    app.run(debug=True, host='0.0.0.0', port=5000)
