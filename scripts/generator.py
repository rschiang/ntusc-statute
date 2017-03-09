#!/usr/bin/env python
# generator.py - iterate and generate statute
import glob
import os.path
from parser import parse_act
from renderer import HtmlRenderer

class Category(object):
    def __init__(self, slug=None, caption=None, label=None, folders=None, acts=None):
        self.slug = slug
        self.caption = caption
        self.label = label
        self.folders = folders or []
        self.acts = acts or []


CATEGORIES = [
    Category(slug='supreme', caption='基本法與綜合性法規', label='基本法', folders=['1_基本法', '2_綜合性法規']),
    Category(slug='admin', caption='行政部門', label='行政', folders=['3_會長暨行政部門篇']),
    Category(slug='legis', caption='立法部門', label='立法', folders=['4_立法部門篇']),
    Category(slug='judicial', caption='司法部門', label='司法', folders=['5_司法部門篇']),
    ]

def generate(path='source/laws/', output='statute.html'):
    buf = open(output, 'w+')
    renderer = HtmlRenderer(buf=buf)
    renderer.render_head()

    # Read in
    for category in CATEGORIES:
        count = 0
        for pattern in (os.path.join(path, f, '*.txt') for f in category.folders):
            for file_path in sorted(glob.glob(pattern)):
                count += 1
                print(file_path)
                with open(file_path, 'r') as file_buf:
                    act = parse_act(file_buf)
                    hash_id = '{}_{:02}'.format(category.slug, count)
                    category.acts.append((hash_id, act))

    # Build cover and TOC

    # Render individual categories
    for category in CATEGORIES:
        renderer.render_category(category.caption, category.slug, category.label)
        for hash_id, act in category.acts:
            renderer.render_act(act, hash_id)

    renderer.render_tail()
    buf.close()


if __name__ == '__main__':
    generate()
