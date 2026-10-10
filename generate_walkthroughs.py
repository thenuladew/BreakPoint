import os

os.makedirs("docs", exist_ok=True)

md1 = """# 🕵️‍♂️ BREAKPOINT CTF: Stage 1 OSINT Walkthrough

> 💡 **Scenario:** You need to identify the external contractor whose credentials were compromised. This will provide the first flag and critical information for the next stage.

---

## 🔍 1. Initial Reconnaissance

You start by accessing the target contractor website at `http://localhost:8081` (Port 8081). 

Browse the website to gather information about the personnel. Pay special attention to the **Team** or **About Us** sections where employees and contractors are listed.

## 🛠️ 2. Finding the Target User

On the **Team** page (`/team.html`), scroll down to the "EXTERNAL CONTRACTORS" section.
You will find a profile for:
- **Name:** Oshii
- **Role:** Senior Systems Integration Lead
- **Username:** `oshii_ext`

*Keep this username and exact role title ("Senior Systems Integration Lead") safe. You will need them in upcoming stages.*

## 🚩 3. Recovering the Flag

While you are on the `team.html` page, right-click and select **View Page Source** (or press `Ctrl+U`).

Scroll to the very bottom of the HTML source code. Hidden within an HTML comment intended for the development team, you will find the first flag:

```html
<!--
  NOTE TO DEV TEAM (Tharaka): contractor onboarding for oshii_ext completed.
  Portal access provisioned via the contractor management system.
  Flag: BP{gh0st_1n_f00tpr1nt_osh11_ext}
  Remove this comment before production deployment — S.Perera
-->
```

**Flag 1:** `BP{gh0st_1n_f00tpr1nt_osh11_ext}`

Submit this flag to the main dashboard (`http://localhost:8080`) to unlock Stage 2!
"""

with open("docs/walkthrough_stage1.md", "w") as f:
    f.write(md1)

md2 = """# 🔓 BREAKPOINT CTF: Stage 2 IDOR Walkthrough

> 💡 **Scenario:** Armed with the knowledge that an external contractor's account exists on the Contractor Portal, your goal is to bypass authorization controls to access their private documents.

---

## 🔍 1. Accessing the Portal

Navigate to the Contractor Portal at `http://localhost:8082` (Port 8082).
Log in using the guest credentials provided on the login page:
- **Username:** `guest`
- **Password:** `guest2048`

## 🛠️ 2. Identifying the IDOR Vulnerability

Once logged in, click on **"View Document"** for the "Guest Onboarding Guide".

Observe the URL in your browser's address bar. It will look something like this:
`http://localhost:8082/portal/document?id=1001`

The `id` parameter specifies which document to load. Because this application suffers from an **Insecure Direct Object Reference (IDOR)** vulnerability, it does not check if the currently logged-in user actually owns the document they are requesting.

## 🚩 3. Exploiting the IDOR & Recovering the Flag

You need to access the restricted incident transmission document. You can find it by brute-forcing or iterating the document ID parameter.

Try changing the ID in the URL to nearby numbers (e.g., `1000`, `1002`, `1003`...). 

When you change the ID to `1042`:
`http://localhost:8082/portal/document?id=1042`

You will successfully access a restricted document titled **"RESTRICTED: Incident Transmission"**.

Inside this document, you will find:
1. **Flag 2:** `BP{idor_unlocked_portal_access}`
2. A download link for a classified file: `transmission_log_48.txt`

Download the `transmission_log_48.txt` file (you will need it for Stage 3) and submit the flag to the main dashboard to unlock the next stage!
"""

with open("docs/walkthrough_stage2.md", "w") as f:
    f.write(md2)

md3 = """# 🔐 BREAKPOINT CTF: Stage 3 Cryptography Walkthrough

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
"""

with open("docs/walkthrough_stage3.md", "w") as f:
    f.write(md3)

md4 = """# 🖼️ BREAKPOINT CTF: Stage 4 Steganography Walkthrough

> 💡 **Scenario:** You have uncovered the hidden directory of the archival file share and the extraction passphrase. Your objective is to extract hidden malware (the payload) from an image file.

---

## 🔍 1. Locating the Target Image

Navigate to the hidden directory you discovered in Stage 3 on Port 8084:
`http://localhost:8084/repo/classified_assets_2048/`

You will see several telemetry images. Download the target image: `payload_telemetry.jpg`.

## 🛠️ 2. Extracting Hidden Data (Steghide)

The data is hidden inside the image using Steganography. You will need a tool called `steghide` (available on most Linux distributions, including Kali Linux).

Run the following command in your terminal to extract the hidden data from the image:
```bash
steghide extract -sf payload_telemetry.jpg
```

When prompted for the passphrase, enter the one you decrypted in Stage 3:
**Passphrase:** `sovereign_override_991`

## 🚩 3. Recovering the Flag

If the passphrase is correct, `steghide` will extract a hidden file named `payload.txt`.

Read the contents of the extracted file:
```bash
cat payload.txt
```

Inside, you will find:
1. The path to download the malware binary for Stage 5: `/tools/sovereign_inject_x86`
2. **Flag 4:** `BP{steghide_payload_extracted}`

Submit the flag to the main dashboard to unlock Stage 5!
"""

with open("docs/walkthrough_stage4.md", "w") as f:
    f.write(md4)

