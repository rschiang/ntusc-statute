#!/usr/bin/env python
# generator.py - iterate and generate statute
import os
from generator.task import CategoryTask
from renderer import HtmlRenderer

CATEGORIES = [
    CategoryTask(slug='supreme', caption='基本法與綜合性法規', label='基本法', folders=['1_基本法', '2_綜合性法規']),
    CategoryTask(slug='admin', caption='行政部門', label='行政', folders=['3_會長暨行政部門篇']),
    CategoryTask(slug='legis', caption='立法部門', label='立法', folders=['4_立法部門篇']),
    CategoryTask(slug='judicial', caption='司法部門', label='司法', folders=['5_司法部門篇']),
    CategoryTask(slug='interpret', caption='學生法院解釋', label='解釋', folders=['6_學生法院解釋']),
    CategoryTask(slug='appendix', caption='附錄', label='附錄', folders=['7_附錄', '../../statute/appendix/']),
    ]

def generate(path='source/laws/', output='statute.html', is_printing=True):
    buf = open(output, 'w+')
    renderer = HtmlRenderer(buf=buf)
    renderer.render_head(title='國立臺灣大學學生會簡明法規彙編', meta={
        'author': '國立臺灣大學開源社',
        'description': '收錄自治規程、規則條文、以及相關之公眾法規。',
        })

    # Read in
    for category in CATEGORIES:
        category.load(base_path=path)

    # Append online version artifacts
    if not is_printing:
        renderer.render_file('statute/online/badge.html')
        renderer.render_section('intro', '我們貢獻這所大學于宇宙之精神。')

    # Build cover and TOC
    renderer.render_index_head()
    for category in CATEGORIES:
        renderer.render_index_category(category)
    renderer.render_index_tail()

    # Render individual categories
    for category in CATEGORIES:
        renderer.render_category(category)
        if category.is_intp:
            for entry in category.entries:
                renderer.render_interpretation(entry)
        else:
            for entry in category.entries:
                renderer.render_act(entry)

    # Append print version artifacts
    if is_printing:
        renderer.render_section('intro', '我們貢獻這所大學于宇宙之精神。')
        renderer.render_file('statute/print/copyright.html')

    renderer.render_tail()
    buf.close()


if __name__ == '__main__':
    is_printing = (os.environ.get('TARGET') != 'display')
    generate(is_printing=is_printing)
