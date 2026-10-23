"""Génère les pages statiques du site EchoResta.

Usage : python3 _build/build.py   (depuis la racine du dépôt)
En-tête, pied de page, icônes et contenus des formations sont partagés entre toutes les pages.
"""
import json, pathlib, re, sys
from urllib.parse import quote

S = pathlib.Path(__file__).resolve().parent
OUT = S.parent
sys.path.insert(0, str(S))
from metiers import CATEGORIES, METIERS, QUIZ  # noqa: E402

PHONE = '+225 07 68 84 20 38'
WHATSAPP = '2250768842038'  # numéro WhatsApp au format international, sans + ni espaces
WHATSAPP_AFFICHE = '+225 07 68 84 20 38'
PLUS_CODE = '92JH+FW'  # code de localisation Google (Plus Code) du centre, à Abidjan
GPS = '5.381188,-3.970187'  # coordonnées correspondant au Plus Code
MAPS_ITINERAIRE = f'https://www.google.com/maps/dir/?api=1&destination={GPS}'
MAPS_OUVRIR = f'https://www.google.com/maps/search/?api=1&query={GPS}'
BY_CAT = {k: [m for m in METIERS if m['cat'] == k] for k in CATEGORIES}

icons = (S / 'icons.html').read_text().replace('</svg>', '''  <symbol id="i-check" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></symbol>
  <symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></symbol>
  <symbol id="i-award" viewBox="0 0 24 24"><circle cx="12" cy="8" r="6"/><path d="M15.5 13 17 22l-5-3-5 3 1.5-9"/></symbol>
  <symbol id="i-level" viewBox="0 0 24 24"><path d="M4 20V14M10 20V9M16 20V4M22 20H2"/></symbol>
  <symbol id="i-target" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></symbol>
  <symbol id="i-eye" viewBox="0 0 24 24"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></symbol>
  <symbol id="i-heart" viewBox="0 0 24 24"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/></symbol>
  <symbol id="i-star" viewBox="0 0 24 24"><path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></symbol>
  <symbol id="i-clock2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></symbol>
  <symbol id="i-bed" viewBox="0 0 24 24"><path d="M2 4v16M2 8h18a2 2 0 0 1 2 2v10M2 17h20M6 8v9"/></symbol>
  <symbol id="i-clipboard" viewBox="0 0 24 24"><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/></symbol>
  <symbol id="i-moon" viewBox="0 0 24 24"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></symbol>
  <symbol id="i-bell" viewBox="0 0 24 24"><path d="M3 20a1 1 0 0 1-1-1v-1a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v1a1 1 0 0 1-1 1Z"/><path d="M20 16a8 8 0 1 0-16 0M12 4v4M10 4h4"/></symbol>
  <symbol id="i-utensils" viewBox="0 0 24 24"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2M7 2v20M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/></symbol>
  <symbol id="i-chef" viewBox="0 0 24 24"><path d="M17 21a1 1 0 0 0 1-1v-5.35c0-.46.32-.84.73-1.04a4 4 0 0 0-2.14-7.59 5 5 0 0 0-9.18 0 4 4 0 0 0-2.14 7.59c.41.2.73.58.73 1.04V20a1 1 0 0 0 1 1Z"/><path d="M6 17h12"/></symbol>
  <symbol id="i-cocktail" viewBox="0 0 24 24"><path d="M8 22h8M12 11v11M19 3l-7 8-7-8Z"/></symbol>
  <symbol id="i-trend" viewBox="0 0 24 24"><path d="M22 7 13.5 15.5l-5-5L2 17"/><path d="M16 7h6v6"/></symbol>
  <symbol id="i-lang" viewBox="0 0 24 24"><path d="m5 8 6 6M4 14l6-6 2-3M2 5h12M7 2h1M22 22l-5-10-5 10M14 18h6"/></symbol>
  <symbol id="i-chat" viewBox="0 0 24 24"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path d="M8.5 10.5c0 2.5 2.5 5 5 5l1.5-1.5-2-1-1 .8c-.9-.4-1.6-1.1-2-2l.8-1-1-2Z"/></symbol>
</svg>''', 1)

NAV = [('index.html', 'Accueil'), ('apropos.html', 'À propos'), ('formations.html', 'Formations'), ('contact.html', 'Contact')]


def url(m):
    return f'formation-{m["slug"]}.html'


