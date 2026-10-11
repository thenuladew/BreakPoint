# BREAKPOINT — Member 4 Integration, Testing and Evaluation Report

**Module / Assignment:** [Enter module and assignment number]  
**Project:** BREAKPOINT — SOVEREIGN Incident Response CTF  
**Role:** Member 4 — Integration, Testing, Evaluation and Documentation  
**Student name:** [Enter name]  
**Student ID:** [Enter student ID]  
**Group members:** [Enter names]  
**Submission date:** [Enter date]  
**Repository:** https://github.com/thenuladew/BreakPoint

---

## Document purpose

This document records the integration and verification work carried out for BREAKPOINT. It is intended to demonstrate how the six-stage CTF environment fits together, how expected and unexpected behaviour is tested, whether reset and recovery work, and how implementation decisions compare with the original design.

**Evidence rule:** Results must be recorded from tests that were actually performed. Until a test has been executed, its status is **Not tested**. Do not label a test as passed, claim a vulnerability is prevented, or invent a defect and fix without supporting evidence.

## 1. Project overview and integration scope

BREAKPOINT is a Docker-based, six-stage cyber defence and incident-response CTF. Its scenario places the player in a fictional 2048 incident involving SOVEREIGN, an autonomous strategic defence system whose launch countdown has been triggered by a compromised contractor pipeline. Players investigate the incident through a sequence of challenges.

The repository README describes a Flask/SQLite platform, an Nginx edge proxy, Docker services and networks, salted SHA-256 flag validation, a hint system and a 60-minute countdown associated with the critical injection phase. These are documented design claims; their runtime behaviour must be verified during testing.

### 1.1 Member 4 responsibilities

- Verify the complete player journey and integration between the platform and challenge stages.
- Prepare test cases for normal, invalid and out-of-order actions.
- Record defects, investigate causes, document fixes and retest.
- Check for unintended shortcuts that bypass intended challenge paths.
- Verify single-stage and full-environment reset/recovery, where supported.
- Update the risk register with actual outcomes.
- Compare the original design with the final implementation and justify changes.
- Develop and explain an original testing script that supports the assignment's learning outcomes.
- Collect clear, reproducible evidence for the final demonstration.

### 1.2 In scope and limitations

This report focuses on integration, functional testing, recovery, security-oriented challenge validation and project evaluation. It does not replace the individual stage walkthroughs prepared by the challenge developers.

Testing must be performed only against the authorised BREAKPOINT lab environment. Any host-isolation or container-escape conclusion requires evidence appropriate to that claim; a simple application-level test is not sufficient to prove host isolation.

## 2. System overview and stage dependency map

The README identifies the following stage sequence and access points. These are the documented entry points, not proof that every dependency has already been tested.

| Component | Challenge / purpose | Documented access or handoff |
|---|---|---|
| Platform | SOVEREIGN Core dashboard, scoring and flag submission | `http://localhost:8080` |
| Stage 1 | Ghost in the Footprint — OSINT / reconnaissance | `http://localhost:8081` |
| Stage 2 | The Contractor Portal — web security / IDOR | `http://localhost:8082` |
| Stage 3 | Silent Signals — cryptography | Downloaded from Stage 2 |
| Stage 4 | Buried Warning — steganography | `http://localhost:8084` |
| Stage 5 | The Injection Tool — reverse engineering | Downloaded from Stage 4 |
| Stage 6 | Last Authorization — forensics and authorisation API | `http://localhost:8090` |

### 2.1 Expected player journey

1. The player enters through the main platform.
2. The player investigates and solves Stage 1, then submits the relevant flag.
3. The player progresses to Stage 2 and obtains the intended artifact or clue for Stage 3.
4. The player solves the cryptography challenge and continues through the intended sequence.
5. Stage 4 supplies the artifact needed for Stage 5.
6. The player analyses the Stage 5 injection tool and uses the findings in the final Stage 6 forensic/authorisation challenge.
7. The player submits the final flag or performs the intended final action, and the platform records the outcome.

**Verification required:** Confirm each step against the current platform code and actual challenge files. In particular, verify the exact credentials, artifacts, flag-to-stage mapping, unlocking rules and final completion condition. Do not assume that the README's stage order automatically enforces access control.

### 2.2 Dependency matrix

Complete this matrix after inspecting the stage code and running the challenges.

