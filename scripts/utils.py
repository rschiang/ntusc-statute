# utils.py - additional functions
import re

# Common constants
RE_CJK_NUMERICS = r'〇ㄧ一二三四五六七八九十百'
RE_CJK_NUMERICS_MIXED = r'〇ㄧ一二三四五六七八九十壹貳參肆伍陸柒捌玖拾'
RE_CJK_PATTERN = '[\u3400-\u4DB5\u4E00-\u9FD5]'
RE_CJK_BOUNDARY_PRE = re.compile(r'(?<=' + RE_CJK_PATTERN + r')\s*([\d\-A-Za-z\(]+)')
RE_CJK_BOUNDARY_POST = re.compile(r'([\d\-A-Za-z\)]+)\s*(?=' + RE_CJK_PATTERN + r')')
RE_FULLWIDTH_BRACKET = re.compile(r'（([A-Za-z\u00c0-\u04ff\s]+)）')
RE_HALFWIDTH_BRACKET = re.compile(r'\(([^A-Za-z\)）]+)\)')

UNICODE_THIN_SPACE = '\u2009'
RE_REPL_PRE = UNICODE_THIN_SPACE + r'\1'
RE_REPL_POST = r'\1' + UNICODE_THIN_SPACE
RE_REPL_FULLWIDTH_BRACKET = r'（\1）'
RE_REPL_HALFWIDTH_BRACKET = r'(\1)'

def normalize_spaces(text):
    text = text.replace('\u3000', '')
    text = RE_CJK_BOUNDARY_PRE.sub(RE_REPL_PRE, text)
    text = RE_CJK_BOUNDARY_POST.sub(RE_REPL_POST, text)
    return text

def normalize_brackets(text):
    text = RE_HALFWIDTH_BRACKET.sub(RE_REPL_FULLWIDTH_BRACKET, text)
    text = RE_FULLWIDTH_BRACKET.sub(RE_REPL_HALFWIDTH_BRACKET, text)
    return text
