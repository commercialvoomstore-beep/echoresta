"""Espace recrutement : page d'aiguillage, fiche de besoin (employeurs) et fiche candidat (professionnels).

Les pages utilisent Tailwind CSS (compilé dans assets/recrutement.css, voir _build/tailwind.config.js ;
préfixe « tw- », sans remise à zéro des styles du site)
et sont envoyés par e-mail via Web3Forms, comme les autres formulaires du site.
"""

TAILWIND = '<link rel="stylesheet" href="assets/recrutement.css">'

# ---------------------------------------------------------------- Petits composants communs
def classes_champ(accent):
    ring = 'focus:tw-border-nuit-700 focus:tw-ring-nuit-700/10' if accent == 'nuit' else 'focus:tw-border-amber-600 focus:tw-ring-amber-500/15'
    return (f'tw-w-full tw-rounded-lg tw-border tw-border-solid tw-border-slate-300 tw-bg-white tw-px-4 tw-py-3 tw-text-[15px] '
            f'tw-text-slate-900 placeholder:tw-text-slate-400 focus:tw-outline-none focus:tw-ring-4 {ring} tw-transition')


LABEL = 'tw-mb-2 tw-block tw-text-sm tw-font-semibold tw-text-slate-800'


def puce(nom, valeur, etiquette, accent, type_='checkbox', icone=''):
    actif = ('peer-checked:tw-border-nuit-800 peer-checked:tw-bg-nuit-800 peer-checked:tw-text-white hover:tw-border-nuit-700'
             if accent == 'nuit' else
             'peer-checked:tw-border-amber-600 peer-checked:tw-bg-amber-600 peer-checked:tw-text-white hover:tw-border-amber-500')
    ic = f'<svg class="ic tw-h-[18px] tw-w-[18px]"><use href="#{icone}"/></svg>' if icone else ''
    return (f'<label class="tw-cursor-pointer"><input type="{type_}" name="{nom}" value="{valeur}" class="tw-peer tw-sr-only">'
            f'<span class="tw-inline-flex tw-items-center tw-gap-2 tw-rounded-full tw-border tw-border-solid tw-border-slate-300 tw-bg-white '
            f'tw-px-4 tw-py-2 tw-text-sm tw-font-semibold tw-text-slate-700 tw-transition peer-focus-visible:tw-ring-4 '
            f'peer-focus-visible:tw-ring-slate-400/30 {actif}">{ic}{etiquette}</span></label>')


def groupe(nom, etiquette, valeurs, accent, type_='checkbox', requis=False, icones=None):
    icones = icones or {}
    puces = ''.join(puce(nom, v, v, accent, type_, icones.get(v, '')) for v in valeurs)
    attr = f' data-requis="{etiquette}"' if requis else ''
    return (f'<div class="sm:tw-col-span-2" data-groupe="{nom}" data-label="{etiquette}"{attr}>'
            f'<span class="{LABEL}">{etiquette}{" *" if requis else ""}</span>'
            f'<div class="tw-flex tw-flex-wrap tw-gap-2">{puces}</div>'
            f'<p class="tw-mt-2 tw-hidden tw-text-sm tw-font-semibold tw-text-red-700" data-erreur>Choisissez au moins une option.</p></div>')


def champ(id_, etiquette, accent, requis=False, type_='text', large=False, attrs='', aide=''):
    req = ' required' if requis else ''
    span = ' sm:tw-col-span-2' if large else ''
    a = f'<p class="tw-mt-1.5 tw-text-[13px] tw-text-slate-500">{aide}</p>' if aide else ''
    return (f'<div class="{span.strip()}"><label class="{LABEL}" for="{id_}">{etiquette}{" *" if requis else ""}</label>'
            f'<input id="{id_}" name="{id_}" type="{type_}" class="{classes_champ(accent)}" data-label="{etiquette}"{req} {attrs}>{a}</div>')


