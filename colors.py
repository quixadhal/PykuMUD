# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

"""
This file contains the various color conversion tables
used to change color tokens into output formats.

There are currently two basic types of color token systems
supported by the terminal handler.

The first is a style made popular by several Dikurivative
games, which uses a single character "magic" symbol, followed
by a single character to represent the color or terminal
function being represented.

An example would be &r meaning red foreground text.

Because different MUD's developed these systems in parallel,
sometimes copying each other, but often re-inventing the
wheel, there are multiple different formats with different
symbols mapping to different colors or functions.

In keeping with this tradition, I've used my own symbol
which was chosen to have the lowest impact on native python
string formatting functions.

The second type of system is the Pinkfish style code
system, used by LPMUD's.  In this system, a color or
function name is surrounded by a color token, chosen
to be unlikely to occur in natural text.

An example would be %^RED%^red foreground text%^RESET%^.

Because of the way this was originally coded, it is legal
to combine color names with only a single seperating token,
rather than a full surround.

Thus, %^RED%^%^BOLD%^bright red%^RESET%^, and
%^BOLD%^RED%^bright red%^RESET%^ should look the same.

"ansi", "greyscale", and "mxp" are only valid as output
types, although the first two COULD be implemented as input
types if there were some reason to do so.

"i3" and "imc2" are used by various intermud networks,
and are used as both input and output types when sending
or receiving from those networks.

"pyku", "rom", and "smaug" are normally used as input
types, however if you wanted to convert data from one
type of MUD to another, they could be output types as well.

The "unknown" type is used to strip out all color codes,
and is not valid as an input type.

Finally, there is a TTYPE_MAP which is used to map known
client terminal types (as reported by the client over
TELNET) to one of our supported types.  This is usually
a "best guess", since the underlying terminal can't be
obtained.  ANSI is a pretty good default these days.

"""
from collections import namedtuple
import log_system

logger = log_system.init_logging()

TERMINAL_TYPES = ('unknown', 'pyku', 'rom', 'smaug', 'imc2', 'ansi', 'greyscale', 'i3', 'mxp')

ColorToken = namedtuple('ColorToken', TERMINAL_TYPES)

TTYPE_MAP = {
    'tinyfugue': 'ansi',
}

COLOR_MAP = {}

COLOR_MAP['unknown'] = {
}

