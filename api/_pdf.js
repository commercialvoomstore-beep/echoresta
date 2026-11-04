// Récapitulatif PDF d'une demande, joint aux e-mails (api/envoyer.js) pour garder une trace de la demande.
// Mise en page dans le style du site : Merriweather et Open Sans, bleu nuit et rouge, logo EchoResta.
// Fichier préfixé par « _ » : Vercel ne le publie pas comme une adresse.

const { PDFDocument, rgb, setCharacterSpacing } = require('pdf-lib');
const fontkit = require('@pdf-lib/fontkit');
const POLICES = require('./_polices');
const LOGO = require('./_logo');
const { TYPES, personne, dateLongue } = require('./_gabarits');

const hex = h => rgb(parseInt(h.slice(1, 3), 16) / 255, parseInt(h.slice(3, 5), 16) / 255, parseInt(h.slice(5, 7), 16) / 255);
const C = { navy: hex('#13296b'), red: hex('#c0152f'), ink: hex('#222222'), muted: hex('#6b6f7b'), line: hex('#e3e6ee'),
            soft: hex('#f3f5fa'), rose: hex('#f3b4bf'), clair: hex('#c9d2ec'), blanc: rgb(1, 1, 1) };
const L = 595.28, H = 841.89, M = 48, BAS = 64; // A4 en points, marges
const COL = 170; // largeur de la colonne des libellés

const MOTS = {
  fr: { doc: 'Récapitulatif de demande', no: 'n°', ecole: 'École de l’Hôtellerie & Restauration', recue: 'Reçue le', demandeur: 'Demandeur', autres: 'Autres informations', suite: 'suite',
        page: (i, n) => `Page ${i} / ${n}`, fichier: 'demande',
        note: (date, page) => `Document généré automatiquement le ${date} à partir du formulaire du site www.echoresta.ci${page}. Conservez-le comme trace de votre demande.` },
  en: { doc: 'Request summary', no: 'no.', ecole: 'School of Hospitality & Catering', recue: 'Received on', demandeur: 'Requester', autres: 'Other information', suite: 'continued',
        page: (i, n) => `Page ${i} of ${n}`, fichier: 'request',
        note: (date, page) => `Document generated automatically on ${date} from the form on www.echoresta.ci${page}. Keep it as a record of your request.` },
};
const PIED = ecole => `EchoResta — ${ecole} · Angré Star 14, Cocody, Abidjan · +225 07 68 84 20 38 · www.echoresta.ci`;

// Découpe un texte en lignes qui tiennent dans la largeur donnée (mots trop longs coupés, retours à la ligne gardés)
function couper(texte, police, taille, largeur) {
  const lignes = [];
  for (const para of String(texte).replace(/\t/g, ' ').split(/\r?\n/)) {
    let ligne = '';
    for (let mot of para.split(/ +/)) {
      while (police.widthOfTextAtSize(mot, taille) > largeur) { // mot plus long qu'une ligne (adresse e-mail, lien…)
        let n = mot.length;
        while (n > 1 && police.widthOfTextAtSize(mot.slice(0, n), taille) > largeur) n--;
        if (ligne) { lignes.push(ligne); ligne = ''; }
        lignes.push(mot.slice(0, n)); mot = mot.slice(n);
      }
      const essai = ligne ? ligne + ' ' + mot : mot;
      if (police.widthOfTextAtSize(essai, taille) <= largeur) ligne = essai;
      else { lignes.push(ligne); ligne = mot; }
    }
    lignes.push(ligne);
  }
  return lignes.length ? lignes : [''];
}

// Réponses regroupées par section, comme dans les e-mails
function groupes(d, autres) {
  const vus = new Set(), g = [];
  for (const [titre, cles] of d.sections) {
    const l = cles.map(k => d.champs.find(([c]) => c === k)).filter(Boolean);
    l.forEach(([k]) => vus.add(k));
    if (l.length) g.push([titre, l]);
  }
  const reste = d.champs.filter(([k]) => !vus.has(k));
  if (reste.length) g.push([g.length ? autres : '', reste]);
  return g;
}