def wa_link(text):
    return f'https://wa.me/{WHATSAPP}?text=' + quote(text)


def submenu():
    def col(*cats):
        out = []
        for c in cats:
            out.append(f'          <h6>{CATEGORIES[c]}</h6>')
            out += [f'          <a href="{url(m)}">{m["titre"]}</a>' for m in BY_CAT[c]]
        return '        <div>\n' + '\n'.join(out) + '\n        </div>'
    return '\n'.join([col('hotellerie', 'langues'), col('restauration'),
                      '        <a class="all" href="formations.html">Toutes les formations →</a>'])


def header(active):
    links = []
    for href, label in NAV:
        cls = ' class="active"' if href == active else ''
        if href == 'formations.html':
            links.append(f'''      <div class="has-sub">
        <a href="formations.html"{cls}>Formations <svg class="ic"><use href="#i-down"/></svg></a>
        <div class="submenu mega">
{submenu()}
        </div>
      </div>''')
        else:
            links.append(f'      <a href="{href}"{cls}>{label}</a>')
    links = '\n'.join(links)
    return f'''<div class="topbar">
  <div class="container">
    <span><svg class="ic"><use href="#i-phone"/></svg>{PHONE}</span>
    <span><svg class="ic"><use href="#i-pin"/></svg>Angré Star 14, Cocody — Abidjan, Côte d’Ivoire</span>
    <span><svg class="ic"><use href="#i-mail"/></svg>contact@echoresta.ci</span>
  </div>
</div>

<header class="site">
  <div class="container">
    <a href="index.html" class="brand">
      <div class="brand-logo"><img src="images/logo.jpg" alt="Logo EchoResta"></div>
      <div>
        <div class="brand-name">EchoResta</div>
        <div class="brand-tag">Hôtellerie &amp; Restauration</div>
      </div>
    </a>
    <nav class="main" id="nav">
{links}
      <button class="search-btn" aria-label="Rechercher"><svg class="ic"><use href="#i-search"/></svg></button>
      <a href="contact.html#formulaire" class="btn btn-red nav-cta">S’inscrire</a>
    </nav>
    <button class="burger" aria-label="Menu"><svg class="ic"><use href="#i-menu"/></svg></button>
  </div>
</header>
'''


FOOTER = f'''<footer class="big">
  <div class="container">
    <div class="cols">
      <div>
        <div class="f-brand"><img src="images/logo.jpg" alt=""><b>EchoResta</b></div>
        <p>Cabinet de formation en hôtellerie et restauration à Abidjan. Des parcours pratiques, une double certification et un stage garanti en entreprise.</p>
      </div>
      <div>
        <h5>Navigation</h5>
        <ul>
{chr(10).join(f'          <li><a href="{h}">{l}</a></li>' for h, l in NAV)}
        </ul>
      </div>
      <div>
        <h5>Formations</h5>
        <ul>
{chr(10).join(f'          <li><a href="{url(m)}">{m["titre"]}</a></li>' for m in METIERS)}
        </ul>
      </div>
      <div>
        <h5>Nous joindre</h5>
        <ul class="f-contact">
          <li><svg class="ic"><use href="#i-pin"/></svg><a href="{MAPS_OUVRIR}" target="_blank" rel="noopener">Angré Star 14, Cocody — Abidjan<br>Localisation : {PLUS_CODE}</a></li>
          <li><svg class="ic"><use href="#i-phone"/></svg>{PHONE}</li>
          <li><svg class="ic"><use href="#i-chat"/></svg><a href="{wa_link('Bonjour EchoResta')}" target="_blank" rel="noopener">WhatsApp : {WHATSAPP_AFFICHE}</a></li>
          <li><svg class="ic"><use href="#i-mail"/></svg>contact@echoresta.ci</li>
          <li><svg class="ic"><use href="#i-clock"/></svg>Lun – Ven : 8h00 – 17h00</li>
        </ul>
      </div>
    </div>
    <div class="bottom">
      <span>© 2026 EchoResta — Hôtellerie &amp; Restauration. Tous droits réservés.</span>
      <span>Abidjan, Côte d’Ivoire</span>
    </div>
  </div>
</footer>
'''

