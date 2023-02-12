# Mkdocs Snippets Plugin

This plugin allows you to include snippets into your mkdocs documentation.

## Features

* Multiple snippets per file thanks to YAML syntax.
* Snippets are loaded from any (nested) directory inside the configured `snippets_dir`.
  * This allows you to organize your snippets in a way that makes sense for you. 
* Recursively include snippets in snippets.
* Links in snippets are automatically converted to relative links based on the snippet's location.
  * This allows you to use links in your snippets without having to worry about the snippet's location.
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
It is allowed to have any amount of files and subdirectories inside the snippet directory.

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
The default snippet syntax is `@Snippet:snippetFile:snippetID`.

### Links in Snippets
Links in snippets are automatically converted to relative links based on where the snippet is used.
This allows you to use links in your snippets without having to worry that the snippet might be used in a directory
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
