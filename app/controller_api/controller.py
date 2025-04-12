"""
This module handles all the logic for managing the crawling process and scheduling settings.

- Triggers a full crawl of all articles.
- Triggers the crawl of an individual article by its URL.
- Retrieves and updates the scheduler settings for periodic crawling.
"""

from flask import Blueprint, jsonify, request
from app.crawler.crawler import start_full_crawl, crawl_article_page, store_article_and_versions
from app.db.models import SchedulerSettings, db

# Blueprint to handle routes for crawling and scheduler settings
controller = Blueprint("controller", __name__)

# --- Trigger a full crawl of all articles ---
@controller.route("/crawl", methods=["POST"])
def trigger_full_crawl():
    """
    Triggers a full crawl of all articles. It calls the 'start_full_crawl' function,
    which scrapes the overview page, fetches each article, and stores the data in the database.
    """
    start_full_crawl()
    return jsonify({"message": "Full crawl triggered."}), 200


# --- Trigger crawl of an individual article ---
@controller.route("/crawl/article", methods=["POST"])
def trigger_article_crawl():
    """
    Triggers the crawl of an individual article by its URL. The URL is passed as JSON in the request body.
    The function fetches the article's content, extracts key data (headline, subheadline, body),
    and stores it in the database if new or updated.
    """
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    article_data = crawl_article_page(url)
    if not article_data:
        return jsonify({"error": "Failed to crawl the article"}), 500

    store_article_and_versions(article_data)
    return jsonify({"message": "Article crawled and stored."}), 200


# --- Get or update scheduler settings ---
@controller.route("/scheduler/settings", methods=["PUT", "GET"])
def manage_scheduler_settings():
    """
    Manages the settings for the crawler's scheduling frequency and its enabled status.

    - **GET**: Retrieves the current scheduler settings from the database. If none exist,
      default settings are created (frequency: 1 hour, enabled: True).
    - **PUT**: Updates the scheduler settings based on the provided JSON in the request body.
      The settings include 'frequency_hours' (how often the crawl should occur) and 'is_enabled' 
      (whether the scheduler is active).
    """
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