COLOR_MAP['pyku'] = {
    '[d': ColorToken('',    '[d',   '{d',   '&x',   '~x',   '\033[30m',     '\033[38;5;232m',   '%^BLACK%^',            '<COLOR FORE=\"#000000\">' ),
    '[r': ColorToken('',    '[r',   '{r',   '&r',   '~r',   '\033[31m',     '\033[38;5;237m',   '%^RED%^',              '<COLOR FORE=\"#bb0000\">' ),
    '[g': ColorToken('',    '[g',   '{g',   '&g',   '~g',   '\033[32m',     '\033[38;5;237m',   '%^GREEN%^',            '<COLOR FORE=\"#00bb00\">' ),
    '[y': ColorToken('',    '[y',   '{y',   '&O',   '~y',   '\033[33m',     '\033[38;5;244m',   '%^ORANGE%^',           '<COLOR FORE=\"#bbbb00\">' ),
    '[b': ColorToken('',    '[b',   '{b',   '&b',   '~b',   '\033[34m',     '\033[38;5;237m',   '%^BLUE%^',             '<COLOR FORE=\"#0000bb\">' ),
    '[m': ColorToken('',    '[m',   '{m',   '&p',   '~p',   '\033[35m',     '\033[38;5;244m',   '%^MAGENTA%^',          '<COLOR FORE=\"#bb00bb\">' ),
    '[c': ColorToken('',    '[c',   '{c',   '&c',   '~c',   '\033[36m',     '\033[38;5;244m',   '%^CYAN%^',             '<COLOR FORE=\"#00bbbb\">' ),
    '[w': ColorToken('',    '[w',   '{w',   '&w',   '~w',   '\033[37m',     '\033[38;5;250m',   '%^WHITE%^',            '<COLOR FORE=\"#bbbbbb\">' ),

    '[D': ColorToken('',    '[D',   '{D',   '&z',   '~z',   '\033[1;30m',   '\033[38;5;240m',   '%^BOLD%^BLACK%^',      '<COLOR FORE=\"#555555\">'),
    '[R': ColorToken('',    '[R',   '{R',   '&R',   '~R',   '\033[1;31m',   '\033[38;5;245m',   '%^BOLD%^RED%^',        '<COLOR FORE=\"#ff5555\">'),
    '[G': ColorToken('',    '[G',   '{G',   '&G',   '~G',   '\033[1;32m',   '\033[38;5;245m',   '%^BOLD%^GREEN%^',      '<COLOR FORE=\"#55ff55\">'),
    '[Y': ColorToken('',    '[Y',   '{Y',   '&Y',   '~Y',   '\033[1;33m',   '\033[38;5;251m',   '%^BOLD%^ORANGE%^',     '<COLOR FORE=\"#ffff55\">'),
    '[B': ColorToken('',    '[B',   '{B',   '&B',   '~B',   '\033[1;34m',   '\033[38;5;245m',   '%^BOLD%^BLUE%^',       '<COLOR FORE=\"#5555ff\">'),
    '[M': ColorToken('',    '[M',   '{M',   '&P',   '~P',   '\033[1;35m',   '\033[38;5;251m',   '%^BOLD%^MAGENTA%^',    '<COLOR FORE=\"#ff55ff\">'),
    '[C': ColorToken('',    '[C',   '{C',   '&C',   '~C',   '\033[1;36m',   '\033[38;5;251m',   '%^BOLD%^CYAN%^',       '<COLOR FORE=\"#55ffff\">'),
    '[W': ColorToken('',    '[W',   '{W',   '&W',   '~W',   '\033[1;37m',   '\033[38;5;255m',   '%^BOLD%^WHITE%^',      '<COLOR FORE=\"#ffffff\">'),

    '[*': ColorToken('',    '[*',   '{*',   '',     '',     '\007',         '\007',             '',                     ''),
    '[/': ColorToken('',    '[/',   '{/',   '',     '',     '\012',         '\012',             '',                     ''),

    '[[': ColorToken('[',   '[[',   '[',    '[',    '[',    '[',            '[',                '[',                    '['),
    ']]': ColorToken(']',   ']]',   ']',    ']',    ']',    ']',            ']',                ']',                    ']'),

    '[x': ColorToken('',    '[x',   '{x',   '&d',   '~!',   '\033[0m',      '\033[0m',          '%^RESET%^',            '<RESET>'),
    '[L': ColorToken('',    '[L',   '{L',   '&L',   '~L',   '\033[1m',      '\033[1m',          '%^BOLD%^',             '<BOLD>'),
    '[i': ColorToken('',    '[i',   '{i',   '&i',   '~i',   '\033[3m',      '\033[3m',          '%^ITALIC%^',           '<ITALIC>'),
    '[u': ColorToken('',    '[u',   '{u',   '&u',   '~u',   '\033[4m',      '\033[4m',          '%^UNDERLINE%^',        '<UNDERLINE>'),
    '[f': ColorToken('',    '[f',   '{f',   '&f',   '~$',   '\033[5m',      '\033[5m',          '%^FLASH%^',            '<FONT COLOR=BLINK>'),
    '[V': ColorToken('',    '[v',   '{v',   '&v',   '~v',   '\033[7m',      '\033[7m',          '%^REVERSE%^',          '<FONT COLOR=INVERSE>'),
    '[s': ColorToken('',    '[s',   '{s',   '&s',   '~s',   '\033[9m',      '\033[9m',          '%^STRIKETHRU%^',       '<STRIKEOUT>'),

    '[H': ColorToken('',    '[H',   '{H',   '',     '',     '\033[H',       '\033[H',           '%^HOME%^',             ''),  # Home
    '[_': ColorToken('',    '[_',   '{_',   '',     '',     '\033[K',       '\033[K',           '%^CLEARLINE%^',        ''),  # Clear to end of line
    '[@': ColorToken('',    '[@',   '{@',   '',     '',     '\033[J',       '\033[J',           '',                     ''),  # Clear to end of screen
    '[^': ColorToken('',    '[^',   '{^',   '',     '',     '\033[A',       '\033[A',           '%^CURS_UP%^',          ''),  # Cursor up
    '[v': ColorToken('',    '[v',   '{v',   '',     '',     '\033[B',       '\033[B',           '%^CURS_DOWN%^',        ''),  # Cursor down
    '[>': ColorToken('',    '[>',   '{>',   '',     '',     '\033[C',       '\033[C',           '%^CURS_RIGHT%^',       ''),  # Cursor right
    '[<': ColorToken('',    '[<',   '{<',   '',     '',     '\033[D',       '\033[D',           '%^CURS_LEFT%^',        ''),  # Cursor left

    # Background colors
    ']d': ColorToken('',    ']d',   '}d',   '^x',   '^x',   '\033[40m',     '\033[48;5;232m',   '%^B_BLACK%^',          '<COLOR BACK=\"#000000\">'),
    ']r': ColorToken('',    ']r',   '}r',   '^r',   '^r',   '\033[41m',     '\033[48;5;237m',   '%^B_RED%^',            '<COLOR BACK=\"#bb0000\">'),
    ']g': ColorToken('',    ']g',   '}g',   '^g',   '^g',   '\033[42m',     '\033[48;5;237m',   '%^B_GREEN%^',          '<COLOR BACK=\"#00bb00\">'),
    ']y': ColorToken('',    ']y',   '}y',   '^O',   '^y',   '\033[43m',     '\033[48;5;244m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#bbbb00\">'),
    ']b': ColorToken('',    ']b',   '}b',   '^b',   '^b',   '\033[44m',     '\033[48;5;237m',   '%^B_BLUE%^',           '<COLOR BACK=\"#0000bb\">'),
    ']m': ColorToken('',    ']m',   '}m',   '^p',   '^p',   '\033[45m',     '\033[48;5;244m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#bb00bb\">'),
    ']c': ColorToken('',    ']c',   '}c',   '^c',   '^c',   '\033[46m',     '\033[48;5;244m',   '%^B_CYAN%^',           '<COLOR BACK=\"#00bbbb\">'),
    ']w': ColorToken('',    ']w',   '}w',   '^w',   '^w',   '\033[47m',     '\033[48;5;250m',   '%^B_WHITE%^',          '<COLOR BACK=\"#bbbbbb\">'),

    # Background colors cannot BE bold in ANSI
    ']D': ColorToken('',    ']D',   '}D',   '^z',   '^z',   '\033[40m',     '\033[48;5;240m',   '%^B_BLACK%^',          '<COLOR BACK=\"#555555\">'),
    ']R': ColorToken('',    ']R',   '}R',   '^R',   '^R',   '\033[41m',     '\033[48;5;245m',   '%^B_RED%^',            '<COLOR BACK=\"#ff5555\">'),
    ']G': ColorToken('',    ']G',   '}G',   '^G',   '^G',   '\033[42m',     '\033[48;5;245m',   '%^B_GREEN%^',          '<COLOR BACK=\"#55ff55\">'),
    ']Y': ColorToken('',    ']Y',   '}Y',   '^Y',   '^Y',   '\033[43m',     '\033[48;5;251m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#ffff55\">'),
    ']B': ColorToken('',    ']B',   '}B',   '^B',   '^B',   '\033[44m',     '\033[48;5;245m',   '%^B_BLUE%^',           '<COLOR BACK=\"#5555ff\">'),
    ']M': ColorToken('',    ']M',   '}M',   '^P',   '^P',   '\033[45m',     '\033[48;5;251m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#ff55ff\">'),
    ']C': ColorToken('',    ']C',   '}C',   '^C',   '^C',   '\033[46m',     '\033[48;5;251m',   '%^B_CYAN%^',           '<COLOR BACK=\"#55ffff\">'),
    ']W': ColorToken('',    ']W',   '}W',   '^W',   '^W',   '\033[47m',     '\033[48;5;255m',   '%^B_WHITE%^',          '<COLOR BACK=\"#ffffff\">'),
}

