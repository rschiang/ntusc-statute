#!/usr/bin/env python
# generator.py - iterate and generate statute
import glob
import os.path
from parser import parse_act
from renderer import HtmlRenderer

CATEGORIES = [
    ('supreme', ['1_基本法', '2_綜合性法規']),
    ('admin', ['3_會長暨行政部門篇']),
    ('legis', ['4_立法部門篇']),
    ('judicial', ['5_司法部門篇']),
    ]

def generate(path='source/laws/', output='statute.html'):
    buf = open(output, 'w+')
    renderer = HtmlRenderer(buf=buf)
    renderer.render_head()
    for slug, folders in CATEGORIES:
        count = 0
        for pattern in (os.path.join(path, f, '*.txt') for f in folders):
            for file_path in sorted(glob.glob(pattern)):
                print(file_path)
                count += 1
                with open(file_path, 'r') as file_buf:
                    act = parse_act(file_buf)
                    renderer.render_act(act, '{}_{:02}'.format(slug, count))
    renderer.render_tail()
    buf.close()


if __name__ == '__main__':
    generate()
