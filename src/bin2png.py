import zlib

with open('chararom', 'wb') as f:
    while True:
        b = f.read(16)
