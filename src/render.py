import zlib
import struct


class Render:
    def __init__(self):
        pass

    def render(self, data):
        pass


def makePNG(data, height=None, width=None):
    def I1(value):
        return struct.pack("!B", value & (2**8-1))

    def I4(value):
        return struct.pack("!I", value & (2**32-1))
    # compute width&height from data if not explicit
    if height is None:
        height = len(data)  # rows
    if width is None:
        width = 0
        for row in data:
            if width < len(row):
                width = len(row)
    # generate these chunks depending on image type
    makeIHDR = True
    makeIDAT = True
    makeIEND = True
    png = b"\x89" + "PNG\r\n\x1A\n".encode('ascii')
    if makeIHDR:
        colortype = 2  # true gray image (no palette)
        bitdepth = 8  # with one byte per pixel (0..255)
        compression = 0  # zlib (no choice here)
        filtertype = 0  # adaptive (each scanline seperately)
        interlaced = 0  # no
        IHDR = I4(width) + I4(height) + I1(bitdepth)
        IHDR += I1(colortype) + I1(compression)
        IHDR += I1(filtertype) + I1(interlaced)
        block = "IHDR".encode('ascii') + IHDR
        png += I4(len(IHDR)) + block + I4(zlib.crc32(block))
    if makeIDAT:
        raw = b""
        for y in range(height):
            raw += b"\0"  # no filter for this scanline
            for x in range(width):
                c = b"\0"  # default black pixel
                if y < len(data) and x < len(data[y]):
                    c = I1(data[y][x])
                raw += c
        compressor = zlib.compressobj()
        compressed = compressor.compress(raw)
        compressed += compressor.flush()  # !!
        block = "IDAT".encode('ascii') + compressed
        png += I4(len(compressed)) + block + I4(zlib.crc32(block))
    if makeIEND:
        block = "IEND".encode('ascii')
        png += I4(0) + block + I4(zlib.crc32(block))
    return png


if __name__ == "__main__":
    with open('ramp.png', 'wb') as f:
        data = []
        for i in range(256):
            col = []
            for j in range(256):
                col.append(j % 256)
                col.append((j + 64) % 256)
                col.append((j + 128) % 256)
            data.append(col)

        f.write(makePNG(data))
        f.close()
