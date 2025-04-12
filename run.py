"""
This module sets up the Flask application and handles database setup and scheduler initialization.

- Initializes the Flask app using the factory function `create_app()`.
- Creates the database tables if they don't exist.
- Starts the scheduler for scheduled background tasks like crawling.
"""

from app import create_app
from app.db.models import db
from app.scheduler.scheduler import start_scheduler

app = create_app()  # Initialize Flask app using the factory function

with app.app_context():  # Ensure that the app context is active for database setup
    db.create_all()  # Creates all tables defined in the models (Article, ArticleVersion, etc.) if they do not exist
    start_scheduler()  # Initializes and starts the scheduler for background tasks like crawling

if __name__ == "__main__":
    app.run(debug=True)  # Runs the app with debugging enabled (useful in development)
