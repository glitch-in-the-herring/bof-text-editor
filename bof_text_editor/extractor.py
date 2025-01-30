#!/usr/bin/env python3

import os
from pathlib import Path

import emi #type: ignore

punct_map3 = {
    0x3a: "(",
    0x3b: ")",
    0x3c: ",",
    0x3d: "-",
    0x3e: ".",
    0x3f: "/",
    0x5c: "?",
    0x5d: "!",
    0x8b: "+",
    0x8c: "~",
    0x8d: "&",
    0x8e: "\'",
    0x8f: ":",
    0x90: "\"",
    0x91: ";",
    0x92: "[SYMBOL 0x92]",
    0x93: "%",
    0xff: " ",
}

punct_map4 = [
    32,
    33, 
    34, 
    37, 
    37, 
    39,
    40, 
    41, 
    43, 
    44, 
    45, 
    46, 
    47, 
    58, 
    59, 
    63,
]

symbol_map3 = [
    0x7b,
    0x7c,
    0x7d,
    0x7e,
    0x80,
    0x81,
    0x82,
    0x83,
    0x84,
    0x85,
    0x86,
    0x87,
    0x88,
    0x89,
    0x8a,
]

symbol_map4 = [
    0x24,
    0x2a,
    0x3c,
    0x3e,
    0x40,
    0x5b,
    0x5d,
    0x5e,
    0x5f,
    0x60,
    0x7b,
    0x7c,
    0x7d,
    0x7e
]

textbox_pos_map = [
    "BM",
    "MM",
    "TM",
    "TL",
    "TR",
    "BL",
    "BR",
]

textbox_vis_map3 = {
    0x00: "NV",
    0x40: "SV",
    0x80: "NI",
}

textbox_vis_map4 = {
    0x00: "NV",
    0x20: "DV",
    0x40: "SV",
    0x80: "NI",
}

effect_map3 = [
    "SHK_S",
    "SHK_L",
    "SHK_P",
    "BIG0_S",
    "BIG1_S",
    "BIG2_S",
    "BIG0_L",
    "BIG1_L",
    "BIG2_L",
    "BIG0_P",
    "BIG1_P",
    "BIG2_P",
    "SML0_S",
    "SML1_S",
    "SML2_S",
    "SML0_L",
    "SML1_L",
    "SML2_L",
    "SML0_P",
    "SML1_P",
    "SML2_P",
    "WAV_L",
    "WAV_H",
    "JMP0",
    "JMP1",
    "JMP2",
]

effect_map4 = [
    "SHK",
    "SHK_H",
    "BIG",
    "BIG_H",
    "BBIG",
    "BBIG_H",
    "SML",
    "SML_H",
    "WAV",
    "JMP",
    "BIG_2",
]

party_map3 = [
    "RYU",
    "NINA",
    "GARR",
    "TEEPO",
    "REI",
    "MOMO",
    "PECO",
]

color_map3 = [
    "PURPLE",
    "RED",
    "CYAN",
    "YELLOW",
    "PINK",
    "GREEN",
    "BLACK",
]

party_map4 = [
    "RYU",
    "NINA",
    "CRAY",
    "SCIAS",
    "URSULA",
    "ERSHIN",
    "FOULU",
]

color_map4 = [
    "GREY",
    "RED",
    "CYAN",
    "Green",
    "PINK",
    "YELLOW",
    "MAGENTA",
    "WHITE",
]

selection_map4 = {
    0x90: "OVR_B",
    0x80: "OVR_S",
    0x70: "RPL",
}

zenny_map4 = {
    0x00: "TR",
    0x01: "TL",
    0x02: "BR",
    0x03: "BL",
}

portrait_source_map4 = {
    0x00: "AREA",
    0x50: "DEF",
    0x80: "AREA_M",
    0xd0: "DEF_M",
}

portrait_pos_map4 = {
    0x00: "L",
    0x40: "R",
    0x80: "LL",
    0xc0: "RR",
}

inventory_map4 = {
    0x00: "ITEM",
    0x01: "WEAPON",
    0x02: "ARMOR",
    0x03: "ACC",
    0x04: "SPELL",
    0x05: "KEY",
}

def to_int(b):
    return int.from_bytes(b, byteorder="little")


def is_alphanum3(a):
    return (a >= 65 and a <= 90) \
        or (a >= 97 and a <= 122) \
        or (a >= 48 and a <= 57)

def is_safe4(a):
    return is_alphanum3(a) or (a in punct_map4)

def is_punct3(b):
    if b in punct_map3.keys():
        return punct_map3[b]
    else:
        return None


