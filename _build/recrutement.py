"""Espace recrutement : page d'aiguillage, fiche de besoin (employeurs) et fiche candidat (professionnels).

Les pages utilisent Tailwind CSS (compilé dans assets/recrutement.css, voir _build/tailwind.config.js ;
préfixe « tw- », sans remise à zéro des styles du site)
et sont envoyés par e-mail via Web3Forms, comme les autres formulaires du site.
"""

TAILWIND = '<link rel="stylesheet" href="assets/recrutement.css">'

# ---------------------------------------------------------------- Petits composants communs
def classes_champ(accent):
    ring = 'focus:tw-border-nuit-700 focus:tw-ring-nuit-700/10' if accent == 'nuit' else 'focus:tw-border-amber-600 focus:tw-ring-amber-500/15'
    return (f'tw-w-full tw-rounded-lg tw-border tw-border-solid tw-border-slate-300 tw-bg-white tw-px-4 tw-py-3 tw-font-sans tw-text-[15px] '
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


def case(nom, valeur, accent, type_='checkbox'):
    """Case à cocher visible, disposée en grille (listes longues : âges, tâches)."""
    actif = ('has-[:checked]:tw-border-nuit-700 has-[:checked]:tw-bg-nuit-50 has-[:checked]:tw-text-nuit-900 tw-accent-nuit-800'
             if accent == 'nuit' else 'has-[:checked]:tw-border-amber-500 has-[:checked]:tw-bg-amber-50 tw-accent-amber-600')
    return (f'<label class="tw-flex tw-cursor-pointer tw-items-center tw-gap-3 tw-rounded-lg tw-border tw-border-solid tw-border-slate-200 '
            f'tw-bg-white tw-px-3 tw-py-2.5 tw-text-[13.5px] tw-leading-snug tw-text-slate-700 tw-transition hover:tw-border-slate-400 sm:tw-px-3.5 sm:tw-text-sm {actif}">'
            f'<input type="{type_}" name="{nom}" value="{valeur}" class="tw-m-0 tw-h-4 tw-w-4 tw-shrink-0">{valeur}</label>')


def groupe(nom, etiquette, valeurs, accent, type_='checkbox', requis=False, icones=None, cle=None, grille=False):
    icones = icones or {}
    puces = (''.join(case(nom, v, accent, type_) for v in valeurs) if grille
             else ''.join(puce(nom, v, v, accent, type_, icones.get(v, '')) for v in valeurs))
    disposition = 'tw-grid tw-grid-cols-2 tw-gap-2 lg:tw-grid-cols-3' if grille else 'tw-flex tw-flex-wrap tw-gap-2'
    attr = f' data-requis="{etiquette}"' if requis else ''
    return (f'<div class="sm:tw-col-span-2" data-groupe="{nom}" data-label="{cle or etiquette}"{attr}>'
            f'<span class="{LABEL}">{etiquette}{" *" if requis else ""}</span>'
            f'<div class="{disposition}">{puces}</div>'
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


def whatsapp(id_, etiquette, accent, requis=True):
    """Téléphone avec indicatif à drapeau (composant du site) et champ Tailwind."""
    return (f'<div><span class="{LABEL}" id="{id_}-label">{etiquette}{" *" if requis else ""}</span>'
            f'<div class="tel-field tw-tel tw-tel-{accent}">'
            f'{liste_drapeaux(id_ + "_ind", id_ + "-label", "indicatif", requis=False, defaut="+225")}'
            f'<input id="{id_}" name="{id_}" type="tel" inputmode="tel"{" required" if requis else ""} autocomplete="tel-national" placeholder="07 00 00 00 00" '
            f'class="{classes_champ(accent)} tw-rounded-l-none" aria-labelledby="{id_}-label" data-label="{etiquette}" data-indicatif="{id_}_ind"></div></div>')


def salaire(id_, etiquette, accent, periodes):
    return (f'<div class="sm:tw-col-span-2"><label class="{LABEL}" for="{id_}">{etiquette}</label>'
            f'<div class="tw-grid tw-grid-cols-1 tw-gap-3 sm:tw-grid-cols-[minmax(0,1fr)_200px]">'
            f'<div class="tw-relative"><input id="{id_}" name="{id_}" type="text" inputmode="numeric" placeholder="Ex. 150 000" '
            f'class="{classes_champ(accent)} tw-pr-20 tw-tabular-nums" data-label="{etiquette}" data-fcfa>'
            f'<span class="tw-pointer-events-none tw-absolute tw-inset-y-0 tw-right-4 tw-flex tw-items-center tw-text-sm tw-font-bold tw-text-slate-500">FCFA</span></div>'
            f'<select id="{id_}_periode" name="{id_}_periode" class="{classes_champ(accent)}" data-label="Période du salaire">'
            + ''.join(f'<option>{p}</option>' for p in periodes) + '</select></div></div>')


def montant(id_, etiquette, accent):
    return (f'<div><label class="{LABEL}" for="{id_}">{etiquette}</label><div class="tw-relative">'
            f'<input id="{id_}" name="{id_}" type="text" inputmode="numeric" placeholder="Ex. 100 000" '
            f'class="{classes_champ(accent)} tw-pr-20 tw-tabular-nums" data-label="{etiquette}" data-fcfa>'
            f'<span class="tw-pointer-events-none tw-absolute tw-inset-y-0 tw-right-4 tw-flex tw-items-center tw-text-sm tw-font-bold tw-text-slate-500">FCFA</span></div></div>')


def intertitre(texte, aide=''):
    a = f'<p class="tw-mb-0 tw-mt-1 tw-text-sm tw-text-slate-500">{aide}</p>' if aide else ''
    return (f'<div class="sm:tw-col-span-2 tw-mt-3 tw-border-0 tw-border-t tw-border-dashed tw-border-slate-200 tw-pt-7">'
            f'<h3 class="tw-m-0 tw-font-serif tw-text-lg tw-text-slate-900">{texte}</h3>{a}</div>')


def si(condition, contenu):
    """Champs affichés seulement quand le choix « nom=valeur » est coché (voir main.js)."""
    return (f'<div class="sm:tw-col-span-2 tw-hidden tw-grid tw-grid-cols-1 tw-gap-x-6 tw-gap-y-5 tw-rounded-xl tw-bg-slate-50 tw-p-5 sm:tw-grid-cols-2" '
            f'data-si="{condition}">{contenu}</div>')


def bloc(num, titre, sous_titre, contenu, accent):
    chiffre = 'tw-text-red-700' if accent == 'nuit' else 'tw-text-amber-600'
    filet = ' tw-border-0 tw-border-t tw-border-solid tw-border-slate-200' if num > 1 else ''
    return f'''        <div class="tw-px-5 tw-py-8 sm:tw-px-10 sm:tw-py-10{filet}">
          <div class="tw-mb-7 tw-flex tw-items-baseline tw-gap-4 sm:tw-gap-5">
            <span class="tw-font-serif tw-text-2xl tw-font-bold {chiffre} sm:tw-text-3xl">{num:02d}</span>
            <div><h2 class="tw-m-0 tw-font-serif tw-text-xl tw-leading-snug tw-text-slate-900 sm:tw-text-2xl">{titre}</h2>
            <p class="tw-mb-0 tw-mt-1 tw-text-sm tw-text-slate-500">{sous_titre}</p></div>
          </div>
          <div class="tw-grid tw-grid-cols-1 tw-gap-x-6 tw-gap-y-5 sm:tw-grid-cols-2">
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
    cadre = ' tw-border-0 tw-border-t tw-border-solid tw-border-slate-200 tw-bg-slate-50/70 tw-px-5 tw-py-8 sm:tw-px-10'
    return f'''        <div class="tw-grid tw-gap-4{cadre}">
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
PANNEAU = ('fiche tw-overflow-hidden tw-rounded-2xl tw-border-0 tw-border-t-4 tw-border-solid {bord} tw-bg-white '
           'tw-shadow-[0_1px_3px_rgba(15,23,42,.08),0_20px_50px_-20px_rgba(15,23,42,.25)] tw-ring-1 tw-ring-slate-200')
TACHES = [('Hôtellerie & restauration', ['Service en salle', 'Accueil / Hôtesse', 'Réception', 'Audit de nuit', 'Bar', 'Cuisine de restaurant',
                                         'Étages / chambres', 'Gouvernante d’hôtel', 'Plonge']),
          ('Cuisine', ['Cuisine ivoirienne authentique', 'Cuisine africaine', 'Cuisine européenne', 'Cuisine européenne élaborée',
                       'Cuisine arabe', 'Cuisine asiatique']),
          ('Nounou (garde d’enfants)', ['Nounou 0 à 2 ans', 'Nounou 2 à 5 ans', 'Nounou 5 à 10 ans', 'Nounou + 10 ans', 'Suivi scolaire',
                                        'Autres (à préciser)']),
          ('Ménage', ['Nettoyage des surfaces', 'Nettoyage des vitres', 'Entretien des chambres', 'Entretien des salles de bain',
                      'Lessive à la main', 'Lessive à la machine', 'Lessive à la main et à la machine', 'Repassage', 'Rangement']),
          ('Auxiliaire de vie', ['Personnes âgées', 'Malades à domicile', 'Adulte handicapé', 'Enfant handicapé']),
          ('Chauffeur', ['Chauffeur de famille', 'Chauffeur personnel']),
          ('Gestion globale', ['Majordome', 'Gouvernante'])]
TACHES_HTML = ''.join(groupe(f'ec-t{n}', titre, valeurs, A, cle=f'Tâches – {titre}', grille=True) for n, (titre, valeurs) in enumerate(TACHES, 1))

client_form = f'''<section class="tw-bg-white tw-px-4 tw-py-14 sm:tw-py-20 ec">
  <div class="tw-mx-auto tw-max-w-4xl">
{entete('Recherche du personnel · Employeurs', 'Fiche de besoin de personnel',
        'Hôtels, restaurants, résidences, entreprises ou particuliers : décrivez le profil recherché, les tâches et les conditions de travail. Notre équipe vous propose des candidats formés et vous recontacte rapidement.', A)}
    <form id="form-client" class="{PANNEAU.format(bord='tw-border-nuit-800')}" data-key="{WEB3FORMS_KEY}" data-wa="{WHATSAPP}" data-sujet="Besoin de personnel" novalidate>
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
{bloc(1, 'Identification du besoin', 'Le profil de la ou des personnes que vous recherchez.',
      liste('ec-nombre', 'Je cherche', [f'{n} personne' + ('s' if n > 1 else '') for n in range(1, 11)] + ['Plus de 10 personnes'], A, True)
      + liste('ec-genre', 'Genre', ['Homme', 'Femme', 'Peu importe'], A, True)
      + groupe('ec-age', 'Tranche d’âge', ['18 à 25 ans', '25 à 30 ans', '30 à 35 ans', '35 à 40 ans', '40 à 45 ans', '45 à 50 ans',
                                           '50 ans et +', 'Peu importe l’âge'], A, type_='radio', requis=True, grille=True)
      + groupe('ec-sachant', 'Sachant', ['Lire', 'Écrire', 'Peu importe'], A, requis=True)
      + groupe('ec-niveau', 'Ayant le niveau', ['Élémentaire', 'Secondaire', 'Supérieur', 'Peu importe', 'Autre'], A, type_='radio', requis=True)
      + si('ec-niveau=Autre', champ('ec-niveau-autre', 'Précisez la formation', A, large=True, attrs='placeholder="Ex. CAP cuisine, BTS hôtellerie…"'))
      + intertitre('Pour exécuter les tâches suivantes', 'Cochez toutes les tâches attendues.')
      + TACHES_HTML
      + zone_texte('ec-taches-autres', 'Autre(s) tâche(s)', A)
      + intertitre('Niveau d’aptitude recherché')
      + groupe('ec-echelle', 'Échelle de compétence (de 1 à 10)', [f'{n:02d}' for n in range(1, 11)], A, type_='radio', requis=True)
      + groupe('ec-maitrise', 'Niveau de maîtrise', ['Débutant', 'Intermédiaire', 'Expert'], A, type_='radio', requis=True)
      + intertitre('Autres indications')
      + zone_texte('ec-details', 'Détails', A, 'Langues parlées, qualités attendues, expérience souhaitée…'), A)}
{bloc(2, 'Conditions de travail de l’employé', 'Logement, horaires, début de la mission et salaire.',
      groupe('ec-loge', 'Logé sur le lieu de travail ?', ['Oui', 'Non', 'Peu importe'], A, type_='radio', requis=True)
      + si('ec-loge=Oui', champ('ec-sortie', 'Heure de sortie', A, type_='time') + champ('ec-reprise', 'Heure de reprise', A, type_='time'))
      + groupe('ec-temps', 'Temps de travail', ['Plein temps', 'Temps partiel'], A, type_='radio', requis=True)
      + si('ec-temps=Temps partiel', champ('ec-debut-h', 'Heure de début', A, type_='time') + champ('ec-fin-h', 'Heure de fin', A, type_='time'))
      + groupe('ec-contrat', 'Type de contrat', ['CDI', 'CDD', 'Extra (mission ponctuelle)', 'Stage'], A, type_='radio')
      + groupe('ec-horaires', 'Horaires', ['Continus', 'En coupure', 'Travail de nuit', 'Week-ends et jours fériés'], A)
      + liste('ec-debut', 'Début de la mission', ['Immédiatement', 'Dans 1 à 3 jours', 'Dans 1 semaine', 'Dans 2 semaines', 'Dans 1 mois',
                                                  'Date à convenir'], A, True)
      + '<div class="tw-hidden sm:tw-block"></div>'
      + montant('ec-salaire-min', 'Salaire prévisionnel minimum', A)
      + montant('ec-salaire-max', 'Salaire prévisionnel maximum', A)
      + groupe('ec-avantages', 'Avantages', ['Repas', 'Transport', 'Primes'], A)
      + zone_texte('ec-particularite', 'Autre particularité', A), A)}
{bloc(3, 'Votre identité', 'Pour que notre équipe puisse vous recontacter.',
      liste('ec-civilite', 'Genre', ['Homme', 'Femme'], A, True)
      + liste('ec-situation', 'Situation familiale', ['Célibataire', 'En couple', 'Marié(e)', 'Divorcé(e)', 'Veuf / Veuve'], A, True)
      + groupe('ec-enfant', 'Enfants', ['Oui', 'Non'], A, type_='radio', requis=True)
      + si('ec-enfant=Oui', champ('ec-age-enfants', 'Âge des enfants', A, large=True, attrs='placeholder="Ex. 2 ans, 5 ans, 7 ans"'))
      + champ('ec-nom', 'Nom', A, True, attrs='autocomplete="family-name"')
      + champ('ec-prenoms', 'Prénoms', A, True, attrs='autocomplete="given-name"')
      + liste('ec-zone', 'Lieu d’habitation', ZONES, A, True)
      + champ('ec-adresse', 'Quartier', A, attrs='placeholder="Ex. Riviera 3, Angré…"')
      + whatsapp('ec-tel', 'Téléphone', A)
      + whatsapp('ec-whatsapp', 'Téléphone WhatsApp', A, requis=False)
      + champ('ec-email', 'E-mail', A, True, 'email', large=True, attrs='autocomplete="email"')
      + liste('ec-type', 'Vous êtes', ['Particulier', 'Hôtel', 'Restaurant', 'Bar / Lounge', 'Traiteur / Événementiel', 'Résidence hôtelière',
                                       'Entreprise', 'Autre'], A, True)
      + champ('ec-etablissement', 'Établissement ou société', A, attrs='autocomplete="organization" placeholder="Si vous recrutez pour une structure"'), A)}
{pied_formulaire(A, 'J’accepte d’être recontacté(e) par EchoResta au sujet de ce besoin de personnel.', 'Envoyer la fiche de besoin',
                 f'Votre fiche est envoyée à notre équipe par e-mail. Une question ? {PHONE}')}
    </form>
{merci('Votre fiche de besoin est envoyée', 'Merci ! Notre équipe étudie votre demande et vous recontacte rapidement avec des profils adaptés.', A)}
  </div>
</section>
'''
page('espace_client.html', *seo.PAGES['espace_client.html'],
     page_hero('Recherche du personnel : recrutez en hôtellerie, restauration et services', '<a href="recrutement.html">Recrutement</a><span>/</span>Recherche du personnel',
               'images/directeur-hotel.jpg', 'Une fiche simple pour nous décrire le profil, les tâches et les conditions de travail du personnel recherché.') + client_form,
     'recrutement.html', head_extra=TAILWIND,
     schemas=[seo.fil_ariane(('Accueil', ''), ('Recrutement', 'recrutement.html'), ('Recherche du personnel', 'espace_client.html'))])

# ================================================================ Espace candidat : fiche d'inscription candidat
A = 'or'
POSTES = ['Cuisine', 'Salle', 'Bar', 'Réception', 'Étages']
ICONES_POSTES = {'Cuisine': 'i-chef', 'Salle': 'i-utensils', 'Bar': 'i-cocktail', 'Réception': 'i-bell', 'Étages': 'i-bed'}


def fichier(id_, etiquette, aide, accept, multiple=False):
    return f'''<div class="{'sm:tw-col-span-2' if multiple else ''}">
              <span class="{LABEL}">{etiquette}</span>
              <label for="{id_}" class="tw-flex tw-cursor-pointer tw-flex-col tw-items-center tw-justify-center tw-gap-2 tw-rounded-xl tw-border tw-border-dashed tw-border-slate-300 tw-bg-white tw-px-4 tw-py-6 tw-text-center tw-transition hover:tw-border-amber-500 hover:tw-bg-slate-50">
                <svg class="ic tw-h-7 tw-w-7 tw-text-amber-600"><use href="#i-upload"/></svg>
                <span class="tw-text-sm tw-font-bold tw-text-slate-900">Choisir {'des fichiers' if multiple else 'un fichier'}</span>
                <span class="tw-text-xs tw-text-slate-500">{aide}</span>
                <span class="tw-text-sm tw-font-semibold tw-text-slate-800" data-fichiers="{id_}"></span>
              </label>
              <input id="{id_}" name="{id_}" type="file" accept="{accept}" class="tw-sr-only" data-label="{etiquette}"{' multiple' if multiple else ''}>
            </div>'''


candidat_form = f'''<section class="tw-bg-white tw-px-4 tw-py-14 sm:tw-py-20 ec ec-or">
  <div class="tw-mx-auto tw-max-w-4xl">
{entete('Espace candidat · Professionnels', 'Fiche d’inscription candidat',
        'Cuisiniers, serveurs, barmen, réceptionnistes, femmes et valets de chambre : inscrivez-vous pour être mis en relation avec des hôtels et restaurants qui recrutent.', A)}
    <form id="form-candidat" class="{PANNEAU.format(bord='tw-border-amber-500')}" data-key="{WEB3FORMS_KEY}" data-wa="{WHATSAPP}" data-sujet="Candidature emploi" novalidate>
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
