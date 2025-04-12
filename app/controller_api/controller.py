from flask import Blueprint, jsonify, request
from app.crawler.crawler import start_full_crawl, crawl_article_page, store_article_and_versions
from app.db.models import SchedulerSettings, db



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


@controller.route("/scheduler/settings", methods=["PUT", "GET"])
def manage_scheduler_settings():
    if request.method == "GET":
        # Get the current scheduler settings
        settings = SchedulerSettings.query.first()
        if not settings:
            # If no settings exist, create a default one
            settings = SchedulerSettings(frequency_hours=1, is_enabled=True)  # Default values
            db.session.add(settings)
            db.session.commit()

        return jsonify({"frequency_hours": settings.frequency_hours, "is_enabled": settings.is_enabled}), 200

    elif request.method == "PUT":
        # Update scheduler settings
        data = request.get_json()

        # Retrieve values from the request
        frequency_hours = data.get("frequency_hours")  # Ensure this matches the JSON key
        is_enabled = data.get("is_enabled")  # Ensure this matches the JSON key

        # Validate input
        if frequency_hours is None or is_enabled is None:
            return jsonify({"error": "Missing required fields: 'frequency_hours' and 'is_enabled'"}), 400

        # Retrieve or create the settings
        settings = SchedulerSettings.query.first()
        if settings:
            settings.frequency_hours = frequency_hours
            settings.is_enabled = is_enabled
        else:
            # Create new settings if none exist
            settings = SchedulerSettings(frequency_hours=frequency_hours, is_enabled=is_enabled)

        # Add to session and commit
        db.session.add(settings)
        db.session.commit()

        return jsonify({"message": "Scheduler settings updated."}), 200