| Transition | Required flag / artifact / prerequisite | How the next stage is unlocked | Evidence | Status |
|---|---|---|---|---|
| Platform → Stage 1 | [Verify] | [Verify] | [Screenshot/log] | Not tested |
| Stage 1 → Stage 2 | [Verify] | [Verify] | [Screenshot/log] | Not tested |
| Stage 2 → Stage 3 | [Verify artifact/handoff] | [Verify] | [Screenshot/log] | Not tested |
| Stage 3 → Stage 4 | [Verify] | [Verify] | [Screenshot/log] | Not tested |
| Stage 4 → Stage 5 | [Verify artifact/handoff] | [Verify] | [Screenshot/log] | Not tested |
| Stage 5 → Stage 6 | [Verify] | [Verify] | [Screenshot/log] | Not tested |
| Stage 6 → Completion | [Verify final condition] | [Verify] | [Screenshot/log] | Not tested |

### 2.3 Integration acceptance criteria

- The documented services start using the documented deployment process.
- The platform is reachable through its intended entry point.
- Each challenge and artifact handoff works as designed.
- Correct flags are accepted and invalid flags are rejected.
- Stage progression follows the actual design, including any intentionally available parallel access.
- The scoring and completion state agree with the player's actions.
- Restart and reset procedures restore the documented baseline.
- The environment behaves consistently after a clean deployment.

## 3. Test strategy and test cases

### 3.1 Test approach

Testing is divided into:

- **Positive / happy-path tests:** intended actions succeed.
- **Negative tests:** incorrect inputs and unauthorised actions are rejected.
- **Dependency / boundary tests:** required prerequisites are enforced and state transitions behave correctly.
- **Recovery tests:** reset or restart restores the intended state.
- **Security-oriented tests:** look for accidental exposure, unintended shortcuts and misconfiguration.
- **Regression tests:** previously fixed issues remain fixed after a change.

Record the date, environment, software revision, steps, expected result, actual result, evidence and status for each test.

### 3.2 Test case register

The cases below are a starting plan. Update the steps to match the actual implementation before execution.

| ID | Test objective | Procedure | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| TC-01 | Clean deployment | Follow the README setup on a clean test environment | Required services start and remain healthy | [Record] | Not tested |
| TC-02 | Platform reachability | Open the main dashboard on port 8080 | Dashboard responds as expected | [Record] | Not tested |
| TC-03 | Correct flag | Submit a valid flag for an available stage | Flag is accepted and state updates correctly | [Record] | Not tested |
| TC-04 | Incorrect flag | Submit a deliberately invalid flag | Flag is rejected without granting progress | [Record] | Not tested |
| TC-05 | Empty / malformed submission | Submit empty input and malformed flag values | Input is handled safely; no false acceptance | [Record] | Not tested |
| TC-06 | Stage dependency | Attempt a later-stage action without its required prerequisite | Behaviour matches the documented progression rules | [Record] | Not tested |
| TC-07 | Artifact handoff: Stage 2 → 3 | Complete the intended Stage 2 path and use its artifact in Stage 3 | Artifact is available and usable as designed | [Record] | Not tested |
| TC-08 | Artifact handoff: Stage 4 → 5 | Complete the intended Stage 4 path and use its artifact in Stage 5 | Artifact is available and usable as designed | [Record] | Not tested |
| TC-09 | Scoring consistency | Submit valid and invalid flags and inspect score/progress | Score and progress reflect accepted actions only | [Record] | Not tested |
| TC-10 | Service restart | Restart the documented services | Services recover and expected state persists or resets according to design | [Record] | Not tested |
| TC-11 | Single-stage reset | Use the documented stage-reset mechanism, if provided | Target stage returns to its defined baseline | [Record] | Not tested / N/A |
| TC-12 | Full-environment reset | Use the documented full-reset procedure | All relevant components return to the defined baseline | [Record] | Not tested |
| TC-13 | Unintended flag exposure | Inspect public responses, static files, image layers and container configuration within the lab | No unintended shortcut exposes protected flags | [Record] | Not tested |
| TC-14 | Network separation | Inspect configured networks and test only the relevant authorised connectivity paths | Observed reachability matches the intended network policy | [Record] | Not tested |
| TC-15 | Countdown behaviour | Enter the intended countdown-triggering phase and observe timer behaviour | Timer starts and expires according to the specification | [Record] | Not tested |
| TC-16 | Regression after fixes | Re-run relevant tests after a defect fix | Previously passing behaviour remains correct | [Record] | Not tested |

