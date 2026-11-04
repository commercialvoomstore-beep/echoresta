// Mise en page des e-mails envoyés par api/envoyer.js :
//   - emailEcole     : la demande reçue dans la boîte de l'école (toujours en français) ;
//   - emailDemandeur : l'accusé de réception envoyé à la personne (en français ou en anglais).
// HTML pour e-mails : tableaux et styles en ligne, seuls compris par Outlook, Gmail et les messageries mobiles.
// Fichier préfixé par « _ » : Vercel ne le publie pas comme une adresse.

const C = { navy: '#13296b', red: '#c0152f', ink: '#222222', muted: '#6b6f7b', line: '#e3e6ee', soft: '#f3f5fa', green: '#15803d' };
const SERIF = "Georgia,'Times New Roman',serif";
const SANS = 'Arial,Helvetica,sans-serif';
const SITE = 'https://www.echoresta.ci';
const TEL = '+225 07 68 84 20 38';
const WA = 'https://wa.me/2250768842038';
const LOGO_CID = 'logo-echoresta';

// Type de formulaire : libellé, objet de l'accusé de réception et prochaines étapes pour la personne
const TYPES = {
  contact: {
    fr: { nom: 'Demande de contact', objet: 'Votre demande est bien reçue', recu: 'votre demande',
          etapes: ['Notre équipe étudie votre message et vous répond sous 48 h.',
                   'Pour une réponse plus rapide, appelez-nous ou écrivez-nous sur WhatsApp du lundi au vendredi, de 8h à 17h.'] },
    en: { nom: 'Contact request', objet: 'We have received your request', recu: 'your request',
          etapes: ['Our team is reviewing your message and will reply within 48 hours.',
                   'For a faster answer, call us or message us on WhatsApp Monday to Friday, 8 am to 5 pm.'] },
  },
  'rendez-vous': {
    fr: { nom: 'Demande de rendez-vous', objet: 'Votre demande de rendez-vous est bien reçue', recu: 'votre demande de rendez-vous',
          etapes: ['Nous vous confirmons le rendez-vous par e-mail, téléphone ou WhatsApp dans les meilleurs délais.',
                   'Adresse : Angré Star 14, Cocody, Abidjan (code de localisation Google : 92JH+FW).'] },
    en: { nom: 'Appointment request', objet: 'We have received your appointment request', recu: 'your appointment request',
          etapes: ['We will confirm your appointment by email, phone or WhatsApp as soon as possible.',
                   'Address: Angré Star 14, Cocody, Abidjan (Google location code: 92JH+FW).'] },
  },
  inscription: {
    fr: { nom: 'Inscription à une formation', objet: 'Votre inscription est bien reçue', recu: 'votre fiche d’inscription',
          etapes: ['Notre équipe étudie votre fiche et vous appelle pour fixer votre entretien d’inscription.',
                   'Préparez les pièces du dossier : 2 photos d’identité récentes, 1 copie de la pièce d’identité et 1 CV.'] },
    en: { nom: 'Course enrolment', objet: 'We have received your enrolment', recu: 'your enrolment form',
          etapes: ['Our team is reviewing your form and will call you to arrange your enrolment interview.',
                   'Prepare the documents for your file: 2 recent passport photos, 1 copy of your ID document and 1 CV.'] },
  },
  'besoin de personnel': {
    fr: { nom: 'Besoin de personnel', objet: 'Votre fiche de besoin est bien reçue', recu: 'votre fiche de besoin de personnel',
          etapes: ['Notre équipe étudie votre besoin et sélectionne des profils formés aux métiers de l’hôtellerie et de la restauration.',
                   'Nous vous recontactons rapidement avec des candidats adaptés à votre établissement.'] },
    en: { nom: 'Staffing request', objet: 'We have received your staffing request', recu: 'your staffing request',
          etapes: ['Our team is reviewing your needs and selecting profiles trained in hotel and restaurant professions.',
                   'We will get back to you quickly with candidates suited to your establishment.'] },
  },
  candidature: {
    fr: { nom: 'Candidature emploi', objet: 'Votre candidature est bien reçue', recu: 'votre candidature',
          etapes: ['Notre équipe étudie votre candidature et vos documents.',
                   'Nous vous mettons ensuite en relation avec des hôtels et des restaurants qui recrutent.'],
          sansDocuments: `Dernière étape : envoyez votre CV, votre photo et vos diplômes sur WhatsApp au ${TEL}.` },
    en: { nom: 'Job application', objet: 'We have received your application', recu: 'your application',
          etapes: ['Our team is reviewing your application and your documents.',
                   'We will then put you in touch with hotels and restaurants that are hiring.'],
          sansDocuments: `Last step: send your CV, photo and diplomas on WhatsApp to ${TEL}.` },
  },
  autre: {
    fr: { nom: 'Demande', objet: 'Votre demande est bien reçue', recu: 'votre demande', etapes: ['Notre équipe étudie votre demande et vous recontacte rapidement.'] },
    en: { nom: 'Request', objet: 'We have received your request', recu: 'your request', etapes: ['Our team is reviewing your request and will get back to you quickly.'] },
  },
};