MAP = f'''<section class="map">
  <div class="container map-head">
    <div class="map-info">
      <span class="map-pin"><svg class="ic"><use href="#i-pin"/></svg></span>
      <div><b>Angré Star 14, Cocody — Abidjan</b><span>Code de localisation Google : <strong>{PLUS_CODE}</strong> · Lun – Ven, 8h – 17h</span></div>
    </div>
    <div class="map-actions">
      <a class="btn btn-red" href="{MAPS_ITINERAIRE}" target="_blank" rel="noopener">Itinéraire</a>
      <a class="btn btn-outline" href="{MAPS_OUVRIR}" target="_blank" rel="noopener">Ouvrir dans Google Maps</a>
    </div>
  </div>
  <iframe loading="lazy" title="Carte : EchoResta, Angré Star 14 ({PLUS_CODE})"
    src="https://www.google.com/maps?q={GPS}&z=16&output=embed"></iframe>
</section>
'''


def page(file, title, desc, body, active, wa_text='Bonjour, je souhaite contacter le service commercial d’EchoResta.'):
    html = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
</head>
<body>

{icons}

{header(active)}
{body}
{FOOTER}
<a class="wa-float" href="{wa_link(wa_text)}" target="_blank" rel="noopener" aria-label="Contactez le service commercial sur WhatsApp"><svg class="ic"><use href="#i-chat"/></svg><span><small>WhatsApp</small>Contactez le service commercial</span></a>

<div class="search-overlay" id="search" hidden>
  <div class="search-box">
    <button class="search-close" aria-label="Fermer">&times;</button>
    <input type="search" id="search-input" placeholder="Rechercher une formation, une page…" autocomplete="off">
    <ul id="search-results"></ul>
  </div>
</div>
<script src="assets/data.js"></script>
<script src="assets/main.js"></script>
</body>
</html>
'''
    (OUT / file).write_text(html)


def page_hero(title, crumb, img, sub=''):
    sub = f'\n    <p class="hero-sub">{sub}</p>' if sub else ''
    return f'''<section class="page-hero" style="background-image:url('{img}')">
  <div class="container">
    <h1>{title}</h1>
    <div class="crumbs"><a href="index.html">Accueil</a><span>/</span>{crumb}</div>{sub}
  </div>
</section>
'''


def quiz_question_html(i):
    """Première question écrite dans la page, pour qu'elle s'affiche avant le script."""
    q = QUIZ[i]
    answers = '\n'.join(f'          <button type="button" data-i="{j}">{label}</button>' for j, (label, _) in enumerate(q['r']))
    return f'''        <div class="quiz-progress"><span style="width:0%"></span></div>
        <p class="quiz-count">Question 1 / {len(QUIZ)}</p>
        <h3>{q['q']}</h3>
        <div class="quiz-answers">
{answers}
        </div>'''


# =========================================================== Accueil
metier_tiles = '\n'.join(f'''      <a class="metier" href="{url(m)}">
        <span class="m-ico"><svg class="ic"><use href="#{m['icon']}"/></svg></span>
        <span class="m-cat">{CATEGORIES[m['cat']]}</span>
        <b>{m['titre']}</b>
        <span class="m-court">{m['court']}</span>
        <span class="m-dur"><svg class="ic"><use href="#i-clock"/></svg>{m['duree']}</span>
      </a>''' for m in METIERS)

SECTION_METIERS = f'''<section class="metiers center" id="metiers">
  <div class="container">
    <div class="eyebrow">{len(METIERS)} formations métiers</div>
    <h2>Choisissez votre futur métier</h2>
    <div class="sep"></div>
    <p class="lead">De la cuisine à la direction d’hôtel : des formations courtes et pratiques pour entrer vite dans la vie active.</p>
    <div class="metier-grid">
{metier_tiles}
    </div>
    <a href="formations.html" class="btn btn-outline">Voir toutes les formations <svg class="ic"><use href="#i-arrow"/></svg></a>
  </div>
</section>

