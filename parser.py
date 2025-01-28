from lark import Lark
from lark import Transformer

with open("grammar.lark", "r") as f:
    parser = Lark(f)

with open("test.txt", "r") as f:
    text = f.read()

tree = parser.parse(text)

# print(tree.pretty())

class SyntaxTransformer(Transformer):
    _punct_map = {
        "(": 0x3a,
        ")": 0x3b,
        ",": 0x3c,
        "-": 0x3d,
        ".": 0x3e,
        "/": 0x3f,
        "?": 0x5c,
        "!": 0x5d,
        "+": 0x8b,
        "\'": 0x8e,
        ":": 0x8f,
        "\"": 0x90,
        "%": 0x93,
    }

    _color_map = {
        "PURPLE": 0x01,
        "RED": 0x02,
        "CYAN": 0x03,
        "YELLOW": 0x04,
        "PINK": 0x05,
        "GREEN": 0x06,
        "BLACK": 0x07,
    }

    _effect_map = {
        "SHK_S": 0x00,
        "SHK_L": 0x01,
        "SHK_P": 0x02,
        "BIG0_S": 0x03,
        "BIG1_S": 0x04,
        "BIG2_S": 0x05,
        "BIG0_L": 0x06,
        "BIG1_L": 0x07,
        "BIG2_L": 0x08,
        "BIG0_P": 0x09,
        "BIG1_P": 0x0a,
        "BIG2_P": 0x0b,
        "SML0_S": 0x0c,
        "SML1_S": 0x0d,
        "SML2_S": 0x0e,
        "SML0_L": 0x0f,
        "SML1_L": 0x10,
        "SML2_L": 0x11,
        "SML0_P": 0x12,
        "SML1_P": 0x13,
        "SML2_P": 0x14,
        "WAV_L": 0x15,
        "WAV_H": 0x16,
        "JMP0": 0x17,
        "JMP1": 0x18,
        "JMP2": 0x19,
    }

    _party_map = {
        "RYU": 0x00,
        "NINA": 0x01,
        "GARR": 0x02,
        "TEEPO": 0x03,
        "REI": 0x04,
        "MOMO": 0x05,
        "PECO": 0x06,
    }

    def hex_number(self, h):
        h, = h
        return int(h[2:], base=16)


    def number(self, n):
        n, = n
        return int(n)


    def variable(self, v):
        name, v, *_ = v
        return (str(name), v)

    def safe_alphanum(self, c):
        c, = c
        return ord(c)
    

    def space(self, s):
        return 0xff

    
    def punct(self, p):
        p, = p
        return self._punct_map[p]

    
    def end_newline(self, l):
        return l[0] + [0x01]


    def end_newbox(self, l):
        return l[0] + [0x20]


    def string_text(self, s):
        ret = []
        for i in s:
            ret.extend(i)
        return ret


    def string(self, s):
        return s[0]


    def content_string(self, s):
        return s[0] + [0x00]

    
    def content(self, c):
        return c[0]


    def inline_formatting(self, f):
        ret = []
        for i in f:
            ret.extend(i)
        return ret

    
    def color_start(self, c):
        color = str(c[0]).upper()
        return [0x05, self._color_map[color]]


    def color_end(self, c):
        return 0x06

    
    def inline_color(self, c):
        return c[0] + c[1] + [c[2]]


    def inline_effect(self, c):
        return [c[0]] + c[1] + c[2]


    def effect_start(self, e):
        return 0x0d


    def effect_end(self, e):
        effect = str(e[0]).upper()
        return [0x0e, 0x0f, self._effect_map[effect]]

    
    def pause(self, p):
        p0, p1 = p
        return p0 + [0x0b] + p1


    def inline_macro(self, m):
        return m[0] + m[1] + m[2]


    def macro_block(self, m):
        return m[0]


    def party_start(self, m):
        return [0x04] + m


    def placeholder_start(self, m):
        return [0x07] + m
    

    def symbol_start(self, m):
        return m

    
    def duration_start(self, m):
        return [0x16] + m


    def party_macro(self, m):
        member = str(m[0]).upper()
        return self._party_map[member]


    def placeholder_macro(self, m):
        return m[0]


    def symbol_macro(self, m):
        return m[0]


    def duration_macro(self, m):
        return m[0]
    

    start = list
    variables = dict
    safe_text = list

transform = SyntaxTransformer().transform(tree)
print(transform[1])
