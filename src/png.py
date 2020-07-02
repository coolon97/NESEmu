import zlib
import struct
import binascii

PNG_HEAD = 8
IHDR_HEAD = 12
IHDR_WIDTH = 16
IHDR_HEGIHT = 20
IHDR_BITDEPTH = 24
IHDR_COLORTYPE = 25
IHDR_COMPTYPE = 26
IHDR_FILTYPE = 27
IHDR_INTERLACE = 28
IHDR_CRC = 29

CHUNK_STEP = 4


class PNG:
    def __init__(self, filepath=None):
        if filepath is not None:
            self.data = self.read(filepath)

    def read(self, filepath):
        print("file " + filepath + " Loading...")
        buf = b''
        with open(filepath, 'rb') as f:
            buf = f.read()
            f.close()
        self.readFromBinary(buf)

    def readFromBinary(self, buf):
        if buf[:PNG_HEAD] != b"\x89PNG\r\n\x1a\n":
            print("This file is not PNG format.")

        self.LENGTH = 13

        if buf[IHDR_HEAD:IHDR_WIDTH] != b'IHDR':
            print("Invalid: Not found IHDR chunk")

        self.WIDTH = int.from_bytes(buf[IHDR_WIDTH:IHDR_HEGIHT], 'big')

        self.HEIGHT = int.from_bytes(buf[IHDR_HEGIHT:IHDR_BITDEPTH], 'big')

        self.BITDEPTH = int.from_bytes(
            buf[IHDR_BITDEPTH:IHDR_COLORTYPE], 'big')

        self.COLORTYPE = int.from_bytes(
            buf[IHDR_COLORTYPE:IHDR_COMPTYPE], 'big')

        self.COMPTYPE = int.from_bytes(
            buf[IHDR_COMPTYPE:IHDR_FILTYPE], 'big')
        if self.COMPTYPE != 0:
            print("Invalid: Unknown compression method")

        self.FILTYPE = int.from_bytes(buf[IHDR_FILTYPE:IHDR_INTERLACE], 'big')
        if self.COMPTYPE != 0:
            print("Invalid: Unknown filter method")

        self.INTERLACE = int.from_bytes(
            buf[IHDR_INTERLACE:IHDR_CRC], 'big')

        c_data = int.from_bytes(buf[IHDR_CRC:IHDR_CRC + 4], 'big')
        c_calc = binascii.crc32(buf[IHDR_HEAD:IHDR_INTERLACE + 1])
        if c_data != c_calc:
            print("Invalid: This PNG is broken")
        self.CRC = c_data

        print("width    : " + str(self.WIDTH))
        print("height   : " + str(self.HEIGHT))
        print("depth    : " + str(self.BITDEPTH))
        print("colortype: " + str(self.COLORTYPE))
        print("interlace: " + str(self.INTERLACE))

        cursor = IHDR_CRC + 4
        png_data = b''
        isIDAT = True
        while (isIDAT):
            chunk_size = int.from_bytes(buf[cursor:cursor + CHUNK_STEP], 'big')
            chunk_type = buf[cursor + CHUNK_STEP:cursor + CHUNK_STEP * 2]
            print("chunk type: " + chunk_type.decode('utf8'))

            if chunk_type == b'IEND':
                isIDAT = False
            elif chunk_type == b'IDAT':
                png_data += buf[cursor + CHUNK_STEP *
                                2: cursor + CHUNK_STEP * 2 + chunk_size]

            cursor = cursor + chunk_size + CHUNK_STEP * 3

        decompressed_data = zlib.decompress(png_data)

    def __bitsPerPixel(colortype, depth=None):
        if colortype == 0:
            return depth
        elif colortype == 2:
            return depth * 3
        elif colortype == 3:
            return depth
        elif colortype == 4:
            return depth * 2
        elif colortype == 6:
            return depth * 4
        else:
            print("Invalid: Unknown color type.")

    def __applyFilter(data, width, height, bitsPerPixel, bytesPerPixel):
        pass

    def write(self, fiiepath):
        pass

    def getRGB(self):
        pass

    def getRGBA(self):
        pass

    def uncompress(self, data):
        pass


if __name__ == "__main__":
    p = PNG("../Assets/lenna.png")