COLOR_MAP['rom'] = {
    '{d': ColorToken('',    '[d',   '{d',   '&x',   '~x',   '\033[30m',     '\033[38;5;232m',   '%^BLACK%^',            '<COLOR FORE=\"#000000\">' ),
    '{r': ColorToken('',    '[r',   '{r',   '&r',   '~r',   '\033[31m',     '\033[38;5;237m',   '%^RED%^',              '<COLOR FORE=\"#bb0000\">' ),
    '{g': ColorToken('',    '[g',   '{g',   '&g',   '~g',   '\033[32m',     '\033[38;5;237m',   '%^GREEN%^',            '<COLOR FORE=\"#00bb00\">' ),
    '{y': ColorToken('',    '[y',   '{y',   '&O',   '~y',   '\033[33m',     '\033[38;5;244m',   '%^ORANGE%^',           '<COLOR FORE=\"#bbbb00\">' ),
    '{b': ColorToken('',    '[b',   '{b',   '&b',   '~b',   '\033[34m',     '\033[38;5;237m',   '%^BLUE%^',             '<COLOR FORE=\"#0000bb\">' ),
    '{m': ColorToken('',    '[m',   '{m',   '&p',   '~p',   '\033[35m',     '\033[38;5;244m',   '%^MAGENTA%^',          '<COLOR FORE=\"#bb00bb\">' ),
    '{c': ColorToken('',    '[c',   '{c',   '&c',   '~c',   '\033[36m',     '\033[38;5;244m',   '%^CYAN%^',             '<COLOR FORE=\"#00bbbb\">' ),
    '{w': ColorToken('',    '[w',   '{w',   '&w',   '~w',   '\033[37m',     '\033[38;5;250m',   '%^WHITE%^',            '<COLOR FORE=\"#bbbbbb\">' ),

    '{D': ColorToken('',    '[D',   '{D',   '&z',   '~z',   '\033[1;30m',   '\033[38;5;240m',   '%^BOLD%^BLACK%^',      '<COLOR FORE=\"#555555\">'),
    '{R': ColorToken('',    '[R',   '{R',   '&R',   '~R',   '\033[1;31m',   '\033[38;5;245m',   '%^BOLD%^RED%^',        '<COLOR FORE=\"#ff5555\">'),
    '{G': ColorToken('',    '[G',   '{G',   '&G',   '~G',   '\033[1;32m',   '\033[38;5;245m',   '%^BOLD%^GREEN%^',      '<COLOR FORE=\"#55ff55\">'),
    '{Y': ColorToken('',    '[Y',   '{Y',   '&Y',   '~Y',   '\033[1;33m',   '\033[38;5;251m',   '%^BOLD%^ORANGE%^',     '<COLOR FORE=\"#ffff55\">'),
    '{B': ColorToken('',    '[B',   '{B',   '&B',   '~B',   '\033[1;34m',   '\033[38;5;245m',   '%^BOLD%^BLUE%^',       '<COLOR FORE=\"#5555ff\">'),
    '{M': ColorToken('',    '[M',   '{M',   '&P',   '~P',   '\033[1;35m',   '\033[38;5;251m',   '%^BOLD%^MAGENTA%^',    '<COLOR FORE=\"#ff55ff\">'),
    '{C': ColorToken('',    '[C',   '{C',   '&C',   '~C',   '\033[1;36m',   '\033[38;5;251m',   '%^BOLD%^CYAN%^',       '<COLOR FORE=\"#55ffff\">'),
    '{W': ColorToken('',    '[W',   '{W',   '&W',   '~W',   '\033[1;37m',   '\033[38;5;255m',   '%^BOLD%^WHITE%^',      '<COLOR FORE=\"#ffffff\">'),

    '{*': ColorToken('',    '[*',   '{*',   '',     '',     '\007',         '\007',             '',                     ''),
    '{/': ColorToken('',    '[/',   '{/',   '',     '',     '\012',         '\012',             '',                     ''),

    '{{': ColorToken('{',   '{',    '{{',   '{',    '{',    '{',            '{',                '{',                    '{'),
    '}}': ColorToken('}',   '}',    '}}',   '}}',   '}',    '}',            '}',                '}',                    '}'),

    '{x': ColorToken('',    '[x',   '{x',   '&d',   '~!',   '\033[0m',      '\033[0m',          '%^RESET%^',            '<RESET>'),
    '{L': ColorToken('',    '[L',   '{L',   '&L',   '~L',   '\033[1m',      '\033[1m',          '%^BOLD%^',             '<BOLD>'),
    '{i': ColorToken('',    '[i',   '{i',   '&i',   '~i',   '\033[3m',      '\033[3m',          '%^ITALIC%^',           '<ITALIC>'),
    '{u': ColorToken('',    '[u',   '{u',   '&u',   '~u',   '\033[4m',      '\033[4m',          '%^UNDERLINE%^',        '<UNDERLINE>'),
    '{f': ColorToken('',    '[f',   '{f',   '&f',   '~$',   '\033[5m',      '\033[5m',          '%^FLASH%^',            '<FONT COLOR=BLINK>'),
    '{V': ColorToken('',    '[v',   '{v',   '&v',   '~v',   '\033[7m',      '\033[7m',          '%^REVERSE%^',          '<FONT COLOR=INVERSE>'),
    '{s': ColorToken('',    '[s',   '{s',   '&s',   '~s',   '\033[9m',      '\033[9m',          '%^STRIKETHRU%^',       '<STRIKEOUT>'),

    '{H': ColorToken('',    '[H',   '{H',   '',     '',     '\033[H',       '\033[H',           '%^HOME%^',             ''),  # Home
    '{_': ColorToken('',    '[_',   '{_',   '',     '',     '\033[K',       '\033[K',           '%^CLEARLINE%^',        ''),  # Clear to end of line
    '{@': ColorToken('',    '[@',   '{@',   '',     '',     '\033[J',       '\033[J',           '',                     ''),  # Clear to end of screen
    '{^': ColorToken('',    '[^',   '{^',   '',     '',     '\033[A',       '\033[A',           '%^CURS_UP%^',          ''),  # Cursor up
    '{v': ColorToken('',    '[v',   '{v',   '',     '',     '\033[B',       '\033[B',           '%^CURS_DOWN%^',        ''),  # Cursor down
    '{>': ColorToken('',    '[>',   '{>',   '',     '',     '\033[C',       '\033[C',           '%^CURS_RIGHT%^',       ''),  # Cursor right
    '{<': ColorToken('',    '[<',   '{<',   '',     '',     '\033[D',       '\033[D',           '%^CURS_LEFT%^',        ''),  # Cursor left

    # Background colors
    '}d': ColorToken('',    ']d',   '}d',   '^x',   '^x',   '\033[40m',     '\033[48;5;232m',   '%^B_BLACK%^',          '<COLOR BACK=\"#000000\">'),
    '}r': ColorToken('',    ']r',   '}r',   '^r',   '^r',   '\033[41m',     '\033[48;5;237m',   '%^B_RED%^',            '<COLOR BACK=\"#bb0000\">'),
    '}g': ColorToken('',    ']g',   '}g',   '^g',   '^g',   '\033[42m',     '\033[48;5;237m',   '%^B_GREEN%^',          '<COLOR BACK=\"#00bb00\">'),
    '}y': ColorToken('',    ']y',   '}y',   '^O',   '^y',   '\033[43m',     '\033[48;5;244m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#bbbb00\">'),
    '}b': ColorToken('',    ']b',   '}b',   '^b',   '^b',   '\033[44m',     '\033[48;5;237m',   '%^B_BLUE%^',           '<COLOR BACK=\"#0000bb\">'),
    '}m': ColorToken('',    ']m',   '}m',   '^p',   '^p',   '\033[45m',     '\033[48;5;244m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#bb00bb\">'),
    '}c': ColorToken('',    ']c',   '}c',   '^c',   '^c',   '\033[46m',     '\033[48;5;244m',   '%^B_CYAN%^',           '<COLOR BACK=\"#00bbbb\">'),
    '}w': ColorToken('',    ']w',   '}w',   '^w',   '^w',   '\033[47m',     '\033[48;5;250m',   '%^B_WHITE%^',          '<COLOR BACK=\"#bbbbbb\">'),

    # Background colors cannot BE bold in ANSI
    '}D': ColorToken('',    ']D',   '}D',   '^z',   '^z',   '\033[40m',     '\033[48;5;240m',   '%^B_BLACK%^',          '<COLOR BACK=\"#555555\">'),
    '}R': ColorToken('',    ']R',   '}R',   '^R',   '^R',   '\033[41m',     '\033[48;5;245m',   '%^B_RED%^',            '<COLOR BACK=\"#ff5555\">'),
    '}G': ColorToken('',    ']G',   '}G',   '^G',   '^G',   '\033[42m',     '\033[48;5;245m',   '%^B_GREEN%^',          '<COLOR BACK=\"#55ff55\">'),
    '}Y': ColorToken('',    ']Y',   '}Y',   '^Y',   '^Y',   '\033[43m',     '\033[48;5;251m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#ffff55\">'),
    '}B': ColorToken('',    ']B',   '}B',   '^B',   '^B',   '\033[44m',     '\033[48;5;245m',   '%^B_BLUE%^',           '<COLOR BACK=\"#5555ff\">'),
    '}M': ColorToken('',    ']M',   '}M',   '^P',   '^P',   '\033[45m',     '\033[48;5;251m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#ff55ff\">'),
    '}C': ColorToken('',    ']C',   '}C',   '^C',   '^C',   '\033[46m',     '\033[48;5;251m',   '%^B_CYAN%^',           '<COLOR BACK=\"#55ffff\">'),
    '}W': ColorToken('',    ']W',   '}W',   '^W',   '^W',   '\033[47m',     '\033[48;5;255m',   '%^B_WHITE%^',          '<COLOR BACK=\"#ffffff\">'),
}

