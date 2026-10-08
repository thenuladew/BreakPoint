/**
 * BREAKPOINT CTF — Dashboard JS V3
 */

const TEAM_TOKEN = document.querySelector('meta[name="team-token"]')?.content || "";
const timerStartedMeta = document.querySelector('meta[name="timer-started"]')?.content === 'true';

// ── Typewriter Intro ──────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
  if (!timerStartedMeta) {
    runTypewriterIntro();
  }
});

const introLines = [
  { text: '[SYS] Establishing secure connection...', cls: 'sys', delay: 15, pause: 400 },
  { text: '[SYS] Channel encrypted. TLS 1.3 handshake complete.', cls: 'sys', delay: 15, pause: 300 },
  { text: '[SYS] Authenticating credentials...', cls: 'sys', delay: 15, pause: 600 },
  { text: '', cls: '', delay: 0, pause: 200 },
  { text: 'AUTHENTICATION SUCCESSFUL', cls: 'ok', delay: 25, pause: 500 },
  { text: 'CLEARANCE: LEVEL 4 — VERIFIED', cls: 'ok', delay: 25, pause: 800 },
  { text: '', cls: '', delay: 0, pause: 400 },
  { text: '╔══════════════════════════════════════════════════════════╗', cls: 'sys', delay: 5, pause: 100 },
  { text: '║  W A R N I N G                                         ║', cls: 'danger', delay: 5, pause: 100 },
  { text: '╚══════════════════════════════════════════════════════════╝', cls: 'sys', delay: 5, pause: 600 },
  { text: '', cls: '', delay: 0, pause: 200 },
  { text: 'This system is currently operating under RESTRICTED INCIDENT CONDITIONS.', cls: 'warn', delay: 20, pause: 300 },
  { text: '', cls: '', delay: 0, pause: 200 },
  { text: 'INCIDENT ID:      SOV-2741', cls: 'danger', delay: 20, pause: 200 },
  { text: 'STATUS:           ACTIVE', cls: 'danger', delay: 20, pause: 200 },
  { text: 'CLASSIFICATION:   TOP SECRET', cls: 'danger', delay: 20, pause: 600 },
  { text: '', cls: '', delay: 0, pause: 400 },
  { text: 'SECURITY INCIDENT BRIEFING', cls: 'header', delay: 0, pause: 400 },
  { text: 'SOVEREIGN has detected unauthorized activity across multiple', cls: 'bright', delay: 12, pause: 50 },
  { text: 'infrastructure nodes. Initial investigation indicates that', cls: 'bright', delay: 12, pause: 50 },
  { text: 'privileged contractor credentials were used to access', cls: 'bright', delay: 12, pause: 50 },
  { text: 'restricted systems.', cls: 'bright', delay: 12, pause: 300 },
  { text: '', cls: '', delay: 0, pause: 200 },
  { text: 'The identity and objectives of the operator remain unknown.', cls: 'bright', delay: 12, pause: 50 },
  { text: 'The attacker may have modified or manipulated parts of', cls: 'bright', delay: 12, pause: 50 },
  { text: 'SOVEREIGN.', cls: 'bright', delay: 12, pause: 500 },
  { text: '', cls: '', delay: 0, pause: 300 },
  { text: 'Your task: Investigate the compromise. Recover evidence.', cls: 'ok', delay: 18, pause: 100 },
  { text: 'Determine what happened to the system.', cls: 'ok', delay: 18, pause: 800 },
];

async function typeText(el, text, speed) {
  return new Promise(resolve => {
    if (!text) { resolve(); return; }
    let i = 0;
    const cursor = document.createElement('span');
    cursor.className = 'typed-cursor';
    el.appendChild(cursor);
    function next() {
      if (i < text.length) {
        el.insertBefore(document.createTextNode(text[i]), cursor);
        i++;
        setTimeout(next, speed + (Math.random() * speed * 0.4));
      } else {
        cursor.remove();
        resolve();
      }
    }
    next();
  });
}

