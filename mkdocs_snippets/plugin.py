import io
import logging
import os.path
import re
from os import walk
from typing import Optional

import yaml
from mkdocs.exceptions import PluginError

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from mkdocs.config import config_options as option
from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page


class SnippetPluginConfig(Config):
    directory = option.Type(str, default="snippets")
    delimiter = option.Type(str, default="@")
    identifier = option.Type(str, default="Snippet")
    divider_char = option.Type(str, default=":")


class Snippets(BasePlugin[SnippetPluginConfig]):
    snippets = {}

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_config(self, config: MkDocsConfig) -> None:
        self.snippet_syntax_start = self.config.delimiter + self.config.identifier + self.config.divider_char
        self.snippet_syntax_pattern = re.compile(
            f"{self.snippet_syntax_start}(.*){self.config.divider_char}(.*){self.config.delimiter}")

    # Builds a snippet index based on all files in the snippets_directory
    def on_files(self, files: Files, *, config: MkDocsConfig) -> Optional[Files]:
        snippets_dir = config.docs_dir + "/" + self.config.directory
        for (dirpath, dirnames, filenames) in walk(snippets_dir):
            for filename in filenames:
                if not filename.endswith(".yml"):
                    continue
                file_path = dirpath + "/" + filename
                file = open(file_path, "r")
                file_snippets = read_snippets_from_file(file.read())

                snippet_file_address = file_path.split(snippets_dir)[1].strip("/").strip("\\")
                snippet_address = snippet_file_address.split(".")[0]

                self.snippets[snippet_address] = file_snippets
        return files

    def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files) -> Optional[str]:
        if not page.is_page:
            return markdown
        mkdown = self.resolve_snippet(markdown, page)
        return mkdown

    def resolve_snippet(self, markdown: str, page: Page) -> str:
        matches = re.findall(self.snippet_syntax_pattern, markdown)
        if matches is not None:
            for match in matches:
                snippet_address = match[0]
                snippet_id = match[1]

                snippet_file = f"{self.config.directory}/{snippet_address}.yml"
                if snippet_address not in self.snippets:
                    raise PluginError(f"The page '{page.title}' tried to load a snippet from the non-existent file"
                                      f" '{snippet_file}'!")

                if snippet_id not in self.snippets[snippet_address]:
                    raise PluginError(f"The page '{page.title}' contains the unknown snippet id '{snippet_id}' from "
                                      f"snippet file '{snippet_file}'. However, the snippet file does not contain this "
                                      f"snippet!")

                snippet_content = self.snippets[snippet_address][snippet_id]

                snippet_content = relativize_links(snippet_content, page.abs_url, snippet_id)

                snippet_content = self.preserve_indentation(snippet_content, markdown)

                # Resolve nested snippets
                re.findall(self.snippet_syntax_pattern, snippet_content)
                if matches is not None:
                    snippet_content = self.resolve_snippet(snippet_content, page)

                snippet_call = f"{self.snippet_syntax_start}{snippet_address}{self.config.divider_char}{snippet_id}" \
                               f"{self.config.delimiter}"
                markdown = markdown.replace(snippet_call, snippet_content)

        return markdown

    def preserve_indentation(self, snippet_content: str, markdown: str) -> str:
        indent_pattern = re.compile(rf"^\s+(?={self.snippet_syntax_pattern.pattern})", re.RegexFlag.MULTILINE)
        indent = re.search(indent_pattern, markdown)
        if indent is not None and len(indent.group(0)) > 1:
            indent = indent.group(0)
            snippet_content = snippet_content.replace("\n", "\n" + indent)
        return snippet_content


def read_snippets_from_file(file_content) -> dict[str, str]:
    snippets = {}
    obj = yaml.safe_load(file_content)
    if obj is not None:
        for node in obj:
            snippets[node] = obj[node]
    return snippets


markdown_link_pattern = re.compile(r"\[(.*)\]\((.*(#.*)?)\)")


def relativize_links(snippet_content, current_path, snippet_id) -> str:
    matches = re.findall(markdown_link_pattern, snippet_content)
    for match in matches:
        link_text = match[0]
        link = match[1]
        heading_link = match[2]

        if "://" in link:
            continue

        if link.startswith("../"):
            raise PluginError(f"The link '{link}' in the snippet '{snippet_id}' is a relative link! "
                              f"Relative links in snippets cannot be resolved correctly. Please read the usage section"
                              f" of the snippet plugin in README.md to learn how to format links.")

        link_and_filetype = link.split(".")

        if len(link_and_filetype) == 1:
            raise PluginError(f"The link '{link}' in the snippet '{snippet_id}' does not have a file type! "
                              f"Is it an absolute link? Those are not supported by mkdocs and may break in the deployed"
                              f"docs! Please read the usage section in README.md to learn how to format links.")

        link_without_filetype = link_and_filetype[0]
        filetype = link_and_filetype[1]

        if current_path is None:
            # The docs are hosted in the root
            current_path_without_filename = ''
        else:
            current_path_without_filename = current_path.rsplit("/", 2)[0]

        current_path_without_filename = remove_mike_version_from_path(current_path_without_filename)

        relative_link = os.path.relpath(f"docs/{link_without_filetype}", f"docs/{current_path_without_filename}")

        relative_link += "." + filetype
        if heading_link is not None:
            relative_link += heading_link
        relative_link = relative_link.replace("\\", "/")

        if relative_link.startswith("docs/"):
            relative_link = relative_link[5:]

        snippet_content = snippet_content.replace(f"[{link_text}]({link})", f"[{link_text}]({relative_link})")
    return snippet_content


mike_version_prefix_pattern = re.compile("(/[^/]*/)")


def remove_mike_version_from_path(current_path_without_filename):
    env = os.environ.copy()
    if "MIKE_DOCS_VERSION" in env:
        match = re.search(mike_version_prefix_pattern, current_path_without_filename)
        if match:
            current_path_without_filename = current_path_without_filename[match.end():]
    return current_path_without_filename
