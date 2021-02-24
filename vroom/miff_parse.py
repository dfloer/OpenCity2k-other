import struct
from collections import defaultdict

# Exception classes so that raised exceptions can be more descriptive.
class MIFFParse(BaseException):
    """
    Exceptions for when parsing a MIFF file fails.
    """
    def __init__(self, message):
        self.message = message

def parse_scenario(raw_data):
    header = raw_data[0 : 4]
    if header != b'MIFF':
        raise MIFFParse(f"File header is not b'MIFF', got: {header}.")
    scn_size = uint32(raw_data[0x14 : 0x18])
    if scn_size != len(raw_data):
        raise MIFFParse(f"File reported {scn_size}B long, but is {len(raw_data)}B.")
    num_segments = uint32(raw_data[4 : 8])
    segments = [char4(raw_data[x : x + 4]) for x in range(8, 8 + 4 * num_segments, 4)]
    print(segments)
    unk1 = uint32(raw_data[0x10 : 0x14])
    unk2 = uint32(raw_data[0x18 : 0x1C])
    print(f"unknowns: {unk1},  {unk2}")
    raw_chunks = split_chunks(raw_data[0x1C : ])
    parsed_chunks = cleanup_chunks(raw_chunks)
    return parsed_chunks



def split_chunks(segment):
    # Must start with a chunk name:
    idx = 0
    chunks = defaultdict(list)
    while idx < len(segment):
        name = char4(segment[idx : idx + 4])
        idx += 4
        chunk_len = uint32(segment[idx : idx + 4]) - 8
        idx += 4
        data = segment[idx : idx + chunk_len ]
        chunks[name] += [data]
        idx += chunk_len
    return chunks

def cleanup_chunks(chunks):
    parsed_chunks = {}
    string_keys = ("CITY", "NAME", "ITXT", "WTXT", "LTXT", "LABL")
    single_value_keys = ("TIME", "BNUS", "LOCX", "LOCY", "#CHK", "#PKG", "#EVS", "PACK", "AMMO", "LAPS", "PRGN", "#AIS", "CHKB")
    byte_keys = ("IANM", "WANM", "LANM")
    for k, v in chunks.items():
        if k in string_keys:
            parsed_chunks[k] = string(v[0])
        elif k in single_value_keys:
            parsed_chunks[k] = uint32(v[0])
        elif k in byte_keys:
            parsed_chunks[k] = uint8(v[0])
        else:
            parsed_chunks[k] = v
    parsed_chunks["CHCK"] = [coords(x) for x in chunks["CHCK"]]
    # parsed_chunks["ANAI"] = [[uint32(x[y : y + 4]) for y in range(0, len(x), 4)] for x in chunks["ANAI"]]
    return parsed_chunks


def uint32(b):
    return struct.unpack('<I', b)[0]

def char4(b):
    return struct.unpack('4s', b)[0].decode("ascii")[::-1]

def string(b):
    return b[:-1].decode("ascii")

def uint16(b):
    return struct.unpack('<H', b)[0]

def coords(b):
    return uint16(b[0 : 2]), uint16(b[2 : 4])

def uint8(b):
    return struct.unpack('<B', b)[0]