# renderer/html.py - Renders to HTML5 statute
from .base import Renderer
from io import StringIO

class HtmlRenderer(Renderer):

    def render(self, act, buf=None):
        self.buf = buf or StringIO()
        self.render_act(act)
        return self.buf

    def render_act(self, act):
        buf = self.buf
        buf.write('<article class="act">\n')
        buf.write('<header>')
        buf.write(act.name)
        buf.write('</header>\n')
        buf.write('<ol class="history">\n')
        for h in act.history:
            buf.write('<li>')
            buf.write(h)
            buf.write('</li>\n')
        buf.write('</ol>\n')
        super().render_act(act)
        buf.write('</article>')

    def render_text(self, text):
        buf = self.buf
        buf.write('<p>')
        buf.write(text)
        buf.write('</p>\n')

    def render_chapter(self, chapter):
        buf = self.buf
        buf.write('<h5>{number}　{caption}</h5>\n'.format(**chapter.__dict__))

    def render_article(self, article):
        buf = self.buf
        buf.write('<h6 data-number="">{number}<span class="caption">（{caption}）</span></h6>\n'.format(**article.__dict__))
        if len(article.subitems) == 1:
            buf.write('<p>')
            buf.write(article.subitems[0].caption)
            buf.write('</p>\n')
        else:
            buf.write('<ol class="paragraphs">')
            super().render_article(article)
            buf.write('</ol>\n')

    def render_paragraph(self, paragraph):
        buf = self.buf
        buf.write('<li>')
        buf.write(paragraph.caption)
        buf.write('</li>\n')
        if paragraph.subitems:
            buf.write('<ol class="subsections">\n')
            super().render_paragraph(paragraph)
            buf.write('</ol>\n')

    def render_subsection(self, subsection):
        buf = self.buf
        buf.write('<li>')
        buf.write(subsection.caption)
        buf.write('</li>\n')
        if subsection.subitems:
            buf.write('<ol class="items">\n')
            super().render_subsection(subsection)
            buf.write('</ol>\n')

    def render_item(self, item):
        buf = self.buf
        buf.write('<li>')
        buf.write(item)
        buf.write('</li>\n')
