from mkdocs_snippets.plugin import relativize_links


class TestClass:

    def test_skip_external_links(self):
        snippet_content = '''\
        [Link](https://www.betonquest.org)
        '''
        result = relativize_links(snippet_content, "current_path", "snippet_id")
        assert result == snippet_content, "External HTTP links were changed but must be untouched."