COLOR_MAP['smaug'] = {
    '&x': ColorToken('',    '[d',   '{d',   '&x',   '~x',   '\033[30m',     '\033[38;5;232m',   '%^BLACK%^',            '<COLOR FORE=\"#000000\">' ),
    '&r': ColorToken('',    '[r',   '{r',   '&r',   '~r',   '\033[31m',     '\033[38;5;237m',   '%^RED%^',              '<COLOR FORE=\"#bb0000\">' ),
    '&g': ColorToken('',    '[g',   '{g',   '&g',   '~g',   '\033[32m',     '\033[38;5;237m',   '%^GREEN%^',            '<COLOR FORE=\"#00bb00\">' ),
    '&O': ColorToken('',    '[y',   '{y',   '&O',   '~y',   '\033[33m',     '\033[38;5;244m',   '%^ORANGE%^',           '<COLOR FORE=\"#bbbb00\">' ),
    '&b': ColorToken('',    '[b',   '{b',   '&b',   '~b',   '\033[34m',     '\033[38;5;237m',   '%^BLUE%^',             '<COLOR FORE=\"#0000bb\">' ),
    '&p': ColorToken('',    '[m',   '{m',   '&p',   '~p',   '\033[35m',     '\033[38;5;244m',   '%^MAGENTA%^',          '<COLOR FORE=\"#bb00bb\">' ),
    '&c': ColorToken('',    '[c',   '{c',   '&c',   '~c',   '\033[36m',     '\033[38;5;244m',   '%^CYAN%^',             '<COLOR FORE=\"#00bbbb\">' ),
    '&w': ColorToken('',    '[w',   '{w',   '&w',   '~w',   '\033[37m',     '\033[38;5;250m',   '%^WHITE%^',            '<COLOR FORE=\"#bbbbbb\">' ),

    '&z': ColorToken('',    '[D',   '{D',   '&z',   '~z',   '\033[1;30m',   '\033[38;5;240m',   '%^BOLD%^BLACK%^',      '<COLOR FORE=\"#555555\">'),
    '&R': ColorToken('',    '[R',   '{R',   '&R',   '~R',   '\033[1;31m',   '\033[38;5;245m',   '%^BOLD%^RED%^',        '<COLOR FORE=\"#ff5555\">'),
    '&G': ColorToken('',    '[G',   '{G',   '&G',   '~G',   '\033[1;32m',   '\033[38;5;245m',   '%^BOLD%^GREEN%^',      '<COLOR FORE=\"#55ff55\">'),
    '&Y': ColorToken('',    '[Y',   '{Y',   '&Y',   '~Y',   '\033[1;33m',   '\033[38;5;251m',   '%^BOLD%^ORANGE%^',     '<COLOR FORE=\"#ffff55\">'),
    '&B': ColorToken('',    '[B',   '{B',   '&B',   '~B',   '\033[1;34m',   '\033[38;5;245m',   '%^BOLD%^BLUE%^',       '<COLOR FORE=\"#5555ff\">'),
    '&P': ColorToken('',    '[M',   '{M',   '&P',   '~P',   '\033[1;35m',   '\033[38;5;251m',   '%^BOLD%^MAGENTA%^',    '<COLOR FORE=\"#ff55ff\">'),
    '&C': ColorToken('',    '[C',   '{C',   '&C',   '~C',   '\033[1;36m',   '\033[38;5;251m',   '%^BOLD%^CYAN%^',       '<COLOR FORE=\"#55ffff\">'),
    '&W': ColorToken('',    '[W',   '{W',   '&W',   '~W',   '\033[1;37m',   '\033[38;5;255m',   '%^BOLD%^WHITE%^',      '<COLOR FORE=\"#ffffff\">'),

    '&&': ColorToken('&',   '&',    '&',    '&&',   '&',    '&',            '&',                '&',                    '&'),
    '^^': ColorToken('^',   '^',    '^',    '^^',   '^^',   '^',            '^',                '^',                    '^'),
    '}}': ColorToken('}',   '}',    '}}',   '}}',   '}',    '}',            '}',                '}',                    '}'),

    '&d': ColorToken('',    '[x',   '{x',   '&d',   '~!',   '\033[0m',      '\033[0m',          '%^RESET%^',            '<RESET>'),
    '&L': ColorToken('',    '[L',   '{L',   '&L',   '~L',   '\033[1m',      '\033[1m',          '%^BOLD%^',             '<BOLD>'),
    '&i': ColorToken('',    '[i',   '{i',   '&i',   '~i',   '\033[3m',      '\033[3m',          '%^ITALIC%^',           '<ITALIC>'),
    '&u': ColorToken('',    '[u',   '{u',   '&u',   '~u',   '\033[4m',      '\033[4m',          '%^UNDERLINE%^',        '<UNDERLINE>'),
    '&f': ColorToken('',    '[f',   '{f',   '&f',   '~$',   '\033[5m',      '\033[5m',          '%^FLASH%^',            '<FONT COLOR=BLINK>'),
    '&v': ColorToken('',    '[v',   '{v',   '&v',   '~v',   '\033[7m',      '\033[7m',          '%^REVERSE%^',          '<FONT COLOR=INVERSE>'),
    '&s': ColorToken('',    '[s',   '{s',   '&s',   '~s',   '\033[9m',      '\033[9m',          '%^STRIKETHRU%^',       '<STRIKEOUT>'),

    '&I': ColorToken('',    '[i',   '{i',   '&i',   '~i',   '\033[3m',      '\033[3m',          '%^ITALIC%^',           '<ITALIC>'),
    '&U': ColorToken('',    '[u',   '{u',   '&u',   '~u',   '\033[4m',      '\033[4m',          '%^UNDERLINE%^',        '<UNDERLINE>'),
    '&F': ColorToken('',    '[f',   '{f',   '&f',   '~$',   '\033[5m',      '\033[5m',          '%^FLASH%^',            '<FONT COLOR=BLINK>'),
    '&V': ColorToken('',    '[v',   '{v',   '&v',   '~v',   '\033[7m',      '\033[7m',          '%^REVERSE%^',          '<FONT COLOR=INVERSE>'),
    '&S': ColorToken('',    '[s',   '{s',   '&s',   '~s',   '\033[9m',      '\033[9m',          '%^STRIKETHRU%^',       '<STRIKEOUT>'),

    # Background colors
    '^x': ColorToken('',    ']d',   '}d',   '^x',   '^x',   '\033[40m',     '\033[48;5;232m',   '%^B_BLACK%^',          '<COLOR BACK=\"#000000\">'),
    '^r': ColorToken('',    ']r',   '}r',   '^r',   '^r',   '\033[41m',     '\033[48;5;237m',   '%^B_RED%^',            '<COLOR BACK=\"#bb0000\">'),
    '^g': ColorToken('',    ']g',   '}g',   '^g',   '^g',   '\033[42m',     '\033[48;5;237m',   '%^B_GREEN%^',          '<COLOR BACK=\"#00bb00\">'),
    '^O': ColorToken('',    ']y',   '}y',   '^O',   '^y',   '\033[43m',     '\033[48;5;244m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#bbbb00\">'),
    '^b': ColorToken('',    ']b',   '}b',   '^b',   '^b',   '\033[44m',     '\033[48;5;237m',   '%^B_BLUE%^',           '<COLOR BACK=\"#0000bb\">'),
    '^p': ColorToken('',    ']m',   '}m',   '^p',   '^p',   '\033[45m',     '\033[48;5;244m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#bb00bb\">'),
    '^c': ColorToken('',    ']c',   '}c',   '^c',   '^c',   '\033[46m',     '\033[48;5;244m',   '%^B_CYAN%^',           '<COLOR BACK=\"#00bbbb\">'),
    '^w': ColorToken('',    ']w',   '}w',   '^w',   '^w',   '\033[47m',     '\033[48;5;250m',   '%^B_WHITE%^',          '<COLOR BACK=\"#bbbbbb\">'),

    # Background colors cannot BE bold in ANSI
    '^z': ColorToken('',    ']D',   '}D',   '^z',   '^z',   '\033[40m',     '\033[48;5;240m',   '%^B_BLACK%^',          '<COLOR BACK=\"#555555\">'),
    '^R': ColorToken('',    ']R',   '}R',   '^R',   '^R',   '\033[41m',     '\033[48;5;245m',   '%^B_RED%^',            '<COLOR BACK=\"#ff5555\">'),
    '^G': ColorToken('',    ']G',   '}G',   '^G',   '^G',   '\033[42m',     '\033[48;5;245m',   '%^B_GREEN%^',          '<COLOR BACK=\"#55ff55\">'),
    '^Y': ColorToken('',    ']Y',   '}Y',   '^Y',   '^Y',   '\033[43m',     '\033[48;5;251m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#ffff55\">'),
    '^B': ColorToken('',    ']B',   '}B',   '^B',   '^B',   '\033[44m',     '\033[48;5;245m',   '%^B_BLUE%^',           '<COLOR BACK=\"#5555ff\">'),
    '^P': ColorToken('',    ']M',   '}M',   '^P',   '^P',   '\033[45m',     '\033[48;5;251m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#ff55ff\">'),
    '^C': ColorToken('',    ']C',   '}C',   '^C',   '^C',   '\033[46m',     '\033[48;5;251m',   '%^B_CYAN%^',           '<COLOR BACK=\"#55ffff\">'),
    '^W': ColorToken('',    ']W',   '}W',   '^W',   '^W',   '\033[47m',     '\033[48;5;255m',   '%^B_WHITE%^',          '<COLOR BACK=\"#ffffff\">'),

    # Blinking colors
    '}x': ColorToken('',    '[f[d', '{f{d', '}x',   '`x',   '\033[5;30m',   '\033[5;38;5;232m', '%^FLASH%^BLACK%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#000000\">'),
    '}r': ColorToken('',    '[f[r', '{f{r', '}r',   '`r',   '\033[5;31m',   '\033[5;38;5;237m', '%^FLASH%^RED%^',       '<FONT COLOR=BLINK><COLOR FORE=\"#bb0000\">'),
    '}g': ColorToken('',    '[f[g', '{f{g', '}g',   '`g',   '\033[5;32m',   '\033[5;38;5;237m', '%^FLASH%^GREEN%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#00bb00\">'),
    '}O': ColorToken('',    '[f[y', '{f{y', '}O',   '`y',   '\033[5;33m',   '\033[5;38;5;244m', '%^FLASH%^ORANGE%^',    '<FONT COLOR=BLINK><COLOR FORE=\"#bbbb00\">'),
    '}b': ColorToken('',    '[f[b', '{f{b', '}b',   '`b',   '\033[5;34m',   '\033[5;38;5;237m', '%^FLASH%^BLUE%^',      '<FONT COLOR=BLINK><COLOR FORE=\"#0000bb\">'),
    '}p': ColorToken('',    '[f[m', '{f{m', '}p',   '`p',   '\033[5;35m',   '\033[5;38;5;244m', '%^FLASH%^MAGENTA%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#bb00bb\">'),
    '}c': ColorToken('',    '[f[c', '{f{c', '}c',   '`c',   '\033[5;36m',   '\033[5;38;5;244m', '%^FLASH%^CYAN%^',      '<FONT COLOR=BLINK><COLOR FORE=\"#00bbbb\">'),
    '}w': ColorToken('',    '[f[w', '{f{w', '}w',   '`w',   '\033[5;37m',   '\033[5;38;5;250m', '%^FLASH%^WHITE%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#bbbbbb\">'),

    '}z': ColorToken('',    ']f]D', '{f{D', '}z',   '`z',   '\033[5;1;30m', '\033[5;38;5;240m', '%^FLASH%^BOLD%^BLACK%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#555555\">'),
    '}R': ColorToken('',    ']f]R', '{f{R', '}R',   '`R',   '\033[5;1;31m', '\033[5;38;5;245m', '%^FLASH%^BOLD%^RED%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#ff5555\">'),
    '}G': ColorToken('',    ']f]G', '{f{G', '}G',   '`G',   '\033[5;1;32m', '\033[5;38;5;245m', '%^FLASH%^BOLD%^GREEN%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#55ff55\">'),
    '}Y': ColorToken('',    ']f]Y', '{f{Y', '}Y',   '`Y',   '\033[5;1;33m', '\033[5;38;5;251m', '%^FLASH%^BOLD%^ORANGE%^',  '<FONT COLOR=BLINK><COLOR FORE=\"#ffff55\">'),
    '}B': ColorToken('',    ']f]B', '{f{B', '}B',   '`B',   '\033[5;1;34m', '\033[5;38;5;245m', '%^FLASH%^BOLD%^BLUE%^',    '<FONT COLOR=BLINK><COLOR FORE=\"#5555ff\">'),
    '}P': ColorToken('',    ']f]M', '{f{M', '}P',   '`P',   '\033[5;1;35m', '\033[5;38;5;251m', '%^FLASH%^BOLD%^MAGENTA%^', '<FONT COLOR=BLINK><COLOR FORE=\"#ff55ff\">'),
    '}C': ColorToken('',    ']f]C', '{f{C', '}C',   '`C',   '\033[5;1;36m', '\033[5;38;5;251m', '%^FLASH%^BOLD%^CYAN%^',    '<FONT COLOR=BLINK><COLOR FORE=\"#55ffff\">'),
    '}W': ColorToken('',    ']f]W', '{f{W', '}W',   '`W',   '\033[5;1;37m', '\033[5;38;5;255m', '%^FLASH%^BOLD%^WHITE%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#ffffff\">'),
}

