from mkdocs.structure.files import File, Files
from mkdocs.config import Config
from mkdocs.structure.pages import Page
from mkdocs.structure.toc import get_toc


def monkey_patch():
    # Monkey patch the File class so that it recognizes .jinja
    # files as documentation pages
    _file_is_documentation_page = File.is_documentation_page
    def is_documentation_page(self: File) -> bool:
        return self.src_uri.endswith('.jinja') or _file_is_documentation_page(self)
    File.is_documentation_page = is_documentation_page

    # Monkey patch the Page class so that it allows skipping Markdown
    # rendering in case the source is .jinja
    _page_render = Page.render
    def render(self, config: Config, files: Files):
        if self.file.src_uri.endswith('.jinja'):
            if self.markdown is None:
                raise RuntimeError("`markdown` field hasn't been set (via `read_source`)")
            self.content = self.markdown
            self.toc = get_toc([])
        else:
            _page_render(self, config, files)
    Page.render = render
