# renderer.py  - prettify and renders HTML statute text
from io import StringIO
from statute import Chapter

class Renderer(object):

    def render(self, act, buf=None):
        self.buf = buf or StringIO()
        self.render_act(act)
        return self.buf

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

class MarkdownRenderer(Renderer):

    def render_act(self, act):
        buf = self.buf
        buf.write('# ')
        buf.write(act.name)
        buf.write('\n\n')
        for h in act.history:
            buf.write('* ')
            buf.write(h)
            buf.write('\n')
        buf.write('\n')
        super().render_act(act)

    def render_text(self, text):
        buf = self.buf
        buf.write('> ')
        buf.write(text)
        buf.write('\n')

    def render_chapter(self, chapter):
        self.buf.write('## {number} {caption}\n'.format(**chapter.__dict__))

    def render_article(self, article):
        self.buf.write('  ### {number} ({caption})\n'.format(**article.__dict__))
        super().render_article(article)

    def render_paragraph(self, paragraph):
        buf = self.buf
        buf.write(' ' * 4)
        buf.write('- ')
        buf.write(paragraph.caption)
        buf.write('\n')
        super().render_paragraph(paragraph)

    def render_subsection(self, subsection):
        buf = self.buf
        buf.write(' ' * 6)
        buf.write('- ')
        buf.write(subsection.caption)
        buf.write('\n')
        super().render_subsection(subsection)

    def render_item(self, item):
        buf = self.buf
        buf.write(' ' * 8)
        buf.write('- ')
        buf.write(item)
        buf.write('\n')