def liste(id_, etiquette, valeurs, accent, requis=False, large=False, vide='— Choisir —'):
    req = ' required' if requis else ''
    span = ' sm:tw-col-span-2' if large else ''
    opts = ''.join(f'<optgroup label="{v[0]}">' + ''.join(f'<option>{x}</option>' for x in v[1]) + '</optgroup>' if isinstance(v, tuple)
                   else f'<option>{v}</option>' for v in valeurs)
    return (f'<div class="{span.strip()}"><label class="{LABEL}" for="{id_}">{etiquette}{" *" if requis else ""}</label>'
            f'<select id="{id_}" name="{id_}" class="{classes_champ(accent)}" data-label="{etiquette}"{req}>'
            f'<option value="">{vide}</option>{opts}</select></div>')


def zone_texte(id_, etiquette, accent, placeholder='', requis=False):
    return (f'<div class="sm:tw-col-span-2"><label class="{LABEL}" for="{id_}">{etiquette}{" *" if requis else ""}</label>'
            f'<textarea id="{id_}" name="{id_}" rows="4" class="{classes_champ(accent)} tw-resize-y" data-label="{etiquette}" '
            f'placeholder="{placeholder}"{" required" if requis else ""}></textarea></div>')


def whatsapp(id_, etiquette, accent):
    """Téléphone avec indicatif à drapeau (composant du site) et champ Tailwind."""
    return (f'<div><span class="{LABEL}" id="{id_}-label">{etiquette} *</span>'
            f'<div class="tel-field tw-tel tw-tel-{accent}">'
            f'{liste_drapeaux(id_ + "_ind", id_ + "-label", "indicatif", requis=False, defaut="+225")}'
            f'<input id="{id_}" name="{id_}" type="tel" inputmode="tel" required autocomplete="tel-national" placeholder="07 00 00 00 00" '
            f'class="{classes_champ(accent)} tw-rounded-l-none" aria-labelledby="{id_}-label" data-label="{etiquette}" data-indicatif="{id_}_ind"></div></div>')


def salaire(id_, etiquette, accent, periodes):
    return (f'<div class="sm:tw-col-span-2"><label class="{LABEL}" for="{id_}">{etiquette}</label>'
            f'<div class="tw-grid tw-grid-cols-1 tw-gap-3 sm:tw-grid-cols-[minmax(0,1fr)_200px]">'
            f'<div class="tw-relative"><input id="{id_}" name="{id_}" type="text" inputmode="numeric" placeholder="Ex. 150 000" '
            f'class="{classes_champ(accent)} tw-pr-20 tw-tabular-nums" data-label="{etiquette}" data-fcfa>'
            f'<span class="tw-pointer-events-none tw-absolute tw-inset-y-0 tw-right-4 tw-flex tw-items-center tw-text-sm tw-font-bold tw-text-slate-500">FCFA</span></div>'
            f'<select id="{id_}_periode" name="{id_}_periode" class="{classes_champ(accent)}" data-label="Période du salaire">'
            + ''.join(f'<option>{p}</option>' for p in periodes) + '</select></div></div>')


def bloc(num, titre, sous_titre, contenu, accent):
    pastille = 'tw-bg-nuit-800 tw-text-white' if accent == 'nuit' else 'tw-bg-amber-500 tw-text-white'
    fond = 'tw-border-slate-200 tw-bg-white' if accent == 'nuit' else 'tw-border-amber-200/70 tw-bg-white'
    return f'''        <div class="tw-rounded-2xl tw-border tw-border-solid {fond} tw-p-5 tw-shadow-sm sm:tw-p-8">
          <div class="tw-mb-6 tw-flex tw-items-start tw-gap-4">
            <span class="tw-flex tw-h-10 tw-w-10 tw-shrink-0 tw-items-center tw-justify-center tw-rounded-full {pastille} tw-font-serif tw-text-lg tw-font-bold">{num}</span>
            <div><h2 class="tw-m-0 tw-font-serif tw-text-xl tw-leading-snug tw-text-slate-900 sm:tw-text-2xl">{titre}</h2>
            <p class="tw-mt-1 tw-text-sm tw-text-slate-500">{sous_titre}</p></div>
          </div>
          <div class="tw-grid tw-grid-cols-1 tw-gap-5 sm:tw-grid-cols-2">
{contenu}
          </div>
        </div>'''


