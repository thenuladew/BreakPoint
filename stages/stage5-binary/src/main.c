#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Decoy strings to confuse `strings` command
const char* decoy1 = "password=admin12345";
const char* decoy2 = "auth_key=SUPER_SECRET_KEY_99";
const char* decoy3 = "override=true";
const char* decoy4 = "Connecting to 192.168.1.100...";

void print_banner() {
    printf("==========================================\n");
    printf(" SOVEREIGN CORE INJECTION UTILITY v2.4\n");
    printf(" WARNING: UNAUTHORIZED USE IS PROHIBITED\n");
    printf("==========================================\n");
}

int check_credential(const char* input) {
    // Expected password: "omega_protocol_initiated"
    // XOR key: 0x5A
    unsigned char expected_xor[] = {0x35, 0x37, 0x3f, 0x3d, 0x3b, 0x5, 0x2a, 0x28, 0x35, 0x2e, 0x35, 0x39, 0x35, 0x36, 0x5, 0x33, 0x34, 0x33, 0x2e, 0x33, 0x3b, 0x2e, 0x3f, 0x3e};
    int len = sizeof(expected_xor);
    
    if (strlen(input) != len) {
        return 0;
    }
    
    for (int i = 0; i < len; i++) {
        if ((input[i] ^ 0x5A) != expected_xor[i]) {
            return 0;
        }
    }
    return 1;
}

int main(int argc, char *argv[]) {
    print_banner();
    
    if (argc != 2) {
        printf("Usage: %s <override_credential>\n", argv[0]);
        return 1;
    }
    
    if (check_credential(argv[1])) {
        printf("\n[+] CREDENTIAL ACCEPTED.\n");
        printf("[+] OVERRIDE PROTOCOL INITIATED.\n\n");
        
        // Fetch flag from environment or use default if compiled in
        // Since it's a binary, we'll just hardcode the flag or generate it at compile time.
        // But for simplicity, we hardcode the Stage 5 flag directly in the binary.
        // We will obfuscate the flag slightly so it doesn't show up in `strings` easily.
        
        // Flag: BP{xor_obfuscation_reversed}
        unsigned char enc_flag[] = {0x0, 0x12, 0x39, 0x3a, 0x2d, 0x30, 0x1d, 0x2d, 0x20, 0x24, 0x37, 0x31, 0x21, 0x23, 0x36, 0x2b, 0x2d, 0x2c, 0x1d, 0x30, 0x27, 0x34, 0x27, 0x30, 0x31, 0x27, 0x26, 0x3f};
        
        printf("FLAG: ");
        for(int i=0; i<sizeof(enc_flag); i++){
            putchar(enc_flag[i] ^ 0x42);
        }
        printf("\n\n");
        
        printf("Client Identifier IoC: SOV-INJ-CLIENT-9914\n");
        printf("Use this identifier to trace the unauthorized session in the Stage 6 audit logs.\n");
    } else {
        printf("\n[-] ACCESS DENIED: Invalid override credential.\n");
        printf("[-] This incident has been logged.\n");
    }
    
    return 0;
}
