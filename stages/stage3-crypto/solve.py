#!/usr/bin/env python3
import base64
import os

KEY = "seniorsystemsintegrationlead"

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    key_len = len(key)
    key_as_int = [ord(i) for i in key]
    ciphertext_int = [ord(i) for i in ciphertext]
    plaintext = ''
    
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_idx % key_len].lower()) - 97
            if char.islower():
                plaintext += chr((ord(char) - 97 - shift) % 26 + 97)
            else:
                plaintext += chr((ord(char) - 65 - shift) % 26 + 65)
            key_idx += 1
        else:
            plaintext += char
            
    return plaintext

def solve():
    target_path = os.path.join(os.path.dirname(__file__), "..", "stage2-portal", "static", "downloads", "transmission_log_48.txt")
    
    if not os.path.exists(target_path):
        print(f"Error: {target_path} not found. Run generate_artifacts.py first.")
        return
        
    with open(target_path, "r") as f:
        encoded_b64 = f.read().strip()
        
    # 1. Base64 Decode
    encrypted_vigenere = base64.b64decode(encoded_b64).decode('utf-8')
    
    # 2. Vigenere Decrypt
    plaintext = vigenere_decrypt(encrypted_vigenere, KEY)
    
    print("--- Decrypted Plaintext ---")
    print(plaintext)
    
    if "BP{" in plaintext:
        print("\n[SUCCESS] Flag found in plaintext!")
    else:
        print("\n[FAILED] Flag not found.")

if __name__ == "__main__":
    solve()