COLOR_MAP['i3'] = {
    'BLACK':        ColorToken('', '[d', '{d', '&x', '~x', '\033[30m',      '\033[38;5;232m',   '%^BLACK%^',        '<COLOR FORE=\"#000000\">'),
    'RED':          ColorToken('', '[r', '{r', '&r', '~r', '\033[31m',      '\033[38;5;237m',   '%^RED%^',          '<COLOR FORE=\"#bb0000\">'),
    'GREEN':        ColorToken('', '[g', '{g', '&g', '~g', '\033[32m',      '\033[38;5;237m',   '%^GREEN%^',        '<COLOR FORE=\"#00bb00\">'),
    'ORANGE':       ColorToken('', '[y', '{y', '&O', '~y', '\033[33m',      '\033[38;5;244m',   '%^ORANGE%^',       '<COLOR FORE=\"#bbbb00\">'),
    'BLUE':         ColorToken('', '[b', '{b', '&b', '~b', '\033[34m',      '\033[38;5;237m',   '%^BLUE%^',         '<COLOR FORE=\"#0000bb\">'),
    'MAGENTA':      ColorToken('', '[m', '{m', '&p', '~p', '\033[35m',      '\033[38;5;244m',   '%^MAGENTA%^',      '<COLOR FORE=\"#bb00bb\">'),
    'CYAN':         ColorToken('', '[c', '{c', '&c', '~c', '\033[36m',      '\033[38;5;244m',   '%^CYAN%^',         '<COLOR FORE=\"#00bbbb\">'),
    'WHITE':        ColorToken('', '[w', '{w', '&w', '~w', '\033[37m',      '\033[38;5;250m',   '%^WHITE%^',        '<COLOR FORE=\"#bbbbbb\">'),
    'YELLOW':       ColorToken('', '[Y', '{Y', '&Y', '~Y', '\033[1;33m',    '\033[38;5;251m',   '%^BOLD%^ORANGE%^', '<COLOR FORE=\"#ffff55\">'),

    'RESET':        ColorToken('', '[x', '{x', '&d', '~!', '\033[0m',       '\033[0m',          '%^RESET%^',        '<RESET>'),
    'BOLD':         ColorToken('', '[L', '{L', '&L', '~L', '\033[1m',       '\033[1m',          '%^BOLD%^',         '<BOLD>'),
    'ITALIC':       ColorToken('', '[i', '{i', '&i', '~i', '\033[3m',       '\033[3m',          '%^ITALIC%^',       '<ITALIC>'),
    'UNDERLINE':    ColorToken('', '[u', '{u', '&u', '~u', '\033[4m',       '\033[4m',          '%^UNDERLINE%^',    '<UNDERLINE>'),
    'FLASH':        ColorToken('', '[f', '{f', '&f', '~$', '\033[5m',       '\033[5m',          '%^FLASH%^',        '<FONT COLOR=BLINK>'),
    'REVERSE':      ColorToken('', '[v', '{v', '&v', '~v', '\033[7m',       '\033[7m',          '%^REVERSE%^',      '<FONT COLOR=INVERSE>'),
    'STRIKETHRU':   ColorToken('', '[s', '{s', '&s', '~s', '\033[9m',       '\033[9m',          '%^STRIKETHRU%^',   '<STRIKEOUT>'),

    'HOME':         ColorToken('', '[H', '{H', '', '', '\033[H', '\033[H', '%^HOME%^',          ''),  # Home
    'CLEARLINE':    ColorToken('', '[_', '{_', '', '', '\033[K', '\033[K', '%^CLEARLINE%^',     ''),  # Clear to end of line
    'CURS_UP':      ColorToken('', '[^', '{^', '', '', '\033[A', '\033[A', '%^CURS_UP%^',       ''),  # Cursor up
    'CURS_DOWN':    ColorToken('', '[v', '{v', '', '', '\033[B', '\033[B', '%^CURS_DOWN%^',     ''),  # Cursor down
    'CURS_RIGHT':   ColorToken('', '[>', '{>', '', '', '\033[C', '\033[C', '%^CURS_RIGHT%^',    ''),  # Cursor right
    'CURS_LEFT':    ColorToken('', '[<', '{<', '', '', '\033[D', '\033[D', '%^CURS_LEFT%^',     ''),  # Cursor left

    'B_BLACK':      ColorToken('', ']d', '}d', '^x', '^x', '\033[40m', '\033[48;5;232m', '%^B_BLACK%^',   '<COLOR BACK=\"#000000\">'),
    'B_RED':        ColorToken('', ']r', '}r', '^r', '^r', '\033[41m', '\033[48;5;237m', '%^B_RED%^',     '<COLOR BACK=\"#bb0000\">'),
    'B_GREEN':      ColorToken('', ']g', '}g', '^g', '^g', '\033[42m', '\033[48;5;237m', '%^B_GREEN%^',   '<COLOR BACK=\"#00bb00\">'),
    'B_ORANGE':     ColorToken('', ']y', '}y', '^O', '^y', '\033[43m', '\033[48;5;244m', '%^B_ORANGE%^',  '<COLOR BACK=\"#bbbb00\">'),
    'B_BLUE':       ColorToken('', ']b', '}b', '^b', '^b', '\033[44m', '\033[48;5;237m', '%^B_BLUE%^',    '<COLOR BACK=\"#0000bb\">'),
    'B_MAGENTA':    ColorToken('', ']m', '}m', '^p', '^p', '\033[45m', '\033[48;5;244m', '%^B_MAGENTA%^', '<COLOR BACK=\"#bb00bb\">'),
    'B_CYAN':       ColorToken('', ']c', '}c', '^c', '^c', '\033[46m', '\033[48;5;244m', '%^B_CYAN%^',    '<COLOR BACK=\"#00bbbb\">'),
    'B_WHITE':      ColorToken('', ']w', '}w', '^w', '^w', '\033[47m', '\033[48;5;250m', '%^B_WHITE%^',   '<COLOR BACK=\"#bbbbbb\">'),
    'B_YELLOW':     ColorToken('', ']Y', '}Y', '^Y', '^Y', '\033[43m', '\033[48;5;251m', '%^B_ORANGE%^',  '<COLOR BACK=\"#ffff55\">'),
}

