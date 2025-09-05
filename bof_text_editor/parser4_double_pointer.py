from lark import Lark
from lark import Transformer

with open("./bof_text_editor/grammars/bof4_double_pointer_grammar.lark", "r") as f:
    parser = Lark(f)

class SyntaxTransformer(Transformer):
    _color_map = {
        "GREY": 0x01,
        "RED": 0x02,
        "CYAN": 0x03,
        "GREEN": 0x04,
        "PINK": 0x05,
        "YELLOW": 0x06,
        "MAGENTA": 0x07,
        "WHITE": 0x08,
    }

    _effect_map = {
        "SHK": 0x00,
        "SHK_H": 0x01,
        "BIG_1": 0x02,
        "BIG_H": 0x03,
        "BBIG": 0x04,
        "BBIG_H": 0x05,
        "SML": 0x06,
        "SML_H": 0x07,
        "WAV": 0x08,
        "JMP": 0x09,
        "BIG_2": 0x0a,
    }

    _party_map = {
        "RYU": 0x00,
        "NINA": 0x01,
        "CRAY": 0x02,
        "SCIAS": 0x03,
        "URSULA": 0x04,
        "ERSHIN": 0x05,
        "FOULU": 0x06,
    }

    _selection_map = {
        "OVR_B": 0x90,
        "OVR_S_1": 0x80,
        "RPL": 0x70,
        "OVR_S_2": 0x00,
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
        "DV": 0x20,
        "SV": 0x40,
        "NI": 0x80,
    }

    _zenny_map = {
        "TR": 0x00,
        "TL": 0x01,
        "BR": 0x02,
        "BL": 0x03,
    }

    _portrait_source_map = {
        "AREA" : 0x00,
        "DEF" : 0x50,
        "AREA_M" : 0x80,
        "DEF_M" : 0xd0,
    }

    _portrait_pos_map = {
        "L": 0x00,
        "R": 0x40,
        "LL": 0x80,
        "RR": 0xc0,
    }

    _inventory_map = {
        "ITEM": 0x00,
        "WEAPON": 0x01,
        "ARMOR": 0x02,
        "ACC": 0x03,
        "SPELL": 0x04,
        "KEY": 0x05,
    }

    _typing_map = {
        "TRUE": 0x00,
        "FALSE": 0x01,
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


    def safe_chars(self, c):
        return ord(c[0])
    
    
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


    def normal_content_string(self, s):
        return [-1] + s[0] + [0x00]


    def endreference_content_string(self, s):
        return [-1] + s[0] + s[1]
    
    
    def content(self, c):
        return self.concat(c)


    def inline_formatting(self, f):
        return self.concat(f)

    
    def str_color(self, c):
        color = str(c[1]).upper()
        return [0x05, self._color_map[color]]

    
    def int_color(self, c):
        return [0x05, c[1]]


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


    def halfspace(self, l):
        l0, l1 = l
        return p0 + [0x0e] + p1


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


    def longsymbol_start(self, m):
        return [0x15] + m

    
    def duration_start(self, m):
        return [0x16] + m


    def selection_start(self, m):
        m, = m
        return [0x14] + [m[0]] + [0x0c] + [m[1]]

    
    def zenny_start(self, m):
        return [0x1c] + m


    def portrait_start(self, m):
        m, = m
        return [0x17] + [m[0], m[1]]


    def inventory_start(self, m):
        m, = m
        return [0x09] + [m[0], m[1]]


    def reference_start(self, m):
        m, = m
        return [0x18] + [m[0], m[1]]

    
    def typing_start(self, m):
        return [0x10] + m


    def unknown_start(self, m):
        return m

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
    

    def longsymbol_macro(self, m):
        return m[1]


    def duration_macro(self, m):
        return m[1]


    def selection_macro(self, m):
        selection = str(m[3]).upper()
        return [m[1], self._selection_map[selection] | m[5]]

    
    def zenny_macro(self, m):
        zenny = str(m[1]).upper()
        return self._zenny_map[zenny]


    def indexed_portrait(self, m):
        source = str(m[1]).upper()
        pos = str(m[5]).upper()
        return [self._portrait_source_map[source] | m[3], 
        self._portrait_pos_map[pos] | m[7]]

    def portrait_clear(self, m):
        return [0xff, 0xff]


    def inventory_macro(self, m):
        source = str(m[3]).upper()
        return [m[1], self._inventory_map[source]]


    def reference_macro(self, m):
        return [m[1], m[3]]


    def typing_macro(self, m):
        typing = str(m[1]).upper()
        return self._typing_map[typing]


    def unknown_macro(self, m):
        return m[1] % 255


    def endreference_macro(self, m):
        return [0x19, m[1], m[3]]


    def multiline_formatting(self, f):
        return f[0]
    

    def multiline_color(self, c):
        return self.concat(c[:-1]) + [c[-1]]


    def multiline_effect(self, e):
        return [e[0]] + self.concat(e[1:])


    def external_pointer_wrapper(self, c):
        return c[1]

    
    def external_pointer_content(self, c):
        return self.concat([c])


    start = list
    variables = dict
    safe_text = list
    external_pointer_string = list


class Processor():
    def __init__(self, padding=True, as_bytes=True):
        self.padding = padding
        self.as_bytes = as_bytes


    def process(self, transform_output):
        var, byte_arrays = transform_output
        ret_ptr = []
        ret_str = []
        
        self.ptsize = 512
        if "PTSIZE" in var.keys():
            self.ptsize = var["PTSIZE"] & 0xffff

        self.target = "output.bin"
        if "TARGET" in var.keys():
            self.target = var["TARGET"]
        
        pos = 0
        for i in byte_arrays:
            local_var, local_byte_array = i
            
            local_ptr_size = 512
            if "PTSIZE" in local_var.keys():
                local_ptr_size = local_var["PTSIZE"] & 0xffff

            local_ptr = []
            local_str = []
            local_pos = 0
            for j in local_byte_array:
                if j >= 0:
                    local_str.append(j)
                    local_pos += 1
                else:
                    local_ptr.extend([k for k in int.to_bytes(local_ptr_size + local_pos, length=2, byteorder="little")])
            
            local_ptr_remainder = -len(local_ptr) % local_ptr_size
            local_ptr.extend(
                [k for k in int.to_bytes(len(local_str) + local_ptr_size - 1, length=2, byteorder="little")] * (local_ptr_remainder // 2)
            )
            
            inner_section = local_ptr + local_str
            
            ret_str.extend(inner_section)
            ret_ptr.extend([k for k in int.to_bytes(self.ptsize + pos, length=2, byteorder="little")])
            pos += len(inner_section)

        ptr_remainder = -len(ret_ptr) % self.ptsize
        ret_ptr.extend(
            [i for i in int.to_bytes(len(ret_str) + self.ptsize - 1, length=2, byteorder="little")] * (ptr_remainder // 2)
        )

        original_len = len(ret_ptr + ret_str)

        if self.padding:
            str_remainder = -(len(ret_str) + self.ptsize) % 2048
            ret_str.extend([0x5f] * str_remainder)

        if self.as_bytes:
            return bytes(ret_ptr + ret_str), self.target, original_len
        else:
            return ret_ptr + ret_str, self.target, original_len