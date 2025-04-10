import requests
from bs4 import BeautifulSoup
from app.db.models import db, Article, ArticleVersion
from datetime import datetime
from hashlib import md5
from dotenv import load_dotenv
import os
import json
import logging


logging.basicConfig(level=logging.INFO)

load_dotenv()


BASE_URL = os.getenv("BASE_URL")

#crawl the overview page  to get all individual article links
def crawl_links_overview_page():
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print("Failed")
        return []
    
    #Parse the html content with beautifulSoup
    soup = BeautifulSoup(response.text, "lxml")

    #find all article links
    article_links = []

    for link in soup.find_all("a", class_="teaser__link"):
        article_url = link.get("href")
        if article_url and article_url.startswith("/"):
            article_url = BASE_URL + article_url
        article_links.append(article_url)

    return article_links

#Crawl an individual article page to extract its data
def crawl_article_page(url):

    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, "lxml")


    headline = soup.find("meta", property="og:title")["content"]
    subheadline = soup.find("meta", property="og:description")["content"]

    # Get full article body (from JSON-LD structured data script tag)
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

# Store article and its versions in the database, ensuring versioning 
def store_article_and_versions(article_data):

    # Extracting required fields from article_data
    url = article_data.get("url")
    headline = article_data.get("headline")
    subheadline = article_data.get("subheadline")
    full_text = article_data.get("full_text")
    last_updated = article_data.get("last_updated", datetime.utcnow())

    if not url or not full_text:
        logging.info("Missing URL or full_text. Skipping article.")
        return

    # Check if the article already exists
    article = Article.query.filter_by(url=url).first()

    # If article doesn't exist, create a new one with the extracted data
    if not article:
        article = Article(
            url=url,
            headline=headline,
            subheadline=subheadline,
            full_text=full_text,
            last_updated=last_updated
        )
        db.session.add(article)
        db.session.commit()
        logging.info(f"New article created: {url}")

    # Check if this version is different from the previous one by hashing the content,
    # for a much faster comparison 
    current_hash = md5(full_text.encode("utf-8")).hexdigest()

    # Get the lastest version of the article
    previous_version = ArticleVersion.query.filter_by(article_id=article.id).order_by(ArticleVersion.last_updated.desc()).first()

    # If the hash matches the previous version just skip creating a new version
    if previous_version and previous_version.content_hash == current_hash:
        logging.info(f"Article {url} has no changes. Skipping versioning.")
        return

    # Get the last version's number to determine the next version number, 
    # helps to keep track for a better versioning
    last_version = (
        ArticleVersion.query
        .filter_by(article_id=article.id)
        .order_by(ArticleVersion.version_number.desc())
        .first()
    )

    new_version_number = 1 if not last_version else last_version.version_number + 1
    
    # Create a new version for the article
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

#Run the crawler to get the links from the overview page and then all individual articles
def start_full_crawl ():

    article_links = crawl_links_overview_page()

    for article_url in article_links:
        article_data = crawl_article_page(article_url)
        if article_data:
            store_article_and_versions(article_data)

