import os
import sys
sys.path.insert(0, os.path.abspath('.'))  # This allows Sphinx to find your modules

project = 'Future Demand Coding Challenge'
copyright = '2025, Denis Tola'
author = 'Denis Tola'
release = '0.0.1'

extensions = [
    'sphinx.ext.autodoc',  # Enables docstring documentation
    'sphinx.ext.viewcode',  # Adds links to the source code in the generated docs
    'sphinx.ext.napoleon',  # Supports Google-style and NumPy-style docstrings
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Options for HTML output
html_theme = 'alabaster'
html_static_path = ['_static']
