"""
This module handles the scheduling of crawling tasks using the APScheduler library.
The scheduler periodically runs the `start_full_crawl` function based on settings stored in the database.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from app.crawler.crawler import start_full_crawl
import logging
from app import create_app
from app.db.models import SchedulerSettings

# Initialize the background scheduler
scheduler = BackgroundScheduler()

# Set up logging to track the scheduler's status
logging.basicConfig(level=logging.INFO)

def start_scheduler():
    """
    Starts the background scheduler based on settings stored in the database.

    The scheduler will execute the `start_full_crawl` function periodically with an interval defined 
    by the `frequency_hours` setting from the `SchedulerSettings` table. The job is only added if the
    scheduler is enabled in the database.
    
    Steps:
    1. Creates a Flask app instance.
    2. Fetches scheduler settings from the database.
    3. If the scheduler is enabled, adds a job to the scheduler with the defined interval.
    4. Starts the scheduler.
    """
    
    app = create_app()  # Create the Flask app instance

    # Wrapper function to ensure start_full_crawl() runs within the Flask app context
    def run_in_app_context():
        with app.app_context():
            start_full_crawl()  # Call the crawling function

    # Fetch scheduler settings from the database
    settings = SchedulerSettings.query.first()

    if not settings:
        logging.error("Scheduler settings not found in the database.")
        return  # Stop if settings are not found

    # Check if the scheduler is enabled and add the job if so
    if settings.is_enabled:
        scheduler.add_job(
            func=run_in_app_context,
            trigger="interval",
            hours=settings.frequency_hours,  # Use the frequency_hours from the settings
            id="hourly_overview_crawl",  # A unique identifier for the job
            replace_existing=True  # Ensure any existing job with the same ID is replaced
        )
        scheduler.start()  # Start the scheduler
        logging.info(f"Scheduler started with frequency {settings.frequency_hours} hours.")
    else:
        logging.info("Scheduler is disabled. No job will be scheduled.")  # Log if disabled
