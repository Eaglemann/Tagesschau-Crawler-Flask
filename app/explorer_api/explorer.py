"""
This module defines the routes for exploring articles and their versions.

- **/explorer/articles**: Lists all articles in the system.
- **/explorer/articles/<article_id>/versions**: Retrieves all versions of a specific article.
- **/explorer/articles/<article_id>/compare**: Compares the two most recent versions of a specific article.
- **/explorer/articles/search**: Searches for articles based on keywords in the headline, subheadline, or full text of their latest versions.
"""

from flask import Blueprint, jsonify, request
from app.db.models import Article, ArticleVersion
from sqlalchemy import func
from app.db.models import db

# Initialize the blueprint for exploring articles
explorer = Blueprint("explorer", __name__)

# --- Route to List All Articles ---
@explorer.route("/explorer/articles", methods=["GET"])
def list_articles():
    """
    Retrieves all articles in the database.

    Returns a list of articles with their ID and URL.

    """
    articles = Article.query.all()
    result = [
        {
            "id": article.id,
            "url": article.url,
        }
        for article in articles
    ]
    return jsonify(result), 200


# --- Route to Get Versions of an Article ---
@explorer.route("/explorer/articles/<int:article_id>/versions", methods=["GET"])
def get_article_versions(article_id):
    """
    Retrieves all versions of a specific article based on its ID.

    Returns a list of versions with their ID, version number, headline, subheadline, 
    last update time, and crawl timestamp.

    """
    versions = (
        ArticleVersion.query
        .filter_by(article_id=article_id)
        .order_by(ArticleVersion.version_number.asc())
        .all()
    )

    if not versions:
        return jsonify({"error": "No versions found for this article"}), 404

    result = [
        {
            "id": version.id,
            "version_number": version.version_number,
            "headline": version.headline,
            "subheadline": version.subheadline,
            "last_updated": version.last_updated.isoformat(),
            "crawled_at": version.crawled_at.isoformat(),
        }
        for version in versions
    ]
    return jsonify(result), 200


# --- Route to Compare Two Versions of an Article ---
@explorer.route("/explorer/articles/<int:article_id>/compare", methods=["GET"])
def compare_article_versions(article_id):
    """
    Compares the two most recent versions of a specific article.

    Returns the details of both versions for comparison, including headline, subheadline, 
    and full text for each version.

    """
    # Get the two latest versions for the article
    latest_versions = (
        ArticleVersion.query
        .filter_by(article_id=article_id)
        .order_by(ArticleVersion.version_number.desc())
        .limit(2)  # Limited to 2 most recent versions
        .all()
    )

    if len(latest_versions) < 2:
        return jsonify({"error": "Not enough versions to compare"}), 404

    # Extract the two versions
    version_1 = latest_versions[0]
    version_2 = latest_versions[1]

    # Return the comparison of the two versions
    comparison = {
        "version_1": {
            "version_number": version_1.version_number,
            "headline": version_1.headline,
            "subheadline": version_1.subheadline,
            "full_text": version_1.full_text,
        },
        "version_2": {
            "version_number": version_2.version_number,
            "headline": version_2.headline,
            "subheadline": version_2.subheadline,
            "full_text": version_2.full_text,
        },
    }

    return jsonify(comparison), 200


# --- Route to Search Articles ---
@explorer.route("/explorer/articles/search", methods=["GET"])
def search_articles():
    """
    Searches for articles based on a keyword in the latest version's headline, subheadline, or full text.

    Accepts the query parameter 'q' to search for articles that match the keyword.

    """
    keyword = request.args.get("q", "").strip()
    if not keyword:
        return jsonify({"error": "Query parameter 'q' is required."}), 400

    # Subquery to get the most recent version of each article
    subquery = (
        db.session.query(
            ArticleVersion.article_id,
            func.max(ArticleVersion.version_number).label("max_version")
        )
        .group_by(ArticleVersion.article_id)
        .subquery()
    )

    # Join to get the latest version details
    latest_versions = (
        db.session.query(ArticleVersion)
        .join(
            subquery,
            (ArticleVersion.article_id == subquery.c.article_id) & 
            (ArticleVersion.version_number == subquery.c.max_version)
        )
        .filter(
            (ArticleVersion.headline.ilike(f"%{keyword}%")) |
            (ArticleVersion.subheadline.ilike(f"%{keyword}%")) |
            (ArticleVersion.full_text.ilike(f"%{keyword}%"))
        )
        .all()
    )

    result = [
        {
            "article_id": version.article_id,
            "version_number": version.version_number,
            "headline": version.headline,
            "subheadline": version.subheadline,
            "full_text": version.full_text,
            "last_updated": version.last_updated.isoformat(),
            "crawled_at": version.crawled_at.isoformat(),
        }
        for version in latest_versions
    ]

    return jsonify(result), 200