ZONES = [('Abidjan', ['Cocody', 'Plateau', 'Marcory', 'Treichville', 'Koumassi', 'Port-Bouët', 'Yopougon', 'Abobo', 'Adjamé',
                      'Attécoubé', 'Bingerville', 'Anyama', 'Songon']),
         ('Intérieur du pays', ['Grand-Bassam', 'Assinie', 'Jacqueville', 'Yamoussoukro', 'San-Pédro', 'Bouaké', 'Korhogo', 'Autre ville']),
         ('Autre', ['Autre pays'])]


def bouton(texte, accent):
    c = ('tw-bg-nuit-800 hover:tw-bg-nuit-950 focus-visible:tw-ring-nuit-700/30' if accent == 'nuit'
         else 'tw-bg-amber-600 hover:tw-bg-amber-700 focus-visible:tw-ring-amber-500/30')
    return (f'<button type="submit" class="tw-inline-flex tw-w-full tw-cursor-pointer tw-items-center tw-justify-center tw-gap-2 tw-rounded-xl '
            f'tw-border-0 tw-px-6 tw-py-4 tw-font-sans tw-text-[15px] tw-font-bold tw-uppercase tw-tracking-wider tw-text-white tw-shadow-lg '
            f'tw-transition focus-visible:tw-outline-none focus-visible:tw-ring-4 {c}" data-envoyer>{texte}</button>')


def pied_formulaire(accent, consentement, bouton_txt, note):
    coche = 'tw-accent-nuit-800' if accent == 'nuit' else 'tw-accent-amber-600'
    return f'''        <div class="tw-grid tw-gap-4">
          <label class="tw-flex tw-cursor-pointer tw-items-start tw-gap-3 tw-text-sm tw-text-slate-600"><input type="checkbox" required class="tw-mt-1 tw-h-4 tw-w-4 {coche}"> {consentement}</label>
          {bouton(bouton_txt, accent)}
          <p class="tw-text-center tw-text-[13px] tw-text-slate-500">{note}</p>
          <p class="tw-hidden tw-rounded-lg tw-bg-red-50 tw-p-4 tw-text-sm tw-font-semibold tw-text-red-800" data-echec></p>
        </div>'''


def merci(titre, texte, accent, extra=''):
    bord = 'tw-border-nuit-800' if accent == 'nuit' else 'tw-border-amber-500'
    return f'''      <div class="tw-hidden tw-rounded-2xl tw-border-0 tw-border-t-4 tw-border-solid {bord} tw-bg-white tw-p-6 tw-text-center tw-shadow-sm sm:tw-p-10" data-merci>
        <h2 class="tw-m-0 tw-font-serif tw-text-2xl tw-text-slate-900">{titre}</h2>
        <p class="tw-mx-auto tw-mt-3 tw-max-w-lg tw-text-slate-600">{texte}</p>{extra}
        <pre class="tw-mt-6 tw-whitespace-pre-wrap tw-break-words tw-rounded-xl tw-bg-slate-50 tw-p-5 tw-text-left tw-font-sans tw-text-sm tw-leading-relaxed tw-text-slate-700" data-recap></pre>
      </div>'''


def entete(eyebrow, titre, texte, accent):
    c = 'tw-text-red-700' if accent == 'nuit' else 'tw-text-amber-700'
    return f'''      <div class="tw-mb-8 tw-text-center sm:tw-mb-10">
        <p class="tw-text-xs tw-font-bold tw-uppercase tw-tracking-[0.2em] {c}">{eyebrow}</p>
        <h2 class="tw-mx-auto tw-mt-3 tw-max-w-2xl tw-font-serif tw-text-[26px] tw-leading-tight tw-text-slate-900 sm:tw-text-4xl">{titre}</h2>
        <p class="tw-mx-auto tw-mt-4 tw-max-w-2xl tw-text-[15px] tw-leading-relaxed tw-text-slate-600 sm:tw-text-base">{texte}</p>
      </div>'''


