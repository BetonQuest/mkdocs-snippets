# Mkdocs Snippets Plugin

This plugin allows you to include snippets in your mkdocs documentation.
It is available as a [PyPI package](https://pypi.org/project/mkdocs-snippets/).

## Features

* Organize your snippets in a way that makes sense for you: 
  * Multiple snippets per file thanks to YAML syntax.
  * Snippets are loaded from any (nested) directory inside the configured `snippets_dir`.
  * Recursively include snippets in snippets!
* Documentation links in snippets are automatically converted to relative links based on the snippet's location.
  * This allows you to link to other documentation pages from your snippets without having to worry about the snippet's location.
  * Also works with `mike`!
* Snippets preserve the indentation of the snippet call.
  * This allows you to use snippets in lists and code blocks without having to worry about indentation. 
* Customizable snippet syntax.

## Installation
`pip install mkdocs-snippets`

`pip install mkdocs-exclude` (recommended)

Consider adding the plugins to a `requirements.txt` file alongside other Python dependencies for your project.

## Setup
Add the plugin to your `mkdocs.yml` file:
It is recommended to use the `mkdocs-exclude` plugin to exclude the snippet directory from the documentation build.
This will save you from a lot of warnings about files that are not referenced in the `nav` configuration.
```yaml
plugins:
  - search
  - exclude:
      glob:
        - snippets/*
  - snippets
```

## Usage
The plugin will load snippets from the default directory `snippets` which must be inside your documentation directory.
It is allowed to have any number of files and subdirectories inside the snippet directory.

These files must be in the YAML format.
```yaml
mySnippet: |- 
    This is a snippet.
    It can contain multiple lines.

# |- is the YAML Multiline Indicator
myOtherSnippet: |-
    This is another snippet. 
```
All top level keys in the snippet file are treated as snippets. Every key is a snippet ID.

### Snippet Syntax
The default snippet syntax is `@Snippet:snippetFile:snippetID@`.

### Links in Snippets
Internal documentation links in snippets are automatically converted to relative links based on where the snippet is used.
This allows you to use documentation links in your snippets without having to worry that the snippet might be used in a directory
in which the link does not work.
Therefore, links in the snippet must be written as if they were in the root of the documentation directory.

#### Example
Consider the following documentation structure (`docs/` is the documentation's root directory):

`docs/API/Overview.md`

`docs/API/Client/Cookbook.md`

A snippet would look like this:
```yaml
mySnippet: |-
    This is a snippet.
    It contains a link to the [API Overview](API/Overview.md).
myOtherSnippet: |-
    This is another snippet.
    It contains a link to the [Client API Cookbook](API/Client/Cookbook.md).
```
No leading slashes or relative paths are allowed. The file type (`.md`) must be specified.
The snippets can now be used in any file without the links breaking.

## Configuration

If you want to customize the snippet syntax or directory, you can do so by adding the following configuration:
```yaml
plugins:
  - search
  - snippets:
    directory: "mySnippetDirectory"
    delimiter: "|"
    identifier: "snip"
    divider_char: ">"
```

## Contributing
This section is for contributors and maintainers.

### Setup Dev Environment

```bash
 pip install -r requirements/dev-requirements.txt
 pip install -r requirements/requirements.txt
```

### Releasing 
To release a new version of the plugin, follow the steps in the official Python [packaging guide](https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives).

### Dependency Management
To manage dependencies, we use [pip-tools](https://github.com/jazzband/pip-tools) to generate `requirements.txt`/`dev-requirements.txt` files from `requirements.in`/`dev-requirements.in`.

To update your local environment with the latest dependencies, run:
```bash
pip-sync requirements/requirements.txt requirements/dev-requirements.txt
```
