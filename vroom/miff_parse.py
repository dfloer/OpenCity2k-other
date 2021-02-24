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
    parsed_chunks["LABL"] = [x for x in parsed_chunks["LABL"].split(chr(1)) if x != '']
    if "ANAI" in parsed_chunks:
        parsed_chunks["ANAI"] = [[int32(x[y : y + 4]) for y in range(0, len(x), 4)] for x in parsed_chunks["ANAI"]]
    if "EVNT" in parsed_chunks:
        parsed_chunks["EVNT"] = [parse_event(x) for x in parsed_chunks["EVNT"]]
    if "EVNT" in parsed_chunks:
        parsed_chunks["EVTG"] = [parse_evtg(x) for x in parsed_chunks["EVTG"]]
    if "APAK" in parsed_chunks:
        parsed_chunks["APAK"] = [parse_apak(x) for x in parsed_chunks["APAK"]]
    parsed_chunks["EPSD"] = [[uint32(x[y : y + 4]) for y in range(0, len(x), 4)] for x in parsed_chunks["EPSD"]]
    return parsed_chunks

def parse_event(raw):
    data = [uint32(raw[x : x + 4]) for x in range(4, 0x20, 4)]
    extra = [raw[0x20 : -4]]
    return {"id": uint32(raw[0 :  4]), "data": data, "extra": extra, "len": len(data) + 1 + len(extra)}

def parse_apak(raw):
    result = raw[ : -4]
    apak_id = uint32(raw[0 : 4])
    data = [int32(result[x : x + 4]) for x in range(4, 20, 4)]
    extra = result[20 :]
    text = []
    wave = []
    extra = [x for x in string(extra).split(chr(1)) if x != '']
    for x in extra:
        if "wav" in x or "WAV" in x:
            wave += [x]
        else:
            text += [x]

    return {"id": apak_id, "data": data, "text": text, "wave": wave}

def parse_evtg(raw):
    result = []
    raw = raw[ : -2]
    for x in range(len(raw) // 4):
        result += [uint32(raw[x * 4 : x * 4 + 4])]
    return result


def uint32(b):
    return struct.unpack('<I', b)[0]

def int32(b):
    return struct.unpack('<i', b)[0]

def char4(b):
    return struct.unpack('4s', b)[0].decode("ascii")[::-1]

def string(b, code="windows-1252"):
    return b[:-1].decode(code)

def uint16(b):
    return struct.unpack('<H', b)[0]

def coords(b):
    return uint16(b[0 : 2]), uint16(b[2 : 4])

def uint8(b):
    return struct.unpack('<B', b)[0]