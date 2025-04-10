from apscheduler.schedulers.background import BackgroundScheduler
from app.crawler.crawler import start_full_crawl
import logging
from app import create_app
from app.db.models import SchedulerSettings

scheduler = BackgroundScheduler()

logging.basicConfig(level=logging.INFO)

def start_scheduler():
    app = create_app()  # Create the Flask app instance

    # Wrapper function to ensure start_full_crawl() runs within the app context
    def run_in_app_context():
        with app.app_context():
            start_full_crawl()

    # Fetch scheduler settings from the database
    settings = SchedulerSettings.query.first()

    if not settings:
        logging.error("Scheduler settings not found in the database.")
        return

    if settings.is_enabled:
        scheduler.add_job(
            func=run_in_app_context,
            trigger="interval",
            hours=settings.frequency_hours,
            id="hourly_overview_crawl",
            replace_existing=True
        )
        scheduler.start()
        logging.info(f"Scheduler started with frequency {settings.frequency_hours} hours.")
    else:
        logging.info("Scheduler is disabled. No job will be scheduled.")
