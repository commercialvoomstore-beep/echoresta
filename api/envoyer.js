// Fonction Vercel : reçoit les formulaires du site,
//   1. les enregistre dans la base Neon Postgres (table « demandes »),
//   2. envoie la demande par e-mail dans la boîte Microsoft 365 de l'école (Microsoft Graph),
//   3. envoie un accusé de réception à la personne, si elle a donné son adresse e-mail.
// Mise en page des e-mails : api/_gabarits.js ; logo intégré : api/_logo.js ;
// récapitulatif PDF joint aux deux e-mails : api/_pdf.js (français pour l'école, langue du formulaire pour la personne).
//
// Les secrets ne sont jamais dans le code : ils se règlent dans Vercel → Settings → Environment Variables.
//   MS_CLIENT_SECRET : la « Valeur » du secret client de l'application « Echoresta » (Microsoft Entra ID)
//   DATABASE_URL     : adresse de connexion Neon (ajoutée automatiquement quand Neon est relié au projet Vercel)
// Facultatif (valeurs par défaut ci-dessous) : MS_TENANT_ID, MS_CLIENT_ID, MAIL_FROM (boîte qui envoie), MAIL_TO (boîte qui reçoit).
// La demande est acceptée si elle a été enregistrée ou envoyée ; sinon la page propose WhatsApp (voir assets/main.js).

const { neon } = require('@neondatabase/serverless');
const { emailEcole, emailDemandeur, LOGO_CID } = require('./_gabarits');
const { pdfDemande } = require('./_pdf');
const LOGO = require('./_logo');

const TENANT = process.env.MS_TENANT_ID || 'ffe8f65f-6b4d-42cc-b8f8-b6a4febd98e4';
const CLIENT = process.env.MS_CLIENT_ID || 'af5fc564-d935-48aa-b512-d72830c631a0';
const DE = process.env.MAIL_FROM || 'contact@voomnetformation.ci';
const A = process.env.MAIL_TO || DE;
const BASE = process.env.DATABASE_URL || process.env.POSTGRES_URL || '';

