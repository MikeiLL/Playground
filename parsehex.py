# Read a file as hex dump
def hex_dump(filepath, bytes_per_line=16):
    with open(filepath, 'rb') as f:
        offset = 0
        while chunk := f.read(bytes_per_line):
            hex_part = ' '.join(f'{b:02x}' for b in chunk)
            ascii_part = ''.join(
                chr(b) if 32 <= b < 127 else '.' for b in chunk
            )
            print(f'{offset:08x}: {hex_part:<{bytes_per_line*3}}  {ascii_part}')
            offset += len(chunk)

hex_dump('example.bin')

# Convert hex string to bytes
hex_str = '48656c6c6f20576f726c64'
data = bytes.fromhex(hex_str)
print(data.decode('utf-8'))  # "Hello World"

# Convert bytes to hex string
text = 'Hello World'
hex_output = text.encode('utf-8').hex()
print(hex_output)  # "48656c6c6f20576f726c64"

# Parse a hex dump back to binary
import re

def parse_hex_dump(dump_text):
    """Extract raw bytes from a hex dump string."""
    result = bytearray()
    for line in dump_text.strip().split('\n'):
        # Remove offset and ASCII columns, keep hex bytes
        match = re.match(r'[0-9a-f]+:\s+((?:[0-9a-f]{2}\s*)+)', line, re.I)
        if match:
            hex_bytes = match.group(1).strip()
            result.extend(bytes.fromhex(hex_bytes.replace(' ', '')))
    return bytes(result)

# Identify file type by magic bytes
SIGNATURES = {
    b'\x89PNG': 'PNG image',
    b'\xff\xd8\xff': 'JPEG image',
    b'%PDF': 'PDF document',
    b'PK\x03\x04': 'ZIP archive',
    b'\x7fELF': 'ELF binary',
    b'MZ': 'Windows executable',
    b'SQLite': 'SQLite database',
}

def identify_file(filepath):
    with open(filepath, 'rb') as f:
        header = f.read(8)
    for sig, name in SIGNATURES.items():
        if header.startswith(sig):
            return name
    return 'Unknown'

print(identify_file('photo.png'))  # "PNG image"