def extractor(source_filename, verbose, mode, out_filename=None):
    source_path = Path(source_filename)
    if out_filename is None:
        out_filename = source_filename + "_extracted.txt"
    out_path = Path(out_filename)

    if not source_path.exists():
        raise FileNotFoundError(f"Source file {source_filename} not found!")

    with open(source_path, "rb") as source_file:
        toc = source_file.read(0x800)
        if not emi.validate(toc):
            raise ValueError(f"Source file {source_filename} is not a valid EMI file!")
        
        toc_entries = emi.browse_toc(toc)
        text_entry = emi.find_toc(toc_entries, b"\x00\x00\x01\x80")

        if text_entry is None:
            raise ValueError(f"Source file {source_filename} does not ontain a text section!")

        source_file.seek(text_entry.start)
        text_section = source_file.read(text_entry.size)

    with open(out_path, "w") as out_file:
        ptsize = to_int(text_section[:2])
        out_file.write(f"%TARGET=\"{source_filename}\"\n")
        out_file.write(f"%PTSIZE=0x{ptsize:04x}\n")
        if mode == "3": 
            loop_3(text_entry, out_file, text_section)
        elif mode == "4": 
            loop_4(text_entry, out_file, text_section)

        

def loop_3(text_entry, out_file, text_section):
    ptidx0 = 0
    ptidx1 = 1
    pt0 = to_int(text_section[ptidx0*2:ptidx0*2+2])
    idx = pt0
    end = True
    while pt0 < text_entry.size:
        if end:
            out_file.write("^")
            end = False
        else:
            out_file.write("@")
        pt1 = to_int(text_section[ptidx1*2:ptidx1*2+2])

        while pt1 == pt0:
            out_file.write("@")
            ptidx1 += 1
            pt1 = to_int(text_section[ptidx1*2:ptidx1*2+2])
        
        while idx < pt1:
            if is_alphanum3(text_section[idx]):
                out_file.write(chr(text_section[idx]))
                idx += 1
            elif text_section[idx] == 0x5d:
                out_file.write("#")
                idx += 1
            elif (p := is_punct3(text_section[idx])) is not None:
                out_file.write(p)
                idx += 1
            elif text_section[idx] in symbol_map3:
                out_file.write(f"[SYMBOL 0x{c:2x}]")
                idx += 1
            elif text_section[idx] == 0x0c:
                pos = text_section[idx + 1] & 0x0f
                vis = text_section[idx + 1] & 0xf0
                out_file.write(f"[TB {textbox_pos_map[pos]} {textbox_vis_map3[vis]}]")
                idx += 2
            elif text_section[idx] == 0x0d:
                out_file.write("[effect]")
                idx += 1
            elif text_section[idx] == 0x01:
                out_file.write("\n")
                idx += 1
            elif text_section[idx] == 0x0b:
                out_file.write("#")
                idx += 1
            elif text_section[idx] == 0x02:
                out_file.write("|\n")
                idx += 1
            elif text_section[idx] == 0x0f and text_section[idx - 1] == 0x0e:
                out_file.write(f"[/effect={effect_map3[text_section[idx + 1]]}]")
                idx += 3
            elif text_section[idx] == 0x04:
                out_file.write(f"[PARTY {party_map3[text_section[idx + 1]]}]")
                idx += 2
            elif text_section[idx] == 0x05:
                out_file.write(f"[color={color_map3[text_section[idx + 1] - 1]}]")
                idx += 2
            elif text_section[idx] == 0x06:
                out_file.write("[/color]")
                idx += 1
            elif text_section[idx] == 0x07:
                out_file.write(f"[PLACEHOLDER 0x{text_section[idx + 1]:02x}]")
                idx += 2
            elif text_section[idx] == 0x14 and text_section[idx + 2] == 0x0c:
                count = text_section[idx + 3] & 0x0f;
                pos = text_section[idx + 3] & 0xf0;

                if pos == 0:
                    position = "OVR"
                else:
                    position = "NEW"

                out_file.write(f"[SELECTION 0x{text_section[idx + 1]:02x} {position} 0x{count:02x}]")
                idx += 4
            elif text_section[idx] == 0x16:
                out_file.write(f"[DUR 0x{text_section[idx + 1]:02x}]")
                idx += 2
            elif text_section[idx] == 0x00 and idx != pt1 - 1: # seems naive to assume that it's always one byte behind 
                out_file.write("\\\n")
                idx += 1
            elif text_section[idx] == 0x00 and idx == pt1 - 1:
                out_file.write("$\n")
                end = True
                idx += 1

        pt0 = pt1
        ptidx0 = ptidx1
        ptidx1 += 1