**Status values:** Pass, Fail, Blocked, Not tested, or Not applicable. Use Not applicable only with a reason. A failed test is a useful result if it is recorded honestly and followed up.

### 3.3 Test evidence log

| Evidence ID | Related test | Evidence to capture | File / location |
|---|---|---|---|
| EV-01 | TC-01 | Deployment command and service health output | [Path] |
| EV-02 | TC-02 | Browser showing the platform entry point | [Path] |
| EV-03 | TC-03 / TC-04 | Correct and incorrect flag submission outcomes | [Path] |
| EV-04 | TC-06 | Evidence of prerequisite enforcement | [Path] |
| EV-05 | TC-07 / TC-08 | Artifact handoff evidence | [Path] |
| EV-06 | TC-11 / TC-12 | Before-and-after reset state | [Path] |
| EV-07 | TC-13 / TC-14 | Relevant configuration and test results | [Path] |
| EV-08 | Script run | Terminal output showing the automated test summary | [Path] |

Avoid placing real secrets, production credentials or unrestricted flag values in public evidence. Use redaction where appropriate.

## 4. Defect tracking and retesting

Do not invent defects to make the report look more convincing. If no defect is discovered, report the tests performed and the limitations of that testing.

| Defect ID | Related test | Observed behaviour | Root cause | Fix / action | Retest result | Status |
|---|---|---|---|---|---|---|
| BUG-01 | [Test ID] | [Actual observed issue] | [Confirmed cause or under investigation] | [Change made / planned action] | [Evidence] | Open |
| BUG-02 | [Test ID] | [Actual observed issue] | [Confirmed cause or under investigation] | [Change made / planned action] | [Evidence] | Open |

For each defect:

1. Reproduce it and capture the original behaviour.
2. Record the impact and the conditions under which it occurs.
3. Identify the root cause, distinguishing evidence from assumptions.
4. Apply and record the fix.
5. Repeat the original test.
6. Run relevant regression tests.
7. Attach evidence of the final result.

## 5. Unintended-solution and security checks

The goal is to determine whether a player can bypass the intended challenge path through an accidental disclosure or configuration error. Run these checks only in the authorised lab and document the scope of each conclusion.

| ID | Check | Example verification method | Pass condition | Status |
|---|---|---|---|---|
| SEC-01 | Flag in public web content | Inspect browser responses, page source and publicly served static files | No protected flag is unintentionally disclosed | Not tested |
| SEC-02 | Flag in image/build history | Inspect relevant image layers and build history for secrets | No protected plaintext flags or secrets are unintentionally embedded | Not tested |
| SEC-03 | Sensitive container configuration | Review environment variables and container metadata available to the player versus the organiser | Secrets are not exposed through the player's intended access level | Not tested |
| SEC-04 | Directory listing / default credentials | Check exposed routes, file listings and documented credentials | No unintended shortcut grants progress | Not tested |
| SEC-05 | Stage bypass | Try later-stage entry points without the required prerequisite | Access and progression match the documented design | Not tested |
| SEC-06 | Cross-stage network reachability | Review Docker network attachments and test expected connectivity | Reachability matches the intended isolation policy | Not tested |
| SEC-07 | Flag validation | Test wrong, malformed and repeated submissions | Only valid submissions grant the intended progress | Not tested |
| SEC-08 | Host isolation claim | Review network configuration and conduct authorised tests appropriate to the claim | Evidence supports only the isolation conclusions actually tested | Not tested |

### 5.1 Security-check notes

- A failed connection test does not, by itself, prove complete container or host isolation.
- Environment variables and Docker metadata may be available to the Docker host administrator even if they are not available to an ordinary player. State the attacker role and access level for each test.
- If a shortcut succeeds, record the exact path, impact, remediation and retest result. Do not publish sensitive exploit details beyond what the assignment requires.
- Separate application-level access control, Docker network isolation and host security; they are different properties.

## 6. Reset and recovery validation

### 6.1 Baseline definition

Before testing, record the intended clean state. Confirm the available reset commands and their documented effects from the repository; do not assume that restarting containers is equivalent to resetting application data or regenerating challenge artifacts.

| Component / state | Baseline to record | Verification evidence |
|---|---|---|
| Platform / database | Expected progress, score and timer state | [Record] |
| Stage services | Expected service and filesystem state | [Record] |
| Challenge artifacts | Expected artifact availability and contents | [Record] |
| Flags / configuration | Expected configuration without exposing secrets | [Record] |
| Docker networks | Expected network attachments | [Record] |

