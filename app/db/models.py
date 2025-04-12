"""
This module defines the database models for the crawling system.

- **Article**: Represents a single article, including its URL and relationships to versions.
- **ArticleVersion**: Represents a version of an article, including metadata like headline, subheadline, and full text.
- **SchedulerSettings**: Stores settings for the crawling schedule, including frequency and status.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# --- Article Model ---
class Article(db.Model):
    """
    Represents a single article in the system, including its URL and any related versions.

    - **id**: Unique identifier for each article.
    - **url**: The URL of the article, must be unique.
    - **created_at**: The time when the article was first created in the database.
    - **last_crawled_at**: The last time the article was crawled.
    - **versions**: A relationship to the ArticleVersion model, representing multiple versions of the same article.
    """
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_crawled_at = db.Column(db.DateTime, nullable=True)

    # Relationship: one article → many versions
    versions = db.relationship("ArticleVersion", backref="article", lazy=True)

    __table_args__ = (db.Index('ix_article_url', 'url'),)


# --- ArticleVersion Model ---
class ArticleVersion(db.Model):
    """
    Represents a version of an article, storing data such as headline, subheadline, full text,
    and content hash for versioning and deduplication.

    - **id**: Unique identifier for each version of an article.
    - **article_id**: The ID of the article to which this version belongs.
    - **version_number**: The version number for this article version.
    - **headline**: The headline of the article.
    - **subheadline**: The subheadline of the article.
    - **full_text**: The full text of the article.
    - **last_updated**: The timestamp when the article content was last updated.
    - **crawled_at**: The timestamp when the version was crawled and stored.
    - **content_hash**: A hash of the article content, used for versioning and deduplication.
    """
    __tablename__ = 'article_versions'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    headline = db.Column(db.String)
    subheadline = db.Column(db.String)
    full_text = db.Column(db.Text)
    last_updated = db.Column(db.DateTime)
    crawled_at = db.Column(db.DateTime, default=datetime.utcnow)
    content_hash = db.Column(db.String)

    __table_args__ = (db.Index('ix_article_version_article_id_last_updated', 'article_id', 'last_updated'),)


# --- SchedulerSettings Model ---
class SchedulerSettings(db.Model):
    """
    Stores the settings for the crawling schedule.

    - **id**: Unique identifier for the scheduler settings.
    - **frequency_hours**: The frequency (in hours) for the crawl to run.
    - **is_enabled**: Whether the scheduler is enabled or disabled.
    """
    __tablename__ = 'scheduler_settings'

    id = db.Column(db.Integer, primary_key=True)
    frequency_hours = db.Column(db.Integer, nullable=False)  # Ensure this is Integer
    is_enabled = db.Column(db.Boolean, nullable=False)

    def __init__(self, frequency_hours, is_enabled):
        """
        Initialize the scheduler settings.

        :param frequency_hours: The frequency (in hours) for the scheduled crawl.
        :param is_enabled: Whether the scheduler is enabled or disabled.
        """
        self.frequency_hours = frequency_hours
        self.is_enabled = is_enabled
