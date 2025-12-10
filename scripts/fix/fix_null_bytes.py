import sys

# Read the file in binary mode
with open('c:/Users/U S E R/OneDrive/Desktop/claud/models/models.py', 'rb') as f:
    content = f.read()

print(f"Original size: {len(content)} bytes")
print(f"Null bytes found: {content.count(b'\\x00')}")

# Remove null bytes
cleaned = content.replace(b'\x00', b'')

print(f"Cleaned size: {len(cleaned)} bytes")

# Write back
with open('c:/Users/U S E R/OneDrive/Desktop/claud/models/models.py', 'wb') as f:
    f.write(cleaned)

print("File cleaned successfully!")
