import os.path
from urllib.parse import urlsplit, unquote
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
import regex as re


class CaseInsensitiveFiles(BasePlugin):
    # Reference: https://stackoverflow.com/questions/67940820/how-to-extract-markdown-links-with-a-regex
    pattern = re.compile(
        r"(\[((?:[^[\]]+|(?1))+)\])(\(((?:[^()]+|(?3))+)\))", flags=re.IGNORECASE
    )

    def on_page_markdown(
        self, markdown: str, page: Page, config: MkDocsConfig, files: Files
    ):
        # Duplicated code from mkdocs.structure.pages._RelativePathTreeprocessor path_to_url
        # TODO: Figure out a way to patch mkdocs' function
        links: list[tuple[str, str, str]] = re.findall(self.pattern, markdown)
        for _, text, _, link in links:
            actual_link, sep, inner_link = link.partition("#")
            scheme, netloc, path, query, fragment = urlsplit(actual_link)
            # Ignore URLs unless they are a relative link to a source file.
            # AMP_SUBSTITUTE is used internally by Markdown only for email.
            # No '.' in the last part of a path indicates path does not point to a file.
            if scheme or netloc or query or fragment:
                continue

            # Determine the filepath of the target.
            target_uri = os.path.join(os.path.dirname(page.file.src_uri), unquote(path))
            target_uri = os.path.normpath(target_uri).lstrip("/")

            # Validate that the target exists in files collection.
            target_file = files.get_file_from_path(target_uri)
            if target_file is None:
                # Check if case-insensitive file exists
                for key, value in files.src_uris.items():
                    stripped = os.path.normpath(key).lstrip("/")
                    if stripped.casefold() == target_uri.casefold():
                        markdown = re.sub(
                            re.escape(f"[{text}]({actual_link}{sep}{inner_link})"),
                            key,
                            markdown,
                        )
                        break
        return markdown