'''

WHY = [('i-building', 'Stage garanti', 'Chaque stagiaire qui valide sa formation part en stage dans l’un de nos 40 hôtels partenaires.'),
       ('i-users', 'Formateurs du métier', 'Chefs, maîtres d’hôtel, gouvernantes : nos formateurs exercent dans les établissements d’Abidjan.'),
       ('i-award', 'Double certification', 'L’attestation EchoResta et une certification professionnelle reconnue par le secteur.'),
       ('i-chef', 'On apprend en faisant', 'Ateliers en cuisine, en salle, au bar et en chambre : vous pratiquez à chaque séance.'),
       ('i-clock', 'Formations courtes', 'De 2 à 6 mois pour être opérationnel et décrocher un premier poste.'),
       ('i-target', 'Accompagnement vers l’emploi', 'CV, préparation aux entretiens et mise en relation avec les établissements qui recrutent.')]

SECTION_WHY_QUIZ = f'''<section class="why">
  <div class="container">
    <div class="center">
      <div class="eyebrow">Pourquoi EchoResta</div>
      <h2>Ce qui fait la différence</h2>
      <div class="sep"></div>
    </div>
    <div class="why-grid">
{chr(10).join(f'      <div class="why-item"><svg class="ic"><use href="#{i}"/></svg><h3>{t}</h3><p>{d}</p></div>' for i, t, d in WHY)}
    </div>
  </div>
</section>

<section class="quiz-band bg-soft" id="quiz">
  <div class="container quiz-wrap">
    <div class="quiz-intro">
      <div class="eyebrow">Test d’orientation · 30 secondes</div>
      <h2>Quel métier est fait pour vous ?</h2>
      <div class="sep"></div>
      <p>Trois questions pour découvrir la formation qui vous correspond le mieux. Pas besoin de laisser vos coordonnées.</p>
    </div>
    <div class="quiz-card" id="quiz-card" aria-live="polite">
{quiz_question_html(0)}
    </div>
  </div>
</section>

'''

home = (S / 'home-body.html').read_text()
home = (home.replace('href="#inscription" class="btn btn-red">S’inscrire à une session', 'href="contact.html#formulaire" class="btn btn-red">S’inscrire à une session')
            .replace('href="#apropos" class="btn btn-ghost"', 'href="apropos.html" class="btn btn-ghost"')
            .replace('<a href="#" class="btn btn-outline">', '<a href="apropos.html" class="btn btn-outline">')
            .replace('href="#contact" class="btn btn-red">Commencer', 'href="formations.html" class="btn btn-red">Commencer')
            .replace('<section class="stats center" id="formations">', SECTION_METIERS + '<section class="stats center" id="chiffres">')
            .replace('<section class="testimonials">', SECTION_WHY_QUIZ + '<section class="testimonials">'))
assert 'id="metiers"' in home and 'id="quiz"' in home
# La galerie renvoie vers les formations correspondantes
for img, slug in [('galerie-1', 'maitre-hotel'), ('galerie-2', 'cuisinier'), ('galerie-3', 'gouvernante'),
                  ('galerie-4', 'anglais-tourisme-hotellerie'), ('galerie-5', 'bar-mixology'), ('galerie-6', 'serveur-hotesse')]:
    home = re.sub(rf'<a href="#"><img src="images/{img}', f'<a href="formation-{slug}.html"><img src="images/{img}', home)
page('index.html', 'EchoResta — Hôtellerie & Restauration',
     'Cabinet de formation en hôtellerie et restauration à Abidjan : 10 formations métiers, stage garanti.', home + MAP, 'index.html')

# =========================================================== À propos
values = [('i-target', 'Notre mission', 'Former des professionnels opérationnels dès le premier jour, capables de répondre aux standards de l’hôtellerie internationale.'),
          ('i-eye', 'Notre vision', 'Faire d’Abidjan une référence régionale de l’excellence hôtelière, en élevant le niveau de toute la profession.'),
          ('i-heart', 'Nos valeurs', 'Rigueur, sens du service, bienveillance et transmission : ce que nos formateurs pratiquent chaque jour en entreprise.')]
team = [('galerie-2.jpg', 'Chef Marc Kouadio', 'Formateur cuisine'),
        ('galerie-3.jpg', 'Awa Bamba', 'Formatrice gouvernante'),
        ('galerie-5.jpg', 'David Yao', 'Formateur bar & mixologie'),
        ('galerie-6.jpg', 'Serge Konan', 'Formateur service en salle')]
about = page_hero('À propos d’EchoResta', 'À propos', 'images/galerie-1.jpg') + f'''
<section>
  <div class="container split">
    <div class="img"><img src="images/galerie-3.jpg" alt="Formatrice EchoResta"></div>
    <div>
      <div class="eyebrow">Notre histoire</div>
      <h2>Un cabinet né sur le terrain</h2>
      <div class="sep"></div>
      <p>EchoResta a été fondé par des professionnels de l’hôtellerie et de la restauration ivoiriennes, convaincus qu’un métier de service s’apprend d’abord en le pratiquant. Depuis nos premières promotions, nous associons cours théoriques, ateliers pratiques et immersion en entreprise.</p>
      <p>Aujourd’hui, plus de 2500 stagiaires ont été formés et travaillent dans les hôtels, restaurants et établissements partenaires d’Abidjan et de la sous-région.</p>
      <ul class="checks">
        <li><svg class="ic"><use href="#i-check"/></svg>Formateurs issus du secteur, en activité</li>
        <li><svg class="ic"><use href="#i-check"/></svg>Double certification reconnue par la profession</li>
        <li><svg class="ic"><use href="#i-check"/></svg>Stage garanti dans l’un de nos 40 hôtels partenaires</li>
      </ul>
      <a href="formations.html" class="btn btn-outline">Voir nos formations <svg class="ic"><use href="#i-arrow"/></svg></a>
    </div>
  </div>
