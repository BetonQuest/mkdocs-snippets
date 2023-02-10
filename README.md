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
Consider adding the plugin to a `requirements.txt` file alongside other Python dependencies for your project.

## Configuration
Add the plugin to your `mkdocs.yml` file:
```yaml
plugins:
  - search
  - snippets
```

The plugin will load snippets from the default directory `snippets` which must be inside your documentation directory.
The default snippet syntax is `@Snippet:snippetFile:snippetID`.


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
It is recommended to use the mkdocs-exclude plugin to exclude the snippet directory from the documentation build.

```yaml
plugins:
  - search
  - exclude:
      glob:
        - snippets/*
  - snippets:
    directory: "mySnippetDirectory"
    delimiter: "|"
    identifier: "snip"
    divider_char: ">"
```

## Usage

### Snippet Syntax
The default snippet syntax is `@snippet:snippetFile:snippetID`.

### Links in Snippets
Links in snippets are automatically converted to relative links based on the snippet's location.
This allows you to use links in your snippets without having to worry about the snippet's location.
Therefore, links in the snippet must be written as if they were in the root of the documentation directory.