const MOTS = {
  fr: { merci: 'Merci', bienRecu: 'Nous avons bien reçu', suite: 'La suite', reference: 'Référence de votre demande', le: 'le',
        recap: 'Récapitulatif de votre demande', autres: 'Autres informations', question: 'Une question ?',
        horaires: 'Du lundi au vendredi, de 8h à 17h', adresse: 'Angré Star 14, Cocody, Abidjan', wa: 'Écrire sur WhatsApp',
        appeler: 'Appeler l’école', site: 'Voir le site', envoiDocs: 'Envoyer mes documents sur WhatsApp',
        pdf: 'Le récapitulatif de votre demande est joint à cet e-mail : conservez-le.',
        documents: 'Vos documents', documentsRecus: n => `${n} document${n > 1 ? 's' : ''} bien reçu${n > 1 ? 's' : ''} avec votre fiche :`,
        ecole: 'École de l’Hôtellerie &amp; Restauration',
        pied: 'Vous recevez cet e-mail car vous avez rempli un formulaire sur www.echoresta.ci. Si ce n’est pas vous, ignorez simplement ce message.' },
  en: { merci: 'Thank you', bienRecu: 'We have received', suite: 'What happens next', reference: 'Your request reference', le: 'on',
        recap: 'Summary of your request', autres: 'Other information', question: 'Any questions?',
        horaires: 'Monday to Friday, 8 am to 5 pm', adresse: 'Angré Star 14, Cocody, Abidjan', wa: 'Message us on WhatsApp',
        appeler: 'Call the school', site: 'Visit the website', envoiDocs: 'Send my documents on WhatsApp',
        pdf: 'Your request summary is attached to this email: keep it for your records.',
        documents: 'Your documents', documentsRecus: n => `${n} document${n > 1 ? 's' : ''} received with your form:`,
        ecole: 'School of Hospitality &amp; Catering',
        pied: 'You are receiving this email because you filled in a form on www.echoresta.ci. If this was not you, simply ignore this message.' },
};

const e = t => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const court = (t, n) => (t.length > n ? t.slice(0, n - 1).trimEnd() + '…' : t);

// ------------------------------------------------------------------ Informations sur la personne, tirées des réponses
const premier = (champs, cles) => { for (const k of cles) { const v = champs.get(k); if (v) return v; } return ''; };
function personne(d) {
  const ch = new Map(d.champs);
  const complet = premier(ch, ['Nom et prénom', 'Full name']);
  const prenom = premier(ch, ['Prénoms', 'Prénom(s)', 'First names', 'First name(s)']);
  const nomFamille = premier(ch, ['Nom', 'Last name']);
  const nom = complet || [prenom, nomFamille].filter(Boolean).join(' ');
  const tel = d.champs.find(([k, v]) => /t[ée]l[ée]phone|phone|whatsapp/i.test(k) && /\d{6,}/.test(v.replace(/\D/g, '')));
  return {
    nom, prenom: prenom || complet.split(' ')[0] || '',
    societe: premier(ch, ['Établissement ou société', 'Establishment or company']),
    tel: tel ? tel[1] : '', email: d.repondreA,
  };
}
const lienWhatsApp = tel => (/^\+/.test(tel.trim()) ? 'https://wa.me/' + tel.replace(/\D/g, '') : '');
const lienTel = tel => 'tel:' + tel.replace(/[^\d+]/g, '');

