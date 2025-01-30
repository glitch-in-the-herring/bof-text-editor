from lark import Lark
from lark import Transformer

with open("./bof_text_editor/grammars/bof3_grammar.lark", "r") as f:
    parser = Lark(f)

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
        "~": 0x8c,
        "&": 0x8d,
        "\'": 0x8e,
        ":": 0x8f,
        "\"": 0x90,
        ";": 0x91,
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

    _selection_map = {
        "OVR": 0x00,
        "NEW": 0x10,
    }

    _textbox_pos_map = {
        "BM": 0x00,
        "MM": 0x01,
        "TM": 0x02,
        "TL": 0x03,
        "TR": 0x04,
        "BL": 0x05,
        "BR": 0x06,
    }

    _textbox_vis_map = {
        "NV": 0x00,
        "SV": 0x40,
        "NI": 0x80,
    }


    def concat(self, l):
        ret = []
        for i in l:
            ret.extend(i)
        return ret


    def hex_number(self, h):
        h, = h
        return int(h[2:], base=16)


    def number(self, n):
        n, = n
        return int(n)


    def variable(self, v):
        return (str(v[0]).upper(), v[2])

    def int_var(self, v):
        return v[0]
    

    def string_var(self, v):
        return str(v[0])[1:-1]


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
        return l[0] + [0x02]


    def end_null(self, l):
        return l[0] + [0x00]


    def string_text(self, s):
        return self.concat(s)


    def string(self, s):
        return s[0]


    def content_string(self, s):
        return [-1] + s[0] + [0x00]

    
    def content(self, c):
        return self.concat(c)


    def inline_formatting(self, f):
        return self.concat(f)

    
    def color_start(self, c):
        color = str(c[1]).upper()
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
        effect = str(e[1]).upper()
        return [0x0e, 0x0f, self._effect_map[effect]]

    
    def pause(self, p):
        p0, p1 = p
        return p0 + [0x0b] + p1


    def pointer(self, p):
        p0, p1 = p
        return p0 + [-1] + p1


    def inline_macro(self, m):
        return m[0] + m[1] + m[2]


    def macro_block(self, m):
        return m[1]


    def textbox_start(self, m):
        return [0x0c] + m


    def party_start(self, m):
        return [0x04] + m


    def placeholder_start(self, m):
        return [0x07] + m
    

    def symbol_start(self, m):
        return m

    
    def duration_start(self, m):
        return [0x16] + m


    def selection_start(self, m):
        m, = m
        return [0x14] + [m[0]] + [0x0c] + [m[1]]


    def textbox_macro(self, m):
        pos = str(m[1]).upper()
        vis = str(m[3]).upper()
        return self._textbox_pos_map[pos] |  self._textbox_vis_map[vis]

    
    def party_macro(self, m):
        member = str(m[1]).upper()
        return self._party_map[member]


    def placeholder_macro(self, m):
        return m[1]


    def symbol_macro(self, m):
        return m[1]


    def duration_macro(self, m):
        return m[1]


    def selection_macro(self, m):
        selection = str(m[3]).upper()
        return [m[1], self._selection_map[selection] | m[5]]


    def multiline_formatting(self, f):
        return f[0]
    

    def multiline_color(self, c):
        return self.concat(c[:-1]) + [c[-1]]


    def multiline_effect(self, e):
        return [e[0]] + self.concat(e[1:])


    start = list
    variables = dict
    safe_text = list


class Processor():
    def __init__(self, padding=True, as_bytes=True):
        self.padding = padding
        self.as_bytes = as_bytes


    def process(self, transform_output):
        var, byte_array = transform_output
        ret_ptr = []
        ret_str = []
        
        self.ptsize = 512
        if "PTSIZE" in var.keys():
            self.ptsize = var["PTSIZE"] & 0xffff

        self.target = "output.bin"
        if "TARGET" in var.keys():
            self.target = var["TARGET"]
        
        pos = 0
        for i in byte_array:
            if i >= 0:
                ret_str.append(i)
                pos += 1
            else:
                ret_ptr.extend([i for i in int.to_bytes(self.ptsize + pos, length=2, byteorder="little")])

        ptr_remainder = -len(ret_ptr) % self.ptsize
        ret_ptr.extend(
            [i for i in int.to_bytes(len(ret_str) + self.ptsize, length=2, byteorder="little")] * (ptr_remainder // 2)
        )

        if self.padding:
            str_remainder = -(len(ret_str) + self.ptsize) % 2048
            ret_str.extend([0x5f] * str_remainder)

        if self.as_bytes:
            return bytes(ret_ptr + ret_str), self.target
        else:
            return ret_ptr + ret_str, self.target
