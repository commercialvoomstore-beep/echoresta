// Fonction Vercel : envoie les formulaires du site dans la boîte Microsoft 365 de l'école, via Microsoft Graph.
//
// Le secret n'est jamais dans le code : il se règle dans Vercel → Settings → Environment Variables.
//   MS_CLIENT_SECRET (obligatoire) : la « Valeur » du secret client de l'application « Echoresta » (Microsoft Entra ID)
//   MS_TENANT_ID, MS_CLIENT_ID     : identifiants de l'application (valeurs par défaut ci-dessous)
//   MAIL_FROM                      : boîte qui envoie le message (par défaut contact@voomnetformation.ci)
//   MAIL_TO                        : boîte qui le reçoit (par défaut la même)
// Le destinataire est fixé ici : la fonction ne peut pas servir à écrire à une autre adresse.
// Sans secret, ou si Microsoft refuse l'envoi, la page passe au service de secours (voir assets/main.js).

const TENANT = process.env.MS_TENANT_ID || 'ffe8f65f-6b4d-42cc-b8f8-b6a4febd98e4';
const CLIENT = process.env.MS_CLIENT_ID || 'af5fc564-d935-48aa-b512-d72830c631a0';
const DE = process.env.MAIL_FROM || 'contact@voomnetformation.ci';
const A = process.env.MAIL_TO || DE;

// Pages autorisées à utiliser la fonction (le site, ses aperçus Vercel, les essais en local)
const ORIGINES = [/^https:\/\/(www\.)?echoresta\.ci$/, /^https:\/\/echoresta[a-z0-9-]*\.vercel\.app$/, /^http:\/\/localhost(:\d+)?$/];
const MAX_CHAMPS = 80, MAX_CLE = 200, MAX_VALEUR = 5000, MAX_SUJET = 200;
const EMAIL = /^[^\s@<>"]+@[^\s@<>"]+\.[^\s@<>"]+$/;

let jeton = null; // jeton d'accès Microsoft, gardé jusqu'à son expiration

async function obtenirJeton() {
  if (jeton && jeton.expire > Date.now()) return jeton.valeur;
  const r = await fetch(`https://login.microsoftonline.com/${TENANT}/oauth2/v2.0/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: CLIENT, client_secret: process.env.MS_CLIENT_SECRET,
      scope: 'https://graph.microsoft.com/.default', grant_type: 'client_credentials',
    }),
  });
  const d = await r.json().catch(() => ({}));
  if (!r.ok || !d.access_token) throw new Error(`jeton refusé (${r.status}) ${d.error || ''} ${d.error_description || ''}`.trim());
  jeton = { valeur: d.access_token, expire: Date.now() + (Number(d.expires_in || 3600) - 300) * 1000 };
  return jeton.valeur;
}

const echapper = t => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const uneLigne = t => String(t).replace(/[\r\n]+/g, ' ').trim();

function corpsHtml(sujet, champs, page) {
  const lignes = champs.map(([k, v]) =>
    `<tr><th style="text-align:left;vertical-align:top;padding:8px 14px 8px 0;color:#13296b;white-space:nowrap">${echapper(k)}</th>` +
    `<td style="padding:8px 0;color:#1f2937">${echapper(v).replace(/\n/g, '<br>')}</td></tr>`).join('');
  return `<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.5">
<h2 style="color:#13296b;font-size:18px;margin:0 0 16px">${echapper(sujet)}</h2>
<table style="border-collapse:collapse">${lignes}</table>
<p style="color:#6b7280;font-size:13px;margin-top:24px">Message envoyé depuis le formulaire du site www.echoresta.ci${page ? ' (page ' + echapper(page) + ')' : ''}.
Répondez directement à ce message pour écrire à la personne.</p></div>`;
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false });
  }
  const origine = req.headers.origin;
  if (origine && !ORIGINES.some(o => o.test(origine))) return res.status(403).json({ ok: false });

  let d = req.body || {};
  if (typeof d === 'string') { try { d = JSON.parse(d); } catch { d = {}; } }
  if (d.botcheck) return res.status(200).json({ ok: true }); // case anti-robot cochée : rien n'est envoyé

  const champs = d.champs && typeof d.champs === 'object' && !Array.isArray(d.champs)
    ? Object.entries(d.champs).filter(([, v]) => typeof v === 'string' && v.trim()) : [];
  const sujet = uneLigne(d.sujet || 'Demande depuis le site');
  if (!champs.length || champs.length > MAX_CHAMPS || sujet.length > MAX_SUJET
      || champs.some(([k, v]) => k.length > MAX_CLE || v.length > MAX_VALEUR)) {
    return res.status(400).json({ ok: false });
  }
  if (!process.env.MS_CLIENT_SECRET) return res.status(503).json({ ok: false, erreur: 'configuration' });

  const repondreA = typeof d.replyto === 'string' && EMAIL.test(d.replyto.trim()) ? d.replyto.trim() : '';
  const page = typeof d.page === 'string' ? uneLigne(d.page).slice(0, 200) : '';
  const message = {
    subject: /^site echoresta/i.test(sujet) ? sujet : 'Site EchoResta – ' + sujet,
    body: { contentType: 'HTML', content: corpsHtml(sujet, champs, page) },
    toRecipients: [{ emailAddress: { address: A } }],
    ...(repondreA ? { replyTo: [{ emailAddress: { address: repondreA } }] } : {}),
  };
  try {
    const r = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(DE)}/sendMail`, {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + await obtenirJeton(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, saveToSentItems: false }),
    });
    if (r.status !== 202) {
      if (r.status === 401) jeton = null;
      throw new Error(`envoi refusé (${r.status}) ${(await r.text().catch(() => '')).slice(0, 300)}`);
    }
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error('Microsoft Graph :', e.message);
    return res.status(502).json({ ok: false });
  }
};
