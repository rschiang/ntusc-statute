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
            indented_line = buf.readline()
            if not indented_line:
                break

            indented_line = indented_line.rstrip()
            if not indented_line:
                continue

            line = indented_line.lstrip()
            indent = len(indented_line) - len(line)

            if indent == 0:    # Chapter title
                m = re.match(r'^(第\S+)\s+(\S+)', line)
                assert m
                chapter = Chapter(number=m.group(1), caption=m.group(2))
                act.articles.append(chapter)
            elif indent == 2:  # Article
                m = re.match(r'^(?P<number>(第|附件)[^【\s]+)\s*(【(?P<caption>\S+)】)?', line)
                if m:
                    article = Article(number=m.group('number'), caption=(m.group('caption') or ''))
                    act.articles.append(article)
                else:
                    act.articles.append(line)  # Foreword text
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
        import sys
        sys.stderr.write(line)
        raise  # parse failed, malformed file


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python parser.py [file] > output.html')
        sys.exit()

    f = open(sys.argv[1], 'r')
    act = parse_act(f)

    from renderer import MarkdownRenderer
    renderer = MarkdownRenderer()
    print(renderer.render(act).getvalue())
