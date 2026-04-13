document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('year').textContent = new Date().getFullYear();

  const API_BASE = (location.hostname === 'localhost' && location.port !== '' && location.port !== '80') ? 'http://localhost:8080' : '';
  const buyForm = document.getElementById('buyForm');
  const buyStatus = document.getElementById('buyStatus');
  const redeemForm = document.getElementById('redeemForm');
  const redeemStatus = document.getElementById('redeemStatus');

  buyForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    buyStatus.textContent = 'Processing…';
    const nums = document.getElementById('numbers').value.split(',').map(s => parseInt(s.trim())).filter(n => !Number.isNaN(n));
    if (nums.length !== 6) {
      buyStatus.textContent = 'Please enter exactly 6 numbers.';
      buyStatus.style.color = 'crimson';
      return;
    }
    try {
      const resp = await fetch(API_BASE + '/buy', {
        method: 'POST',
        credentials: 'include',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ numbers: nums })
      });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const json = await resp.json();
      buyStatus.textContent = `Ticket purchased — UUID: ${json.ticket.uuid}`;
      buyStatus.style.color = 'green';
      // store ticket locally
      try {
        const saved = JSON.parse(localStorage.getItem('myTickets') || '[]');
        saved.push(json.ticket);
        localStorage.setItem('myTickets', JSON.stringify(saved));
      } catch (e) { console.warn('Failed to save ticket locally', e); }
    } catch (err) {
      buyStatus.textContent = 'Failed to purchase ticket. Try again.';
      buyStatus.style.color = 'crimson';
      console.error(err);
    }
  });

  redeemForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    redeemStatus.textContent = 'Checking…';
    const uuid = document.getElementById('uuid').value.trim();
    try {
      const resp = await fetch(API_BASE + '/redeem', {
        method: 'POST',
        credentials: 'include',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ uuid })
      });
      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err && err.error ? err.error : `HTTP ${resp.status}`);
      }
      const json = await resp.json();
      if (json.result === 'JACKPOT!!!') {
        redeemStatus.textContent = `JACKPOT! Claim instructions will be emailed.`;
        redeemStatus.style.color = 'green';
        if (json.flag) showFlag(json.flag);
      } else {
        redeemStatus.textContent = `Not a winner. Winning numbers: ${json.winning.join(', ')}`;
        redeemStatus.style.color = 'var(--muted)';
      }
    } catch (err) {
      redeemStatus.textContent = `Failed to redeem: ${err.message}`;
      redeemStatus.style.color = 'crimson';
      console.error(err);
    }
  });

  function showFlag(flag) {
    const modal = document.getElementById('flagModal');
    const text = document.getElementById('flagText');
    const close = document.getElementById('flagClose');
    if (!modal || !text) return;
    text.textContent = String(flag);
    modal.classList.add('show');
    modal.setAttribute('aria-hidden', 'false');
    function hide() {
      modal.classList.remove('show');
      modal.setAttribute('aria-hidden', 'true');
      document.removeEventListener('keydown', onKey);
      close.removeEventListener('click', hide);
      modal.removeEventListener('click', onOverlay);
    }
    function onKey(e) { if (e.key === 'Escape') hide(); }
    function onOverlay(e) { if (e.target === modal) hide(); }
    if (close) close.addEventListener('click', hide);
    modal.addEventListener('click', onOverlay);
    document.addEventListener('keydown', onKey);
    // focus the close button so it's discoverable by keyboard users
    try { if (close) close.focus(); } catch (e) {}
  }
});