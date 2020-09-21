#!/usr/bin/env python3
#

# require
# `pip install fonttools`
#

import io
import struct
import sys
import zlib
from urllib.request import urlopen, urlretrieve
from fontTools.ttLib import TTFont

# MathJax woff fonts
BASE_URL = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2'
SRC_MAP = {
    'MJXZERO': 'MathJax_Zero.woff',
    'MJXTEX': 'MathJax_Main-Regular.woff',
    'MJXTEX-B': 'MathJax_Main-Bold.woff',
    'MJXTEX-I': 'MathJax_Math-Italic.woff',
    'MJXTEX-MI': 'MathJax_Main-Italic.woff',
    'MJXTEX-BI': 'MathJax_Math-BoldItalic.woff',
    'MJXTEX-S1': 'MathJax_Size1-Regular.woff',
    'MJXTEX-S2': 'MathJax_Size2-Regular.woff',
    'MJXTEX-S3': 'MathJax_Size3-Regular.woff',
    'MJXTEX-S4': 'MathJax_Size4-Regular.woff',
    'MJXTEX-A': 'MathJax_AMS-Regular.woff',
    'MJXTEX-C': 'MathJax_Calligraphic-Regular.woff',
    'MJXTEX-CB': 'MathJax_Calligraphic-Bold.woff',
    'MJXTEX-FR': 'MathJax_Fraktur-Regular.woff',
    'MJXTEX-FRB': 'MathJax_Fraktur-Bold.woff',
    'MJXTEX-SS': 'MathJax_SansSerif-Regular.woff',
    'MJXTEX-SSB': 'MathJax_SansSerif-Bold.woff',
    'MJXTEX-SSI': 'MathJax_SansSerif-Italic.woff',
    'MJXTEX-SC': 'MathJax_Script-Regular.woff',
    'MJXTEX-T': 'MathJax_Typewriter-Regular.woff',
    'MJXTEX-V': 'MathJax_Vector-Regular.woff',
    'MJXTEX-VB': 'MathJax_Vector-Bold.woff',
}


def convert_streams(infile, outfile):
    WOFFHeader = {
        'signature': struct.unpack(">I", infile.read(4))[0],
        'flavor': struct.unpack(">I", infile.read(4))[0],
        'length': struct.unpack(">I", infile.read(4))[0],
        'numTables': struct.unpack(">H", infile.read(2))[0],
        'reserved': struct.unpack(">H", infile.read(2))[0],
        'totalSfntSize': struct.unpack(">I", infile.read(4))[0],
        'majorVersion': struct.unpack(">H", infile.read(2))[0],
        'minorVersion': struct.unpack(">H", infile.read(2))[0],
        'metaOffset': struct.unpack(">I", infile.read(4))[0],
        'metaLength': struct.unpack(">I", infile.read(4))[0],
        'metaOrigLength': struct.unpack(">I", infile.read(4))[0],
        'privOffset': struct.unpack(">I", infile.read(4))[0],
        'privLength': struct.unpack(">I", infile.read(4))[0]
    }

    outfile.write(struct.pack(">I", WOFFHeader['flavor']))
    outfile.write(struct.pack(">H", WOFFHeader['numTables']))
    maximum = list(filter(lambda x: x[1] <= WOFFHeader['numTables'], [
                   (n, 2**n) for n in range(64)]))[-1]
    searchRange = maximum[1] * 16
    outfile.write(struct.pack(">H", searchRange))
    entrySelector = maximum[0]
    outfile.write(struct.pack(">H", entrySelector))
    rangeShift = WOFFHeader['numTables'] * 16 - searchRange
    outfile.write(struct.pack(">H", rangeShift))

    offset = outfile.tell()

    TableDirectoryEntries = []
    for i in range(0, WOFFHeader['numTables']):
        TableDirectoryEntries.append({
            'tag': struct.unpack(">I", infile.read(4))[0],
            'offset': struct.unpack(">I", infile.read(4))[0],
            'compLength': struct.unpack(">I", infile.read(4))[0],
            'origLength': struct.unpack(">I", infile.read(4))[0],
            'origChecksum': struct.unpack(">I", infile.read(4))[0]
        })
        offset += 4*4

    for entry in TableDirectoryEntries:
        outfile.write(struct.pack(">I", entry['tag']))
        outfile.write(struct.pack(">I", entry['origChecksum']))
        outfile.write(struct.pack(">I", offset))
        outfile.write(struct.pack(">I", entry['origLength']))
        entry['outOffset'] = offset
        offset += entry['origLength']
        if (offset % 4) != 0:
            offset += 4 - (offset % 4)

    for entry in TableDirectoryEntries:
        infile.seek(entry['offset'])
        compressedData = infile.read(entry['compLength'])

        if entry['compLength'] != entry['origLength']:
            uncompressedData = zlib.decompress(compressedData)
        else:
            uncompressedData = compressedData

        outfile.seek(entry['outOffset'])
        outfile.write(uncompressedData)
        offset = entry['outOffset'] + entry['origLength']
        padding = 0
        if (offset % 4) != 0:
            padding = 4 - (offset % 4)
        outfile.write(bytearray(padding))


def rename_fontname(fontfilepath, new_fontname):
    font = TTFont(fontfilepath)
    namerecord_list = font["name"].names

    def get_style():
        # determine font style for this file path from name record nameID 2
        for record in namerecord_list:
            if record.nameID == 2:
                return str(record)
        return None

    style = get_style()
    if len(style) == 0:
        sys.stderr.write(
            f"Unable to detect the font style from the OpenType name table in '{fontfilepath}'."
        )
        return

    # used for the Postscript name in the name table (no spaces allowed)
    postscript_font_name = new_fontname.replace(" ", "")
    # font family name
    nameID1_string = new_fontname
    nameID16_string = new_fontname
    # full font name
    nameID4_string = f"{new_fontname} {style}"
    # Postscript name
    # - no spaces allowed in family name or the PostScript suffix. should be dash delimited
    nameID6_string = f"{postscript_font_name}-{style.replace(' ', '')}"
    # nameID6_string = postscript_font_name + "-" + style.replace(" ", "")

    # modify the opentype table data in memory with updated values
    for record in namerecord_list:
        if record.nameID == 1:
            record.string = nameID1_string
        elif record.nameID == 4:
            record.string = nameID4_string
        elif record.nameID == 6:
            record.string = nameID6_string
        elif record.nameID == 16:
            record.string = nameID16_string

    # write changes to the font file
    try:
        font.save(fontfilepath)
    except Exception as e:
        sys.stderr.write(
            f"ERROR: Unable to write new name to OpenType name table for '{fontfilepath}': {e}."
        )


def main(argv):
    for family, src_filename in SRC_MAP.items():
        dst_filename = src_filename.split('.')[0] + '.otf'
        # dst_filename = family + '.otf'
        src_url = f'{BASE_URL}/{src_filename}'
        print(f'font: "{dst_filename}" <== "{src_url}"')

        with io.BytesIO(urlopen(src_url).read()) as src:
            with open(dst_filename, mode='wb') as dst:
                convert_streams(src, dst)
            rename_fontname(dst_filename, family)

    return 0


# MAIN
if __name__ == '__main__':
    sys.exit(main(sys.argv))