// ------------------------------------------------------------------ Briques de mise en page
const bouton = (texte, lien, fond = C.red, petit = false) =>
  `<table role="presentation" cellspacing="0" cellpadding="0" border="0" style="display:inline-table;margin:${petit ? '0' : '0 8px 8px 0'}"><tr>` +
  `<td bgcolor="${fond}" style="border-radius:6px"><a href="${e(lien)}" style="display:inline-block;padding:${petit ? '8px 14px' : '11px 18px'};font:bold ${petit ? 13 : 14}px ${SANS};color:#ffffff;text-decoration:none;border-radius:6px;white-space:nowrap">${texte}</a></td></tr></table>`;

// Taille d'un fichier lisible : « 240 Ko », « 1,2 Mo » (« 240 KB », « 1.2 MB » en anglais)
const tailleLisible = (n, langue = 'fr') => {
  const [ko, mo] = langue === 'en' ? ['KB', 'MB'] : ['Ko', 'Mo'];
  const t = n < 1024 * 1024 ? `${Math.max(1, Math.round(n / 1024))} ${ko}` : `${(n / 1024 / 1024).toFixed(1)} ${mo}`;
  return langue === 'en' ? t : t.replace('.', ',');
};
const titreSection = (texte, marge = '26px 0 8px') =>
  `<div style="font:bold 11px ${SANS};letter-spacing:1.5px;text-transform:uppercase;color:${C.red};border-left:3px solid ${C.red};padding-left:10px;margin:${marge}">${texte}</div>`;

function entete(badge, ecole) {
  return `<tr><td style="padding:22px 28px;border-bottom:1px solid ${C.line}">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"><tr>
    <td width="64" valign="middle"><img src="cid:${LOGO_CID}" width="56" height="56" alt="EchoResta" style="display:block;border:0"></td>
    <td valign="middle" style="padding-left:12px">
      <div style="font:bold 22px ${SERIF};color:${C.navy};line-height:1.1">EchoResta</div>
      <div style="font:italic 13px ${SERIF};color:${C.muted};margin-top:3px">${ecole}</div>
    </td>
    ${badge ? `<td align="right" valign="middle"><span style="display:inline-block;background:${C.soft};color:${C.navy};font:bold 11px ${SANS};letter-spacing:1px;text-transform:uppercase;padding:7px 10px;border-radius:20px">${badge}</span></td>` : ''}
  </tr></table></td></tr>`;
}

function bandeau(surtitre, titre, infos) {
  return `<tr><td bgcolor="${C.navy}" style="background:${C.navy};padding:26px 28px">
  <div style="font:bold 11px ${SANS};letter-spacing:2px;text-transform:uppercase;color:#f3b4bf">${surtitre}</div>
  <div style="font:bold 22px ${SERIF};color:#ffffff;line-height:1.3;margin-top:8px">${titre}</div>
  ${infos ? `<div style="font:13px ${SANS};color:#c9d2ec;margin-top:10px">${infos}</div>` : ''}
</td></tr>`;
}

