# 🔐 BREAKPOINT CTF: Stage 3 Cryptography Walkthrough

> 💡 **Scenario:** You have downloaded an encrypted transmission log (`transmission_log_48.txt`). You must decrypt this file to uncover the location of the hidden archival node and the passphrase required for the next stage.

---

## 🔍 1. Analyzing the Encrypted File

Open the `transmission_log_48.txt` file you downloaded in Stage 2. It contains a single string of alphanumeric characters. 

The text ends with an `=` sign, which is a classic indicator of **Base64 Encoding**.

## 🛠️ 2. Decoding the Layers

This file is double-encrypted. 

**Step 1: Base64 Decode**
Use a tool like [CyberChef](https://gchq.github.io/CyberChef/) or the command line to decode the string.
```bash
cat transmission_log_48.txt | base64 -d
```
This will result in a new string of characters that still looks like gibberish. This is the second layer of encryption.

**Step 2: Vigenère Cipher Decryption**
The second layer is a **Vigenère Cipher**. To break a Vigenère cipher, you need a secret key.
Recall the specific job role you found for the external contractor in Stage 1: **Senior Systems Integration Lead**.

Convert this title into a continuous lowercase string to form the key: `seniorsystemsintegrationlead`

Use CyberChef (Vigenère Decode module) or an online Vigenère solver.
- **Ciphertext:** (The Base64 decoded output)
- **Key:** `seniorsystemsintegrationlead`

## 🚩 3. Recovering the Flag and Intel

Once decrypted, the plaintext will reveal the Incident Response Directive.

Inside the decrypted text, you will find:
1. The hidden directory path for Stage 4: `/repo/classified_assets_2048/`
2. The extraction passphrase: `sovereign_override_991`
3. **Flag 3:** `BP{vigenere_silence_broken}`

Submit the flag to the main dashboard to unlock Stage 4!
