from flask import Blueprint, jsonify, request
from app.crawler.crawler import start_full_crawl, crawl_article_page, store_article_and_versions

controller = Blueprint("controller", __name__)

@controller.route("/crawl", methods=["POST"])
def trigger_full_crawl():
    start_full_crawl()
    return jsonify({"message": "Full crawl triggered."}), 200

@controller.route("/crawl/article", methods=["POST"])
def trigger_article_crawl():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    article_data = crawl_article_page(url)
    if not article_data:
        return jsonify({"error": "Failed to crawl the article"}), 500

    store_article_and_versions(article_data)
    return jsonify({"message": "Article crawled and stored."}), 200