// Réponses regroupées par section (sections envoyées par la page ; le reste dans « Autres informations »)
function tableaux(d, mots, maxValeur) {
  const vus = new Set(), groupes = [];
  for (const [titre, cles] of d.sections) {
    const lignes = cles.map(k => d.champs.find(([c]) => c === k)).filter(Boolean);
    lignes.forEach(([k]) => vus.add(k));
    if (lignes.length) groupes.push([titre, lignes]);
  }
  const reste = d.champs.filter(([k]) => !vus.has(k));
  if (reste.length) groupes.push([groupes.length ? mots.autres : '', reste]);
  return groupes.map(([titre, lignes]) => `
  ${titre ? titreSection(e(titre)) : ''}
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-collapse:collapse">
  ${lignes.map(([k, v]) => `<tr>
    <td width="38%" valign="top" style="padding:10px 12px 10px 0;border-top:1px solid ${C.line};font:13px ${SANS};color:${C.muted}">${e(k)}</td>
    <td valign="top" style="padding:10px 0;border-top:1px solid ${C.line};font:bold 14px ${SANS};color:${C.ink};line-height:1.5">${e(court(v, maxValeur)).replace(/\n/g, '<br>')}</td>
  </tr>`).join('')}
  </table>`).join('');
}

function page(contenu, preentete) {
  return `<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EchoResta</title></head>
<body style="margin:0;padding:0;background:${C.soft}">
<div style="display:none;max-height:0;overflow:hidden;opacity:0">${e(preentete)}</div>
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="${C.soft}" style="background:${C.soft}"><tr><td align="center" style="padding:28px 12px">
<table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff" style="width:100%;max-width:600px;background:#ffffff;border-top:4px solid ${C.red};border-radius:8px">
${contenu}
</table>
</td></tr></table></body></html>`;
}

const dateLongue = (date, langue) => new Intl.DateTimeFormat(langue === 'en' ? 'en-GB' : 'fr-FR',
  { timeZone: 'Africa/Abidjan', dateStyle: 'full', timeStyle: 'short' }).format(date);

