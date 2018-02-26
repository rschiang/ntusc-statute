# generator/task.py - Derived models for generator use
import glob
import io
import json
import os
import parser
import re
from statute import Category

class Task(object):
    def __init__(self, source, output, generator=None, base_url='', title='', meta=None, categories=None, prepend=None, append=None, options=None):
        self.source = source
        self.output = output
        self.generator = generator
        self.base_url = base_url
        self.title = title
        self.meta = meta or {}
        self.prepend = prepend or []
        self.append = append or []
        self.options = options or {}
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
    def __init__(self, slug, caption, label, folders=None, entries=None, replace=None):
        self.folders = folders or []
        self.replace = replace or []
        self.is_intp = (slug == 'interpret')
        self.counter = 0
        super().__init__(slug=slug, caption=caption, label=label, entries=entries)

    def load(self, base_path='.'):
        for pattern in (os.path.join(base_path, f, '*.txt') for f in self.folders):
            for file_path in sorted(glob.glob(pattern)):
                self.counter += 1
                print(file_path)
                with self.open_file(file_path) as file_buf:
                    bookmark_id = '{}_{:02}'.format(self.slug, self.counter)
                    entry = self.parse_entry(file_buf, bookmark_id)
                    self.entries.append(entry)

    def open_file(self, file_path):
        file_buf = open(file_path, 'r')
        for item in self.replace:
            if file_path.endswith(item['path']):
                expr = item['expr']
                with open(item['repl'], 'r') as repl_buf:
                    repl = repl_buf.read()
                with file_buf:
                    string = file_buf.read()
                # Wraps the replaced buffer like file
                string = re.sub(expr, repl, string, flags=re.MULTILINE)
                return io.StringIO(string)
        return file_buf

    def parse_entry(self, buf, bookmark_id):
        if self.is_intp:
            entry = parser.parse_interpretation(buf)
            entry.bookmark_id = bookmark_id
        else:
            entry = parser.parse_act(buf)
            entry.bookmark_id = bookmark_id
            entry.update_bookmark_id()
        return entry


def render_custom_item(renderer, item):
    if 'path' in item:
        renderer.render_file(item['path'])
    elif 'section' in item:
        renderer.render_section(item['section'], item['content'])
