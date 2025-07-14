#!/usr/bin/env python3

import base64
from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad
import binascii

def decrypt_roundcube_password(encrypted_password, des_key):
    """
    Decrypt Roundcube encrypted password using DES-EDE3-CBC
    
    Args:
        encrypted_password (str): Base64 encoded encrypted password
        des_key (str): DES key from Roundcube config
    
    Returns:
        str: Decrypted password
    """
    try:
        # Base64 decode the encrypted password
        encrypted_data = base64.b64decode(encrypted_password)
        
        # DES3 key must be 24 bytes
        key = des_key.encode('utf-8')[:24]
        
        # Extract IV (first 8 bytes) and ciphertext (remaining bytes)
        iv = encrypted_data[:8]
        ciphertext = encrypted_data[8:]
        
        # Create DES3 cipher object
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        
        # Decrypt and remove padding
        decrypted = cipher.decrypt(ciphertext)
        
        # Remove PKCS7 padding
        try:
            decrypted = unpad(decrypted, DES3.block_size)
        except:
            # If unpad fails, try manual padding removal
            padding_length = decrypted[-1]
            if isinstance(padding_length, str):
                padding_length = ord(padding_length)
            decrypted = decrypted[:-padding_length]
        
        return decrypted.decode('utf-8', errors='ignore')
        
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

def main():
    # Tyler's encrypted password from session
    encrypted_password = "kAizOClTvxwJ8wKJLYNHS8peNXaHoiEG"
    
    # DES key from Roundcube config
    des_key = "rcmail-!24ByteDESkey*Str"
    
    print("=== Roundcube Password Decryptor ===")
    print(f"Encrypted Password: {encrypted_password}")
    print(f"DES Key: {des_key}")
    print("-" * 40)
    
    # Attempt decryption
    decrypted = decrypt_roundcube_password(encrypted_password, des_key)
    
    if decrypted:
        print(f"✅ Decrypted Password: {decrypted}")
    else:
        print("❌ Failed to decrypt password")
        
        # Try alternative method without IV extraction
        try:
            encrypted_data = base64.b64decode(encrypted_password)
            key = des_key.encode('utf-8')[:24]
            
            # Try with zero IV
            cipher = DES3.new(key, DES3.MODE_CBC, b'\x00' * 8)
            decrypted = cipher.decrypt(encrypted_data)
            
            # Remove null bytes and non-printable characters
            decrypted = decrypted.rstrip(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f')
            
            print(f"🔍 Alternative decryption: {decrypted.decode('utf-8', errors='ignore')}")
            
        except Exception as e:
            print(f"Alternative method also failed: {e}")

if __name__ == "__main__":
    main()
