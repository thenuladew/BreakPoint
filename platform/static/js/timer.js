/**
 * BREAKPOINT CTF – Countdown Timer
 * Resilient: reads server-supplied remaining seconds from <meta>,
 * counts down client-side, syncs with /api/timer every 60s.
 */
(function () {
  'use strict';

  const el        = document.getElementById('countdown');
  const metaStart = document.querySelector('meta[name="timer-started"]');
  const metaRem   = document.querySelector('meta[name="timer-remaining"]');
  const metaExp   = document.querySelector('meta[name="timer-expired"]');
  const metaStop  = document.querySelector('meta[name="timer-stopped"]');

  if (!el || !metaStart) return;

  const started = metaStart.content === '1';
  const expired = metaExp  && metaExp.content  === '1';
  const stopped = metaStop && metaStop.content === '1';

  if (!started || expired || stopped) return;  // nothing to tick

  let remaining = parseInt(metaRem.content, 10);
  if (isNaN(remaining) || remaining <= 0) return;

  const hud = el.closest('.hud-timer');

  function fmt(s) {
    const h = Math.floor(s / 3600);
    const m = Math.floor((s % 3600) / 60);
    const sec = s % 60;
    return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}`;
  }

  function markExpired() {
    el.textContent = 'TIME EXPIRED';
    el.classList.add('hud-expired');
    if (hud) hud.classList.add('hud-timer--expired');
  }

  // Tick every second
  const ticker = setInterval(function () {
    remaining -= 1;
    if (remaining <= 0) {
      clearInterval(ticker);
      markExpired();
      return;
    }
    el.textContent = fmt(remaining);

    // Flash red when under 5 minutes
    if (remaining <= 300 && hud) {
      hud.style.borderColor = '#ff3355';
    }
  }, 1000);

  // Re-sync with server every 60 seconds to correct drift
  const token = document.querySelector('meta[name="team-token"]');
  if (token) {
    setInterval(function () {
      fetch('/api/timer', {
        headers: { 'X-Team-Token': token.content }
      })
        .then(r => r.json())
        .then(data => {
          if (data.expired) {
            clearInterval(ticker);
            markExpired();
          } else if (data.stopped) {
            clearInterval(ticker);
            el.textContent = 'MISSION COMPLETE';
            el.classList.add('hud-success');
          } else if (data.remaining_s) {
            remaining = data.remaining_s;
          }
        })
        .catch(() => { /* silently ignore network errors during sync */ });
    }, 60000);
  }
})();