async function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function runTypewriterIntro() {
  const output = document.getElementById('intro-output');
  const btn = document.getElementById('btn-begin');
  if (!output || !btn) return;

  for (const line of introLines) {
    const div = document.createElement('div');
    div.className = 'intro-line ' + line.cls;
    output.appendChild(div);
    if (line.cls === 'header') {
      div.textContent = line.text;
    } else {
      await typeText(div, line.text, line.delay);
    }
    div.classList.add('visible');
    await sleep(line.pause);
    output.scrollTop = output.scrollHeight;
  }
  
  const finalCursor = document.createElement('span');
  finalCursor.className = 'typed-cursor';
  output.appendChild(finalCursor);
  await sleep(400);
  btn.style.display = 'inline-block';
}

// ── Node Selection ────────────────────────────────────────────

function selectNode(stageId, isLocked) {
  if (isLocked) return;

  document.querySelectorAll('.node-entry').forEach(el => el.classList.remove('active'));
  const navItem = document.getElementById(`nav-node-${stageId}`);
  if (navItem) navItem.classList.add('active');

  document.querySelectorAll('.pane-view').forEach(el => el.classList.remove('active'));
  const nodeView = document.getElementById(`view-node-${stageId}`);
  if (nodeView) nodeView.classList.add('active');
}

// ── Start Challenge ───────────────────────────────────────────

async function startChallenge() {
  const btn = document.getElementById("btn-begin");
  if (btn) {
    btn.disabled = true;
    btn.textContent = "[ INITIATING... ]";
  }

  const res = await fetch("/api/start_timer", {
    method: "POST",
    headers: {
      "X-Team-Token": TEAM_TOKEN,
      "Content-Type": "application/json",
    },
  });
  const data = await res.json();

  if (data.success) {
    window.location.reload();
  } else {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "[ BEGIN INVESTIGATION ]";
    }
    alert(data.message || "Could not start timer.");
  }
}

// ── Flag Submission ───────────────────────────────────────────

async function submitFlag(e, stageId) {
  e.preventDefault();
  const form     = e.target;
  const input    = form.querySelector(".flag-input");
  const feedback = document.getElementById(`feedback-${stageId}`);
  const flag     = input.value.trim();

  if (!flag) return;

  feedback.textContent  = "> PROCESSING PAYLOAD...";
  feedback.className    = "terminal-feedback";

  const res = await fetch("/api/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Team-Token": TEAM_TOKEN,
    },
    body: JSON.stringify({ stage_id: stageId, flag }),
  });

  const data = await res.json();

  if (data.success) {
    feedback.textContent = data.message;
    feedback.classList.add("ok");
    
    const scoreEl = document.getElementById("hud-score");
    if (scoreEl && data.points_awarded) {
      scoreEl.textContent = parseInt(scoreEl.textContent, 10) + data.points_awarded;
    }
    
    setTimeout(() => window.location.reload(), 1400);
  } else {
    feedback.textContent = "> ERROR: " + (data.message || "INCORRECT PAYLOAD SIGNATURE.");
    feedback.classList.add("err");
    input.value = "";
    setTimeout(() => {
      feedback.textContent = "";
      feedback.className   = "terminal-feedback";
    }, 4000);
  }
}

// ── Hints ─────────────────────────────────────────────────────

async function getHint(stageId, hintNum) {
  const penalty = hintNum === 1 ? "5%" : "10%";
  const ok = confirm(`WARNING: Requesting Intel ${hintNum} will cost ${penalty} of Node 0${stageId}'s integrity score. Proceed?`);
  if (!ok) return;

  const hintEl = document.getElementById(`hint-${stageId}`);
  hintEl.textContent = "> FETCHING INTEL...";
  hintEl.className = "intel-display";

  const res = await fetch("/api/hint", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Team-Token": TEAM_TOKEN,
    },
    body: JSON.stringify({ stage_id: stageId, hint_number: hintNum }),
  });

  const data = await res.json();
  if (data.success) {
    hintEl.textContent = `> ${data.hint}`;
    hintEl.classList.add("revealed");
  } else {
    hintEl.textContent = "> ERROR: " + (data.message || "COULD NOT LOAD INTEL.");
  }
}
