# converter.py - Converts interpretation text to html
import re
import sys
from io import StringIO
from statute import Interpretation, Heading
from utils import RE_CJK_NUMERICS, normalize_spaces

RE_REPUBLIC_DATE_FORMAT = re.compile(r'(中華)?民國\s*(?P<year>\d+)\s*年\s*(?P<month>\d+)\s*月\s*(?P<day>\d+)\s*日')
RE_CHAPTER_FORMAT = re.compile(r'(解釋(文|理由)|聲請|公告)書?')
RE_HEADING_FORMAT = re.compile(r'([（\(][' + RE_CJK_NUMERICS + r'][）\)]、?|[' + RE_CJK_NUMERICS + r']、|\d\. )[^。]+$')

def parse_interpretation(buf):
    if isinstance(buf, str):
        buf = StringIO(buf)

    try:
        intp = Interpretation()
        intp.name = normalize_spaces(buf.readline().strip())
        assert intp.name
        assert buf.readline() == '\n'

        while True:
            line = buf.readline()
            if line == '\n':
                break

            line = line.strip()
            assert line

            m = RE_REPUBLIC_DATE_FORMAT.fullmatch(line)
            if m:
                intp.date = (m.group('year'), m.group('month'), m.group('day'))
                continue  # Eats the whole line, append later

            if line.startswith('學生法官：'):
                line = line[5:]  # Removes the prefix

            intp.meta.append(line)

        while True:
            indented_line = buf.readline()
            if not indented_line:
                break

            indented_line = indented_line.rstrip()
            if not indented_line:
                continue

            line = indented_line.lstrip()
            indent = len(indented_line) - len(line)

            if indent == 0:
                heading = Heading(line, is_chapter=True)
                intp.subentries.append(heading)
            if ((indent == 2 and not line.startswith('邱丞正、')) or RE_HEADING_FORMAT.fullmatch(line)):  # workaround for bad indent
                heading = Heading(line)
                intp.subentries.append(heading)
            else:
                intp.subentries.append(line)

        return intp
    except AssertionError:
        sys.stderr.write(line)
        raise  # parse failed, malformed file


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python parser/interpretations.py [file] > output.html')
        sys.exit()

    f = open(sys.argv[1], 'r')
    intp = parse_interpretation(f)

    from renderer import HtmlRenderer
    renderer = HtmlRenderer(buf=sys.stdout)
    renderer.render_head()
    renderer.render_interpretation(intp)
    renderer.render_tail()
