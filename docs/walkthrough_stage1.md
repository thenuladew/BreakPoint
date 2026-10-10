# 🕵️‍♂️ BREAKPOINT CTF: Stage 1 OSINT Walkthrough

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
