// Fonction Vercel : documents joints aux fiches candidat (CV, photo, diplômes).
//   POST /api/fichier : reçoit UN fichier (corps brut, 4 Mo au plus) et le range dans la base Neon (table « fichiers »).
//                       En-têtes : X-Nom-Fichier (nom encodé avec encodeURIComponent), X-Champ (ex. « Votre CV »).
//                       Réponse : { ok, id, cle } ; la page les transmet ensuite à /api/envoyer avec le reste de la fiche.
//   GET  /api/fichier?n=<id>&k=<clé> : téléchargement, avec le lien secret envoyé dans l'e-mail de l'école.
// Le type du fichier est reconnu à son contenu (PDF, Word, JPEG, PNG, WebP, HEIC), pas à son nom.
// Un fichier qui n'a été relié à aucune demande est effacé au bout de 24 h.

const crypto = require('crypto');
const { sql, preparer } = require('./_base');

const ORIGINES = [/^https:\/\/(www\.)?echoresta\.ci$/, /^https:\/\/echoresta[a-z0-9-]*\.vercel\.app$/, /^http:\/\/localhost(:\d+)?$/];
const MAX_OCTETS = 4 * 1024 * 1024;   // Vercel refuse les corps de plus de 4,5 Mo
const PAR_HEURE = 40;                 // fichiers au plus par visiteur et par heure
const DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
const EXTENSIONS = { 'application/pdf': 'pdf', 'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp', 'image/heic': 'heic',
                     'application/msword': 'doc', [DOCX]: 'docx' };

// Type reconnu à partir des premiers octets du fichier
function typeDe(b) {
  const debut = (...o) => o.every((x, i) => b[i] === x);
  if (b.slice(0, 5).toString('latin1') === '%PDF-') return 'application/pdf';
  if (debut(0xff, 0xd8, 0xff)) return 'image/jpeg';
  if (debut(0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a)) return 'image/png';
  if (b.slice(0, 4).toString('latin1') === 'RIFF' && b.slice(8, 12).toString('latin1') === 'WEBP') return 'image/webp';
  if (b.slice(4, 8).toString('latin1') === 'ftyp' && /^(heic|heix|hevc|heim|heis|mif1|msf1)$/.test(b.slice(8, 12).toString('latin1'))) return 'image/heic';
  if (debut(0xd0, 0xcf, 0x11, 0xe0, 0xa1, 0xb1, 0x1a, 0xe1)) return 'application/msword';
  if (debut(0x50, 0x4b, 0x03, 0x04) && b.includes('word/')) return DOCX;
  return '';
}

