# statue.py - parses and stores statute text
import re
from io import StringIO
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

def parse_act(buf):
    if isinstance(buf, str):
        buf = StringIO(buf)

    try:
        act = Act()
        act.name = buf.readline().strip()
        assert act.name
        assert buf.readline() == '\n'

        while True:
            line = buf.readline()
            if line == '\n':
                break
            else:
                assert line
                act.history.append(line.strip())

        while True:
            indented_line = buf.readline().rstrip()
            if not indented_line:
                break

            line = indented_line.lstrip()
            indent = len(indented_line) - len(line)

            if indent == 0:    # Chapter title
                m = re.match(r'^(\S+)　(\S+)', line)
                assert m
                chapter = Chapter(number=m.group(1), caption=m.group(2))
                act.articles.append(chapter)
            elif indent == 2:  # Article
                m = re.match(r'^(\S+)　【(\S+)】', line)
                assert m
                article = Article(number=m.group(1), caption=m.group(2))
                act.articles.append(article)
            elif indent == 4:  # Paragraph
                paragraph = Paragraph(caption=line)
                article.subitems.append(paragraph)
            elif indent == 6:  # Subsection
                subsection = Subsection(caption=line)
                paragraph.subitems.append(subsection)
            elif indent == 8:  # Item
                subsection.subitems.append(line)

        return act
    except AssertionError:
        raise  # parse failed, malformed file


if __name__ == '__main__':
    f = open('../example.txt', 'r')
    print(parse_act(f).to_markdown())