PROFILS = ['Serveur / Serveuse', 'Hôtesse d’accueil', 'Maître d’hôtel', 'Cuisinier', 'Commis de cuisine', 'Chef de partie',
           'Pâtissier', 'Barman / Barmaid', 'Réceptionniste', 'Auditeur de nuit', 'Valet / Femme de chambre', 'Gouvernante', 'Plongeur', 'Autre']

# ================================================================ Espace client : fiche de besoin de personnel
A = 'nuit'
client_form = f'''<section class="tw-bg-nuit-50 tw-px-4 tw-py-14 sm:tw-py-20 ec">
  <div class="tw-mx-auto tw-max-w-4xl">
{entete('Espace client · Employeurs', 'Fiche de besoin de personnel en hôtellerie-restauration',
        'Hôtels, restaurants, lounges, traiteurs : décrivez le personnel dont vous avez besoin. Notre équipe étudie votre demande et vous propose des profils formés aux métiers de l’hôtellerie et de la restauration.', A)}
    <form id="form-client" class="fiche tw-grid tw-gap-6" data-key="{WEB3FORMS_KEY}" data-wa="{WHATSAPP}" data-sujet="Besoin de personnel" novalidate>
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
{bloc(1, 'Identification du besoin', 'Combien de personnes et quels profils recherchez-vous ?',
      champ('ec-nombre', 'Nombre de personnes', A, True, 'number', attrs='min="1" max="200" placeholder="Ex. 3"')
      + liste('ec-debut', 'Prise de poste souhaitée', ['Dès que possible', 'Sous 2 semaines', 'Sous 1 mois', 'Date à convenir'], A)
      + groupe('ec-profils', 'Profil(s) recherché(s)', PROFILS, A, requis=True)
      + champ('ec-profil-autre', 'Autre profil (précisez)', A, large=True, attrs='placeholder="Ex. Sommelier, chef de rang…"')
      + liste('ec-experience', 'Expérience minimale', ['Débutant accepté', '1 an', '2 à 3 ans', '5 ans et plus'], A)
      + groupe('ec-langues', 'Compétences linguistiques', ['Français', 'Anglais', 'Espagnol', 'Arabe', 'Autre langue'], A)
      + zone_texte('ec-competences', 'Compétences techniques attendues', A, 'Ex. hygiène HACCP, logiciel hôtelier, cocktails, service au guéridon…'), A)}
{bloc(2, 'Conditions de travail', 'Contrat, horaires et rémunération proposés.',
      groupe('ec-contrat', 'Type de contrat', ['CDI', 'CDD', 'Extra (mission ponctuelle)', 'Stage'], A, type_='radio', requis=True)
      + champ('ec-duree', 'Durée de la mission ou du contrat', A, large=True, attrs='placeholder="Ex. 3 mois, un week-end, un événement…"')
      + groupe('ec-horaires', 'Horaires', ['Continus', 'En coupure', 'Travail de nuit', 'Week-ends et jours fériés'], A)
      + salaire('ec-salaire', 'Salaire proposé', A, ['par mois', 'par jour', 'par prestation', 'à négocier'])
      + groupe('ec-avantages', 'Avantages', ['Logement', 'Repas', 'Transport', 'Primes'], A), A)}
{bloc(3, 'Identité de l’établissement', 'Pour que notre équipe puisse vous recontacter.',
      champ('ec-etablissement', 'Nom de l’hôtel ou du restaurant', A, True, large=True, attrs='autocomplete="organization"')
      + liste('ec-type', 'Type d’établissement', ['Hôtel', 'Restaurant', 'Bar / Lounge', 'Traiteur / Événementiel', 'Résidence hôtelière', 'Autre'], A, True)
      + champ('ec-contact', 'Nom du contact', A, True, attrs='autocomplete="name"')
      + champ('ec-fonction', 'Fonction', A, attrs='placeholder="Ex. Directeur, DRH, gérant…"')
      + whatsapp('ec-whatsapp', 'Téléphone WhatsApp', A)
      + champ('ec-email', 'E-mail', A, True, 'email', attrs='autocomplete="email"')
      + liste('ec-zone', 'Zone géographique', ZONES, A, True)
      + champ('ec-adresse', 'Adresse ou quartier', A, attrs='placeholder="Ex. Riviera 3, zone 4…"'), A)}
{pied_formulaire(A, 'J’accepte d’être recontacté(e) par EchoResta au sujet de ce besoin de personnel.', 'Envoyer la fiche de besoin',
                 f'Votre fiche est envoyée à notre équipe par e-mail. Une question ? {PHONE}')}
    </form>
{merci('Votre fiche de besoin est envoyée', 'Merci ! Notre équipe étudie votre demande et vous recontacte rapidement avec des profils adaptés.', A)}
  </div>
</section>
'''
page('espace_client.html', *seo.PAGES['espace_client.html'],
     page_hero('Espace client : recrutez du personnel en hôtellerie-restauration', '<a href="recrutement.html">Recrutement</a><span>/</span>Espace client',
               'images/directeur-hotel.jpg', 'Une fiche simple pour nous décrire le personnel dont votre établissement a besoin.') + client_form,
     'recrutement.html', head_extra=TAILWIND,
     schemas=[seo.fil_ariane(('Accueil', ''), ('Recrutement', 'recrutement.html'), ('Espace client', 'espace_client.html'))])