// Nom de fichier propre : sans dossier ni caractères de contrôle, avec la bonne extension
function nomPropre(brut, type) {
  let n = '';
  try { n = decodeURIComponent(String(brut || '')); } catch { n = String(brut || ''); }
  n = n.split(/[\\/]/).pop().replace(/[\u0000-\u001f\u007f"<>|*?:]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 120);
  const ext = EXTENSIONS[type];
  if (!n) n = 'document';
  if (!new RegExp(`\\.${ext === 'jpg' ? 'jpe?g' : ext}$`, 'i').test(n)) n = n.replace(/\.[a-z0-9]{1,5}$/i, '') + '.' + ext;
  return n.replace(/\s+(\.[a-z0-9]+)$/i, '$1');
}

// Empreinte du visiteur (adresse IP chiffrée, jamais gardée en clair) pour limiter les envois
const empreinte = req => {
  const ip = String(req.headers['x-forwarded-for'] || req.socket?.remoteAddress || '').split(',')[0].trim();
  return crypto.createHmac('sha256', process.env.MS_CLIENT_SECRET || process.env.DATABASE_URL || 'echoresta').update(ip).digest('hex').slice(0, 20);
};

async function lireCorps(req) {
  if (Buffer.isBuffer(req.body)) return req.body;
  const morceaux = [];
  let n = 0;
  for await (const c of req) {
    n += c.length;
    if (n > MAX_OCTETS) return null;
    morceaux.push(c);
  }
  return Buffer.concat(morceaux);
}

async function recevoir(req, res) {
  const origine = req.headers.origin;
  if (origine && !ORIGINES.some(o => o.test(origine))) return res.status(403).json({ ok: false });
  if (Number(req.headers['content-length'] || 0) > MAX_OCTETS) return res.status(413).json({ ok: false, erreur: 'taille' });
  const corps = await lireCorps(req);
  if (!corps || corps.length > MAX_OCTETS) return res.status(413).json({ ok: false, erreur: 'taille' });
  if (!corps.length) return res.status(400).json({ ok: false });
  const type = typeDe(corps);
  if (!type) return res.status(415).json({ ok: false, erreur: 'type' });
  const champ = (() => { try { return decodeURIComponent(String(req.headers['x-champ'] || '')); } catch { return ''; } })()
    .replace(/[\r\n]+/g, ' ').trim().slice(0, 120) || 'Document';
  const nom = nomPropre(req.headers['x-nom-fichier'], type);
  const qui = empreinte(req);

  await preparer();
  const [{ n }] = await sql`SELECT count(*)::int AS n FROM fichiers WHERE origine = ${qui} AND recu_le > now() - interval '1 hour'`;
  if (n >= PAR_HEURE) return res.status(429).json({ ok: false, erreur: 'limite' });
  const cle = crypto.randomBytes(16).toString('hex');
  const [ligne] = await sql`INSERT INTO fichiers (champ, nom, taille, type, cle, origine, contenu)
    VALUES (${champ}, ${nom}, ${corps.length}, ${type}, ${cle}, ${qui}, decode(${corps.toString('base64')}, 'base64')) RETURNING id`;
  // Ménage : fichiers envoyés mais jamais reliés à une demande (fiche abandonnée)
  await sql`DELETE FROM fichiers WHERE demande_id IS NULL AND recu_le < now() - interval '24 hours'`.catch(() => {});
  return res.status(200).json({ ok: true, id: String(ligne.id), cle, nom, taille: corps.length, type });
}

async function telecharger(req, res) {
  const q = req.query || Object.fromEntries(new URL(req.url, 'http://x').searchParams);
  const id = String(q.n || ''), cle = String(q.k || '');
  if (!/^\d{1,18}$/.test(id) || !/^[0-9a-f]{32}$/.test(cle)) return res.status(404).send('Document introuvable.');
  await preparer();
  const [f] = await sql`SELECT nom, type, encode(contenu, 'base64') AS contenu FROM fichiers
    WHERE id = ${id} AND cle = ${cle} AND demande_id IS NOT NULL`;
  if (!f) return res.status(404).send('Document introuvable.');
  const affichable = /^(application\/pdf|image\/(jpeg|png|webp))$/.test(f.type); // ouvert dans le navigateur ; Word est téléchargé
  const ascii = f.nom.replace(/[^\x20-\x7e]/g, '_').replace(/"/g, '');
  res.setHeader('Content-Type', f.type);
  res.setHeader('Content-Disposition', `${affichable ? 'inline' : 'attachment'}; filename="${ascii}"; filename*=UTF-8''${encodeURIComponent(f.nom)}`);
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Referrer-Policy', 'no-referrer');
  res.setHeader('Cache-Control', 'private, no-store');
  res.setHeader('X-Robots-Tag', 'noindex');
  return res.status(200).send(Buffer.from(f.contenu, 'base64'));
}

module.exports = async (req, res) => {
  if (!sql) return res.status(503).json({ ok: false, erreur: 'configuration' });
  try {
    if (req.method === 'POST') return await recevoir(req, res);
    if (req.method === 'GET' || req.method === 'HEAD') return await telecharger(req, res);
    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ ok: false });
  } catch (e) {
    console.error('Fichier :', e.message);
    return res.status(500).json({ ok: false });
  }
};

module.exports.typeDe = typeDe;
module.exports.nomPropre = nomPropre;
