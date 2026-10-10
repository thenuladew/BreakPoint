# 🔓 BREAKPOINT CTF: Stage 2 IDOR Walkthrough

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