// ------------------------------------------------------------------ E-mail reçu par l'école
function emailEcole(d) {
  const t = (TYPES[d.formulaire] || TYPES.autre).fr, p = personne(d);
  const infos = [`Reçue le ${e(dateLongue(d.date, 'fr'))}`, d.id ? `demande n° ${e(d.id)}` : '',
                 d.langue === 'en' ? 'formulaire rempli en anglais' : ''].filter(Boolean).join(' · ');
  const titre = e(d.sujet.replace(/^site echoresta\s*[:–-]\s*/i, ''));
  const boutons = [
    p.email ? bouton('Répondre par e-mail', `mailto:${p.email}?subject=${encodeURIComponent('EchoResta – ' + d.sujet.replace(/^site echoresta\s*[:–-]\s*/i, ''))}`) : '',
    lienWhatsApp(p.tel) ? bouton('WhatsApp', lienWhatsApp(p.tel), C.green) : '',
    p.tel ? bouton('Appeler', lienTel(p.tel), C.navy) : '',
  ].join('');
  const demandeur = `<tr><td style="padding:24px 28px 4px">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="${C.soft}" style="background:${C.soft};border-radius:8px"><tr><td style="padding:18px 20px">
    <div style="font:bold 11px ${SANS};letter-spacing:1.5px;text-transform:uppercase;color:${C.muted}">Demandeur</div>
    <div style="font:bold 19px ${SERIF};color:${C.ink};margin-top:6px">${e(p.nom || 'Non précisé')}</div>
    ${p.societe ? `<div style="font:14px ${SANS};color:${C.ink};margin-top:2px">${e(p.societe)}</div>` : ''}
    <div style="font:14px ${SANS};color:${C.muted};margin-top:8px;line-height:1.6">
      ${p.tel ? `Téléphone : <a href="${e(lienTel(p.tel))}" style="color:${C.navy};font-weight:bold;text-decoration:none">${e(p.tel)}</a><br>` : ''}
      ${p.email ? `E-mail : <a href="mailto:${e(p.email)}" style="color:${C.navy};font-weight:bold;text-decoration:none">${e(p.email)}</a>` : ''}
    </div>
    ${boutons ? `<div style="margin-top:14px">${boutons}</div>` : ''}
  </td></tr></table></td></tr>`;
  const docs = d.documents || [];
  const documents = docs.length ? `<tr><td style="padding:20px 28px 0">
  ${titreSection(`${d.formulaire === 'candidature' ? 'Documents du candidat' : 'Documents joints'} (${docs.length})`, '0 0 8px')}
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-collapse:collapse">
  ${docs.map(f => `<tr>
    <td valign="middle" style="padding:11px 12px 11px 0;border-top:1px solid ${C.line}">
      <div style="font:13px ${SANS};color:${C.muted}">${e(f.champ)}</div>
      <div style="font:bold 14px ${SANS};color:${C.ink};margin-top:2px;word-break:break-all">${e(f.nom)}</div>
      <div style="font:12px ${SANS};color:${f.joint ? C.green : C.muted};margin-top:2px">${tailleLisible(f.taille)} · ${f.joint ? 'joint à cet e-mail' : 'trop volumineux pour être joint : utilisez le lien'}</div>
    </td>
    <td align="right" valign="middle" width="96" style="padding:11px 0;border-top:1px solid ${C.line}">${bouton('Ouvrir', f.lien, C.navy, true)}</td>
  </tr>`).join('')}
  </table>
  <div style="font:12px ${SANS};color:${C.muted};line-height:1.5;margin-top:8px">Les liens « Ouvrir » restent valables : ils ouvrent le document enregistré dans la base. Ne les transmettez qu’à des personnes de confiance.</div>
</td></tr>` : d.formulaire === 'candidature' ? `<tr><td style="padding:20px 28px 0">
  <div style="background:#fff7e6;border:1px solid #f3d38b;border-radius:8px;padding:12px 16px;font:13px ${SANS};color:#7a4b00;line-height:1.5">
    <b>Aucun document reçu avec cette fiche.</b> Le candidat a été invité à envoyer son CV, sa photo et ses diplômes sur WhatsApp.</div>
</td></tr>` : '';
  const html = page(`${entete('Nouvelle demande', MOTS.fr.ecole)}
${bandeau(t.nom, titre, infos)}
${demandeur}
${documents}
<tr><td style="padding:4px 28px 8px">${tableaux(d, MOTS.fr, 5000)}</td></tr>
<tr><td style="padding:22px 28px 26px;border-top:1px solid ${C.line};font:12px ${SANS};color:${C.muted};line-height:1.6">
  ${d.consentement ? `Consentement donné par la personne (case cochée) : « ${e(d.consentement)} »<br>` : ''}
  ${d.pdf && d.pdf.fr ? `Récapitulatif PDF joint : <b style="color:${C.ink}">${e(d.pdf.fr)}</b>.<br>` : ''}
  ${p.email ? 'Le bouton « Répondre » de votre messagerie écrit directement à la personne.<br>' : ''}
  Envoyé automatiquement par le formulaire du site <a href="${SITE}${e(d.page || '/')}" style="color:${C.navy}">www.echoresta.ci${e(d.page || '')}</a>${d.id ? ` · enregistré dans la base Neon (table demandes, n° ${e(d.id)})` : ''}.
</td></tr>`, `${t.nom} · ${p.nom} · ${p.tel || p.email}`);
  return { sujet: /^site echoresta/i.test(d.sujet) ? d.sujet : 'Site EchoResta – ' + d.sujet, html };
}

