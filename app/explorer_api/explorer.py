from flask import Blueprint, jsonify
from app.db.models import Article, ArticleVersion 

explorer = Blueprint("explorer", __name__)

@explorer.route("/explorer/health", methods=["GET"])
def explorer_health():
    return jsonify({"status": "Explorer API is running"}), 200

@explorer.route("/explorer/articles", methods=["GET"])
def list_articles():
    articles = Article.query.all()
    result = [
        {
            "id": article.id,
            "url": article.url,
        }
        for article in articles
    ]
    return jsonify(result), 200


@explorer.route("/explorer/articles/<int:article_id>/versions", methods=["GET"])
def get_article_versions(article_id):
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


@explorer.route("/explorer/articles/<int:article_id>/compare", methods=["GET"])
def compare_article_versions(article_id):
    # Get the two latest versions for the article
    latest_versions = (
        ArticleVersion.query
        .filter_by(article_id=article_id)
        .order_by(ArticleVersion.version_number.desc())
        .limit(2)  # Here it is limited to 2 most recent versions
        .all()
    )

    # If less than two versions are found cant compare and return an error
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


