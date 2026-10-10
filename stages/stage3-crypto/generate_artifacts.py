#!/usr/bin/env python3
import base64
import os

KEY = "seniorsystemsintegrationlead"

def vigenere_encrypt(plaintext: str, key: str) -> str:
    key_len = len(key)
    key_as_int = [ord(i) for i in key]
    plaintext_int = [ord(i) for i in plaintext]
    ciphertext = ''
    
    # We only encrypt alphabetical characters to make it classical Vigenere,
    # or we can encrypt all printable characters. Let's just encrypt alphabet characters.
    # Wait, the payload contains curly braces, underscores, and numbers in the flag.
    # Classical Vigenere leaves punctuation and numbers as is.
    key_idx = 0
    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_idx % key_len].lower()) - 97
            if char.islower():
                ciphertext += chr((ord(char) - 97 + shift) % 26 + 97)
            else:
                ciphertext += chr((ord(char) - 65 + shift) % 26 + 65)
            key_idx += 1
        else:
            ciphertext += char
            
    return ciphertext

def generate():
    # Load flag from environment or use default
    flag_stage3 = os.environ.get("FLAG_STAGE3", "BP{vigenere_silence_broken}")
    
    plaintext = f"""[BEGIN CLASSIFIED TRANSMISSION]

INCIDENT RESPONSE DIRECTIVE #48

Operator,

If you are reading this, the primary network has been compromised.
The rogue AI node has initiated lockdown protocols.

I have hidden the next set of tools in the archival file share.
Directory path: /repo/classified_assets_2048/

You will need the following passphrase to extract the payload from the telemetry images:
PASSPHRASE: "sovereign_override_991"

Also, here is your authorization flag for reaching this step:
FLAG: {flag_stage3}

Good luck.
[END TRANSMISSION]"""

    print("--- Plaintext ---")
    print(plaintext)
    
    # 1. Vigenere Encrypt
    encrypted_vigenere = vigenere_encrypt(plaintext, KEY)
    
    # 2. Base64 Encode
    encoded_b64 = base64.b64encode(encrypted_vigenere.encode('utf-8')).decode('utf-8')
    
    # Ensure output directory exists
    out_dir = os.path.join(os.path.dirname(__file__), "..", "stage2-portal", "static", "downloads")
    os.makedirs(out_dir, exist_ok=True)
    
    out_path = os.path.join(out_dir, "transmission_log_48.txt")
    with open(out_path, "w") as f:
        f.write(encoded_b64)
        
    print(f"\nArtifact successfully generated and written to: {out_path}")

if __name__ == "__main__":
    generate()