// ------------------------------------------------------------------ Accusé de réception pour la personne
function emailDemandeur(d) {
  const L = d.langue === 'en' ? 'en' : 'fr', m = MOTS[L], t = (TYPES[d.formulaire] || TYPES.autre)[L], p = personne(d);
  const docs = d.documents || [];
  const sansDocs = d.formulaire === 'candidature' && !docs.length;
  const etapes = sansDocs ? [t.sansDocuments, t.etapes[1]] : [...t.etapes];
  const creneau = d.champs.find(([k]) => k === 'Rendez-vous' || k === 'Appointment');
  if (creneau) etapes.unshift((L === 'en' ? 'Requested slot: ' : 'Créneau demandé : ') + creneau[1] + '.');
  const ref = d.id ? `<tr><td style="padding:0 28px">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border:1px solid ${C.line};border-radius:8px"><tr>
    <td style="padding:14px 18px;font:13px ${SANS};color:${C.muted}">${m.reference}<br><span style="font:bold 20px ${SERIF};color:${C.navy}">n° ${e(d.id)}</span></td>
    <td align="right" style="padding:14px 18px;font:13px ${SANS};color:${C.muted}">${e(dateLongue(d.date, L))}</td>
  </tr>${d.pdf && d.pdf[L] ? `<tr><td colspan="2" style="padding:12px 18px;border-top:1px solid ${C.line};font:13px ${SANS};color:${C.ink}">
    <b style="color:${C.red}">PDF</b>&nbsp; ${m.pdf} <span style="color:${C.muted}">(${e(d.pdf[L])})</span></td></tr>` : ''}</table></td></tr>` : '';
  const html = page(`${entete('', m.ecole)}
${bandeau(e(t.nom), L === 'en' ? `${m.merci}${p.prenom ? ', ' + e(p.prenom) : ''}!` : `${m.merci}${p.prenom ? ' ' + e(p.prenom) : ''}&nbsp;!`, `${m.bienRecu} ${t.recu}.`)}
<tr><td style="padding:26px 28px 18px">
  <div style="font:bold 17px ${SERIF};color:${C.ink};margin-bottom:10px">${m.suite}</div>
  ${etapes.map(x => `<table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin:0 0 10px"><tr>
    <td valign="top" style="padding:1px 10px 0 0;font:bold 15px ${SANS};color:${C.green}">✓</td>
    <td style="font:15px ${SANS};color:${C.ink};line-height:1.55">${e(x)}</td></tr></table>`).join('')}
  ${sansDocs ? `<div style="margin-top:12px">${bouton(m.envoiDocs, WA, C.green)}</div>` : ''}
</td></tr>
${docs.length ? `<tr><td style="padding:0 28px 18px">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="${C.soft}" style="background:${C.soft};border-radius:8px"><tr><td style="padding:14px 18px">
    <div style="font:bold 15px ${SERIF};color:${C.ink}">${m.documents}</div>
    <div style="font:13px ${SANS};color:${C.muted};margin:4px 0 6px">${m.documentsRecus(docs.length)}</div>
    ${docs.map(f => `<div style="font:14px ${SANS};color:${C.ink};line-height:1.6;word-break:break-all"><span style="color:${C.green};font-weight:bold">✓</span>&nbsp; ${e(f.nom)} <span style="color:${C.muted}">(${tailleLisible(f.taille, L)})</span></div>`).join('')}
  </td></tr></table></td></tr>` : ''}
${ref}
<tr><td style="padding:10px 28px 6px">
  <div style="font:bold 17px ${SERIF};color:${C.ink};margin-top:14px">${m.recap}</div>
  ${tableaux(d, m, 400)}
</td></tr>
<tr><td style="padding:24px 28px">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="${C.soft}" style="background:${C.soft};border-radius:8px"><tr><td style="padding:18px 20px">
    <div style="font:bold 16px ${SERIF};color:${C.ink}">${m.question}</div>
    <div style="font:14px ${SANS};color:${C.muted};margin:6px 0 14px;line-height:1.6">${TEL} · ${m.horaires}<br>${m.adresse}</div>
    ${bouton(m.wa, WA, C.green)}${bouton(m.appeler, 'tel:+2250768842038', C.navy)}${bouton(m.site, L === 'en' ? SITE + '/en/' : SITE)}
  </td></tr></table>
</td></tr>
<tr><td style="padding:18px 28px 26px;border-top:1px solid ${C.line};font:12px ${SANS};color:${C.muted};line-height:1.6">
  <b style="color:${C.navy}">EchoResta</b> — ${m.ecole} · ${m.adresse} · <a href="${SITE}" style="color:${C.navy}">www.echoresta.ci</a><br>${m.pied}
</td></tr>`, `${m.bienRecu} ${t.recu}.`).replace('<html lang="fr">', `<html lang="${L}">`);
  return { sujet: 'EchoResta – ' + t.objet, html };
}

module.exports = { emailEcole, emailDemandeur, LOGO_CID, TYPES, personne, dateLongue, tailleLisible, SITE };
