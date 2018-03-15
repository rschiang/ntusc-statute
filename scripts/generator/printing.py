# generator/printing.py
from .task import render_custom_item
from renderer import HtmlRenderer

def generate(task):
    buf = open(task.output, 'w+')
    renderer = HtmlRenderer(buf=buf)
    renderer.render_head(title=task.title, meta=task.meta, base_url=task.base_url)

    # Read in
    for category in task.categories:
        category.load(base_path=task.source)

    # Build cover and TOC
    renderer.render_index_head()
    for category in task.categories:
        renderer.render_index_category(category)
    renderer.render_index_tail()

    # Process prepends
    for item in task.prepend:
        render_custom_item(renderer, item)

    # Render individual categories
    for category in task.categories:
        renderer.render_category(category)
        if category.is_intp:
            for entry in category.entries:
                renderer.render_interpretation(entry)
        else:
            for entry in category.entries:
                renderer.render_act(entry)
        # Render blank pages if requested
        for i in range(category.blanks):
            renderer.render_blank()

    # Process appends
    for item in task.append:
        render_custom_item(renderer, item)

    renderer.render_tail()
    buf.close()
