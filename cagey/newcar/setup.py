# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = 'r1',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = ganji.settings']},
)
