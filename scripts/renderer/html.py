# renderer/html.py - Renders to HTML5 statute
import re
from .base import Renderer
from io import StringIO
from statute import Chapter
from utils import normalize_spaces

RE_ARTICLE_NUMBERING = re.compile(r'^第([〇ㄧ一二三四五六七八九十]+)條(之[〇ㄧ一二三四五六七八九十]+)?')
RE_ATTACHMENT_NUMBERING = re.compile(r'^附件（?([〇ㄧ一二三四五六七八九十]+)）?')
RE_SUBSECTION_NUMBERING = re.compile(r'^[〇ㄧ一二三四五六七八九十]+、\s*')
RE_ITEM_NUMBERING = re.compile(r'^\([〇ㄧ一二三四五六七八九十]+\)\s*')
RE_DELETED_FORMAT = re.compile(r'^[（\(]刪除[\)）]')
RE_EMPHASIS_FORMAT = re.compile(r'(（(編按|例如|備註|附註)：[^）]+）)')
RE_NUMERIC_DATE_FORMAT = re.compile(r'^(\d+)\.(\d+)\.(\d+)\s*')

def apply_emphasis(text):
    return RE_EMPHASIS_FORMAT.sub(r'<span class="note">\1</span>', text)

class HtmlRenderer(Renderer):

    def __init__(self, buf=None):
        self.buf = buf or StringIO()

    def render(self, act):
        self.render_head()
        self.render_act(act)
        self.render_tail()
        return self.buf

    def render_head(self, title=None, meta=None):
        buf = self.buf
        buf.write('<html lang="zh-Hant">\n'
                  '<head>\n'
                  '<meta charset="utf-8" />\n'
                  '<link rel="stylesheet" href="styles/common.css" />\n'
                  '<link rel="stylesheet" href="styles/print.css" media="print" />\n'
                  '<link rel="stylesheet" href="styles/screen.css" media="screen" />\n')
        if title:
            buf.write('<title>')
            buf.write(title)
            buf.write('</title>\n')
        if meta:
            for name, content in meta.items():
                buf.write('<meta name="')
                buf.write(name)
                buf.write('" content="')
                buf.write(content)
                buf.write('" />\n')
        buf.write('</head>\n'
                  '<body>\n')

    def render_tail(self):
        self.buf.write('</body>\n'
                       '</html>\n')

    def render_index_head(self):
        self.buf.write('<nav>\n'
                       '<header>目錄</header>\n')

    def render_index_category(self, category):
        buf = self.buf
        buf.write('<h4><a href="#{slug}">{caption}</a></h4>\n'.format(**category.__dict__))
        buf.write('<ul class="indices">\n')
        for act in category.acts:
            self.render_index_act(act)
        buf.write('</ul>\n')

    def render_index_act(self, act):
        buf = self.buf
        buf.write('<li><a href="#{bookmark_id}">{name}</a></li>\n'.format(**act.__dict__))
        chapters = [i for i in act.articles if isinstance(i, Chapter) and '章' in i.number]
        if chapters:
            buf.write('<ul class="chapters">\n')
            for chapter in chapters:
                self.render_index_chapter(chapter)
            buf.write("</ul>")

    def render_index_chapter(self, chapter):
        self.buf.write('<li><a href="#{bookmark_id}">{number}　{caption}</a></li>\n'.format(**chapter.__dict__))

    def render_index_tail(self):
        self.buf.write('</nav>\n')

    def render_section(self, slug, caption):
        self.buf.write('<section id="{slug}">\n'
                       '{caption}\n'
                       '</section>\n'.format(slug=slug, caption=caption))

    def render_category(self, category):
        self.buf.write('<section id="{slug}" data-category-label="{label}">\n'
                       '{caption}\n'
                       '</section>\n'.format(**category.__dict__))

    def render_act(self, act):
        buf = self.buf
        buf.write('<article class="act">\n')
        if act.bookmark_id:
            buf.write('<header id="')
            buf.write(act.bookmark_id)
            buf.write('">')
        else:
            buf.write('<header>')
        buf.write(act.name)
        buf.write('</header>\n')
        buf.write('<ol class="history">\n')
        for h in act.history:
            buf.write('<li>')
            h = h.replace('中華民國', '民國').replace('學生代表大會', '學代會')
            h = RE_NUMERIC_DATE_FORMAT.sub(r'民國\1年\2月\3日', h)
            h = normalize_spaces(h)
            h = apply_emphasis(h)
            buf.write(h)
            if h[-1] not in '>）)。':  # Consider <span> as well
                buf.write('。')
            buf.write('</li>\n')
        buf.write('</ol>\n')
        super().render_act(act)
        buf.write('</article>\n')

    def render_text(self, text):
        buf = self.buf
        buf.write('<p>')
        buf.write(apply_emphasis(text))
        buf.write('</p>\n')

    def render_chapter(self, chapter):
        buf = self.buf
        chapter.number = chapter.number.replace('ㄧ', '一')  # Those who mistaken bopomofo with kanji should apologize
        grade = 4 if '章' in chapter.number else 5
        if chapter.bookmark_id:
            buf.write('<h{} id="{}">'.format(grade, chapter.bookmark_id))
        else:
            buf.write('<h{}>'.format(grade))
        buf.write('{number}　{caption}</h{grade}>\n'.format(grade=grade, **chapter.__dict__))

    def render_article(self, article):
        buf = self.buf
        article.number = article.number.replace('ㄧ', '一')  # Those who mistaken bopomofo with kanji should apologize
        if '附件' in article.number:
            buf.write('<h6 data-appendix data-number="')
            buf.write(RE_ATTACHMENT_NUMBERING.sub(r'附件\1', article.number))
        else:
            buf.write('<h6 data-number="')
            buf.write(RE_ARTICLE_NUMBERING.sub(r'\1\2', article.number))
        buf.write('">')
        buf.write(article.number)
        if article.caption:
            buf.write('<span class="caption">（')
            buf.write(article.caption)
            buf.write('）</span>')
        if len(article.subitems) == 1 and RE_DELETED_FORMAT.match(article.subitems[0].caption):
            buf.write('\u200b<span class="caption deleted">（刪除）</span></h6>\n')
            return  # Short circuit
        buf.write('</h6>\n')
        if article.subitems:
            buf.write('<ol class="paragraphs">')
            super().render_article(article)
            buf.write('</ol>\n')

    def render_paragraph(self, paragraph):
        buf = self.buf
        buf.write('<li>')
        buf.write(apply_emphasis(normalize_spaces(paragraph.caption)))
        buf.write('</li>\n')
        if paragraph.subitems:
            buf.write('<ol class="subsections">\n')
            super().render_paragraph(paragraph)
            buf.write('</ol>\n')

    def render_subsection(self, subsection):
        buf = self.buf
        caption = RE_SUBSECTION_NUMBERING.sub('', subsection.caption)
        buf.write('<li>')
        buf.write(apply_emphasis(normalize_spaces(caption)))
        buf.write('</li>\n')
        if subsection.subitems:
            buf.write('<ol class="items">\n')
            super().render_subsection(subsection)
            buf.write('</ol>\n')

    def render_item(self, item):
        buf = self.buf
        item = RE_ITEM_NUMBERING.sub('', item)
        buf.write('<li>')
        buf.write(apply_emphasis(normalize_spaces(item)))
        buf.write('</li>\n')