### 6.2 Recovery test procedure

1. Record the repository revision and starting state.
2. Start the environment using the documented command.
3. Complete a safe, repeatable action that changes state.
4. Run the documented reset operation, if available. If no dedicated reset exists, record that limitation rather than inventing a command.
5. Verify the relevant application state, challenge artifacts, services and timer.
6. Repeat the original action to confirm the environment is usable again.
7. Save before-and-after evidence.

### 6.3 Reset test record

| Test ID | Reset scope | Before state | Operation performed | Expected after state | Actual after state | Status |
|---|---|---|---|---|---|---|
| REC-01 | Single stage | [Record] | [Documented command / N/A] | [Record] | [Record] | Not tested |
| REC-02 | Full environment | [Record] | [Documented command] | [Record] | [Record] | Not tested |
| REC-03 | Restart / recovery | [Record] | [Documented command] | [Record] | [Record] | Not tested |

## 7. Risk register outcomes

Import the actual risks from Assignment 01. The rows below are examples of categories to check, not claims that these risks occurred or were successfully mitigated.

| Risk ID | Risk from original register | Planned mitigation | Actual outcome and evidence | Final status |
|---|---|---|---|---|
| R-01 | A challenge becomes unsolvable | Peer testing and validation | [Record evidence and result] | Pending |
| R-02 | A player bypasses intended progression | Dependency and shortcut tests | [Record evidence and result] | Pending |
| R-03 | Service fails during deployment | Health checks and deployment testing | [Record evidence and result] | Pending |
| R-04 | Challenge state cannot be restored | Documented reset and recovery test | [Record evidence and result] | Pending |
| R-05 | Project milestones overrun | Milestone tracking and prioritisation | [Record evidence and result] | Pending |
| R-06 | Secret or flag is accidentally exposed | Configuration review and unintended-solution tests | [Record evidence and result] | Pending |

Use a consistent outcome label: **Mitigated**, **Occurred**, **Changed**, **Accepted**, or **Unresolved**. Explain the reasoning and reference evidence for each final status.

## 8. Assignment 01 design versus final implementation

Compare the original proposal with the final repository and runtime behaviour. Every meaningful difference should have a technical explanation and evidence.

| Area | Assignment 01 plan | Final implementation | Reason for change | Impact / evidence |
|---|---|---|---|---|
| Stage design and order | [Copy from original proposal] | [Verify repository] | [Technical justification] | [Evidence] |
| Platform / framework | [Planned tool] | Flask / SQLite documented in README | [Explain any change] | [Evidence] |
| Reverse proxy | [Planned approach] | Nginx documented in README | [Explain any change] | [Evidence] |
| Deployment / isolation | [Planned approach] | Docker services and networks documented in README | [Explain any change] | [Evidence] |
| Flag validation | [Planned design] | Salted SHA-256 validation documented in README | [Explain any change] | [Evidence] |
| Reset / recovery | [Planned approach] | [Verify actual mechanism] | [Explain any change] | [Evidence] |
| Other features | [Planned features] | [Actual features] | [Reason] | [Evidence] |

A good justification explains the original requirement, the technical limitation or trade-off, the selected alternative, and the effect on security, reliability, repeatability or learning objectives. Do not use “ran out of time” as the only explanation where a technical reason can be established.

## 9. Original automated integration-testing script

### 9.1 Purpose

Develop an original script to reduce the time required for repeatable integration checks. The script should report test outcomes clearly and return a non-zero exit status when a required check fails.

The final implementation must be based on the actual platform routes, validation responses and reset mechanism. Do not hard-code guessed API endpoints or assume the platform accepts flags through an HTTP API until this has been verified.

### 9.2 Planned functionality

1. Check whether required services are running.
2. Check that the platform endpoint responds.
3. Exercise valid and invalid flag submissions through the supported interface, where safe and technically possible.
4. Verify a documented stage dependency or artifact handoff.
5. Run reset verification only when a supported reset procedure exists and the environment is safe to reset.
6. Print a clear PASS / FAIL / SKIP summary.
7. Exit with an appropriate status code so the result can be used in a repeatable workflow.

### 9.3 Script design record

| Item | Decision / implementation |
|---|---|
| Script filename | [Choose, e.g. `integration_test.py`] |
| Language | [Choose and justify] |
| Services / routes checked | [Verify] |
| Test inputs | Use lab-only test values; protect secrets |
| Reset behaviour | [Documented mechanism or omitted with reason] |
| Output format | Per-test result and final summary |
| Failure handling | Record errors; non-zero exit code when required checks fail |
| Execution evidence | [Terminal output path] |

