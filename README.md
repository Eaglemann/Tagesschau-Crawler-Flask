# FutureDemand-CC

This is a web scraping and article versioning application built with Flask, PostgreSQL, Docker, and various Python libraries. The application crawls news articles, stores them in a PostgreSQL database, and tracks versions of articles whenever changes occur. Additionally, it provides an API for triggering crawls and retrieving stored articles.

## Features

- Full web scraping (crawler) for articles from external sources.
- Versioning system to store and track updates to articles.
- REST API with endpoints for triggering crawls and retrieving article versions.
- Dockerized environment for easy setup and deployment.
- Automated testing with pytest.

## Tech Stack

- **Backend**: Flask, Python 3.x
- **Database**: PostgreSQL
- **Web Scraping**: Custom crawler logic implemented in Python.
- **API**: Flask-based REST API with endpoints for managing crawls and article versions.
- **Testing**: Pytest for unit testing.
- **Docker**: Containerized application using Docker.
- **Environment Variables**: `.env` file for configuration (database URI, secret key, etc.).

## Installation

Follow these steps to get the application up and running on your local machine:

### Prerequisites

- Docker and Docker Compose installed.
- Python 3.x installed if you prefer running the app locally without Docker.
- PostgreSQL running locally or using an online PostgreSQL service.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Eaglemann/future-demand-challange.git
cd future-demand-challange
```

### Step 2: Set Up Environment Variables

Create a .env file in the root directory and add your PostgreSQL database connection URI and Flask secret key. Example:

```bash
SQLALCHEMY_DATABASE_URI=postgresql://user:password@host:port/dbname
SECRET_KEY=your-secret-key-here
```

### Step 3: Run the Application Locally (Without Docker)

Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### Step 4: Docker Setup (Optional)

You can run the application with Docker for an isolated environment.

```bash
docker compose build
docker compose up
```


### Step 5: Test the app

The app will be available at 
```bash
http://localhost:5000/swagger
```

### Step 6 : Run Tests (Optional)

```bash
pytest tests
```
