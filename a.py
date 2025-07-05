# decode_flag.py
import base64
import string

flag = "8Y1NqlFnturKzYLnLUGOt1gr4hc9jNQbnlf6Zivhbz98izwyhZ"

# ลอง Base64
try:
    decoded = base64.b64decode(flag + "==")  # เพิ่ม padding
    print("Base64:", decoded)
except:
    pass

# ลอง Reverse
print("Reversed:", flag[::-1])

# ลอง Caesar Cipher (shift ต่างๆ)
def caesar_decode(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
        else:
            result += char
    return result

for i in range(1, 26):
    print(f"Caesar {i}:", caesar_decode(flag, i))