COLOR_MAP['imc2'] = {
    '~x': ColorToken('',    '[d',   '{d',   '&x',   '~x',   '\033[30m',     '\033[38;5;232m',   '%^BLACK%^',            '<COLOR FORE=\"#000000\">' ),
    '~r': ColorToken('',    '[r',   '{r',   '&r',   '~r',   '\033[31m',     '\033[38;5;237m',   '%^RED%^',              '<COLOR FORE=\"#bb0000\">' ),
    '~g': ColorToken('',    '[g',   '{g',   '&g',   '~g',   '\033[32m',     '\033[38;5;237m',   '%^GREEN%^',            '<COLOR FORE=\"#00bb00\">' ),
    '~y': ColorToken('',    '[y',   '{y',   '&O',   '~y',   '\033[33m',     '\033[38;5;244m',   '%^ORANGE%^',           '<COLOR FORE=\"#bbbb00\">' ),
    '~b': ColorToken('',    '[b',   '{b',   '&b',   '~b',   '\033[34m',     '\033[38;5;237m',   '%^BLUE%^',             '<COLOR FORE=\"#0000bb\">' ),
    '~p': ColorToken('',    '[m',   '{m',   '&p',   '~p',   '\033[35m',     '\033[38;5;244m',   '%^MAGENTA%^',          '<COLOR FORE=\"#bb00bb\">' ),
    '~c': ColorToken('',    '[c',   '{c',   '&c',   '~c',   '\033[36m',     '\033[38;5;244m',   '%^CYAN%^',             '<COLOR FORE=\"#00bbbb\">' ),
    '~w': ColorToken('',    '[w',   '{w',   '&w',   '~w',   '\033[37m',     '\033[38;5;250m',   '%^WHITE%^',            '<COLOR FORE=\"#bbbbbb\">' ),

    '~z': ColorToken('',    '[D',   '{D',   '&z',   '~z',   '\033[1;30m',   '\033[38;5;240m',   '%^BOLD%^BLACK%^',      '<COLOR FORE=\"#555555\">'),
    '~R': ColorToken('',    '[R',   '{R',   '&R',   '~R',   '\033[1;31m',   '\033[38;5;245m',   '%^BOLD%^RED%^',        '<COLOR FORE=\"#ff5555\">'),
    '~G': ColorToken('',    '[G',   '{G',   '&G',   '~G',   '\033[1;32m',   '\033[38;5;245m',   '%^BOLD%^GREEN%^',      '<COLOR FORE=\"#55ff55\">'),
    '~Y': ColorToken('',    '[Y',   '{Y',   '&Y',   '~Y',   '\033[1;33m',   '\033[38;5;251m',   '%^BOLD%^ORANGE%^',     '<COLOR FORE=\"#ffff55\">'),
    '~B': ColorToken('',    '[B',   '{B',   '&B',   '~B',   '\033[1;34m',   '\033[38;5;245m',   '%^BOLD%^BLUE%^',       '<COLOR FORE=\"#5555ff\">'),
    '~P': ColorToken('',    '[M',   '{M',   '&P',   '~P',   '\033[1;35m',   '\033[38;5;251m',   '%^BOLD%^MAGENTA%^',    '<COLOR FORE=\"#ff55ff\">'),
    '~C': ColorToken('',    '[C',   '{C',   '&C',   '~C',   '\033[1;36m',   '\033[38;5;251m',   '%^BOLD%^CYAN%^',       '<COLOR FORE=\"#55ffff\">'),
    '~W': ColorToken('',    '[W',   '{W',   '&W',   '~W',   '\033[1;37m',   '\033[38;5;255m',   '%^BOLD%^WHITE%^',      '<COLOR FORE=\"#ffffff\">'),

    '~~': ColorToken('~',   '~',    '~',    '~',    '~~',   '~',            '~',                '~',                    '~'),
    '^^': ColorToken('^',   '^',    '^',    '^^',   '^^',   '^',            '^',                '^',                    '^'),
    '``': ColorToken('`',   '`',    '`',    '`',    '``',   '`',            '`',                '`',                    '`'),

    '~!': ColorToken('',    '[x',   '{x',   '&d',   '~!',   '\033[0m',      '\033[0m',          '%^RESET%^',            '<RESET>'),
    '~L': ColorToken('',    '[L',   '{L',   '&L',   '~L',   '\033[1m',      '\033[1m',          '%^BOLD%^',             '<BOLD>'),
    '~i': ColorToken('',    '[i',   '{i',   '&i',   '~i',   '\033[3m',      '\033[3m',          '%^ITALIC%^',           '<ITALIC>'),
    '~u': ColorToken('',    '[u',   '{u',   '&u',   '~u',   '\033[4m',      '\033[4m',          '%^UNDERLINE%^',        '<UNDERLINE>'),
    '~$': ColorToken('',    '[f',   '{f',   '&f',   '~$',   '\033[5m',      '\033[5m',          '%^FLASH%^',            '<FONT COLOR=BLINK>'),
    '~v': ColorToken('',    '[v',   '{v',   '&v',   '~v',   '\033[7m',      '\033[7m',          '%^REVERSE%^',          '<FONT COLOR=INVERSE>'),
    '~s': ColorToken('',    '[s',   '{s',   '&s',   '~s',   '\033[9m',      '\033[9m',          '%^STRIKETHRU%^',       '<STRIKEOUT>'),

    '~Z': ColorToken('',    '',     '',     '&Z',   '~Z',   '',             '',                 '',                     ''),  # Random foreground
    '~D': ColorToken('',    '[D',   '{D',   '&z',   '~z',   '\033[1;30m',   '\033[38;5;240m',   '%^BOLD%^BLACK%^',      '<COLOR FORE=\"#555555\">'),
    '~m': ColorToken('',    '[m',   '{m',   '&p',   '~p',   '\033[35m',     '\033[38;5;244m',   '%^MAGENTA%^',          '<COLOR FORE=\"#bb00bb\">'),
    '~d': ColorToken('',    '[w',   '{w',   '&w',   '~w',   '\033[37m',     '\033[38;5;250m',   '%^WHITE%^',            '<COLOR FORE=\"#bbbbbb\">'),
    '~M': ColorToken('',    '[M',   '{M',   '&P',   '~P',   '\033[1;35m',   '\033[38;5;251m',   '%^BOLD%^MAGENTA%^',    '<COLOR FORE=\"#ff55ff\">'),

    # Background colors
    '^x': ColorToken('',    ']d',   '}d',   '^x',   '^x',   '\033[40m',     '\033[48;5;232m',   '%^B_BLACK%^',          '<COLOR BACK=\"#000000\">'),
    '^r': ColorToken('',    ']r',   '}r',   '^r',   '^r',   '\033[41m',     '\033[48;5;237m',   '%^B_RED%^',            '<COLOR BACK=\"#bb0000\">'),
    '^g': ColorToken('',    ']g',   '}g',   '^g',   '^g',   '\033[42m',     '\033[48;5;237m',   '%^B_GREEN%^',          '<COLOR BACK=\"#00bb00\">'),
    '^y': ColorToken('',    ']y',   '}y',   '^O',   '^y',   '\033[43m',     '\033[48;5;244m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#bbbb00\">'),
    '^b': ColorToken('',    ']b',   '}b',   '^b',   '^b',   '\033[44m',     '\033[48;5;237m',   '%^B_BLUE%^',           '<COLOR BACK=\"#0000bb\">'),
    '^p': ColorToken('',    ']m',   '}m',   '^p',   '^p',   '\033[45m',     '\033[48;5;244m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#bb00bb\">'),
    '^c': ColorToken('',    ']c',   '}c',   '^c',   '^c',   '\033[46m',     '\033[48;5;244m',   '%^B_CYAN%^',           '<COLOR BACK=\"#00bbbb\">'),
    '^w': ColorToken('',    ']w',   '}w',   '^w',   '^w',   '\033[47m',     '\033[48;5;250m',   '%^B_WHITE%^',          '<COLOR BACK=\"#bbbbbb\">'),

    # Background colors cannot BE bold in ANSI
    '^z': ColorToken('',    ']D',   '}D',   '^z',   '^z',   '\033[40m',     '\033[48;5;240m',   '%^B_BLACK%^',          '<COLOR BACK=\"#555555\">'),
    '^R': ColorToken('',    ']R',   '}R',   '^R',   '^R',   '\033[41m',     '\033[48;5;245m',   '%^B_RED%^',            '<COLOR BACK=\"#ff5555\">'),
    '^G': ColorToken('',    ']G',   '}G',   '^G',   '^G',   '\033[42m',     '\033[48;5;245m',   '%^B_GREEN%^',          '<COLOR BACK=\"#55ff55\">'),
    '^Y': ColorToken('',    ']Y',   '}Y',   '^Y',   '^Y',   '\033[43m',     '\033[48;5;251m',   '%^B_ORANGE%^',         '<COLOR BACK=\"#ffff55\">'),
    '^B': ColorToken('',    ']B',   '}B',   '^B',   '^B',   '\033[44m',     '\033[48;5;245m',   '%^B_BLUE%^',           '<COLOR BACK=\"#5555ff\">'),
    '^P': ColorToken('',    ']M',   '}M',   '^P',   '^P',   '\033[45m',     '\033[48;5;251m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#ff55ff\">'),
    '^C': ColorToken('',    ']C',   '}C',   '^C',   '^C',   '\033[46m',     '\033[48;5;251m',   '%^B_CYAN%^',           '<COLOR BACK=\"#55ffff\">'),
    '^W': ColorToken('',    ']W',   '}W',   '^W',   '^W',   '\033[47m',     '\033[48;5;255m',   '%^B_WHITE%^',          '<COLOR BACK=\"#ffffff\">'),

    '^D': ColorToken('',    ']D',   '}D',   '^z',   '^z',   '\033[40m',     '\033[48;5;232m',   '%^B_BLACK%^',          '<COLOR BACK=\"#555555\">'),
    '^m': ColorToken('',    ']m',   '}m',   '^p',   '^p',   '\033[45m',     '\033[48;5;244m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#bb00bb\">'),
    '^d': ColorToken('',    ']w',   '}w',   '^w',   '^w',   '\033[47m',     '\033[48;5;250m',   '%^B_WHITE%^',          '<COLOR BACK=\"#bbbbbb\">'),
    '^M': ColorToken('',    ']M',   '}M',   '^P',   '^P',   '\033[45m',     '\033[48;5;244m',   '%^B_MAGENTA%^',        '<COLOR BACK=\"#ff55ff\">'),

    # Blinking colors
    '`x': ColorToken('',    '[f[d', '{f{d', '}x',   '`x',   '\033[5;30m',   '\033[5;38;5;232m', '%^FLASH%^BLACK%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#000000\">'),
    '`r': ColorToken('',    '[f[r', '{f{r', '}r',   '`r',   '\033[5;31m',   '\033[5;38;5;237m', '%^FLASH%^RED%^',       '<FONT COLOR=BLINK><COLOR FORE=\"#bb0000\">'),
    '`g': ColorToken('',    '[f[g', '{f{g', '}g',   '`g',   '\033[5;32m',   '\033[5;38;5;237m', '%^FLASH%^GREEN%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#00bb00\">'),
    '`y': ColorToken('',    '[f[y', '{f{y', '}O',   '`y',   '\033[5;33m',   '\033[5;38;5;244m', '%^FLASH%^ORANGE%^',    '<FONT COLOR=BLINK><COLOR FORE=\"#bbbb00\">'),
    '`b': ColorToken('',    '[f[b', '{f{b', '}b',   '`b',   '\033[5;34m',   '\033[5;38;5;237m', '%^FLASH%^BLUE%^',      '<FONT COLOR=BLINK><COLOR FORE=\"#0000bb\">'),
    '`p': ColorToken('',    '[f[m', '{f{m', '}p',   '`p',   '\033[5;35m',   '\033[5;38;5;244m', '%^FLASH%^MAGENTA%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#bb00bb\">'),
    '`c': ColorToken('',    '[f[c', '{f{c', '}c',   '`c',   '\033[5;36m',   '\033[5;38;5;244m', '%^FLASH%^CYAN%^',      '<FONT COLOR=BLINK><COLOR FORE=\"#00bbbb\">'),
    '`w': ColorToken('',    '[f[w', '{f{w', '}w',   '`w',   '\033[5;37m',   '\033[5;38;5;250m', '%^FLASH%^WHITE%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#bbbbbb\">'),

    '`z': ColorToken('',    ']f]D', '{f{D', '}z',   '`z',   '\033[5;1;30m', '\033[5;38;5;240m', '%^FLASH%^BOLD%^BLACK%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#555555\">'),
    '`R': ColorToken('',    ']f]R', '{f{R', '}R',   '`R',   '\033[5;1;31m', '\033[5;38;5;245m', '%^FLASH%^BOLD%^RED%^',     '<FONT COLOR=BLINK><COLOR FORE=\"#ff5555\">'),
    '`G': ColorToken('',    ']f]G', '{f{G', '}G',   '`G',   '\033[5;1;32m', '\033[5;38;5;245m', '%^FLASH%^BOLD%^GREEN%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#55ff55\">'),
    '`Y': ColorToken('',    ']f]Y', '{f{Y', '}Y',   '`Y',   '\033[5;1;33m', '\033[5;38;5;251m', '%^FLASH%^BOLD%^ORANGE%^',  '<FONT COLOR=BLINK><COLOR FORE=\"#ffff55\">'),
    '`B': ColorToken('',    ']f]B', '{f{B', '}B',   '`B',   '\033[5;1;34m', '\033[5;38;5;245m', '%^FLASH%^BOLD%^BLUE%^',    '<FONT COLOR=BLINK><COLOR FORE=\"#5555ff\">'),
    '`P': ColorToken('',    ']f]M', '{f{M', '}P',   '`P',   '\033[5;1;35m', '\033[5;38;5;251m', '%^FLASH%^BOLD%^MAGENTA%^', '<FONT COLOR=BLINK><COLOR FORE=\"#ff55ff\">'),
    '`C': ColorToken('',    ']f]C', '{f{C', '}C',   '`C',   '\033[5;1;36m', '\033[5;38;5;251m', '%^FLASH%^BOLD%^CYAN%^',    '<FONT COLOR=BLINK><COLOR FORE=\"#55ffff\">'),
    '`W': ColorToken('',    ']f]W', '{f{W', '}W',   '`W',   '\033[5;1;37m', '\033[5;38;5;255m', '%^FLASH%^BOLD%^WHITE%^',   '<FONT COLOR=BLINK><COLOR FORE=\"#ffffff\">'),

    '`D': ColorToken('',    '[f[D', '{f{D', '}z',   '`z',   '\033[5;1;30m', '\033[5;48;5;232m', '%^FLASH%^BOLD%^B_BLACK%^',  '<FONT COLOR=BLINK><COLOR FORE=\"#555555\">'),
    '`m': ColorToken('',    '[f[m', '{f{m', '}p',   '`p',   '\033[5;35m',   '\033[5;48;5;244m', '%^FLASH%^MAGENTA%^',        '<FONT COLOR=BLINK><COLOR FORE=\"#bb00bb\">'),
    '`d': ColorToken('',    '[f[w', '{f{w', '}w',   '`w',   '\033[5;37m',   '\033[5;48;5;250m', '%^FLASH%^WHITE%^',          '<FONT COLOR=BLINK><COLOR FORE=\"#bbbbbb\">'),
    '`M': ColorToken('',    '[f[M', '{f{M', '}P',   '`P',   '\033[5;1;35m', '\033[5;48;5;244m', '%^FLASH%^BOLD%^MAGENTA%^',  '<FONT COLOR=BLINK><COLOR FORE=\"#ff55ff\">'),
}
