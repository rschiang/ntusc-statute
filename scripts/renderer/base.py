# renderer/base.py  - declare renderer base class
from statute import Chapter

class Renderer(object):

    # Public methods

    def render(self, act):
        pass

    # Internal methods

    def render_act(self, act):
        for article in act.articles:
            if isinstance(article, str):
                self.render_text(text=article)
            elif isinstance(article, Chapter):
                self.render_chapter(chapter=article)
            else:
                self.render_article(article=article)

    def render_text(self, text):
        pass

    def render_chapter(self, chapter):
        pass

    def render_article(self, article):
        for paragraph in article.subitems:
            self.render_paragraph(paragraph)

    def render_paragraph(self, paragraph):
        for subsection in paragraph.subitems:
            self.render_subsection(subsection)

    def render_subsection(self, subsection):
        for item in subsection.subitems:
            self.render_item(item)

    def render_item(self, item):
        pass
