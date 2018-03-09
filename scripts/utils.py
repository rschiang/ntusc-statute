# utils.py - additional functions
import re

# Common constants
RE_CJK_NUMERICS = r'〇ㄧ一二三四五六七八九十百零'
RE_CJK_NUMERICS_MIXED = r'〇ㄧ一二三四五六七八九十零壹貳參肆伍陸柒捌玖拾'
RE_CJK_NUMERICS_SINGLE = r'一二三四五六七八九十'
RE_CJK_PATTERN = '[\u3400-\u4DB5\u4E00-\u9FD5]'
RE_CJK_BOUNDARY_PRE = re.compile(r'(?<=' + RE_CJK_PATTERN + r')\s*([\d\-A-Za-z\(]+)')
RE_CJK_BOUNDARY_POST = re.compile(r'([\d\-A-Za-z\)]+)\s*(?=' + RE_CJK_PATTERN + r')')
RE_CJK_BRACKETED_NUMBER = re.compile(r'[（\(]([' + RE_CJK_NUMERICS + r']+)[\)）]')
RE_BRACKETED_NUMBER = re.compile(r'[（\(](\d+)[\)）]')
RE_FULLWIDTH_BRACKET = re.compile(r'（([A-Za-z\u00c0-\u04ff\s]+)）')
RE_HALFWIDTH_BRACKET = re.compile(r'\(([^A-Za-z\)）]+)\)')

UNICODE_THIN_SPACE = '\u2009'
RE_REPL_PRE = UNICODE_THIN_SPACE + r'\1'
RE_REPL_POST = r'\1' + UNICODE_THIN_SPACE
RE_REPL_FULLWIDTH_BRACKET = r'（\1）'
RE_REPL_HALFWIDTH_BRACKET = r'(\1)'

CJK_NUMERIC_INDEX = '零一二三四五六七八九'
CJK_BRACKETED_NUMBERS = '㈠㈡㈢㈣㈤㈥㈦㈧㈨㈩'


def normalize_spaces(text):
    text = text.replace('\u3000', '')
    text = RE_CJK_BOUNDARY_PRE.sub(RE_REPL_PRE, text)
    text = RE_CJK_BOUNDARY_POST.sub(RE_REPL_POST, text)
    return text

def normalize_brackets(text):
    text = RE_HALFWIDTH_BRACKET.sub(RE_REPL_FULLWIDTH_BRACKET, text)
    text = RE_FULLWIDTH_BRACKET.sub(RE_REPL_HALFWIDTH_BRACKET, text)
    return text

def normalize_bracketed_numbers(text):
    text = RE_BRACKETED_NUMBER.sub(r'<span class="bracketed number">\1</span>', text)
    text = RE_CJK_BRACKETED_NUMBER.sub(repl_cjk_bracketed_numbers, text)
    return text

def convert_cjk_number(text):
    # Sniff alphanumerics
    if text.isdecimal():
        return text.lstrip('0')

    # Normalize numeric representation
    text = text.replace('〇', '零').replace('ㄧ', '一')
    result = 0

    # Sniff numeric type, handle formats like 一零三, 五四
    if len(text) > 1 and '十' not in text and '百' not in text:
        while len(text):
            result *= 10
            result += CJK_NUMERIC_INDEX.index(text[0])
            text = text[1:]
        return result

    # Process regular format
    digit = 0
    for char in text:
        value = CJK_NUMERIC_INDEX.find(char)
        if value >= 0:
            digit = value
        else:
            # Guess unit
            if char == '百':
                unit = 100
            elif char == '十':
                unit = 10
            # 一 is probably omitted
            if digit == 0:
                result += unit
            else:
                result += digit * unit
            # Reset digit
            digit = 0
    # Add the last digit
    if digit > 0:
        result += digit
    return result

def repl_cjk_bracketed_numbers(matchobj):
    text = matchobj.group(1)
    index = RE_CJK_NUMERICS_SINGLE.find(text)
    if index >= 0:
        return CJK_BRACKETED_NUMBERS[index]
    else:
        return '({})'.format(convert_cjk_number(text))

def repl_cjk_date(matchobj):
    return '民國{}年{}月{}日'.format(
        convert_cjk_number(matchobj.group('year')),
        convert_cjk_number(matchobj.group('month')),
        convert_cjk_number(matchobj.group('day')))

def repl_cjk_semester(matchobj):
    return '{}學年度第{}學期'.format(
        convert_cjk_number(matchobj.group('year')),
        convert_cjk_number(matchobj.group('semester')))

def repl_numeric_date(matchobj):
    return '民國{}年{}月{}日'.format(*(d.lstrip('0') for d in matchobj.groups()))

def repl_numeric_inline_date(matchobj):
    return '{}年{}月{}日'.format(*(d.lstrip('0') for d in matchobj.groups()))
