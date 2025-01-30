from collections import namedtuple

def validate(emi):
    return emi[8:16] == b"MATH_TBL"


def browse_toc(emi):
    count = int.from_bytes(emi[:2], byteorder="little")
    section_start = 0x800
    toc_entry = namedtuple("toc_entry", ["toc_addr", "start", "size", "signature"])
    ret = []
    for i in range(count):
        base = 0x10 * (i + 1)
        size = int.from_bytes(emi[base:base+4], byteorder="little")
        signature = emi[base+4:base+8]
        ret.append(toc_entry(base, section_start, size, signature))
        section_start += size + (-size % 2048)
    return ret


def find_toc(toc_entries, signature):
    for toc_entry in toc_entries:
        if toc_entry.signature == signature:
            return toc_entry
    return None
