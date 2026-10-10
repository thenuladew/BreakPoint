# 📘 BREAKPOINT CTF: Master Walkthrough & Solution Guide

Welcome to the definitive guide for completing the **BREAKPOINT** CTF. This guide is meant for instructors or participants who are stuck and need a step-by-step resolution path for all 6 stages.

---

## 🔍 Stage 1: Ghost in the Footprint (OSINT)
**Objective**: Identify the target contractor and find the first flag.
**Target Port**: `8081`

### Solution:
1. Navigate to the fictional contractor website at `http://<TARGET_IP>:8081`.
2. Browse the **Staff Directory** or the **Blog**. Look for an external contractor who recently posted or is highlighted. You will identify **Oshii** (`oshii_ext`).
3. Note down Oshii's exact Job Title: **"Senior Systems Integration Lead"**.
4. Inspect the page source (HTML) of the blog post or about page. Hidden in an HTML comment or styling attribute, you will find the flag:
   **Flag 1**: `BP{gh0st_1n_f00tpr1nt_osh11_ext}`
5. Submit this to the main dashboard to unlock Stage 2.

---

## 🌐 Stage 2: The Contractor Portal (Web Security / IDOR)
**Objective**: Exploit an IDOR vulnerability to access the target's portal account.
**Target Port**: `8082`

### Solution:
1. Navigate to `http://<TARGET_IP>:8082`.
2. Login using the public guest credentials provided on the login page (`guest` / `guest2048`).
3. View your profile/invoice. Observe the URL, which looks something like `http://<TARGET_IP>:8082/portal/document?id=1001` (or similar ID).
4. Recall the username from Stage 1: `oshii_ext`. You need to find their user ID.
5. Brute-force or change the `id=` parameter sequentially (e.g., `1042`).
6. Once you hit the correct ID (`1042`), you will bypass authorization (Insecure Direct Object Reference) and view the contractor's private dashboard.
7. Here you will find the flag and a download link for an encrypted text file.
   **Flag 2**: `BP{idor_unlocked_portal_access}`
8. **Action**: Download `transmission_log_48.txt`. Submit the flag to unlock Stage 3.

---

## 🔐 Stage 3: Silent Signals (Cryptography)
**Objective**: Decrypt the transmission log using keys gathered from Stage 1.
**Target File**: `transmission_log_48.txt`

### Solution:
1. The downloaded file contains a block of encrypted text.
2. Recall the hint/job title from Stage 1: **"Senior Systems Integration Lead"**.
3. The text is encrypted with a **Vigenère Cipher**, followed by **Base64** encoding.
4. **Step A**: Decode the Base64 text. You will get another string of gibberish.
5. **Step B**: Use a tool like **CyberChef** (Vigenère Decode). Set the key to `seniorsystemsintegrationlead` (the job title, no spaces, lowercase).
6. The decrypted text will reveal:
   - The Stage 3 Flag.
   - The hidden directory for Stage 4: `/repo/classified_assets_2048/`
   - The Steghide passphrase for Stage 4: `sovereign_override_991`
   **Flag 3**: `BP{vigenere_silence_broken}`
7. Submit the flag to unlock Stage 4.

---

## 🖼️ Stage 4: Buried Warning (Steganography)
**Objective**: Extract hidden data from an image file share.
**Target Port**: `8084`

### Solution:
1. Navigate to the hidden directory discovered in Stage 3: `http://<TARGET_IP>:8084/repo/classified_assets_2048/`.
2. Download all the images (e.g., `payload_telemetry.jpg`, decoy images).
3. Using a Linux machine (or Kali), use the `steghide` tool to extract data from the target image.
   ```bash
   steghide extract -sf payload_telemetry.jpg
   ```
4. When prompted for a passphrase, enter the one found in Stage 3: `sovereign_override_991`.
5. This will extract a hidden `payload.txt` file.
6. Read the extracted file. It contains the Stage 4 Flag and the path to the Stage 5 binary (`/tools/sovereign_inject_x86`).
   **Flag 4**: `BP{steghide_payload_extracted}`
7. Submit the flag to unlock Stage 5.

---

## 💻 Stage 5: The Injection Tool (Reverse Engineering)
**Objective**: Reverse engineer an obfuscated Linux ELF binary to recover credentials.
**Target File**: `sovereign_inject_x86` (from Port `8084`)

### Solution:
1. Download the binary: `http://<TARGET_IP>:8084/tools/sovereign_inject_x86`.
2. Open the binary in **Ghidra** or **IDA Pro**.
3. Decompile the `main` function. You will notice XOR-based obfuscation logic.
4. By statically analyzing the XOR key and the encoded byte array, or by dynamically debugging with `gdb` and setting breakpoints after the decryption routine, you can recover the correct password.
5. Run the binary and provide the recovered password.
   ```bash
   chmod +x sovereign_inject_x86
   ./sovereign_inject_x86 <recovered_password>
   ```
6. The program will output:
   - The Stage 5 Flag.
   - The Client Identifier IoC: `SOV-INJ-CLIENT-9914`
   - The Authorization Token: `SOV-AUTH-TOKEN-2048-XRAY`
   **Flag 5**: `BP{xor_obfuscation_reversed}`
7. Submit the flag. **WARNING**: Submitting this flag triggers the 60-minute countdown timer!

---

## 🛑 Stage 6: Last Authorization (Forensics & API Security)
**Objective**: Correlate logs and PCAP to find a rogue session, then revoke it via API.
**Target Port**: `8090` (Unlocked after submitting Stage 5 flag)

### Solution:
1. Access `http://<TARGET_IP>:8090` and download the two artifacts: `capture.pcap` and `sovereign_audit.log`.
2. Analyze the `sovereign_audit.log`. Look for an anomaly where a session bypasses human approval. You will find:
   `[WARN] Automated override sequence initiated. Source unverified.`
   `[INFO] Core authorized session REQ-8891-BETA.`
3. Analyze the `capture.pcap` in **Wireshark**. Filter for HTTP POST requests and locate the payload for session `REQ-8891-BETA`.
4. Verify the HTTP headers of that request; it matches the Client ID from Stage 5 (`SOV-INJ-CLIENT-9914`).
5. Construct a POST request (using Postman or cURL) to the `/api/v1/revoke` endpoint to halt the launch:
   ```bash
   curl -X POST http://<TARGET_IP>:8090/api/v1/revoke \
        -H "Content-Type: application/json" \
        -H "X-Client-ID: SOV-INJ-CLIENT-9914" \
        -d '{"session_id": "REQ-8891-BETA"}'
   ```
6. The API will respond with a success message containing the final flag:
   **Flag 6**: `BP{sovereign_launch_revoked}`
7. Submit this final flag to the main dashboard to stop the countdown and beat the CTF! 🎉

