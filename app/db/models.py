from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_crawled_at = db.Column(db.DateTime, nullable=True)

    # Relationship: one article → many versions
    versions = db.relationship("ArticleVersion", backref="article", lazy=True)

    __table_args__ = (db.Index('ix_article_url', 'url'),)

class ArticleVersion(db.Model):
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


