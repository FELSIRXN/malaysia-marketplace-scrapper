#!/usr/bin/env python3
"""
Setup configuration for Malaysia Marketplace Scraper package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            requirements.append(line)

setup(
    name='malaysia-marketplace-scraper',
    version='1.0.0',
    author='Malaysia Marketplace Scraper Team',
    author_email='your-email@example.com',
    description='Multi-platform e-commerce scraper for Malaysian marketplaces (Shopee, Lazada, Mudah)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/malaysia-marketplace-scraper',
    py_modules=[
        'main',
        'multi_platform_scraper',
        'base_scraper',
        'shopee_scraper',
        'lazada_scraper',
        'mudah_scraper',
        'facebook_marketplace_scraper',
        'tokopedia_scraper',
        'advanced_analyzer',
        'config',
        'logger'
    ],
    install_requires=requirements,
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'malaysia-scraper=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    keywords='scraper ecommerce malaysia shopee lazada mudah marketplace',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/malaysia-marketplace-scraper/issues',
        'Source': 'https://github.com/yourusername/malaysia-marketplace-scraper',
    },
)