# ================================================================ Espace candidat : fiche d'inscription candidat
A = 'or'
POSTES = ['Cuisine', 'Salle', 'Bar', 'Réception', 'Étages']
ICONES_POSTES = {'Cuisine': 'i-chef', 'Salle': 'i-utensils', 'Bar': 'i-cocktail', 'Réception': 'i-bell', 'Étages': 'i-bed'}


def fichier(id_, etiquette, aide, accept, multiple=False):
    return f'''<div class="sm:tw-col-span-2">
              <span class="{LABEL}">{etiquette}</span>
              <label for="{id_}" class="tw-flex tw-cursor-pointer tw-flex-col tw-items-center tw-justify-center tw-gap-2 tw-rounded-xl tw-border-2 tw-border-dashed tw-border-amber-300 tw-bg-amber-50/60 tw-px-4 tw-py-6 tw-text-center tw-transition hover:tw-border-amber-500 hover:tw-bg-amber-50">
                <svg class="ic tw-h-7 tw-w-7 tw-text-amber-600"><use href="#i-upload"/></svg>
                <span class="tw-text-sm tw-font-bold tw-text-amber-800">Choisir {'des fichiers' if multiple else 'un fichier'}</span>
                <span class="tw-text-xs tw-text-slate-500">{aide}</span>
                <span class="tw-text-sm tw-font-semibold tw-text-slate-800" data-fichiers="{id_}"></span>
              </label>
              <input id="{id_}" name="{id_}" type="file" accept="{accept}" class="tw-sr-only" data-label="{etiquette}"{' multiple' if multiple else ''}>
            </div>'''


