# parser.py - parses statute text to DOM
import re
from io import StringIO
from statute import Act, Chapter, Article, Paragraph, Subsection

def parse_act(buf):
    if isinstance(buf, str):
        buf = StringIO(buf)

    try:
        act = Act()
        act.name = buf.readline().strip()
        assert act.name
        assert buf.readline() == '\n'

        while True:
            line = buf.readline()
            if line == '\n':
                break
            else:
                assert line
                act.history.append(line.strip())

        while True:
            indented_line = buf.readline().rstrip()
            if not indented_line:
                break

            line = indented_line.lstrip()
            indent = len(indented_line) - len(line)

            if indent == 0:    # Chapter title
                m = re.match(r'^(\S+)　(\S+)', line)
                assert m
                chapter = Chapter(number=m.group(1), caption=m.group(2))
                act.articles.append(chapter)
            elif indent == 2:  # Article
                m = re.match(r'^(\S+)　【(\S+)】', line)
                assert m
                article = Article(number=m.group(1), caption=m.group(2))
                act.articles.append(article)
            elif indent == 4:  # Paragraph
                paragraph = Paragraph(caption=line)
                article.subitems.append(paragraph)
            elif indent == 6:  # Subsection
                subsection = Subsection(caption=line)
                paragraph.subitems.append(subsection)
            elif indent == 8:  # Item
                subsection.subitems.append(line)

        return act
    except AssertionError:
        raise  # parse failed, malformed file


if __name__ == '__main__':
    f = open('../example.txt', 'r')
    act = parse_act(f)

    from renderer import HtmlRenderer
    renderer = HtmlRenderer()
    print(renderer.render(act).getvalue())
