# setup.py
from setuptools import setup

config = {
    'name': 'hprint',
    'license': 'MIT',
    'description': 'Print python object in table/json format',
    'author' : 'Hao Ruan',
    'author_email': 'ruanhao1116@gmail.com',
    'keywords': ['utils', 'print', 'json'],
    'version': '1.0',
    'packages': ['hprint'],
    'install_requires': [
        'tabulate',
    ],
    'python_requires': ">=3.7, <4",
    'setup_requires': ['wheel'],
    'classifiers': [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
    ],
}

setup(**config)
# end-of-setup.py
