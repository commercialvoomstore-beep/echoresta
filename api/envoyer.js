// Fonction Vercel : reçoit les formulaires du site,
//   1. les enregistre dans la base Neon Postgres (table « demandes » ; documents joints dans la table « fichiers »),
//   2. envoie la demande par e-mail dans la boîte Microsoft 365 de l'école (Microsoft Graph),
//      avec le récapitulatif PDF et les documents du candidat (joints s'ils tiennent dans l'e-mail, et toujours en lien),
//   3. envoie un accusé de réception à la personne, si elle a donné son adresse e-mail.
// Base : api/_base.js ; documents : api/fichier.js ; mise en page des e-mails : api/_gabarits.js ;
// logo intégré : api/_logo.js ; récapitulatif PDF : api/_pdf.js (français pour l'école, langue du formulaire pour la personne).
//
// Les secrets ne sont jamais dans le code : ils se règlent dans Vercel → Settings → Environment Variables.
//   MS_CLIENT_SECRET : la « Valeur » du secret client de l'application « Echoresta » (Microsoft Entra ID)
//   DATABASE_URL     : adresse de connexion Neon (ajoutée automatiquement quand Neon est relié au projet Vercel)
// Facultatif (valeurs par défaut ci-dessous) : MS_TENANT_ID, MS_CLIENT_ID, MAIL_FROM (boîte qui envoie), MAIL_TO (boîte qui reçoit).
// La demande est acceptée si elle a été enregistrée ou envoyée ; sinon la page propose WhatsApp (voir assets/main.js).

const { sql, preparer } = require('./_base');
const { emailEcole, emailDemandeur, LOGO_CID, personne, SITE } = require('./_gabarits');
const { pdfDemande } = require('./_pdf');
const LOGO = require('./_logo');

const TENANT = process.env.MS_TENANT_ID || 'ffe8f65f-6b4d-42cc-b8f8-b6a4febd98e4';
const CLIENT = process.env.MS_CLIENT_ID || 'af5fc564-d935-48aa-b512-d72830c631a0';
const DE = process.env.MAIL_FROM || 'contact@voomnetformation.ci';
const A = process.env.MAIL_TO || DE;