candidat_form = f'''<section class="tw-bg-gradient-to-b tw-from-amber-50 tw-to-orange-50/40 tw-px-4 tw-py-14 sm:tw-py-20 ec ec-or">
  <div class="tw-mx-auto tw-max-w-4xl">
{entete('Espace candidat · Professionnels', 'Fiche d’inscription candidat',
        'Cuisiniers, serveurs, barmen, réceptionnistes, femmes et valets de chambre : inscrivez-vous pour être mis en relation avec des hôtels et restaurants qui recrutent.', A)}
    <form id="form-candidat" class="fiche tw-grid tw-gap-6" data-key="{WEB3FORMS_KEY}" data-wa="{WHATSAPP}" data-sujet="Candidature emploi" novalidate>
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
{bloc(1, 'Votre identité', 'Pour que les recruteurs puissent vous joindre.',
      champ('cd-nom', 'Nom', A, True, attrs='autocomplete="family-name"')
      + champ('cd-prenoms', 'Prénoms', A, True, attrs='autocomplete="given-name"')
      + whatsapp('cd-whatsapp', 'Téléphone WhatsApp', A)
      + champ('cd-email', 'E-mail', A, False, 'email', attrs='autocomplete="email"')
      + champ('cd-lieu', 'Lieu d’habitation', A, True, attrs='placeholder="Ex. Yopougon, Abidjan"')
      + liste('cd-experience', 'Années d’expérience', ['Moins d’un an', '1 à 2 ans', '3 à 5 ans', '6 à 10 ans', 'Plus de 10 ans'], A, True), A)}
{bloc(2, 'Métier recherché & conditions', 'Le poste que vous visez et vos attentes.',
      groupe('cd-poste', 'Poste recherché', POSTES, A, requis=True, icones=ICONES_POSTES)
      + champ('cd-poste-precis', 'Intitulé du poste', A, large=True, attrs='placeholder="Ex. Chef de partie, chef de rang, night auditor…"')
      + groupe('cd-contrat', 'Type de contrat souhaité', ['CDI', 'CDD', 'Extra'], A)
      + liste('cd-dispo', 'Disponibilité', ['Immédiate', 'Sous 15 jours', 'Sous 1 mois', 'À convenir'], A)
      + salaire('cd-salaire', 'Prétention salariale', A, ['par mois', 'par jour', 'à négocier'])
      + zone_texte('cd-etablissements', 'Derniers établissements fréquentés', A, 'Nom de l’établissement, poste occupé et période. Ex. Hôtel X, commis de cuisine, 2023–2025'), A)}
{bloc(3, 'Justificatifs', 'Sélectionnez vos documents : après l’envoi de la fiche, vous pourrez nous les transmettre en un clic sur WhatsApp.',
      fichier('cd-cv', 'CV', 'PDF, Word ou photo · 5 Mo maximum', '.pdf,.doc,.docx,image/*')
      + fichier('cd-photo', 'Photo professionnelle', 'JPG ou PNG, de face, tenue correcte', 'image/*')
      + fichier('cd-diplomes', 'Diplômes et attestations', 'Plusieurs fichiers possibles', '.pdf,image/*', multiple=True), A)}
{pied_formulaire(A, 'Je certifie l’exactitude des informations et j’accepte d’être recontacté(e) par EchoResta pour des offres d’emploi.',
                 'Envoyer ma candidature', f'Votre fiche est envoyée à notre équipe par e-mail. Une question ? {PHONE}')}
    </form>
{merci('Votre candidature est enregistrée', 'Dernière étape : envoyez vos justificatifs (CV, photo, diplômes) sur WhatsApp. Le message est déjà rédigé, il ne reste qu’à joindre vos fichiers.', A,
       '<a class="tw-mt-6 tw-inline-flex tw-items-center tw-justify-center tw-gap-2 tw-rounded-xl tw-bg-[#15803d] tw-px-6 tw-py-4 tw-font-bold tw-text-white tw-no-underline hover:tw-bg-[#116a32]" data-wa-fichiers target="_blank" rel="noopener"><svg class="ic tw-h-5 tw-w-5"><use href="#i-chat"/></svg>Envoyer mes justificatifs sur WhatsApp</a>')}
  </div>
</section>
'''
page('espace_candidat.html', *seo.PAGES['espace_candidat.html'],
     page_hero('Espace candidat : trouvez un emploi en hôtellerie-restauration', '<a href="recrutement.html">Recrutement</a><span>/</span>Espace candidat',
               'images/serveur-hotesse.jpg', 'Inscrivez-vous en quelques minutes et soyez mis en relation avec des établissements qui recrutent.') + candidat_form,
     'recrutement.html', head_extra=TAILWIND,
     schemas=[seo.fil_ariane(('Accueil', ''), ('Recrutement', 'recrutement.html'), ('Espace candidat', 'espace_candidat.html'))])

