/**
 * BREAKPOINT CTF – Dashboard interactivity
 * Handles: flag submission forms, hint buttons.
 */
(function () {
  'use strict';

  const teamToken = (document.querySelector('meta[name="team-token"]') || {}).content || '';

  // ── Flag forms ──────────────────────────────────────────────
  document.querySelectorAll('.flag-form').forEach(function (form) {
    if (form.dataset.solved) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const stageId  = form.dataset.stage;
      const input    = form.querySelector('.flag-input');
      const feedback = document.getElementById('feedback-' + stageId);
      const btn      = form.querySelector('button');
      const flag     = input.value.trim();

      if (!flag) return;

      btn.disabled = true;
      btn.textContent = '…';
      feedback.textContent = '';
      feedback.className = 'flag-feedback';

      fetch('/api/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Team-Token': teamToken,
        },
        body: JSON.stringify({ stage_id: parseInt(stageId, 10), flag: flag }),
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.success) {
            feedback.textContent = data.message;
            feedback.className   = 'flag-feedback feedback-ok';
            input.disabled       = true;
            btn.style.display    = 'none';
            // Update score in HUD without full reload
            const hudScore = document.getElementById('hud-score');
            if (hudScore && data.points_awarded) {
              hudScore.textContent = parseInt(hudScore.textContent, 10) + data.points_awarded;
            }
            // Reload after 1.5s so stage states refresh
            setTimeout(function () { location.reload(); }, 1500);
          } else {
            feedback.textContent = data.message;
            feedback.className   = 'flag-feedback feedback-err';
            btn.disabled         = false;
            btn.textContent      = 'SUBMIT';
            input.focus();
          }
        })
        .catch(function () {
          feedback.textContent = 'Network error. Try again.';
          feedback.className   = 'flag-feedback feedback-err';
          btn.disabled         = false;
          btn.textContent      = 'SUBMIT';
        });
    });
  });

  // ── Hint buttons ────────────────────────────────────────────
  document.querySelectorAll('.hint-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const stageId = btn.dataset.stage;
      const hintNum = btn.dataset.hint;
      const display = document.getElementById('hint-' + stageId + '-' + hintNum);

      // Already shown – just toggle visibility
      if (display.classList.contains('visible')) {
        display.classList.remove('visible');
        btn.textContent = 'Hint ' + hintNum + ' (−' + (hintNum === '1' ? '5' : '10') + '%)';
        return;
      }

      const confirmed = confirm(
        'Using Hint ' + hintNum + ' will deduct ' +
        (hintNum === '1' ? '5%' : '10%') +
        ' from Stage ' + stageId + ' points. Continue?'
      );
      if (!confirmed) return;

      btn.disabled = true;

      fetch('/api/hint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Team-Token': teamToken,
        },
        body: JSON.stringify({ stage_id: parseInt(stageId, 10), hint_number: parseInt(hintNum, 10) }),
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.success) {
            display.textContent = '💡 ' + data.hint;
            display.classList.add('visible');
            btn.textContent = 'Hint ' + hintNum + ' (shown)';
          }
          btn.disabled = false;
        })
        .catch(function () {
          btn.disabled = false;
          alert('Failed to fetch hint. Try again.');
        });
    });
  });

})();
