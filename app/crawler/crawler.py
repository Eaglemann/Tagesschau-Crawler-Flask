"""
This module handles all the crawling logic for the Tagesschau site.

- Crawls the overview page to grab all article URLs.
- Visits each article and extracts key data (headline, subheadline, body).
- Saves data in DB, with versioning so we don't store duplicates.
"""

import requests
from bs4 import BeautifulSoup
from app.db.models import db, Article, ArticleVersion
from datetime import datetime
from hashlib import md5
from dotenv import load_dotenv
import os
import json
import logging

# Basic logging to track the crawler's activity
logging.basicConfig(level=logging.INFO)

load_dotenv()

# Base URL comes from environment config to avoid hardcoding the value
BASE_URL = os.getenv("BASE_URL")

# --- Crawl the overview page to collect article URLs ---
def crawl_links_overview_page():
    """
    Makes a GET request to the overview page and scrapes all article URLs using BeautifulSoup.
    We search for anchor tags with class 'teaser__link' to get the article links.
    """
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print("Failed")
        return []
    
    soup = BeautifulSoup(response.text, "lxml")

    article_links = []
    for link in soup.find_all("a", class_="teaser__link"):
        article_url = link.get("href")
        # Make the URL absolute if it's relative
        if article_url and article_url.startswith("/"):
            article_url = BASE_URL + article_url
        article_links.append(article_url)

    return article_links


# --- Crawl individual article pages ---
def crawl_article_page(url):
    """
    Given a URL, fetches the article page and extracts important information like 
    headline, subheadline, and the article body. The article body is taken from 
    the JSON-LD structured data tag, which is more reliable than parsing HTML directly.
    """
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, "lxml")

    headline = soup.find("meta", property="og:title")["content"]
    subheadline = soup.find("meta", property="og:description")["content"]

    # The full article text is embedded in a JSON-LD structured data tag
    script_tag = soup.find("script", type="application/ld+json")
    article_json = json.loads(script_tag.string)
    full_text = article_json.get("articleBody", "").strip()

    last_updated = datetime.now()

    return {
        "headline" : headline,
        "subheadline": subheadline,
        "full_text": full_text,
        "last_updated": last_updated,
        "url" : url,
    }


# --- Store article and version changes ---
def store_article_and_versions(article_data):
    """
    Saves the article to the database and adds a new version if the content has changed.
    We use a hash of the article text to check if the content has changed.
    """
    url = article_data.get("url")
    headline = article_data.get("headline")
    subheadline = article_data.get("subheadline")
    full_text = article_data.get("full_text")
    last_updated = article_data.get("last_updated", datetime.utcnow())

    if not url or not full_text:
        logging.info("Missing URL or full_text. Skipping article.")
        return

    # Check if the article already exists in the database
    article = Article.query.filter_by(url=url).first()

    # If article doesn't exist, create a new one
    if not article:
        article = Article(url=url)
        db.session.add(article)
        db.session.commit()
        logging.info(f"New article created: {url}")

    # Hash the content to compare if it has changed
    current_hash = md5(full_text.encode("utf-8")).hexdigest()

    # Get the latest version of the article
    previous_version = (
        ArticleVersion.query
        .filter_by(article_id=article.id)
        .order_by(ArticleVersion.last_updated.desc())
        .first()
    )

    # If the content hasn't changed, skip creating a new version
    if previous_version and previous_version.content_hash == current_hash:
        logging.info(f"Article {url} has no changes. Skipping versioning.")
        return

    # Get the last version number to create the next version
    last_version = (
        ArticleVersion.query
        .filter_by(article_id=article.id)
        .order_by(ArticleVersion.version_number.desc())
        .first()
    )
    new_version_number = 1 if not last_version else last_version.version_number + 1

    # Save the new version
    article_version = ArticleVersion(
        article_id=article.id,
        version_number=new_version_number,
        headline=headline,
        subheadline=subheadline,
        full_text=full_text,
        last_updated=last_updated,
        content_hash=current_hash
    )

    db.session.add(article_version)
    db.session.commit()
    logging.info(f"New version {new_version_number} added for article: {url}")


# --- Entrypoint to run the full crawling process ---
def start_full_crawl():
    """
    Runs the entire crawl process:
    1. Collect article links from the overview page.
    2. Visit each article page.
    3. If the article has changed, save the new version to the database.
    """
    logging.info("Full crawl started at: %s", datetime.now())
    article_links = crawl_links_overview_page()

    for article_url in article_links:
        article_data = crawl_article_page(article_url)
        if article_data:
            store_article_and_versions(article_data)