</section>

<section class="bg-soft center">
  <div class="container">
    <h2>Mission, vision et valeurs</h2>
    <div class="sep"></div>
    <div class="cards">
{chr(10).join(f'      <div class="card"><div class="ico"><svg class="ic"><use href="#{i}"/></svg></div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in values)}
    </div>
  </div>
</section>

<section class="center">
  <div class="container">
    <h2>Nos formateurs</h2>
    <div class="sep"></div>
    <p class="muted" style="margin-top:30px">Des praticiens reconnus qui transmettent les gestes et les standards du métier.</p>
    <div class="team">
{chr(10).join(f'      <div class="member"><img src="images/{img}" alt="{n}"><div class="info"><h4>{n}</h4><span>{r}</span></div></div>' for img, n, r in team)}
    </div>
  </div>
</section>

<section class="banner" style="padding:110px 0 120px">
  <div class="container">
    <h2>Prêt à lancer votre carrière ?</h2>
    <p>Les inscriptions pour la prochaine session sont ouvertes.</p>
    <a href="contact.html#formulaire" class="btn btn-red">S’inscrire à une session</a>
  </div>
</section>
'''
page('apropos.html', 'À propos — EchoResta', 'Histoire, mission et formateurs du cabinet EchoResta.', about, 'apropos.html')

# =========================================================== Formations
cards = '\n'.join(f'''      <article class="course" id="{m['slug']}" data-cat="{m['cat']}">
        <a class="c-ico" href="{url(m)}" tabindex="-1" aria-hidden="true"><svg class="ic"><use href="#{m['icon']}"/></svg></a>
        <div class="body">
          <span class="tag">{CATEGORIES[m['cat']]}</span>
          <h3><a href="{url(m)}">{m['titre']}</a></h3>
          <p>{m['resume']}</p>
          <div class="meta">
            <span><svg class="ic"><use href="#i-clock"/></svg>{m['duree']}</span>
            <span><svg class="ic"><use href="#i-level"/></svg>{m['niveau']}</span>
            <span><svg class="ic"><use href="#i-award"/></svg>Certifiante</span>
          </div>
          <div class="links"><a class="more" href="{url(m)}">Découvrir <svg class="ic"><use href="#i-arrow"/></svg></a><a class="more alt" href="contact.html?formation={m['slug']}#formulaire">S’inscrire</a></div>
        </div>
      </article>''' for m in METIERS)
steps = [('Choisissez', 'Sélectionnez la formation qui correspond à votre projet professionnel.'),
         ('Inscrivez-vous', 'Remplissez le formulaire, nous vous rappelons sous 48 h.'),
         ('Formez-vous', 'Cours pratiques en petits groupes, encadrés par des professionnels.'),
         ('Décrochez votre stage', 'Immersion dans un hôtel partenaire et remise de votre double certification.')]
faq = [('Quels sont les prérequis pour s’inscrire ?', 'La plupart de nos formations sont ouvertes dès 16 ans, sans diplôme exigé. Un entretien de motivation est réalisé avant l’inscription.'),
       ('Les formations sont-elles certifiantes ?', 'Oui. Chaque parcours donne lieu à une double certification : l’attestation EchoResta et une certification professionnelle reconnue par le secteur.'),
       ('Le stage est-il vraiment garanti ?', 'Oui, chaque stagiaire ayant validé sa formation est placé en stage dans l’un de nos 40 hôtels et restaurants partenaires.'),
       ('Quels sont vos horaires ?', 'Nous vous accueillons du lundi au vendredi, de 8h à 17h. Selon la formation, les cours ont lieu le matin ou l’après-midi : contactez-nous pour connaître le prochain calendrier.'),
       ('Je ne sais pas quel métier choisir. Que faire ?', 'Faites notre test d’orientation en trois questions sur la page d’accueil, ou écrivez-nous sur WhatsApp : un conseiller vous aide à choisir.'),
       ('Peut-on payer en plusieurs fois ?', 'Oui, un échéancier peut être mis en place. Les modalités vous sont présentées lors de l’entretien d’inscription.')]
formations = page_hero('Nos formations', 'Formations', 'images/hero.jpg',
                       f'{len(METIERS)} métiers de l’hôtellerie et de la restauration, avec stage garanti en entreprise.') + f'''
<section class="center">
  <div class="container">
    <h2>Choisissez votre parcours</h2>
    <div class="sep"></div>
    <p class="muted" style="margin-top:30px">Vous hésitez ? <a class="link" href="index.html#quiz">Faites le test d’orientation</a> en 30 secondes.</p>
    <div class="filters">
      <button class="active" data-f="all">Toutes ({len(METIERS)})</button>
{chr(10).join(f'      <button data-f="{k}">{v} ({len(BY_CAT[k])})</button>' for k, v in CATEGORIES.items())}
    </div>
    <div class="courses">
{cards}
    </div>
  </div>
</section>

<section class="bg-soft center">
  <div class="container">
    <h2>Comment ça marche ?</h2>
    <div class="sep"></div>
    <div class="steps">
{chr(10).join(f'      <div class="step"><h4>{t}</h4><p>{d}</p></div>' for t, d in steps)}
    </div>
  </div>
</section>

<section class="center">
  <div class="container">
    <h2>Questions fréquentes</h2>
    <div class="sep"></div>
    <div class="faq">
{chr(10).join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)}
    </div>
  </div>
</section>
'''
page('formations.html', 'Formations — EchoResta', 'Les 10 formations métiers EchoResta en hôtellerie et restauration.', formations, 'formations.html')

# =========================================================== Pages métier
LADDER_LABELS = ['Après la formation', 'Avec l’expérience', 'Ensuite', 'À terme']
for old in OUT.glob('formation-*.html'):
    old.unlink()
for m in METIERS:
    visual = (f'<img class="detail-img" src="images/{m["photo"]}" alt="{m["titre"]}">' if m['photo']
              else f'<div class="icon-panel" role="img" aria-label="{m["titre"]}"><svg class="ic"><use href="#{m["icon"]}"/></svg></div>')
    savoir = '\n'.join(f'        <li><svg class="ic"><use href="#i-check"/></svg>{s}</li>' for s in m['savoir'])
    modules = '\n'.join(f'        <li><b>{t}</b><span>{d}</span></li>' for t, d in m['modules'])
    journee = '\n'.join(f'        <li><time>{h}</time><span>{t}</span></li>' for h, t in m['journee'])
    ladder = '\n'.join(f'        <li><small>{LADDER_LABELS[i]}</small>{step}</li>' for i, step in enumerate(m['carriere']))
    qualites = ''.join(f'<span>{q}</span>' for q in m['qualites'])
    lieux = ''.join(f'<span>{q}</span>' for q in m['lieux'])
    others = [o for o in BY_CAT[m['cat']] if o is not m] or BY_CAT['hotellerie'][:3]
    others = '\n'.join(f'        <li><a href="{url(o)}">{o["titre"]}</a></li>' for o in others)
    others += '\n        <li><a href="formations.html">Toutes les formations →</a></li>'
    body = page_hero(m['titre'], f'<a href="formations.html">Formations</a><span>/</span>{m["titre"]}',
                     f'images/{m["fond"]}', m['accroche']) + f'''
<section>
  <div class="container detail">
    <div class="detail-main">
      {visual}

      <div class="eyebrow" style="margin-top:40px">{CATEGORIES[m['cat']]}</div>
      <h2>Le métier en bref</h2>
      <div class="sep"></div>
      <p class="lead-p">{m['resume']} Une formation pratique, animée par des professionnels en activité, pour être opérationnel dès votre premier poste.</p>

      <h3 class="h3">Ce que vous saurez faire</h3>
      <ul class="checks two">
{savoir}
      </ul>

      <h3 class="h3">Le programme</h3>
      <ol class="modules">
{modules}
      </ol>

      <h3 class="h3">{m.get('journee_titre', 'Une journée type')}</h3>
      <ol class="timeline">
{journee}
      </ol>

      <h3 class="h3">Votre évolution de carrière</h3>
      <ol class="ladder">
{ladder}
      </ol>

      <div class="duo">
        <div>
          <h3 class="h3">Les qualités qui comptent</h3>
          <div class="chips">{qualites}</div>
        </div>
        <div>
          <h3 class="h3">Où travailler ?</h3>
          <div class="chips">{lieux}</div>
        </div>
      </div>
    </div>

    <aside class="detail-side">
      <div class="side-box">
        <h4>Infos pratiques</h4>
        <dl>
          <div><dt><svg class="ic"><use href="#i-clock"/></svg>Durée</dt><dd>{m['duree']}</dd></div>
          <div><dt><svg class="ic"><use href="#i-level"/></svg>Niveau</dt><dd>{m['niveau']}</dd></div>
          <div><dt><svg class="ic"><use href="#i-clock2"/></svg>Rythme</dt><dd>{m['rythme']}</dd></div>
          <div><dt><svg class="ic"><use href="#i-users"/></svg>Public</dt><dd>{m['public']}</dd></div>
          <div><dt><svg class="ic"><use href="#i-award"/></svg>Certification</dt><dd>Double certification</dd></div>
          <div><dt><svg class="ic"><use href="#i-building"/></svg>Stage</dt><dd>Garanti en entreprise</dd></div>
        </dl>
        <a href="contact.html?formation={m['slug']}#formulaire" class="btn btn-red" style="width:100%;justify-content:center">S’inscrire à cette formation</a>
        <a href="{wa_link('Bonjour EchoResta, je suis intéressé(e) par la formation ' + m['titre'] + '.')}" target="_blank" rel="noopener" class="side-call"><svg class="ic"><use href="#i-chat"/></svg>Poser une question sur WhatsApp</a>
      </div>
      <div class="side-box light">
        <h4>Autres formations</h4>
        <ul class="side-links">
{others}
        </ul>
      </div>
    </aside>
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>Prêt(e) à vous lancer ?</h2>
    <p>Les inscriptions pour la prochaine session sont ouvertes. Réservez votre place dès maintenant.</p>
    <div class="actions">
      <a href="contact.html?formation={m['slug']}#formulaire" class="btn btn-red">Je m’inscris</a>
      <a href="formations.html" class="btn btn-ghost">Voir les autres formations</a>
    </div>
  </div>
</section>
'''
    page(url(m), f'Formation {m["titre"]} — EchoResta', m['resume'], body, 'formations.html',
         f'Bonjour, je souhaite contacter le service commercial d’EchoResta au sujet de la formation {m["titre"]}.')

# =========================================================== Contact
options = '\n'.join(
    f'              <optgroup label="{CATEGORIES[c]}">\n' +
    '\n'.join(f'                <option value="{m["slug"]}">{m["titre"]}</option>' for m in BY_CAT[c]) +
    '\n              </optgroup>' for c in CATEGORIES)
contact = page_hero('Contact &amp; inscription', 'Contact', 'images/galerie-3.jpg') + f'''
<section>
  <div class="container contact-grid">
    <aside class="info-box">
      <h3>Parlons de votre projet</h3>
      <p>Une question sur nos formations ou une inscription ? Notre équipe vous répond sous 48 h.</p>
      <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-pin"/></svg></div><div><strong>Adresse</strong><span>Angré Star 14, Cocody<br>Abidjan, Côte d’Ivoire<br>Code de localisation : <a href="{MAPS_OUVRIR}" target="_blank" rel="noopener">{PLUS_CODE}</a></span></div></div>
      <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-phone"/></svg></div><div><strong>Téléphone</strong><span>{PHONE}</span></div></div>
      <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-chat"/></svg></div><div><strong>WhatsApp</strong><span><a href="{wa_link('Bonjour EchoResta')}" target="_blank" rel="noopener">{WHATSAPP_AFFICHE}</a></span></div></div>
      <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-mail"/></svg></div><div><strong>E-mail</strong><span>contact@echoresta.ci</span></div></div>
      <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-clock"/></svg></div><div><strong>Horaires</strong><span>Lundi – Vendredi : 8h00 – 17h00</span></div></div>
    </aside>

    <div class="form" id="formulaire" style="scroll-margin-top:140px">
      <form id="form-contact" novalidate>
        <div class="eyebrow">Formulaire</div>
        <h3>Envoyez-nous un message</h3>
        <div class="row">
          <div><label for="nom">Nom complet *</label><input id="nom" name="nom" required autocomplete="name"></div>
          <div><label for="tel">Téléphone *</label><input id="tel" name="tel" type="tel" required autocomplete="tel" placeholder="+225"></div>
          <div><label for="email">E-mail *</label><input id="email" name="email" type="email" required autocomplete="email"></div>
          <div><label for="objet">Objet</label>
            <select id="objet" name="objet">
              <option value="information">Demande d’information</option>
              <option value="inscription">Inscription à une session</option>
              <option value="partenariat">Partenariat entreprise</option>
            </select></div>
          <div class="full"><label for="formation">Formation souhaitée</label>
            <select id="formation" name="formation">
              <option value="">— Je ne sais pas encore —</option>
{options}
            </select></div>
          <div class="full"><label for="message">Message</label><textarea id="message" name="message"></textarea></div>
        </div>
        <label class="consent"><input type="checkbox" required> J’accepte d’être recontacté(e) par EchoResta au sujet de ma demande.</label>
        <button type="submit" class="btn btn-red">Envoyer ma demande</button>
      </form>
      <div class="form-ok" id="form-ok" hidden>
        <h3>Merci, votre demande est envoyée !</h3>
        <p class="muted">Notre équipe vous recontactera sous 48 h.</p>
      </div>
    </div>
  </div>
</section>
''' + MAP
page('contact.html', 'Contact — EchoResta', 'Contactez EchoResta ou inscrivez-vous à une session.', contact, 'contact.html')

# =========================================================== 404
page('404.html', 'Page introuvable — EchoResta', 'Page introuvable.', '''
<section class="center" style="padding:140px 0">
  <div class="container">
    <div class="eyebrow">Erreur 404</div>
    <h2>Cette page est introuvable</h2>
    <div class="sep"></div>
    <p class="muted" style="margin:30px 0 36px">La page demandée n’existe pas ou a été déplacée.</p>
    <a href="index.html" class="btn btn-red">Retour à l’accueil</a>
  </div>
</section>
''', '')

# =========================================================== Données pour la recherche et le test
index = [{'t': 'Accueil', 'u': 'index.html', 'd': 'Présentation du cabinet EchoResta'},
         {'t': 'À propos', 'u': 'apropos.html', 'd': 'Histoire, mission, valeurs et formateurs'},
         {'t': 'Nos formations', 'u': 'formations.html', 'd': 'Les 10 formations, étapes d’inscription et FAQ'},
         {'t': 'Test d’orientation', 'u': 'index.html#quiz', 'd': 'Quel métier est fait pour vous ? Trois questions'},
         {'t': 'Contact & inscription', 'u': 'contact.html', 'd': 'Coordonnées, formulaire et plan d’accès'}]
for m in METIERS:
    kw = ' '.join([CATEGORIES[m['cat']], *(t for t, _ in m['modules']), *m['carriere'], *m['lieux']])
    index.append({'t': m['titre'], 'u': url(m), 'd': m['resume'], 'k': kw})
data = {
    'SEARCH_INDEX': index,
    'METIERS': [{'slug': m['slug'], 'titre': m['titre'], 'icon': m['icon'], 'accroche': m['accroche'], 'duree': m['duree']} for m in METIERS],
    'QUIZ': [{'q': q['q'], 'r': [[label, pts] for label, pts in q['r']]} for q in QUIZ],
}
(OUT / 'assets' / 'data.js').write_text(''.join(f'window.{k}={json.dumps(v, ensure_ascii=False)};\n' for k, v in data.items()))
old_index = OUT / 'assets' / 'search-index.js'
if old_index.exists():
    old_index.unlink()
print('ok :', len(list(OUT.glob('*.html'))), 'pages')
