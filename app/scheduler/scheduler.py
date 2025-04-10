from apscheduler.schedulers.background import BackgroundScheduler
from app.crawler.crawler import start_full_crawl
import logging
from app import create_app

scheduler = BackgroundScheduler()

logging.basicConfig(level=logging.INFO)

def start_scheduler():
    app = create_app() 

    # Wrapper function just to make sure that start_full_crawl() will run inside app_context
    def run_in_app_context():
        with app.app_context():
            start_full_crawl()

    # Schedule the job every 60 minutes
    scheduler.add_job(
        func=run_in_app_context,  # Use the wrapper function
        trigger="interval",
        minutes=60,
        id="minute_overview_crawl",
        replace_existing=True
    )
    scheduler.start()
    logging.info("Scheduler started.")
