# generator/task.py - Derived models for generator use
import glob
import json
import os
import parser
from statute import Category

class Task(object):
    def __init__(self, source, output, generator=None, base_url='', title='', meta=None, categories=None, prepend=None, append=None):
        self.source = source
        self.output = output
        self.generator = generator
        self.base_url = base_url
        self.title = title
        self.meta = meta or {}
        self.prepend = prepend or []
        self.append = append or []
        self.categories = []
        if categories:
            for item in categories:
                category = CategoryTask(**item)
                self.categories.append(category)

    @classmethod
    def from_json(cls, buf):
        entity = json.load(buf)
        return cls(**entity)


class CategoryTask(Category):
    def __init__(self, slug, caption, label, folders=None, entries=None):
        self.folders = folders or []
        self.is_intp = (slug == 'interpret')
        self.counter = 0
        super().__init__(slug=slug, caption=caption, label=label, entries=entries)

    def load(self, base_path='.'):
        for pattern in (os.path.join(base_path, f, '*.txt') for f in self.folders):
            for file_path in sorted(glob.glob(pattern)):
                self.counter += 1
                print(file_path)
                with open(file_path, 'r') as file_buf:
                    bookmark_id = '{}_{:02}'.format(self.slug, self.counter)
                    entry = self.parse_entry(file_buf, bookmark_id)
                    self.entries.append(entry)

    def parse_entry(self, buf, bookmark_id):
        if self.is_intp:
            entry = parser.parse_interpretation(buf)
            entry.bookmark_id = bookmark_id
        else:
            entry = parser.parse_act(buf)
            entry.bookmark_id = bookmark_id
            entry.update_bookmark_id()
        return entry
