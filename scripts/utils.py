# utils.py - additional functions
import re

RE_CJK_PATTERN = '[\u3400-\u4DB5\u4E00-\u9FD5]'
RE_CJK_BOUNDARY_PRE = re.compile(r'(?<=' + RE_CJK_PATTERN + r')([\d\-A-Za-z]+)')
RE_CJK_BOUNDARY_POST = re.compile(r'([\d\-A-Za-z]+)(?=' + RE_CJK_PATTERN + r')')

UNICODE_THIN_SPACE = '\u2009'
RE_REPL_PRE = UNICODE_THIN_SPACE + r'\1'
RE_REPL_POST = r'\1' + UNICODE_THIN_SPACE

def normalize_spaces(text):
    text = text.replace('\u3000', '')
    text = RE_CJK_BOUNDARY_PRE.sub(RE_REPL_PRE, text)
    text = RE_CJK_BOUNDARY_POST.sub(RE_REPL_POST, text)
    return text
