# BREAKPOINT – SOVEREIGN Incident Response CTF

**BREAKPOINT** is a cyber defense and incident response Capture The Flag (CTF) environment. Designed as a comprehensive, immersive 6-stage challenge, players step into the role of a national cyber defense team responding to a critical incident: an unauthorized simulated launch countdown initiated by the autonomous strategic defense system, **SOVEREIGN**.

## The Scenario
*Sri Lanka, 2048.* Corrupted data has been introduced into the SOVEREIGN system via a compromised defense contractor pipeline. A countdown has started. You have 60 minutes to trace the attack chain—from external OSINT footprinting to reverse engineering malware and correlating forensic network traffic—to identify the rogue session and revoke the launch authorization.

## Features
* **6 Custom-Built Stages:** Covering OSINT, Web Security (IDOR), Cryptography (Vigenère/Base64), Steganography, Reverse Engineering, and Network Forensics.
* **Fully Dockerized Isolation:** Every stage runs in isolated Docker networks (`internal: true`) ensuring zero host egress or cross-stage contamination. All traffic flows through a hardened Nginx Edge Proxy.
* **Cinematic CTF Platform:** A custom-built Flask/SQLite dashboard with a cyberpunk-inspired UI, live mission briefings, dynamic flag validation (salted SHA-256), and a penalty-based hint system.
* **Real-Time 60-Minute Countdown:** A persistent, server-side timer that automatically triggers when players reach the critical injection phase (Stage 5), increasing pressure for the final forensic correlation.

---

## Quickstart Guide

### Prerequisites
* **Docker** & **Docker Compose** installed.
* A host machine (Linux/macOS) capable of running 12 lightweight containers.

### Installation & Deployment
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/BreakPoint.git
   cd BreakPoint
   ```
2. **Setup the Environment:**
   ```bash
   cp .env.example .env
   # Open .env and customize your SECRET_KEY and FLAG_SALT
   ```
3. **Launch the CTF Environment:**
   ```bash
   docker compose up -d --build
   ```
4. **Access the Platform:**
   * **Main CTF Dashboard:** `http://localhost:8080`
   * Provide players with this URL. The dashboard acts as the central hub for the mission, scoreboard, and stage handoffs.

---

## Stage Overview & Topology

| Stage | Domain | Title | Challenge Access |
|---|---|---|---|
| **Platform** | Dashboard & Scoring | SOVEREIGN Core | `http://localhost:8080` |
| **Stage 1** | OSINT / Recon | Ghost in the Footprint | `http://localhost:8081` |
| **Stage 2** | Web Security (IDOR) | The Contractor Portal | `http://localhost:8082` |
| **Stage 3** | Cryptography | Silent Signals | *(Downloaded from Stage 2)* |
| **Stage 4** | Steganography | Buried Warning | `http://localhost:8084` |
| **Stage 5** | Reverse Engineering | The Injection Tool | *(Downloaded from Stage 4)* |
| **Stage 6** | Forensics & Auth API | Last Authorization | `http://localhost:8090` |

---

## Repository Structure

```text
BreakPoint/
├── docker-compose.yml       # Root orchestrator for all services and internal networks
├── .env.example             # Environment variables template (flags, salts, keys)
├── platform/                # Flask Control Platform (Port 8080)
├── proxy/                   # Nginx Edge Proxy (Gates traffic and routes domains)
├── stages/                  
│   ├── stage1-osint/        # Fictional defense contractor static site
│   ├── stage2-portal/       # Vulnerable Flask app with IDOR flaw
│   ├── fileshare/           # Nginx file server for Stage 4 & 5 artifacts
│   ├── stage6-authorization/# Final REST API for incident revocation
│   └── ...                  # Generator scripts for Crypto, Stego, and PCAP artifacts
└── docs/                    # Walkthroughs, manuals, and architecture guides
```

## Walkthroughs & Solutions

If you are a CTF organizer, instructor, or a player who is completely stuck, you can find the complete master walkthrough covering all stages and flags in the `docs` directory:
* **[Master Walkthrough Guide](docs/walkthrough_master.md)**

All plaintext flags are stored and managed inside the `.env` file.

---
*Developed for Advanced Cyber Defense Training.*
