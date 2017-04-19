# statute.py - DOM for statute text

class Category(object):
    def __init__(self, slug='', caption='', label='', entries=None):
        self.slug = slug
        self.caption = caption
        self.label = label
        self.entries = entries or []

    def __repr__(self):
        return '<Category {} ({})({})>'.format(self.name, len(self.history), len(self.entries))

class Entry(object):
    def __init__(self, name='', bookmark_id=None):
        self.name = name
        self.bookmark_id = bookmark_id

class Act(Entry):
    def __init__(self, name='', history=None, articles=None, bookmark_id=None):
        super().__init__(name=name, bookmark_id=bookmark_id)
        self.history = history or []
        self.articles = articles or []

    def __repr__(self):
        return '<Act {} ({})({})>'.format(self.name, len(self.history), len(self.articles))

    def update_bookmark_id(self):
        count = 0
        for subitem in self.articles:
            if isinstance(subitem, Chapter):
                count += 1
                subitem.bookmark_id = '{}_ch{:02}'.format(self.bookmark_id, count)
        return count

class Chapter(object):
    def __init__(self, number='', caption=''):
        self.number = number
        self.caption = caption
        self.bookmark_id = None

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

class Interpretation(Entry):
    def __init__(self, name='', meta=None, subentries=None, bookmark_id=None):
        super().__init__(name=name, bookmark_id=bookmark_id)
        self.meta = meta or []
        self.subentries = subentries or []
        self.date = None

    def __repr__(self):
        return '<Interpretation {} ({})({})>'.format(self.name, len(self.meta), len(self.subentries))

class Heading(object):
    def __init__(self, caption='', is_chapter=False):
        self.caption = caption
        self.is_chapter = is_chapter