// Pages autorisées à utiliser la fonction (le site, ses aperçus Vercel, les essais en local)
const ORIGINES = [/^https:\/\/(www\.)?echoresta\.ci$/, /^https:\/\/echoresta[a-z0-9-]*\.vercel\.app$/, /^http:\/\/localhost(:\d+)?$/];
const MAX_CHAMPS = 80, MAX_CLE = 200, MAX_VALEUR = 5000, MAX_SUJET = 200, MAX_SECTIONS = 12;
const ACCUSES_PAR_JOUR = 3; // accusés de réception au plus par adresse et par 24 h (évite d'utiliser le site pour écrire à quelqu'un en boucle)
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
      envoi_email text,
      accuse_email text)`;
    await sql`ALTER TABLE demandes ADD COLUMN IF NOT EXISTS accuse_email text`;
    tablePrete = true;
  }
  const [ligne] = await sql`INSERT INTO demandes (formulaire, sujet, champs, email, page, langue)
    VALUES (${d.formulaire}, ${d.sujet}, ${JSON.stringify(Object.fromEntries(d.champs))}, ${d.repondreA || null}, ${d.page || null}, ${d.langue})
    RETURNING id`;
  return ligne.id;
}

async function accusesRecents(email) {
  const [l] = await sql`SELECT count(*)::int AS n FROM demandes
    WHERE lower(email) = lower(${email}) AND accuse_email = 'envoyé' AND recue_le > now() - interval '24 hours'`;
  return l.n;
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

// Envoi d'un message HTML, avec le logo joint « en ligne » (affiché dans le message, sans téléchargement)
// et, s'il a pu être créé, le récapitulatif PDF en pièce jointe
async function envoyer({ a, sujet, html, repondreA, pdf }) {
  const message = {
    subject: sujet,
    body: { contentType: 'HTML', content: html },
    toRecipients: [{ emailAddress: { address: a } }],
    ...(repondreA ? { replyTo: [{ emailAddress: { address: repondreA } }] } : {}),
    attachments: [{ '@odata.type': '#microsoft.graph.fileAttachment', name: 'logo-echoresta.png', contentType: 'image/png',
                    contentBytes: LOGO, isInline: true, contentId: LOGO_CID },
                  ...(pdf ? [{ '@odata.type': '#microsoft.graph.fileAttachment', name: pdf.nom, contentType: 'application/pdf',
                               contentBytes: pdf.contenu.toString('base64') }] : [])],
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

const uneLigne = t => String(t).replace(/[\r\n]+/g, ' ').trim();

// Sections envoyées par la page : [[titre, [libellés…]], …] ; tout ce qui est mal formé est ignoré
const lireSections = s => (Array.isArray(s) ? s : []).slice(0, MAX_SECTIONS)
  .filter(x => Array.isArray(x) && typeof x[0] === 'string' && Array.isArray(x[1]))
  .map(([t, cles]) => [uneLigne(t).slice(0, 120), cles.filter(k => typeof k === 'string').slice(0, MAX_CHAMPS)]);

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
    sections: lireSections(b.sections),
    sujet: uneLigne(b.sujet || 'Demande depuis le site'),
    formulaire: FORMULAIRES[b.formulaire] || 'autre',
    repondreA: typeof b.replyto === 'string' && EMAIL.test(b.replyto.trim()) ? b.replyto.trim() : '',
    page: typeof b.page === 'string' ? uneLigne(b.page).slice(0, 200) : '',
    langue: b.langue === 'en' ? 'en' : 'fr',
    date: new Date(),
  };
  if (!champs.length || champs.length > MAX_CHAMPS || d.sujet.length > MAX_SUJET
      || champs.some(([k, v]) => k.length > MAX_CLE || v.length > MAX_VALEUR)) {
    return res.status(400).json({ ok: false });
  }
  const microsoft = Boolean(process.env.MS_CLIENT_SECRET);
  if (!sql && !microsoft) return res.status(503).json({ ok: false, erreur: 'configuration' });

  let enregistre = false, envoye = false, accuse = 'sans e-mail';
  if (sql) {
    try { d.id = await enregistrer(d); enregistre = true; } catch (e) { console.error('Neon :', e.message); }
  }
  if (microsoft) {
    // Récapitulatifs PDF : en français pour l'école, dans la langue du formulaire pour la personne
    const pdfs = {};
    for (const lg of new Set(['fr', d.repondreA ? d.langue : 'fr'])) {
      try { pdfs[lg] = await pdfDemande(d, lg); } catch (e) { console.error('PDF :', e.message); }
    }
    d.pdf = Object.fromEntries(Object.entries(pdfs).map(([lg, x]) => [lg, x.nom]));
    try {
      const m = emailEcole(d);
      await envoyer({ a: A, sujet: m.sujet, html: m.html, repondreA: d.repondreA, pdf: pdfs.fr });
      envoye = true;
    } catch (e) { console.error('Microsoft Graph (école) :', e.message); d.erreur = e.message; }
    if (d.repondreA) {
      try {
        if (enregistre && await accusesRecents(d.repondreA) >= ACCUSES_PAR_JOUR) accuse = 'non : limite atteinte';
        else {
          const m = emailDemandeur(d);
          await envoyer({ a: d.repondreA, sujet: m.sujet, html: m.html, pdf: pdfs[d.langue] });
          accuse = 'envoyé';
        }
      } catch (e) { console.error('Microsoft Graph (accusé) :', e.message); accuse = 'échec : ' + e.message.slice(0, 200); }
    }
  }
  if (enregistre) {
    const statut = envoye ? 'envoyé' : (microsoft ? 'échec : ' + (d.erreur || '').slice(0, 200) : 'non configuré');
    try { await sql`UPDATE demandes SET envoi_email = ${statut}, accuse_email = ${accuse} WHERE id = ${d.id}`; }
    catch (e) { console.error('Neon :', e.message); }
  }
  // enregistre / envoye / pdf : utiles pour le test automatique (.github/workflows/test-formulaires.yml)
  if (!enregistre && !envoye) return res.status(502).json({ ok: false, enregistre, envoye });
  return res.status(200).json({ ok: true, enregistre, envoye, accuse: accuse === 'envoyé', pdf: Boolean(d.pdf && d.pdf.fr),
                               ...(d.id ? { numero: String(d.id) } : {}) });
};
