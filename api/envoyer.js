// Fonction Vercel : reçoit les formulaires du site,
//   1. les enregistre dans la base Neon Postgres (table « demandes »),
//   2. les envoie par e-mail dans la boîte Microsoft 365 de l'école, via Microsoft Graph.
//
// Les secrets ne sont jamais dans le code : ils se règlent dans Vercel → Settings → Environment Variables.
//   MS_CLIENT_SECRET : la « Valeur » du secret client de l'application « Echoresta » (Microsoft Entra ID)
//   DATABASE_URL     : adresse de connexion Neon (ajoutée automatiquement quand Neon est relié au projet Vercel)
// Facultatif (valeurs par défaut ci-dessous) : MS_TENANT_ID, MS_CLIENT_ID, MAIL_FROM (boîte qui envoie), MAIL_TO (boîte qui reçoit).
// Le destinataire est fixé ici : la fonction ne peut pas servir à écrire à une autre adresse.
// La demande est acceptée si elle a été enregistrée ou envoyée ; sinon la page propose WhatsApp (voir assets/main.js).

const { neon } = require('@neondatabase/serverless');

const TENANT = process.env.MS_TENANT_ID || 'ffe8f65f-6b4d-42cc-b8f8-b6a4febd98e4';
const CLIENT = process.env.MS_CLIENT_ID || 'af5fc564-d935-48aa-b512-d72830c631a0';
const DE = process.env.MAIL_FROM || 'contact@voomnetformation.ci';
const A = process.env.MAIL_TO || DE;
const BASE = process.env.DATABASE_URL || process.env.POSTGRES_URL || '';

// Pages autorisées à utiliser la fonction (le site, ses aperçus Vercel, les essais en local)
const ORIGINES = [/^https:\/\/(www\.)?echoresta\.ci$/, /^https:\/\/echoresta[a-z0-9-]*\.vercel\.app$/, /^http:\/\/localhost(:\d+)?$/];
const MAX_CHAMPS = 80, MAX_CLE = 200, MAX_VALEUR = 5000, MAX_SUJET = 200;
const EMAIL = /^[^\s@<>"]+@[^\s@<>"]+\.[^\s@<>"]+$/;
const FORMULAIRES = { 'form-contact': 'contact', 'form-rdv': 'rendez-vous', 'form-inscription': 'inscription',
                      'form-client': 'besoin de personnel', 'form-candidat': 'candidature' };

// ------------------------------------------------------------------ Base de données Neon
const sql = BASE ? neon(BASE) : null;
let tablePrete = false;

async function enregistrer(d) {
  if (!tablePrete) {
    // Créée au premier envoi : rien à préparer à la main dans Neon
    await sql`CREATE TABLE IF NOT EXISTS demandes (
      id bigserial PRIMARY KEY,
      recue_le timestamptz NOT NULL DEFAULT now(),
      formulaire text NOT NULL,
      sujet text NOT NULL,
      champs json NOT NULL,
      email text,
      page text,
      langue text,
      envoi_email text)`;
    tablePrete = true;
  }
  const [ligne] = await sql`INSERT INTO demandes (formulaire, sujet, champs, email, page, langue)
    VALUES (${d.formulaire}, ${d.sujet}, ${JSON.stringify(Object.fromEntries(d.champs))}, ${d.repondreA || null}, ${d.page || null}, ${d.langue})
    RETURNING id`;
  return ligne.id;
}

// ------------------------------------------------------------------ E-mail Microsoft 365
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

function corpsHtml(d) {
  const lignes = d.champs.map(([k, v]) =>
    `<tr><th style="text-align:left;vertical-align:top;padding:8px 14px 8px 0;color:#13296b;white-space:nowrap">${echapper(k)}</th>` +
    `<td style="padding:8px 0;color:#1f2937">${echapper(v).replace(/\n/g, '<br>')}</td></tr>`).join('');
  return `<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.5">
<h2 style="color:#13296b;font-size:18px;margin:0 0 16px">${echapper(d.sujet)}</h2>
<table style="border-collapse:collapse">${lignes}</table>
<p style="color:#6b7280;font-size:13px;margin-top:24px">Message envoyé depuis le formulaire du site www.echoresta.ci${d.page ? ' (page ' + echapper(d.page) + ')' : ''}${d.id ? ', demande n° ' + echapper(d.id) : ''}.
Répondez directement à ce message pour écrire à la personne.</p></div>`;
}

async function envoyerEmail(d) {
  const message = {
    subject: /^site echoresta/i.test(d.sujet) ? d.sujet : 'Site EchoResta – ' + d.sujet,
    body: { contentType: 'HTML', content: corpsHtml(d) },
    toRecipients: [{ emailAddress: { address: A } }],
    ...(d.repondreA ? { replyTo: [{ emailAddress: { address: d.repondreA } }] } : {}),
  };
  const r = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(DE)}/sendMail`, {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + await obtenirJeton(), 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, saveToSentItems: false }),
  });
  if (r.status !== 202) {
    if (r.status === 401) jeton = null;
    throw new Error(`envoi refusé (${r.status}) ${(await r.text().catch(() => '')).slice(0, 300)}`);
  }
}

// ------------------------------------------------------------------ Réception d'un formulaire
module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false });
  }
  const origine = req.headers.origin;
  if (origine && !ORIGINES.some(o => o.test(origine))) return res.status(403).json({ ok: false });

  let b = req.body || {};
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch { b = {}; } }
  if (b.botcheck) return res.status(200).json({ ok: true }); // case anti-robot cochée : rien n'est enregistré ni envoyé

  const champs = b.champs && typeof b.champs === 'object' && !Array.isArray(b.champs)
    ? Object.entries(b.champs).filter(([, v]) => typeof v === 'string' && v.trim()) : [];
  const d = {
    champs,
    sujet: uneLigne(b.sujet || 'Demande depuis le site'),
    formulaire: FORMULAIRES[b.formulaire] || 'autre',
    repondreA: typeof b.replyto === 'string' && EMAIL.test(b.replyto.trim()) ? b.replyto.trim() : '',
    page: typeof b.page === 'string' ? uneLigne(b.page).slice(0, 200) : '',
    langue: b.langue === 'en' ? 'en' : 'fr',
  };
  if (!champs.length || champs.length > MAX_CHAMPS || d.sujet.length > MAX_SUJET
      || champs.some(([k, v]) => k.length > MAX_CLE || v.length > MAX_VALEUR)) {
    return res.status(400).json({ ok: false });
  }
  if (!sql && !process.env.MS_CLIENT_SECRET) return res.status(503).json({ ok: false, erreur: 'configuration' });

  let enregistre = false, envoye = false;
  if (sql) {
    try { d.id = await enregistrer(d); enregistre = true; } catch (e) { console.error('Neon :', e.message); }
  }
  if (process.env.MS_CLIENT_SECRET) {
    try { await envoyerEmail(d); envoye = true; } catch (e) { console.error('Microsoft Graph :', e.message); d.erreur = e.message; }
  }
  if (enregistre) {
    const statut = envoye ? 'envoyé' : (process.env.MS_CLIENT_SECRET ? 'échec : ' + (d.erreur || '').slice(0, 200) : 'non configuré');
    try { await sql`UPDATE demandes SET envoi_email = ${statut} WHERE id = ${d.id}`; } catch (e) { console.error('Neon :', e.message); }
  }
  // enregistre / envoye : utiles pour le test automatique (.github/workflows/test-formulaires.yml)
  if (!enregistre && !envoye) return res.status(502).json({ ok: false, enregistre, envoye });
  return res.status(200).json({ ok: true, enregistre, envoye });
};
