# tests/test_controller.py
from unittest.mock import patch

def test_trigger_full_crawl(client):
    with patch("app.controller_api.controller.start_full_crawl") as mock_crawl:
        response = client.post("/controller/crawl")
        assert response.status_code == 200
        assert response.json == {"message": "Full crawl triggered."}
        mock_crawl.assert_called_once()

def test_trigger_article_crawl_success(client):
    fake_url = "http://example.com/article"
    mock_data = {
        "headline": "Test Headline",
        "subheadline": "Test Subheadline",
        "full_text": "Some text here",
        "last_updated": "2024-01-01T00:00:00",
        "url": fake_url,
    }

    with patch("app.controller_api.controller.crawl_article_page", return_value=mock_data):
        with patch("app.controller_api.controller.store_article_and_versions") as mock_store:
            response = client.post("/controller/crawl/article", json={"url": fake_url})
            assert response.status_code == 200
            assert response.json == {"message": "Article crawled and stored."}
            mock_store.assert_called_once_with(mock_data)

def test_trigger_article_crawl_missing_url(client):
    response = client.post("/controller/crawl/article", json={})
    assert response.status_code == 400
    assert response.json == {"error": "URL is required"}

def test_trigger_article_crawl_failed_crawl(client):
    with patch("app.controller_api.controller.crawl_article_page", return_value=None):
        response = client.post("/controller/crawl/article", json={"url": "http://fake.url"})
        assert response.status_code == 500
        assert response.json == {"error": "Failed to crawl the article"}
