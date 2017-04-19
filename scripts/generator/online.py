# generator/printing.py
import os
from .task import render_custom_item
from renderer import HtmlRenderer

def generate_index_page(task, renderer):
    # Read configurations
    prepend_path, append_path = None, None
    if 'index' in task.options:
        prepend_path = task.options['index'].get('prepend')
        append_path = task.options['index'].get('append')

    renderer.render_head(title=task.title, meta=task.meta, base_url=task.base_url)

    # Render index prepend file if applicable
    if prepend_path:
        renderer.render_file(prepend_path)

    # Render TOC
    renderer.render_index_head()
    for category in task.categories:
        renderer.render_index_category(category)
    renderer.render_index_tail()

    # Render index append file if applicable
    if append_path:
        renderer.render_file(append_path)

def generate_entry(task, renderer, entry, is_intp=False):
    # Process header and prepends
    renderer.render_head(title=entry.name, meta=task.options.get('entry_meta', task.meta), base_url=task.base_url)
    for item in task.prepend:
        render_custom_item(renderer, item)

    # Render item
    if is_intp:
        renderer.render_interpretation(entry)
    else:
        renderer.render_act(entry)

    # Process appends and tail
    for item in task.append:
        render_custom_item(renderer, item)
    renderer.render_tail()

def generate(task):
    # Read in
    for category in task.categories:
        category.load(base_path=task.source)

    #　Declare link generation function  # noqa: E265
    def format_href(bookmark_id):
        entry_id, _, ch_id = bookmark_id.partition('_ch')
        category, _, order = entry_id.partition('_')
        if ch_id:
            return '{}{}/{}.html#{}'.format(task.base_url, category, order, bookmark_id)
        elif order:
            return '{}{}/{}.html'.format(task.base_url, category, order)
        else:
            return '#'  # Does not support category index page

    # Generate index (TOC) page
    with open(os.path.join(task.output, 'index.html'), 'w+') as buf:
        renderer = HtmlRenderer(buf)
        renderer.href_formatter = format_href
        generate_index_page(task, renderer)

    # Render individual categories
    for category in task.categories:
        # Create the folder if not exists
        folder = os.path.join(task.output, category.slug)
        if not os.path.exists(folder):
            os.mkdir(folder)

        # Render each file
        for entry in category.entries:
            catgory_name, _, order = entry.bookmark_id.partition('_')
            path = '{}/{}.html'.format(catgory_name, order)
            with open(os.path.join(task.output, path), 'w+') as buf:
                renderer.buf = buf
                generate_entry(task, renderer, entry, category.is_intp)
