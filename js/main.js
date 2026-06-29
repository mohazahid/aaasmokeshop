const STORAGE_KEY = 'aaa_age_confirmed';
const TTL_MS = 24 * 60 * 60 * 1000;

function isAgeConfirmed() {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (!stored) return false;
  try {
    const { timestamp } = JSON.parse(stored);
    return Date.now() - timestamp < TTL_MS;
  } catch {
    return false;
  }
}

function showSite() {
  const gate = document.getElementById('age-gate');
  const content = document.getElementById('site-content');
  gate.style.display = 'none';
  content.classList.add('visible');
  content.removeAttribute('aria-hidden');
  document.getElementById('main-content').focus({ preventScroll: true });
}

function initAgeGate() {
  if (isAgeConfirmed()) { showSite(); return; }

  document.getElementById('age-confirm').addEventListener('click', () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ timestamp: Date.now() }));
    showSite();
  });

  document.getElementById('age-deny').addEventListener('click', () => {
    window.location.href = 'https://www.google.com';
  });
}

document.addEventListener('DOMContentLoaded', initAgeGate);
