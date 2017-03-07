# statue.py - parses and stores statute text
import re
from io import StringIO

class Act(object):
    def __init__(self, name='', history=None, articles=None):
        self.name = name
        self.history = history or []
        self.articles = articles or []

class Chapter(object):
    def __init__(self, number='', caption=''):
        self.number = number
        self.caption = caption

class ArticleBase(object):
    def __init__(self, caption='', subitems=None):
        self.caption = caption
        self.subitems = subitems or []

class Article(ArticleBase):
    def __init__(self, number='', caption='', paragraphs=None):
        super().__init__(caption, paragraphs)
        self.number = number

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
    print(parse_act(f))
