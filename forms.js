// Both forms write straight into Oathlight's own database, through two
// functions that can only add a row — never read one. No third party sees the
// address. The key below is the project's publishable key: it is meant to be
// public and grants nothing beyond those two functions.
const SUPABASE_URL = 'https://asnfwejpjprthfcjgsog.supabase.co';
const SUPABASE_KEY = '';

const CALLS = {
  signup: (form, data) => ['join_waitlist', { p_email: data.get('email'), p_locale: form.dataset.lang || 'en' }],
  delete: (form, data) => ['request_account_deletion', { p_email: data.get('email'), p_note: data.get('note') || null }],
};

async function send(name, body) {
  if (!SUPABASE_KEY) throw new Error('not configured');
  const response = await fetch(`${SUPABASE_URL}/rest/v1/rpc/${name}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', apikey: SUPABASE_KEY, Authorization: `Bearer ${SUPABASE_KEY}` },
    body: JSON.stringify(body),
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
}

document.querySelectorAll('form[data-signup], form[data-delete]').forEach((form) => {
  const kind = form.hasAttribute('data-delete') ? 'delete' : 'signup';

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('button');
    button.disabled = true;

    const note = document.createElement('p');
    note.className = 'form-done';
    note.setAttribute('role', 'status');

    try {
      await send(...CALLS[kind](form, new FormData(form)));
      note.textContent = form.dataset.done;
      form.replaceWith(note);
    } catch (error) {
      // Never claim a request was received when it was not.
      console.error(error);
      button.disabled = false;
      form.querySelector('.form-done')?.remove();
      note.textContent = form.dataset.failed;
      form.append(note);
    }
  });
});
