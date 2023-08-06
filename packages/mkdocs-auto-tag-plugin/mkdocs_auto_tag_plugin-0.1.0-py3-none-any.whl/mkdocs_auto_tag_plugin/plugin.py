import fnmatch
import os
import re
# pip dependency
import mkdocs
from mkdocs.config.config_options import Type
from mkdocs.plugins import BasePlugin
from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page
from mkdocs.structure.files import Files
# local files
from . import warning
from .utils import translate_glob_to_regex


class MyConfig(Config):
    enabled = Type(bool, default=True)
    globs = Type(dict, default={})


class Plugin(BasePlugin[MyConfig]):
    def on_config(self, config: MkDocsConfig, **kwargs) -> Config:
        """
        Called once when the config is loaded.
        It will make modify the config and initialize this plugin.
        """
        self.compiled_globs: list[tuple[re.Pattern,str]] = []

        if self.config.globs:
            for pattern, tag_name in self.config.globs.items():
                # 
                compiled_pattern = re.compile(translate_glob_to_regex(pattern), re.IGNORECASE)
                self.compiled_globs.append((compiled_pattern, tag_name))
                # print("Rule:", pattern, "->", tag_name)
        else:
            warning("No rules were specified")
        return config


    def on_page_markdown(self, markdown: str, page: Page, config: MkDocsConfig, files: Files) -> str:
        self.handle_page(page, config)
        return markdown


    def handle_page(self, page: Page, config: MkDocsConfig) -> None:
        """
        The page_markdown event is called after the page's markdown is loaded from file and can be used to alter the Markdown source text. The meta- data has been stripped off and is available as page.meta at this point.
        See: https://www.mkdocs.org/dev-guide/plugins/#on_page_markdown
        """
        try:
            if self.config.enabled:
                file_path = page.file.src_path
                # If necessary convert the paths to Unix format (so that it works cross platform. And backslashes are always a pain to work with)
                if os.path.sep != "/":
                    file_path = file_path.replace(os.path.sep, "/")
                # print(file_path)
                for re_pattern, tag_name in self.compiled_globs:
                    if re_pattern.fullmatch(file_path):
                        if "tags" in page.meta:
                            page.meta["tags"].append(tag_name)
                        else:
                            page.meta["tags"] = [tag_name]
                        # print("--> matches", re_pattern.pattern, ":", tag_name)
        except Exception as error:
            raise mkdocs.exceptions.PluginError(str(error))


