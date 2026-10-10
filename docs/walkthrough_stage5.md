# 🕵️‍♂️ BREAKPOINT CTF: Stage 5 Reverse Engineering Walkthrough

> 💡 **Scenario:** You have recovered the `sovereign_inject_x86` binary from the archival file share (Node 04). Your objective is to reverse engineer this malware to extract the **Stage 5 Flag** and a critical **IoC (Indicator of Compromise)** required for the final stage.

---

## 🔍 1. Initial Reconnaissance

Once you have downloaded the binary from `http://localhost:8084/tools/sovereign_inject_x86`, make it executable and attempt to run it.

```bash
chmod +x sovereign_inject_x86
./sovereign_inject_x86
```

**Output:**
```text
==========================================
 SOVEREIGN CORE INJECTION UTILITY v2.4
 WARNING: UNAUTHORIZED USE IS PROHIBITED
==========================================
Usage: ./sovereign_inject_x86 <override_credential>
```

The tool requires a password (`<override_credential>`).

### 🪤 Trying Basic Triage (`strings`)
A common first step in reverse engineering is running the `strings` command to look for hardcoded passwords in plaintext:

```bash
strings sovereign_inject_x86 | grep "password"
```

You might find decoy strings such as:
- `password=admin12345`
- `auth_key=SUPER_SECRET_KEY_99`
- `override=true`

> ⚠️ **Warning:** If you try these, the program will reject them. The real password is obfuscated!

---

## 🛠️ 2. Decompiling with Ghidra

To uncover the real password, we must analyze the binary's internal logic. **[Ghidra](https://ghidra-sre.org/)** is the perfect free reverse engineering tool for this.

### Step 2.1: Import the Binary
1. Open Ghidra and create a **New Non-Shared Project** (e.g., "BreakPoint").
2. Press `I` (or `File > Import File`) and select the `sovereign_inject_x86` binary.
3. Keep all default import settings and click **OK**.
4. Double-click the file in your Active Project window to open it in the **CodeBrowser**.
5. When prompted to analyze the file, click **Yes**, leave all default analyzers checked, and click **Analyze**.

### Step 2.2: Locate the Main Function
Because the binary is stripped of debugging symbols (`gcc -s`), Ghidra won't explicitly label the `main` function.

1. In the **Symbol Tree** window (usually on the left), expand the **Functions** folder.
2. Look for `entry` (the program entry point) and click on it.
3. In the decompiler window (on the right), examine the `entry` function. It usually calls a library initialization function like `__libc_start_main`.
4. The first argument passed to `__libc_start_main` is the actual memory address of the `main` function. Double-click it to jump there!

### Step 2.3: Analyze the Logic
Inside `main`, you will see Ghidra's decompiled C-like code. It will look roughly like this:

```c
void FUN_00101234(int param_1, long param_2) {
    print_banner();
    if (param_1 != 2) {
        printf("Usage: %s <override_credential>\n", *(char **)param_2);
        // ... exit logic
    }
    else {
        // This calls check_credential!
        int iVar1 = FUN_00101189(*(char **)(param_2 + 8)); 
        if (iVar1 != 0) {
            puts("\n[+] CREDENTIAL ACCEPTED.");
            // ... prints the flag
        }
    }
}
```

Double-click the function `FUN_00101189` (or whatever generic name Ghidra assigned it) to examine how the password is verified.

---

## 🔓 3. Breaking the XOR Obfuscation

Inside the `check_credential` function, you will discover a loop comparing your input against an array of hex values.

### The C Logic Breakdown
The decompiled code will look something like this:

```c
int check_credential(char *input) {
    long lVar1 = strlen(input);
    if (lVar1 == 24) {
        // Hex array initialization
        byte expected_array[24] = { 0x35, 0x37, 0x3f, 0x3d, 0x3b, 0x05, 0x2a, ... };
        
        for (int i = 0; i < 24; i++) {
            if ((input[i] ^ 0x5a) != expected_array[i]) {
                return 0; // Fail
            }
        }
        return 1; // Success
    }
    return 0; // Fail
}
```

**What is this doing?**
1. The input must be exactly **24 characters long**.
2. A byte array (`expected_array`) is defined.
3. Every character of your input is XOR'd (`^`) with the hex key **`0x5a`**.
4. The result must match the bytes in `expected_array`.

### Reversing the Obfuscation
Because XOR is a symmetric mathematical operation, you can find the original password by simply XOR-ing the `expected_array` with `0x5a` again!

1. **Extract the hex array from Ghidra:** 
   `0x35, 0x37, 0x3f, 0x3d, 0x3b, 0x5, 0x2a, 0x28, 0x35, 0x2e, 0x35, 0x39, 0x35, 0x36, 0x5, 0x33, 0x34, 0x33, 0x2e, 0x33, 0x3b, 0x2e, 0x3f, 0x3e`
2. **Decode it:** Open CyberChef or use a quick Python script.

**Python Solver Script:**
```python
xor_key = 0x5A
enc_pass = [0x35, 0x37, 0x3f, 0x3d, 0x3b, 0x5, 0x2a, 0x28, 0x35, 0x2e, 0x35, 0x39, 
            0x35, 0x36, 0x5, 0x33, 0x34, 0x33, 0x2e, 0x33, 0x3b, 0x2e, 0x3f, 0x3e]

password = "".join([chr(b ^ xor_key) for b in enc_pass])
print(password)
```

Running this script outputs the master password:
> 🔑 **`omega_protocol_initiated`**

---

## 🏆 4. Execution & Reward

Now that you have the correct, reversed credential, run the binary again:

```bash
./sovereign_inject_x86 omega_protocol_initiated
```

**Output:**
```text
==========================================
 SOVEREIGN CORE INJECTION UTILITY v2.4
 WARNING: UNAUTHORIZED USE IS PROHIBITED
==========================================

[+] CREDENTIAL ACCEPTED.
[+] OVERRIDE PROTOCOL INITIATED.

FLAG: BP{xor_obfuscation_reversed}

Client Identifier IoC: SOV-INJ-CLIENT-9914
Use this identifier to trace the unauthorized session in the Stage 6 audit logs.
```

🎉 **Congratulations!** You have successfully reverse-engineered the binary, obtained the Stage 5 flag, and gathered the critical Client Identifier IoC needed to track down the rogue AI in the final stage.
