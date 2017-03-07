# statute.py - DOM for statute text
from utils import buffered

class Act(object):
    def __init__(self, name='', history=None, articles=None):
        self.name = name
        self.history = history or []
        self.articles = articles or []

    def __repr__(self):
        return '<Act {} ({})({})>'.format(self.name, len(self.history), len(self.articles))

    @buffered
    def to_markdown(self, buf=None):
        buf.write('# ')
        buf.write(self.name)
        buf.write('\n\n')
        for h in self.history:
            buf.write('* ')
            buf.write(h)
            buf.write('\n')
        buf.write('\n')
        for article in self.articles:
            if isinstance(article, str):
                buf.write(article)
                buf.write('\n')
            else:
                article.to_markdown(buf)

class Chapter(object):
    def __init__(self, number='', caption=''):
        self.number = number
        self.caption = caption

    def __repr__(self):
        return '<Chapter {number} {caption}>'.format(**self.__dict__)

    def to_markdown(self, buf=None):
        buf.write('{number} {caption}\n'.format(**self.__dict__))

class ArticleBase(object):
    def __init__(self, caption='', subitems=None):
        self.caption = caption
        self.subitems = subitems or []

    def __repr__(self):
        return '<{} {} ({})>'.format(self.__class__.__name__, self.caption, len(self.subitems))

    def subitems_to_markdown(self, buf=None, indent=0):
        for p in self.subitems:
            if isinstance(p, str):
                buf.write(' ' * indent)
                buf.write('- ')
                buf.write(p)
                buf.write('\n')
            else:
                p.to_markdown(buf=buf, indent=indent)

    @buffered
    def to_markdown(self, buf=None, indent=4):
        buf.write(' ' * indent)
        buf.write('- ')
        buf.write(self.caption)
        buf.write('\n')
        self.subitems_to_markdown(buf, indent + 2)

class Article(ArticleBase):
    def __init__(self, number='', caption='', paragraphs=None):
        super().__init__(caption, paragraphs)
        self.number = number

    def __repr__(self):
        return '<Article {} {} ({})>'.format(self.number, self.caption, len(self.subitems))

    @buffered
    def to_markdown(self, buf=None, indent=2):
        buf.write(' ' * indent)
        buf.write('### {number} ({caption})\n'.format(**self.__dict__))
        self.subitems_to_markdown(buf, indent + 2)

class Paragraph(ArticleBase):
    pass

class Subsection(ArticleBase):
    pass
