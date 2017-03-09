# statute.py - DOM for statute text

class Category(object):
    def __init__(self, slug='', caption='', label='', acts=None):
        self.slug = slug
        self.caption = caption
        self.label = label
        self.acts = acts or []

    def __repr__(self):
        return '<Category {} ({})({})>'.format(self.name, len(self.history), len(self.articles))

class Act(object):
    def __init__(self, name='', history=None, articles=None):
        self.name = name
        self.history = history or []
        self.articles = articles or []
        self.bookmark_id = None

    def __repr__(self):
        return '<Act {} ({})({})>'.format(self.name, len(self.history), len(self.articles))

class Chapter(object):
    def __init__(self, number='', caption=''):
        self.number = number
        self.caption = caption

    def __repr__(self):
        return '<Chapter {number} {caption}>'.format(**self.__dict__)

class ArticleBase(object):
    def __init__(self, caption='', subitems=None):
        self.caption = caption
        self.subitems = subitems or []

    def __repr__(self):
        return '<{} {} ({})>'.format(self.__class__.__name__, self.caption, len(self.subitems))

class Article(ArticleBase):
    def __init__(self, number='', caption='', paragraphs=None):
        super().__init__(caption, paragraphs)
        self.number = number

    def __repr__(self):
        return '<Article {} {} ({})>'.format(self.number, self.caption, len(self.subitems))

class Paragraph(ArticleBase):
    pass

class Subsection(ArticleBase):
    pass