### 9.4 Demonstration and explanation

During the demonstration:

- Explain the problem the script solves.
- Show the command used to execute it.
- Explain the key functions and control flow.
- Demonstrate how a failed check appears in the output.
- Explain how the script distinguishes a failed test from a skipped or unavailable test.
- Show the final summary and explain any limitations.

The script must be your own work and you should be able to explain every line. Automated tests support the evidence but do not replace manual security review.

## 10. Results and evaluation

Complete this section after running the tests.

### 10.1 Summary

| Metric | Result |
|---|---|
| Total planned test cases | 16 (initial register) |
| Tests executed | [Count] |
| Passed | [Count] |
| Failed | [Count] |
| Blocked | [Count] |
| Not applicable | [Count] |
| Defects identified | [Count] |
| Defects fixed and retested | [Count] |
| Recovery tests completed | [Count] |

Do not count unexecuted tests as passes.

### 10.2 Evaluation

Discuss:

- Which end-to-end transitions were verified?
- Which defects had the greatest impact, and how were they resolved?
- Which unintended shortcuts were checked, and what was the result?
- Did reset and recovery return the environment to its documented baseline?
- Which original risks occurred, changed or were mitigated?
- Which planned design decisions changed, and why?
- What remains untested, and what additional evidence would increase confidence?

## 11. Evidence index

Store evidence in a consistent directory, for example `docs/member4/evidence/`, unless the team uses another agreed location. Avoid committing secrets, sensitive credentials or unnecessary full flag lists to a public repository.

| Evidence ID | Description | Related section / test | File path |
|---|---|---|---|
| EV-01 | Clean deployment and service status | TC-01 | [Path] |
| EV-02 | Platform reachable | TC-02 | [Path] |
| EV-03 | Valid / invalid flag results | TC-03, TC-04 | [Path] |
| EV-04 | Dependency and handoff proof | TC-06 to TC-08 | [Path] |
| EV-05 | Unintended-solution checks | SEC-01 to SEC-08 | [Path] |
| EV-06 | Reset before / after | REC-01 to REC-03 | [Path] |
| EV-07 | Automated test output | Section 9 | [Path] |
| EV-08 | Design comparison / risk outcomes | Sections 7–8 | [Path] |

## 12. Final video walkthrough plan

Target duration: approximately 4–5 minutes, adjusted to the assignment brief and the evidence available.

| Approx. time | Demonstration | Key point |
|---|---|---|
| 0:00–0:20 | Introduce role and project | Explain that Member 4 verifies integration and quality |
| 0:20–1:00 | Show stage dependency map | Explain the intended order and key artifact handoffs |
| 1:00–1:40 | Demonstrate a representative end-to-end path | Show a real handoff without repeating every individual exploit |
| 1:40–2:30 | Run automated tests and show results | Explain positive and negative tests and the summary |
| 2:30–3:20 | Show an actual defect/fix or a significant test finding | Explain the evidence and retest; do not fabricate a defect |
| 3:20–4:00 | Demonstrate reset/recovery | Show before, operation and after state |
| 4:00–4:40 | Summarise risks and design changes | Give evidence-based outcomes and justifications |
| 4:40–5:00 | State limitations and conclusion | Distinguish verified results from remaining work |

If a planned test cannot be completed live, show the recorded evidence and explain the limitation honestly. Follow any mandatory structure, identity or student-ID requirements in the official assignment brief.

## 13. Completion checklist

- [ ] Original Assignment 01 risk register and design retrieved.
- [ ] Current repository and deployment instructions reviewed.
- [ ] Stage dependencies confirmed from code and runtime behaviour.
- [ ] Test cases updated to match the actual implementation.
- [ ] Tests executed and results recorded accurately.
- [ ] Defects documented and fixes retested, where applicable.
- [ ] Unintended-solution checks performed within the authorised lab.
- [ ] Reset and recovery procedures verified, where supported.
- [ ] Risk outcomes and design differences justified with evidence.
- [ ] Original script implemented, run and explained.
- [ ] Evidence files organised and sensitive information protected.
- [ ] Final video rehearsed against the official assignment requirements.

---

**Report status:** Working draft — pending implementation review and test evidence.  
**Last updated:** [Enter date]