# ================================================================ Page d'aiguillage : deux grands boutons
choix = f'''<section class="tw-bg-nuit-50 tw-px-4 tw-py-16 sm:tw-py-24">
  <div class="tw-mx-auto tw-max-w-5xl">
    <div class="tw-mb-10 tw-text-center sm:tw-mb-14">
      <p class="tw-text-xs tw-font-bold tw-uppercase tw-tracking-[0.2em] tw-text-red-700">Espace recrutement</p>
      <h2 class="tw-mx-auto tw-mt-3 tw-max-w-2xl tw-font-serif tw-text-[28px] tw-leading-tight tw-text-slate-900 sm:tw-text-4xl">Vous recrutez ou vous cherchez un emploi ?</h2>
      <p class="tw-mx-auto tw-mt-4 tw-max-w-xl tw-text-slate-600">Choisissez votre espace pour remplir la fiche qui vous correspond.</p>
    </div>
    <div class="tw-grid tw-grid-cols-1 tw-gap-6 md:tw-grid-cols-2">
      <a href="espace_client.html" class="tw-group tw-relative tw-flex tw-flex-col tw-gap-5 tw-overflow-hidden tw-rounded-3xl tw-bg-nuit-900 tw-p-8 tw-text-white tw-no-underline tw-shadow-xl tw-transition hover:-tw-translate-y-1 hover:tw-shadow-2xl focus-visible:tw-outline-none focus-visible:tw-ring-4 focus-visible:tw-ring-nuit-700/40 sm:tw-p-10">
        <span class="tw-flex tw-h-14 tw-w-14 tw-items-center tw-justify-center tw-rounded-2xl tw-bg-white/10"><svg class="ic tw-h-7 tw-w-7"><use href="#i-building"/></svg></span>
        <span class="tw-text-xs tw-font-bold tw-uppercase tw-tracking-[0.2em] tw-text-white/70">Espace client · Employeurs</span>
        <span class="tw-font-serif tw-text-2xl tw-font-bold tw-leading-snug sm:tw-text-3xl">Je cherche du personnel</span>
        <span class="tw-text-[15px] tw-leading-relaxed tw-text-white/80">Hôtels, restaurants, lounges, traiteurs : décrivez votre besoin, nous vous proposons des profils formés.</span>
        <span class="tw-mt-auto tw-inline-flex tw-items-center tw-gap-2 tw-font-bold">Remplir la fiche de besoin <svg class="ic tw-h-4 tw-w-4 tw-transition group-hover:tw-translate-x-1"><use href="#i-arrow"/></svg></span>
      </a>
      <a href="espace_candidat.html" class="tw-group tw-relative tw-flex tw-flex-col tw-gap-5 tw-overflow-hidden tw-rounded-3xl tw-bg-gradient-to-br tw-from-amber-500 tw-to-amber-700 tw-p-8 tw-text-white tw-no-underline tw-shadow-xl tw-transition hover:-tw-translate-y-1 hover:tw-shadow-2xl focus-visible:tw-outline-none focus-visible:tw-ring-4 focus-visible:tw-ring-amber-500/40 sm:tw-p-10">
        <span class="tw-flex tw-h-14 tw-w-14 tw-items-center tw-justify-center tw-rounded-2xl tw-bg-white/15"><svg class="ic tw-h-7 tw-w-7"><use href="#i-users"/></svg></span>
        <span class="tw-text-xs tw-font-bold tw-uppercase tw-tracking-[0.2em] tw-text-white/80">Espace candidat · Professionnels</span>
        <span class="tw-font-serif tw-text-2xl tw-font-bold tw-leading-snug sm:tw-text-3xl">Je cherche un emploi</span>
        <span class="tw-text-[15px] tw-leading-relaxed tw-text-white/90">Cuisine, salle, bar, réception, étages : inscrivez-vous et soyez mis en relation avec des établissements qui recrutent.</span>
        <span class="tw-mt-auto tw-inline-flex tw-items-center tw-gap-2 tw-font-bold">Remplir la fiche candidat <svg class="ic tw-h-4 tw-w-4 tw-transition group-hover:tw-translate-x-1"><use href="#i-arrow"/></svg></span>
      </a>
    </div>
  </div>
</section>
'''
page('recrutement.html', *seo.PAGES['recrutement.html'],
     page_hero('Recrutement en hôtellerie et restauration à Abidjan', 'Recrutement', 'images/apropos-diplomes.jpg') + choix,
     'recrutement.html', head_extra=TAILWIND,
     schemas=[seo.fil_ariane(('Accueil', ''), ('Recrutement', 'recrutement.html'))])
