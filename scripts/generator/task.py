# generator/task.py - Derived models for generator use
import glob
import hashlib
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
    def __init__(self, slug, caption, label, folders=None, entries=None, replace=None, blanks=None):
        self.folders = folders or []
        self.replace = replace or []
        self.blanks = blanks or 0
        self.is_intp = (slug == 'interpret')
        self.hash_names = []
        super().__init__(slug=slug, caption=caption, label=label, entries=entries)

    def load(self, base_path='.'):
        for pattern in (os.path.join(base_path, f, '*.txt') for f in self.folders):
            for file_path in sorted(glob.glob(pattern)):
                print(file_path)
                with self.open_file(file_path) as file_buf:
                    entry = self.parse_entry(file_buf, self.slug)
                    self.entries.append(entry)

    def open_file(self, file_path):
        file_buf = open(file_path, 'r')
        for item in self.replace:
            if file_path.endswith(item['path']):
                expr = item['expr']
                # Try to load replacement file first
                try:
                    with open(item['repl_path'], 'r') as repl_buf:
                        repl = repl_buf.read()
                except KeyError:
                    # Fallback to use string
                    repl = item['repl']
                # Read in file
                with file_buf:
                    string = file_buf.read()
                # Wraps the replaced buffer like file
                string = re.sub(expr, repl, string, flags=re.MULTILINE)
                return io.StringIO(string)
        return file_buf

    def parse_entry(self, buf, slug):
        entry = parser.parse_interpretation(buf) if self.is_intp else parser.parse_act(buf)
        name = self.generate_unique_name(entry.name)
        entry.bookmark_id = '_'.join((slug, name))
        if not self.is_intp:
            entry.update_bookmark_id()
        return entry

    def generate_unique_name(self, name):
        hashed = hashlib.sha1(name.encode()).hexdigest()
        for end_index in range(6, len(hashed)):
            if hashed[:end_index] not in self.hash_names:
                self.hash_names.append(hashed[:end_index])
                return hashed[:end_index]
        # Unlikely collision. Hmmm.
        return name


def render_custom_item(renderer, item):
    if 'path' in item:
        renderer.render_file(item['path'])
    elif 'section' in item:
        renderer.render_section(item['section'], item['content'])
