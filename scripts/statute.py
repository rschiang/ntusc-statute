# statue.py - parses and stores statute text
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

        return act
    except AssertionError:
        pass  # parse failed, malformed file
