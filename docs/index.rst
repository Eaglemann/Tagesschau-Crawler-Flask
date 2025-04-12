.. Future Demand Coding Challenge documentation master file, created by
   sphinx-quickstart on Thu Apr 13 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Future Demand Coding Challenge documentation!
============================================================

This is the documentation for the Future Demand Coding Challenge project.

Contents
=========
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   installation
   usage
   code_documentation  

Introduction
============
This project is the Future Demand Coding Challenge.

Installation
============
To install the project, clone the repository and install dependencies:

1. Clone the repository:
   git clone https://github.com/eaglemann/future-demand-challange.git

2. Install the required dependencies:
   pip install -r requirements.txt

3. Set up the database and configure any necessary environment variables.

4. Run the app
   python run.py

5. Run with Docker (Optional)
   docker compose build
   docker compose up

6. Run Tests (Optional)
   pytest tests

Usage
=====
After running the project, navigate to localhost:5000/swagger for API documentation.

Code Documentation
==================
.. automodule:: app.crawler.crawler
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: app.explorer_api.explorer
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: app.controller_api.controller
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: app.scheduler.scheduler
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: app.db.models
   :members:
   :undoc-members:
   :show-inheritance:
