# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

"""
Support for color and formatting for various terminals or
terminal-like systems
"""

import re
import log_system

logger = log_system.init_logging()

from colors import TERMINAL_TYPES, COLOR_MAP, TTYPE_MAP

_PARA_BREAK = re.compile(r"(\n\s*\n)", re.MULTILINE)


def word_wrap(text: str, columns=80, indent=4, padding=2):
    """
    Given a block of text, breaks into a list of lines wrapped to
    length.
    """
    paragraphs = _PARA_BREAK.split(text)
    lines = []
    columns -= padding
    for para in paragraphs:
        if para.isspace():
            continue
        line = ' ' * indent
        linelen = len(line)
        words = para.split()
        for word in words:
            bareword = color_convert(word, 'pyku', None)
            if (linelen + 1 + len(bareword)) > columns:
                lines.append(line)
                line = ' ' * padding
                linelen = len(line)
                line += word
                linelen += len(bareword)
            else:
                line += ' ' + word
                linelen += len(bareword) + 1
        if not line.isspace():
            lines.append(line)
    return lines


class Xlator(dict):
    """ All-in-one multiple-string-substitution class """
    def _make_regex(self):
        """ Build re object based on the keys of the current dictionary """
        #x = lambda s: '(?<!' + re.escape(s[0]) + ')' + re.escape(s)
        return re.compile("|".join(map(re.escape, self.keys())))

    def __call__(self, match):
        """ Handler invoked for each regex match """
        return self[match.group(0)][self.otype]

    def xlat(self, text, otype):
        """ Translate text, returns the modified text. """
        self.otype = otype
        return self._make_regex().sub(self, text)


def color_convert(text: str or None, input_type='pyku', output_type='ansi'):
    """
    Given a chunk of text, replace color tokens of the specified input type
    with the appropriate color codes for the given output terminal type
    """
    if not output_type:
        output_type = 'ansi'
    if not input_type:
        input_type = 'rom'
    if text is None or len(text) < 1:
        return text
    if input_type is None or input_type == 'unknown' or input_type not in COLOR_MAP:
        return text
    if output_type is not None and output_type not in TERMINAL_TYPES:
        output_type = None

    if input_type == 'i3':
        words = text.split('%^')
        for word in words:
            if word == '':
                continue
            if word not in COLOR_MAP[input_type]:
                continue
            i = words.index(word)
            if output_type is None:
                words[i] = ''
            else:
                o = TERMINAL_TYPES.index(output_type)
                words[i] = COLOR_MAP[input_type][word][o]
        return ''.join(words)
    else:
        if output_type is None:
            output_type = 'unknown'
        o = TERMINAL_TYPES.index(output_type)
        xl = Xlator(COLOR_MAP[input_type])
        return xl.xlat(text, o)

        # for k in COLOR_MAP[input_type].keys():
        #     if output_type is None:
        #         text = text.replace(k, '')
        #     else:
        #         o = TERMINAL_TYPES.index(output_type)
        #         v = COLOR_MAP[input_type][k][o]
        #         if k != v and v not in COLOR_MAP[input_type]:
        #             text = text.replace(k, v)
        # return text


def escape(text: str, input_type='pyku'):
    """
    Escape all the color tokens in the given text chunk, so they
    can be safely printed through the color parser
    """
    if text is None or text == '':
        return text
    if input_type == 'i3':
        text = text.replace('%^', '%%^^')
    elif input_type == 'pyku':
        text = text.replace('[', '[[')
        text = text.replace(']', ']]')
    elif input_type == 'rom':
        text = text.replace('{', '{{')
        text = text.replace('}', '}}')
    elif input_type == 'smaug':
        text = text.replace('&', '&&')
        text = text.replace('^', '^^')
        text = text.replace('}', '}}')
    elif input_type == 'imc2':
        text = text.replace('~', '~~')
        text = text.replace('^', '^^')
        text = text.replace('`', '``')
    return text


def remap_ttype(ttype: str):
    """
    Remap known terminal types for mud clients and other common terminals
    into one of the supported color mappings, even though we may lose
    information (that we don't use).

    :param ttype:
    :return:
    """
    if ttype in TTYPE_MAP:
        return TTYPE_MAP[ttype]
    return ttype
