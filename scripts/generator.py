#!/usr/bin/env python
# generator.py - iterate and generate statute
import glob
import os.path
from parser import parse_act
from renderer import HtmlRenderer
from statute import Category

class CategoryTask(Category):
    def __init__(self, slug, caption, label, folders=None, acts=None):
        self.folders = folders or []
        super().__init__(slug=slug, caption=caption, label=label, acts=acts)


CATEGORIES = [
    CategoryTask(slug='supreme', caption='基本法與綜合性法規', label='基本法', folders=['1_基本法', '2_綜合性法規']),
    CategoryTask(slug='admin', caption='行政部門', label='行政', folders=['3_會長暨行政部門篇']),
    CategoryTask(slug='legis', caption='立法部門', label='立法', folders=['4_立法部門篇']),
    CategoryTask(slug='judicial', caption='司法部門', label='司法', folders=['5_司法部門篇']),
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
                    act.bookmark_id = '{}_{:02}'.format(category.slug, count)
                    act.update_bookmark_id()
                    category.acts.append(act)

    # Build cover and TOC
    renderer.render_index_head()
    for category in CATEGORIES:
        renderer.render_index_category(category)
    renderer.render_index_tail()

    # Render individual categories
    for category in CATEGORIES:
        renderer.render_category(category)
        for act in category.acts:
            renderer.render_act(act)

    renderer.render_tail()
    buf.close()


if __name__ == '__main__':
    generate()
