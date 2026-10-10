# 🖼️ BREAKPOINT CTF: Stage 4 Steganography Walkthrough

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
