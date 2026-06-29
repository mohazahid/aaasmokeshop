const STORAGE_KEY = 'aaa_age_confirmed';
const TTL_MS = 24 * 60 * 60 * 1000;

function isBot() {
  const ua = navigator.userAgent || '';
  return /googlebot|bingbot|slurp|duckduckbot|baiduspider|yandexbot|facebot|ia_archiver/i.test(ua);
}

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
  if (isBot() || isAgeConfirmed()) { showSite(); return; }

  document.getElementById('age-confirm').addEventListener('click', () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ timestamp: Date.now() }));
    showSite();
  });

  document.getElementById('age-deny').addEventListener('click', () => {
    window.location.href = 'https://www.google.com';
  });
}

function initContactForm() {
  const form = document.getElementById('contact');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = form.querySelector('.form__submit');
    const result = document.getElementById('form-result');

    btn.disabled = true;
    btn.textContent = 'Sending…';
    result.className = 'form__result';
    result.textContent = '';

    try {
      const data = new FormData(form);
      const res = await fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        body: data,
      });
      const json = await res.json();

      if (json.success) {
        result.className = 'form__result success';
        result.textContent = 'Message sent! We\'ll get back to you soon.';
        form.reset();
      } else {
        throw new Error(json.message || 'Submission failed');
      }
    } catch (err) {
      result.className = 'form__result error';
      result.textContent = 'Something went wrong. Please try again.';
    } finally {
      btn.disabled = false;
      btn.textContent = 'Send Message';
    }
  });
}

function initFAQ() {
  document.querySelectorAll('.faq-q').forEach(q => {
    q.addEventListener('click', () => {
      const item = q.closest('.faq-item');
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
      if (!isOpen) item.classList.add('open');
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initAgeGate();
  initContactForm();
  initFAQ();
});
