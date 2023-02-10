from setuptools import setup, find_packages


setup(
    name='mkdocs-snippets',
    version='1.0.0',
    description='Snippets for MkDocs',
    long_description='A plugin for MkDocs that adds the ability to include snippets in your documentation.',
    keywords='mkdocs',
    url='',
    author='CyberOtter',
    author_email='contact@betonquest.org',
    license='MIT',
    python_requires='>=2.7',
    install_requires=[
        'mkdocs>=1.0.4',
        'pyyaml>=6.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'snippets = src.plugin:Snippets'
        ]
    }
)