const rectArrondi = (x, y, l, h, r) => // chemin SVG d'un rectangle à coins arrondis (y = haut du rectangle)
  `M ${x + r} ${y} H ${x + l - r} Q ${x + l} ${y} ${x + l} ${y + r} V ${y + h - r} Q ${x + l} ${y + h} ${x + l - r} ${y + h} H ${x + r} Q ${x} ${y + h} ${x} ${y + h - r} V ${y + r} Q ${x} ${y} ${x + r} ${y} Z`;

async function pdfDemande(d, langue = 'fr') {
  const lg = langue === 'en' ? 'en' : 'fr', m = MOTS[lg], t = (TYPES[d.formulaire] || TYPES.autre)[lg], p = personne(d);
  const doc = await PDFDocument.create();
  doc.registerFontkit(fontkit);
  const f = {};
  for (const [k, v] of Object.entries(POLICES)) f[k] = await doc.embedFont(Buffer.from(v, 'base64'), { subset: true });
  const logo = await doc.embedPng(Buffer.from(LOGO, 'base64'));
  const date = dateLongue(d.date, lg);
  const ref = d.id ? `${m.no} ${d.id}` : '';
  const titreDoc = `EchoResta – ${t.nom}${ref ? ' ' + ref : ''}`;
  doc.setTitle(titreDoc); doc.setAuthor('EchoResta'); doc.setSubject(d.sujet); doc.setCreator('www.echoresta.ci');
  doc.setProducer('EchoResta'); doc.setLanguage(lg === 'en' ? 'en-GB' : 'fr-FR'); doc.setCreationDate(d.date);

  let page, y;
  const texte = (s, x, yy, police, taille, couleur = C.ink, espacement = 0) => {
    if (espacement) page.pushOperators(setCharacterSpacing(espacement));
    page.drawText(s, { x, y: yy, size: taille, font: police, color: couleur });
    if (espacement) page.pushOperators(setCharacterSpacing(0));
  };
  const largeur = (s, police, taille, espacement = 0) => police.widthOfTextAtSize(s, taille) + espacement * Math.max(0, s.length - 1);
  const aDroite = (s, yy, police, taille, couleur, espacement = 0) => texte(s, L - M - largeur(s, police, taille, espacement), yy, police, taille, couleur, espacement);

  // ---------------------------------------------------------------- première page : en-tête, bandeau, demandeur
  page = doc.addPage([L, H]);
  page.drawRectangle({ x: 0, y: H - 5, width: L, height: 5, color: C.red });
  page.drawImage(logo, { x: M, y: H - 84, width: 50, height: 50 });
  texte('EchoResta', M + 62, H - 58, f.titre, 21, C.navy);
  texte(m.ecole, M + 62, H - 75, f.italique, 9.5, C.muted);
  aDroite(m.doc.toUpperCase(), H - 50, f.gras, 7.5, C.muted, 1.4);
  if (ref) aDroite(ref, H - 70, f.titre, 17, C.navy);
  aDroite(date, H - 84, f.texte, 8.5, C.muted);

  // Titre : l'objet de la demande (en français) ; en anglais, le type de demande et le nom de la personne
  const intitule = lg === 'fr' ? d.sujet.replace(/^site echoresta\s*[:–-]\s*/i, '') : t.nom + (p.nom ? ' – ' + p.nom : '');
  const lignesTitre = couper(intitule, f.titre, 15, L - 2 * M).slice(0, 3);
  const hBande = 58 + lignesTitre.length * 20;
  const haut = H - 110;
  page.drawRectangle({ x: 0, y: haut - hBande, width: L, height: hBande, color: C.navy });
  texte(t.nom.toUpperCase(), M, haut - 24, f.gras, 8, C.rose, 1.8);
  lignesTitre.forEach((l, i) => texte(l, M, haut - 46 - i * 20, f.titre, 15, C.blanc));
  texte(`${m.recue} ${date}`, M, haut - hBande + 14, f.texte, 8.5, C.clair);
  y = haut - hBande - 22;

  if (p.nom || p.tel || p.email) {
    const infos = [p.societe, p.tel, p.email].filter(Boolean);
    const hCarte = 52 + infos.length * 14;
    page.drawSvgPath(rectArrondi(0, 0, L - 2 * M, hCarte, 8), { x: M, y, color: C.soft });
    texte(m.demandeur.toUpperCase(), M + 16, y - 20, f.gras, 7.5, C.muted, 1.4);
    texte(p.nom || '—', M + 16, y - 38, f.titre, 13, C.ink);
    infos.forEach((s, i) => texte(s, M + 16, y - 56 - i * 14, f.texte, 9.5, i === 0 && p.societe ? C.ink : C.navy));
    y -= hCarte + 10;
  }

  // ---------------------------------------------------------------- pages suivantes : petit en-tête
  const nouvellePage = () => {
    page = doc.addPage([L, H]);
    page.drawRectangle({ x: 0, y: H - 5, width: L, height: 5, color: C.red });
    page.drawImage(logo, { x: M, y: H - 52, width: 26, height: 26 });
    texte('EchoResta', M + 34, H - 43, f.titre, 11, C.navy);
    aDroite(`${m.doc}${ref ? ' ' + ref : ''}`, H - 43, f.texte, 8.5, C.muted);
    page.drawLine({ start: { x: M, y: H - 62 }, end: { x: L - M, y: H - 62 }, thickness: 0.6, color: C.line });
    y = H - 84;
  };
  const place = h => { if (y - h < BAS) { nouvellePage(); return true; } return false; };

  // ---------------------------------------------------------------- réponses par section
  const xValeur = M + COL, lValeur = L - M - xValeur;
  const titreSection = s => {
    y -= 20;
    page.drawRectangle({ x: M, y: y - 2, width: 2.5, height: 11, color: C.red });
    texte(s.toUpperCase(), M + 10, y, f.gras, 8, C.red, 1.3);
    y -= 10;
  };
  for (const [titre, lignes] of groupes(d, m.autres)) {
    if (titre) { place(48); titreSection(titre); }
    for (const [k, v] of lignes) {
      const lv = couper(v, f.gras, 9.5, lValeur), lk = couper(k, f.texte, 9, COL - 14);
      const h = Math.max(lv.length * 13.5, lk.length * 12.5) + 14;
      if (place(h) && titre) titreSection(`${titre} (${m.suite})`); // section coupée : son titre est repris en haut de la page
      page.drawLine({ start: { x: M, y }, end: { x: L - M, y }, thickness: 0.5, color: C.line });
      lk.forEach((l, i) => texte(l, M, y - 17 - i * 12.5, f.texte, 9, C.muted));
      lv.forEach((l, i) => texte(l, xValeur, y - 17 - i * 13.5, f.gras, 9.5, C.ink));
      y -= h;
    }
  }

  // ---------------------------------------------------------------- note finale
  const note = couper(m.note(date, d.page || ''), f.italique, 8.5, L - 2 * M - 28);
  const hNote = 22 + note.length * 12;
  place(hNote + 24);
  y -= 18;
  page.drawSvgPath(rectArrondi(0, 0, L - 2 * M, hNote, 6), { x: M, y, borderColor: C.line, borderWidth: 0.8 });
  note.forEach((l, i) => texte(l, M + 14, y - 16 - i * 12, f.italique, 8.5, C.muted));

  // ---------------------------------------------------------------- pied de page et numéros de page
  const pages = doc.getPages();
  pages.forEach((pg, i) => {
    page = pg;
    pg.drawLine({ start: { x: M, y: 44 }, end: { x: L - M, y: 44 }, thickness: 0.6, color: C.line });
    texte(PIED(m.ecole), M, 30, f.texte, 7.2, C.muted);
    aDroite(m.page(i + 1, pages.length), 30, f.gras, 7.2, C.navy);
  });

  const nom = `EchoResta-${m.fichier}-${d.id || d.date.toISOString().slice(0, 16).replace(/[-:T]/g, '')}.pdf`;
  return { nom, contenu: Buffer.from(await doc.save()) };
}

module.exports = { pdfDemande };
