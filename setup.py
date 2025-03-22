from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'snippets = src.mkdocs_snippets.plugin:Snippets'
        ]
    }
)
