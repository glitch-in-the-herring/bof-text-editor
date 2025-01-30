import argparse
import os
from pathlib import Path

import emi

cli_parser = argparse.ArgumentParser()

cli_parser.add_argument('filename')
cli_parser.add_argument(
    '-v', 
    '--verbose', 
    action='store_true',
    help='toggle verbose mode')
cli_parser.add_argument(
    '-o', 
    '--out', 
    default=None,
    help='set the name of the output file')


punct_map = {
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

symbol_map = [
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

textbox_pos_map = [
    "BM",
    "MM",
    "TM",
    "TL",
    "TR",
    "BL",
    "BR",
]

textbox_vis_map = {
    0x00: "NV",
    0x40: "SV",
    0x80: "NI",
}

effect_map = [
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

party_map = [
    "RYU",
    "NINA",
    "GARR",
    "TEEPO",
    "REI",
    "MOMO",
    "PECO",
]

color_map = [
    "PURPLE",
    "RED",
    "CYAN",
    "YELLOW",
    "PINK",
    "GREEN",
    "BLACK",
]

def to_int(b):
    return int.from_bytes(b, byteorder="little")


def is_alphanum(a):
    return (a >= 65 and a <= 90) \
        or (a >= 97 and a <= 122) \
        or (a >= 48 and a <= 57)


def is_punct(b):
    if b in punct_map.keys():
        return punct_map[b]
    else:
        return None


def main():
    args = cli_parser.parse_args()
    verbose = args.verbose
    source_filename = args.filename
    source_path = Path(source_filename)
    out_filename = args.out
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
            
            while idx != pt1:
                if is_alphanum(text_section[idx]):
                    out_file.write(chr(text_section[idx]))
                    idx += 1
                elif (p := is_punct(text_section[idx])) is not None:
                    out_file.write(p)
                    idx += 1
                elif text_section[idx] in symbol_map:
                    out_file.write(f"[SYMBOL 0x{c:2x}]")
                    idx += 1
                elif text_section[idx] == 0x0c:
                    pos = text_section[idx + 1] & 0x0f
                    vis = text_section[idx + 1] & 0xf0
                    out_file.write(f"[POS {textbox_pos_map[pos]} {textbox_vis_map[vis]}]")
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
                    out_file.write(f"[/effect={effect_map[text_section[idx + 1]]}]")
                    idx += 3
                elif text_section[idx] == 0x04:
                    out_file.write(f"[PARTY {party_map[text_section[idx + 1]]}]")
                    idx += 2
                elif text_section[idx] == 0x05:
                    out_file.write(f"[color={color_map[text_section[idx + 1] - 1]}]")
                    idx += 2
                elif text_section[idx] == 0x06:
                    out_file.write("[/color]")
                    idx += 1
                elif text_section[idx] == 0x07:
                    out_file.write(f"[PLACEHOLDER 0x{text_section[idx + 1]:02x}]")
                    idx += 2
                elif text_section[idx] == 0x14:
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


if __name__ == "__main__":
    main()
