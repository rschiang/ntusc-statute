# converter.py - Converts interpretation text to html
import re
import sys
from io import StringIO
from utils import normalize_spaces

RE_REPUBLIC_DATE_FORMAT = re.compile(r'(中華)?民國\s*(?P<year>\d+)\s*年\s*(?P<month>\d+)\s*月\s*(?P<day>\d+)\s*日')
RE_META_REMARK_FORMAT = re.compile(r'(（(首席|註[^）]+)）)')
RE_NOTABLE_REMARK_FORMAT = re.compile(r'([（\(](以?下簡?稱|[備附]註|註\s*[\d〇ㄧ一二三四五六七八九十]+)[^）]+[）\)])')
RE_CITATION_FORMAT = re.compile(r'([（\(][^）\)]+參照[）\)])')
RE_CHAPTER_FORMAT = re.compile(r'(解釋(文|理由)|聲請|公告)書?')

def apply_meta_remarks(text):
    return RE_META_REMARK_FORMAT.sub(r'<span class="note">\1</span>', text)

def apply_notable_remarks(text):
    return RE_NOTABLE_REMARK_FORMAT.sub(r'<span class="note">\1</span>', text)

def apply_citation(text):
    return RE_CITATION_FORMAT.sub('<cite>\1</cite>', text)

def convert_interpretation(source, dest, bookmark_id=None):
    if isinstance(source, str):
        source = StringIO(source)

    try:
        # Title
        name = source.readline().strip()
        assert name
        assert source.readline() == '\n'

        dest.write('<article class="interpretation">\n'
                   '<header id="{}">{}</header>\n'
                   .format(bookmark_id or 'top', normalize_spaces(name)))

        # Meta section
        meta = []
        while True:
            line = source.readline()
            if line == '\n':
                break
            line = line.strip()
            assert line

            date_match = RE_REPUBLIC_DATE_FORMAT.match(line)
            if date_match:
                continue  # Eats the whole line, append later

            if line.startswith('學生法官：'):
                line = line[5:]  # Removes the prefix

            meta.append(line)

        dest.write('<div class="meta">\n')
        dest.write(apply_meta_remarks(normalize_spaces('，'.join(meta))))
        dest.write('\n</div>\n')

        while True:
            indented_line = source.readline()
            if not indented_line:
                break

            indented_line = indented_line.rstrip()
            if not indented_line:
                continue

            line = indented_line.lstrip()
            indent = len(indented_line) - len(line)

            if indent == 0:
                heading_match = RE_CHAPTER_FORMAT.fullmatch(line)
                if heading_match:
                    pass
                else:
                    pass
            if indent == 2:
                pass
            else:
                pass

        dest.write('</article>\n')

    except AssertionError:
        sys.stderr.write()
        raise


if __name__ == '__main__':
    f = open('source/laws/6_學生法院解釋/17_第10號.txt', 'r')
    convert_interpretation(source=f, dest=sys.stdout)