// Pages autorisées à utiliser la fonction (le site, ses aperçus Vercel, les essais en local)
const ORIGINES = [/^https:\/\/(www\.)?echoresta\.ci$/, /^https:\/\/echoresta[a-z0-9-]*\.vercel\.app$/, /^http:\/\/localhost(:\d+)?$/];
const MAX_CHAMPS = 80, MAX_CLE = 200, MAX_VALEUR = 5000, MAX_SUJET = 200, MAX_SECTIONS = 12, MAX_FICHIERS = 10, MAX_CONSENTEMENT = 500;
const ACCUSES_PAR_JOUR = 3; // accusés de réception au plus par adresse et par 24 h (évite d'utiliser le site pour écrire à quelqu'un en boucle)
// Microsoft refuse un message de plus de 4 Mo (pièces jointes encodées comprises) : les documents qui ne tiennent pas
// dans cette limite restent accessibles par leur lien de téléchargement, présent dans l'e-mail et dans le PDF.
const LIMITE_MESSAGE = 3.7 * 1024 * 1024;
const EMAIL = /^[^\s@<>"]+@[^\s@<>"]+\.[^\s@<>"]+$/;
const FORMULAIRES = { 'form-contact': 'contact', 'form-rdv': 'rendez-vous', 'form-inscription': 'inscription',
                      'form-client': 'besoin de personnel', 'form-candidat': 'candidature' };

// ------------------------------------------------------------------ Base de données Neon
async function enregistrer(d) {
  await preparer();
  const p = personne(d);
  const [ligne] = await sql`INSERT INTO demandes (formulaire, sujet, nom, telephone, email, societe, champs, sections, consentement, page, langue)
    VALUES (${d.formulaire}, ${d.sujet}, ${p.nom || null}, ${p.tel || null}, ${d.repondreA || null}, ${p.societe || null},
            ${JSON.stringify(Object.fromEntries(d.champs))}, ${d.sections.length ? JSON.stringify(d.sections) : null},
            ${d.consentement || null}, ${d.page || null}, ${d.langue})
    RETURNING id`;
  return String(ligne.id);
}

// Documents envoyés par la page avant la fiche (api/fichier.js) : rattachés à la demande, avec leur lien de téléchargement
async function lierFichiers(id, refs) {
  if (!refs.length) return [];
  const lignes = await sql`UPDATE fichiers f SET demande_id = ${id}, lien = ${SITE + '/api/fichier?n='} || f.id || '&k=' || f.cle
    FROM unnest(${refs.map(r => r.id)}::bigint[], ${refs.map(r => r.cle)}::text[]) AS x(id, cle)
    WHERE f.id = x.id AND f.cle = x.cle AND f.demande_id IS NULL
    RETURNING f.id, f.champ, f.nom, f.taille, f.type, f.lien`;
  const ordre = new Map(refs.map((r, i) => [r.id, i]));
  return lignes.map(l => ({ id: String(l.id), champ: l.champ, nom: l.nom, taille: Number(l.taille), type: l.type, lien: l.lien }))
    .sort((a, b) => ordre.get(a.id) - ordre.get(b.id));
}

async function contenus(ids) {
  if (!ids.length) return new Map();
  const l = await sql`SELECT id, encode(contenu, 'base64') AS b64 FROM fichiers WHERE id = ANY(${ids}::bigint[])`;
  return new Map(l.map(x => [String(x.id), x.b64]));
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

const pieceJointe = (nom, type, base64) => ({ '@odata.type': '#microsoft.graph.fileAttachment', name: nom, contentType: type, contentBytes: base64 });

// Envoi d'un message HTML, avec le logo joint « en ligne » (affiché dans le message, sans téléchargement)
// et les pièces jointes : récapitulatif PDF, documents du candidat
async function envoyer({ a, sujet, html, repondreA, pieces = [] }) {
  const message = {
    subject: sujet,
    body: { contentType: 'HTML', content: html },
    toRecipients: [{ emailAddress: { address: a } }],
    ...(repondreA ? { replyTo: [{ emailAddress: { address: repondreA } }] } : {}),
    attachments: [{ ...pieceJointe('logo-echoresta.png', 'image/png', LOGO), isInline: true, contentId: LOGO_CID }, ...pieces],
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
const taille64 = n => Math.ceil(n / 3) * 4;

// Sections envoyées par la page : [[titre, [libellés…]], …] ; tout ce qui est mal formé est ignoré
const lireSections = s => (Array.isArray(s) ? s : []).slice(0, MAX_SECTIONS)
  .filter(x => Array.isArray(x) && typeof x[0] === 'string' && Array.isArray(x[1]))
  .map(([t, cles]) => [uneLigne(t).slice(0, 120), cles.filter(k => typeof k === 'string').slice(0, MAX_CHAMPS)]);
// Documents envoyés par la page : [{ id, cle }, …]
const lireFichiers = f => (Array.isArray(f) ? f : []).slice(0, MAX_FICHIERS)
  .filter(x => x && /^\d{1,18}$/.test(String(x.id)) && /^[0-9a-f]{32}$/.test(String(x.cle)))
  .map(x => ({ id: String(x.id), cle: String(x.cle) }));

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
    consentement: typeof b.consentement === 'string' ? uneLigne(b.consentement).slice(0, MAX_CONSENTEMENT) : '',
    page: typeof b.page === 'string' ? uneLigne(b.page).slice(0, 200) : '',
    langue: b.langue === 'en' ? 'en' : 'fr',
    date: new Date(),
    documents: [],
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
    if (enregistre) {
      try { d.documents = await lierFichiers(d.id, lireFichiers(b.fichiers)); } catch (e) { console.error('Neon (documents) :', e.message); }
    }
  }
  if (microsoft) {
    // Photo du candidat, affichée sur le récapitulatif PDF
    const photo = d.documents.find(f => /photo/i.test(f.champ) && /^image\/(jpeg|png)$/.test(f.type) && f.taille <= 3 * 1024 * 1024);
    let b64 = new Map();
    if (photo) {
      try { b64 = await contenus([photo.id]); d.photo = { type: photo.type, contenu: Buffer.from(b64.get(photo.id), 'base64') }; }
      catch (e) { console.error('Neon (photo) :', e.message); }
    }

    // Récapitulatifs PDF : l'exemplaire de l'école, en français, avec les liens des documents ;
    // celui de la personne, dans la langue du formulaire, sans lien (il peut être transféré)
    const pdfs = {};
    try { pdfs.ecole = await pdfDemande(d, 'fr', { liens: true }); } catch (e) { console.error('PDF (école) :', e.message); }
    if (d.repondreA) {
      try { pdfs.personne = await pdfDemande(d, d.langue); } catch (e) { console.error('PDF (personne) :', e.message); }
    }
    d.pdf = { ...(pdfs.ecole ? { fr: pdfs.ecole.nom } : {}), ...(pdfs.personne ? { [d.langue]: pdfs.personne.nom } : {}) };

    // Documents joints à l'e-mail de l'école, dans l'ordre de la fiche, tant que le message reste sous la limite de Microsoft
    let place = LIMITE_MESSAGE - 200 * 1024 - taille64(Buffer.byteLength(LOGO, 'base64')) - (pdfs.ecole ? taille64(pdfs.ecole.contenu.length) : 0);
    for (const f of d.documents) {
      f.joint = taille64(f.taille) <= place;
      if (f.joint) place -= taille64(f.taille);
    }
    const aCharger = d.documents.filter(f => f.joint && !b64.has(f.id)).map(f => f.id);
    try { for (const [id, x] of await contenus(aCharger)) b64.set(id, x); } catch (e) { console.error('Neon (contenus) :', e.message); }
    d.documents.forEach(f => { f.joint = f.joint && b64.has(f.id); });
    const piecesEcole = [...(pdfs.ecole ? [pieceJointe(pdfs.ecole.nom, 'application/pdf', pdfs.ecole.contenu.toString('base64'))] : []),
                         ...d.documents.filter(f => f.joint).map(f => pieceJointe(f.nom, f.type, b64.get(f.id)))];
    try {
      const m = emailEcole(d);
      try {
        await envoyer({ a: A, sujet: m.sujet, html: m.html, repondreA: d.repondreA, pieces: piecesEcole });
      } catch (e) {
        if (!d.documents.some(f => f.joint)) throw e;
        // Message refusé avec les documents (taille…) : nouvel essai avec les seuls liens de téléchargement
        console.error('Microsoft Graph (école, avec documents) :', e.message);
        d.documents.forEach(f => { f.joint = false; });
        const m2 = emailEcole(d);
        await envoyer({ a: A, sujet: m2.sujet, html: m2.html, repondreA: d.repondreA, pieces: piecesEcole.slice(0, pdfs.ecole ? 1 : 0) });
      }
      envoye = true;
    } catch (e) { console.error('Microsoft Graph (école) :', e.message); d.erreur = e.message; }
    if (d.repondreA) {
      try {
        if (enregistre && await accusesRecents(d.repondreA) >= ACCUSES_PAR_JOUR) accuse = 'non : limite atteinte';
        else {
          const m = emailDemandeur(d);
          const pdf = pdfs.personne;
          await envoyer({ a: d.repondreA, sujet: m.sujet, html: m.html, pieces: pdf ? [pieceJointe(pdf.nom, 'application/pdf', pdf.contenu.toString('base64'))] : [] });
          accuse = 'envoyé';
        }
      } catch (e) { console.error('Microsoft Graph (accusé) :', e.message); accuse = 'échec : ' + e.message.slice(0, 200); }
    }
  }
  if (enregistre) {
    const statut = envoye ? 'envoyé' : (microsoft ? 'échec : ' + (d.erreur || '').slice(0, 200) : 'non configuré');
    const documents = d.documents.length ? JSON.stringify(d.documents.map(f => ({ champ: f.champ, nom: f.nom, taille: f.taille, lien: f.lien }))) : null;
    try { await sql`UPDATE demandes SET envoi_email = ${statut}, accuse_email = ${accuse}, documents = ${documents} WHERE id = ${d.id}`; }
    catch (e) { console.error('Neon :', e.message); }
  }
  // enregistre / envoye / pdf / documents : utiles pour le test automatique (.github/workflows/test-formulaires.yml)
  if (!enregistre && !envoye) return res.status(502).json({ ok: false, enregistre, envoye });
  return res.status(200).json({ ok: true, enregistre, envoye, accuse: accuse === 'envoyé', pdf: Boolean(d.pdf && d.pdf.fr),
                               documents: d.documents.length, ...(d.id ? { numero: d.id } : {}) });
};