def loop_4(text_entry, out_file, text_section):
    ptidx0 = 0
    ptidx1 = 1
    pt0 = to_int(text_section[ptidx0*2:ptidx0*2+2])
    idx = pt0
    end = True
    while pt0 < text_entry.size:
        if end:
            out_file.write("^")
            end = False
        else:
            out_file.write("@")
        pt1 = to_int(text_section[ptidx1*2:ptidx1*2+2])

        if pt1 == text_entry.size - 1:
            pt1 += 1

        while pt1 == pt0:
            out_file.write("@")
            ptidx1 += 1
            pt1 = to_int(text_section[ptidx1*2:ptidx1*2+2])
        
        while idx < pt1:
            print(idx, ptidx1)
            if is_safe4(text_section[idx]):
                out_file.write(chr(text_section[idx]))
                idx += 1
            elif text_section[idx] in symbol_map4:
                out_file.write(f"[SYMBOL 0x{c:2x}]")
                idx += 1
            elif text_section[idx] == 0x0c:
                pos = text_section[idx + 1] & 0x0f
                vis = text_section[idx + 1] & 0xf0
                out_file.write(f"[TB {textbox_pos_map[pos]} {textbox_vis_map4[vis]}]")
                idx += 2
            elif text_section[idx] == 0x0d:
                out_file.write("[effect]")
                idx += 1
            elif text_section[idx] == 0x01:
                out_file.write("\n")
                idx += 1
            elif text_section[idx] == 0x0b:
                out_file.write("_")
                idx += 1
            elif text_section[idx] == 0x02:
                out_file.write("|\n")
                idx += 1
            elif text_section[idx] == 0x0f and text_section[idx - 1] == 0x0e:
                out_file.write(f"[/effect={effect_map4[text_section[idx + 1]]}]")
                idx += 3
            elif text_section[idx] == 0x04:
                out_file.write(f"[PARTY {party_map4[text_section[idx + 1]]}]")
                idx += 2
            elif text_section[idx] == 0x05:
                out_file.write(f"[color={color_map4[text_section[idx + 1] - 1]}]")
                idx += 2
            elif text_section[idx] == 0x06:
                out_file.write("[/color]")
                idx += 1
            elif text_section[idx] == 0x07:
                out_file.write(f"[PLACEHOLDER 0x{text_section[idx + 1]:02x}]")
                idx += 2
            elif text_section[idx] == 0x14 and text_section[idx + 2] == 0x0c:
                count = text_section[idx + 3] & 0x0f;
                pos = text_section[idx + 3] & 0xf0;
                position = selection_map4[pos]
                out_file.write(f"[SELECTION 0x{text_section[idx + 1]:02x} {position} 0x{count:02x}]")
                idx += 4
            elif text_section[idx] == 0x16:
                out_file.write(f"[DUR 0x{text_section[idx + 1]:02x}]")
                idx += 2
            elif text_section[idx] == 0x00 and idx < pt1 - 1:
                out_file.write("\\\n")
                idx += 1
            elif text_section[idx] == 0x00 and idx == pt1 - 1:
                out_file.write("$\n")
                end = True
                idx += 1
            elif text_section[idx] == 0x1c:
                out_file.write(f"[ZENNY {zenny_map4[text_section[idx + 1]]}]")
                idx += 2
            elif text_section[idx] == 0x17:
                if text_section[idx + 1] == 0xff and text_section[idx + 2] == 0xff:
                    out_file.write("[POR CLEAR]")
                    idx += 3
                    continue

                source = text_section[idx + 1] & 0xf0
                pidx = text_section[idx + 1] & 0x0f
                pos = text_section[idx + 2] & 0xf0
                pal = text_section[idx + 2] & 0x0f
                out_file.write(f"[POR {portrait_source_map4[source]} 0x{pidx:02x} {portrait_pos_map4[pos]} 0x{pal:02x}]")
                idx += 3
            elif text_section[idx] == 0x09:
                out_file.write(f"[INV 0x{text_section[idx +1]:02x} {inventory_map4[text_section[idx + 2]]}]")
                idx += 3
            elif text_section[idx] == 0x18:
                out_file.write(f"[REF 0x{inventory_map4[text_section[idx + 1]]:02x} 0x{text_section[idx + 2]:02x}]")
                idx += 3
            elif text_section[idx] == 0x10:
                typing = "FALSE" if text_section[idx] % 2 else "TRUE"
                out_file.write(f"[TYPE {typing}]")
                idx += 2


        pt0 = pt1
        ptidx0 = ptidx1
        ptidx1 += 1
        if pt0 == text_entry.size - 1:
            out_file.write("$")
            break