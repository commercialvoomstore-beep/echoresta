"""Génère les pages statiques du site EchoResta.

Usage : python3 _build/build.py   (depuis la racine du dépôt)
En-tête, pied de page, icônes et contenus des formations sont partagés entre toutes les pages.
"""
import json, pathlib, sys
from urllib.parse import quote

S = pathlib.Path(__file__).resolve().parent
OUT = S.parent
sys.path.insert(0, str(S))
from metiers import CATEGORIES, METIERS, QUIZ  # noqa: E402
import seo  # noqa: E402
import drapeaux  # noqa: E402
from PIL import Image  # noqa: E402

PHONE = '+225 07 68 84 20 38'
WHATSAPP = '2250768842038'  # numéro WhatsApp au format international, sans + ni espaces
WHATSAPP_AFFICHE = '+225 07 68 84 20 38'
EMAIL = 'contact@echoresta.ci'  # adresse qui reçoit les demandes de rendez-vous et de contact
PLUS_CODE = '92JH+FW'  # code de localisation Google (Plus Code) du centre, à Abidjan
GPS = '5.381188,-3.970187'  # coordonnées correspondant au Plus Code
LIEU = quote(f'{PLUS_CODE} Abidjan')  # Google Maps reconnaît le Plus Code et y place son repère
MAPS_ITINERAIRE = f'https://www.google.com/maps/dir/?api=1&destination={LIEU}'
MAPS_OUVRIR = f'https://www.google.com/maps/search/?api=1&query={LIEU}'
BY_CAT = {k: [m for m in METIERS if m['cat'] == k] for k in CATEGORIES}
LAT, LNG = (float(x) for x in GPS.split(','))
PAGES_PUBLIEES = []  # (fichier, robots) : sert au plan du site (sitemap.xml)


def taille(img):
    """Largeur et hauteur d'une image du dossier images/, pour réserver sa place à l'affichage."""
    w, h = Image.open(OUT / 'images' / img).size
    return f'width="{w}" height="{h}"'

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

NAV = [('index.html', 'Accueil'), ('formations.html', 'Formations'), ('apropos.html', 'À propos'),
       ('rendez-vous.html', 'Rendez-vous'), ('contact.html', 'Contact')]


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
      <div class="brand-logo"><img src="images/logo.png" alt="Logo EchoResta" width="92" height="92"></div>
      <div>
        <div class="brand-name">EchoResta</div>
        <div class="brand-tag">École de l’Hôtellerie &amp; Restauration</div>
      </div>
    </a>
    <nav class="main" id="nav">
{links}
      <button class="search-btn" aria-label="Rechercher"><svg class="ic"><use href="#i-search"/></svg></button>
      <a href="inscription.html" class="btn btn-red nav-cta">S’inscrire</a>
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
        <p>École de formation en hôtellerie et restauration à Abidjan. Double certification internationale (Côte d’Ivoire &amp; Australie) et stage de 6 mois garanti dans les plus grands hôtels.</p>
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
      <span>© 2026 EchoResta — École de l’Hôtellerie &amp; Restauration. Tous droits réservés.</span>
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
  <!-- inert : la carte ne peut pas prendre le focus ni faire défiler la page ; un clic l'ouvre dans Google Maps -->
  <div class="map-frame">
    <iframe inert tabindex="-1" loading="lazy" title="Carte : EchoResta, Angré Star 14 ({PLUS_CODE})"
      src="https://www.google.com/maps?q={LIEU}&z=17&output=embed"></iframe>
    <a class="map-overlay" href="{MAPS_OUVRIR}" target="_blank" rel="noopener"><span><svg class="ic"><use href="#i-pin"/></svg>Voir {PLUS_CODE} dans Google Maps</span></a>
  </div>
</section>
'''


def page(file, title, desc, body, active, wa_text='Bonjour, je souhaite contacter le service commercial d’EchoResta.',
         schemas=(), image='hero-cuisine.jpg', robots='index, follow'):
    canonical = seo.BASE_URL + ('' if file == 'index.html' else file)
    PAGES_PUBLIEES.append((file, robots))
    html = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{seo.SITE_NAME}">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{seo.BASE_URL}images/{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#13296b">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
{seo.balises_json_ld(schemas)}
</head>
<body>

{icons}

{header(active)}
{body}
{FOOTER}
<a class="wa-float" href="{wa_link(wa_text)}" target="_blank" rel="noopener" aria-label="Contactez-nous sur WhatsApp"><svg class="ic"><use href="#i-chat"/></svg><span><small>WhatsApp</small>Contactez-nous</span></a>

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
STEPS = [('Choisissez', 'Sélectionnez la formation qui correspond à votre projet professionnel.'),
         ('Inscrivez-vous', 'Remplissez la fiche d’inscription en ligne, nous vous rappelons sous 48 h.'),
         ('Formez-vous', 'Cours pratiques en petits groupes, encadrés par des professionnels.'),
         ('Décrochez votre stage', 'Stage de 6 mois dans l’un des plus grands hôtels et remise de votre double certification internationale.')]

FIGURES = [('97', '%', 'de diplômés'), ('30', '+', 'formateurs certifiés'), ('40', '', 'hôtels partenaires'), ('2500', '', 'stagiaires formés')]

POLES = [('Hôtellerie &amp; tourisme', 'i-building', 'Hébergement, réception, direction d’établissement et anglais professionnel.',
          BY_CAT['hotellerie'] + BY_CAT['langues']),
         ('Restauration &amp; arts culinaires', 'i-chef', 'Service en salle, cuisine, bar et direction de restaurant.',
          BY_CAT['restauration'])]

APPROCHE = [('i-building', 'Stage de 6 mois garanti', 'Chaque stagiaire qui valide sa formation effectue un stage de 6 mois dans les plus grands hôtels.'),
            ('i-award', 'Double certification internationale', 'Une double certification reconnue en Côte d’Ivoire et en Australie.'),
            ('i-users', 'Des formateurs du métier', 'Chefs, maîtres d’hôtel, gouvernantes : des praticiens qui exercent dans les établissements d’Abidjan.'),
            ('i-chef', 'La pratique avant tout', 'Ateliers en cuisine, en salle, au bar et en chambre : vous pratiquez à chaque séance.')]



def pole_html(titre, icon, desc, items):
    rows = '\n'.join(f'''          <li><a href="{url(m)}">
            <span class="r-ico"><svg class="ic"><use href="#{m['icon']}"/></svg></span>
            <span class="r-txt"><b>{m['titre']}</b><small>{m['court']}</small></span>
            <svg class="ic r-go"><use href="#i-arrow"/></svg>
          </a></li>''' for m in items)
    return f'''      <div class="h-pole">
        <div class="h-pole-head">
          <span class="h-pole-ico"><svg class="ic"><use href="#{icon}"/></svg></span>
          <div><h3>{titre}</h3><p>{desc}</p></div>
          <span class="h-count">{len(items)} formations</span>
        </div>
        <ul class="h-rows">
{rows}
        </ul>
      </div>'''


ANCRES = {'cuisinier': 'cuisinier', 'serveur-hotesse': 'serveur et hôtesse', 'audit-nuit': 'réceptionniste',
          'valet-femme-chambre': 'femme et valet de chambre', 'gouvernante': 'gouvernante', 'bar-mixology': 'barman',
          'maitre-hotel': 'maître d’hôtel'}
liens_metiers = ', '.join(f'<a class="link" href="formation-{slug}.html">{txt}</a>' for slug, txt in ANCRES.items())
liens_metiers += ', ainsi que le <a class="link" href="formation-directeur-hotel.html">management hôtelier</a>, la <a class="link" href="formation-directeur-restaurant.html">gestion de restaurant</a> et l’<a class="link" href="formation-anglais-tourisme-hotellerie.html">anglais professionnel</a>'
LOCAL_HTML = '''<section class="h-local" id="ecole-abidjan">
  <div class="container h-local-grid">
    <div>
      <div class="eyebrow">Votre école à Abidjan</div>
      <h2>Se former aux métiers de l’hôtellerie et de la restauration à Abidjan</h2>
      <div class="sep"></div>
      <p>Abidjan accueille chaque année de nombreux voyageurs d’affaires, touristes et grands événements, et de nouveaux hôtels et restaurants y ouvrent régulièrement. Ces établissements recherchent du personnel formé aux standards internationaux.</p>
      <p>École de l’hôtellerie et de la restauration située à Angré Star 14, dans la commune de Cocody, EchoResta prépare aux métiers les plus demandés : {liens_metiers}. Nos formations sont ouvertes aux stagiaires de toutes les communes d’Abidjan et de l’intérieur du pays.</p>
      <a class="link-arrow" href="contact.html">Nous rendre visite à Angré <svg class="ic"><use href="#i-arrow"/></svg></a>
    </div>
    <div>
      <h3 class="h-faq-title">Questions fréquentes</h3>
      <div class="faq">
{faq}
      </div>
    </div>
  </div>
</section>

'''.format(liens_metiers=liens_metiers, faq='\n'.join(f'        <details><summary>{q}</summary><p>{r}</p></details>' for q, r in seo.ACCUEIL_FAQ))

home = f'''<section class="h-hero">
  <div class="h-hero-media"><img src="images/hero-cuisine.jpg" alt="Brigade de cuisine en formation à l’école hôtelière EchoResta d’Abidjan" {taille("hero-cuisine.jpg")} fetchpriority="high">
    <img class="h-hero-alt" src="images/apropos-diplomes.jpg" alt="Remise des diplômes des stagiaires de l’école hôtelière EchoResta à Abidjan" {taille("apropos-diplomes.jpg")} decoding="async"></div>
  <div class="container">
    <div class="h-hero-text">
      <h1 class="h-kicker">École de l’hôtellerie et de la restauration à Abidjan</h1>
      <p class="h-title">Inspiration, Savoir-faire et Excellence</p>
      <p>Toute belle carrière commence par une bonne formation. Avec EchoResta, acquérez les gestes et les standards de l’hôtellerie et de la restauration pour gravir les échelons du métier.</p>
      <div class="h-actions">
        <a href="formations.html" class="btn btn-red">Découvrir nos formations</a>
        <a href="inscription.html" class="btn btn-ghost">S’inscrire à une session</a>
      </div>
      <ul class="h-hero-points">
        <li><svg class="ic"><use href="#i-check"/></svg>Stage de 6 mois garanti</li>
        <li><svg class="ic"><use href="#i-check"/></svg>Double certification internationale</li>
        <li><svg class="ic"><use href="#i-check"/></svg>Formateurs du secteur</li>
      </ul>
    </div>
  </div>
</section>

<section class="h-figures" aria-label="Chiffres clés">
  <div class="container">
    <div class="h-figures-card">
{chr(10).join(f'      <div><span class="num" data-to="{n}" data-suffix="{suf}">{n}{suf}</span><span>{label}</span></div>' for n, suf, label in FIGURES)}
    </div>
  </div>
</section>

<section class="h-about">
  <div class="container h-about-grid">
    <div>
      <div class="eyebrow">L’école</div>
      <h2>Quelques mots sur EchoResta</h2>
      <div class="sep"></div>
    </div>
    <div>
      <p class="h-lead">École de formation en hôtellerie et restauration basée à Abidjan, EchoResta prépare depuis plusieurs années des professionnels opérationnels dès le premier jour. Cuisine, service en salle, bar, réception, hébergement et anglais professionnel : chaque parcours est animé par des praticiens du secteur.</p>
      <p class="h-lead h-cert">Double certification internationale (Côte d’Ivoire &amp; Australie) et stage de 6 mois garanti dans les plus grands hôtels.</p>
      <blockquote class="h-pull">EchoResta est née d’une conviction : en partageant ce que l’on sait faire, on élève toute la profession.</blockquote>
      <a class="link-arrow" href="apropos.html">Découvrir l’école <svg class="ic"><use href="#i-arrow"/></svg></a>
    </div>
  </div>
</section>

<section class="h-poles bg-soft" id="formations">
  <div class="container">
    <div class="h-head">
      <div>
        <div class="eyebrow">Nos formations</div>
        <h2>Deux pôles, {len(METIERS)} métiers</h2>
      </div>
      <p>Des parcours pratiques, animés par des professionnels, pour entrer rapidement dans la vie active ou évoluer vers l’encadrement.</p>
    </div>
    <div class="h-poles-grid">
{chr(10).join(pole_html(*p) for p in POLES)}
    </div>
    <div class="h-more">
      <a class="btn btn-outline" href="formations.html">Voir le catalogue complet <svg class="ic"><use href="#i-arrow"/></svg></a>
      <a class="link" href="#quiz">Vous hésitez ? Faites le test d’orientation</a>
    </div>
  </div>
</section>

<section class="h-approach">
  <div class="container h-approach-grid">
    <div>
      <div class="h-kicker">Notre approche</div>
      <h2>Une formation tournée vers l’emploi</h2>
      <p>Chaque parcours associe cours, ateliers pratiques et immersion en entreprise, encadrés par des professionnels du secteur.</p>
      <a class="btn btn-ghost" href="apropos.html">Notre méthode</a>
    </div>
    <ul class="h-points">
{chr(10).join(f'      <li><svg class="ic"><use href="#{i}"/></svg><h3>{t}</h3><p>{d}</p></li>' for i, t, d in APPROCHE)}
    </ul>
  </div>
</section>

<section class="center h-steps">
  <div class="container">
    <div class="eyebrow">Inscription</div>
    <h2>Votre parcours en 4 étapes</h2>
    <div class="sep"></div>
    <div class="steps">
{chr(10).join(f'      <div class="step"><h4>{t}</h4><p>{d}</p></div>' for t, d in STEPS)}
    </div>
  </div>
</section>

<section class="h-quote bg-soft">
  <div class="container h-quote-grid">
    <img src="images/temoin-1.jpg" alt="Aminata Coulibaly, gouvernante diplômée d’EchoResta" {taille("temoin-1.jpg")} loading="lazy" decoding="async">
    <figure>
      <div class="eyebrow">Ils témoignent</div>
      <blockquote>Quand on travaille en hôtellerie et qu’on se forme en parallèle, il faut sacrifier du temps personnel. Mon ambition était non seulement d’obtenir ma certification, mais de tirer le meilleur de chaque heure passée en formation.</blockquote>
      <figcaption><b>Aminata Coulibaly</b><span>Gouvernante, promotion 2025</span></figcaption>
    </figure>
  </div>
</section>

<section class="quiz-band" id="quiz">
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

{LOCAL_HTML}<section class="banner h-cta">
  <div class="container">
    <h2>Plus de 2500 stagiaires nous font confiance</h2>
    <p>Rejoignez une communauté de professionnels de l’hôtellerie et de la restauration qui réussissent.</p>
    <div class="h-actions">
      <a href="inscription.html" class="btn btn-red">S’inscrire à une session</a>
      <a href="rendez-vous.html" class="btn btn-ghost">Prendre rendez-vous</a>
    </div>
  </div>
</section>
'''
page('index.html', *seo.PAGES['index.html'], home + MAP, 'index.html',
     schemas=[seo.ecole_schema(PHONE, LAT, LNG, PLUS_CODE), seo.site_schema(), seo.faq_schema(seo.ACCUEIL_FAQ)])

# =========================================================== À propos
values = [('i-target', 'Notre mission', 'Former des professionnels opérationnels dès le premier jour, capables de répondre aux standards de l’hôtellerie internationale.'),
          ('i-eye', 'Notre vision', 'Faire d’Abidjan une référence régionale de l’excellence hôtelière, en élevant le niveau de toute la profession.'),
          ('i-heart', 'Nos valeurs', 'Rigueur, sens du service, bienveillance et transmission : ce que nos formateurs pratiquent chaque jour en entreprise.')]
about = page_hero('EchoResta, école hôtelière à Abidjan', 'À propos', 'images/apropos-diplomes.jpg') + f'''
<section class="h-about">
  <div class="container h-about-grid">
    <div>
      <div class="eyebrow">Notre histoire</div>
      <h2>Une école née sur le terrain</h2>
      <div class="sep"></div>
    </div>
    <div class="story">
      <p>EchoResta a été fondée par des professionnels de l’hôtellerie et de la restauration ivoiriennes, convaincus qu’un métier de service s’apprend d’abord en le pratiquant. Depuis nos premières promotions, nous associons cours théoriques, ateliers pratiques et immersion en entreprise.</p>
      <p>Aujourd’hui, plus de 2500 stagiaires ont été formés et travaillent dans les hôtels, restaurants et établissements partenaires d’Abidjan et de la sous-région.</p>
      <ul class="checks">
        <li><svg class="ic"><use href="#i-check"/></svg>Formateurs issus du secteur, en activité</li>
        <li><svg class="ic"><use href="#i-check"/></svg>Double certification internationale (Côte d’Ivoire &amp; Australie)</li>
        <li><svg class="ic"><use href="#i-check"/></svg>Stage de 6 mois garanti dans les plus grands hôtels</li>
      </ul>
      <a href="formations.html" class="btn btn-outline">Voir nos formations <svg class="ic"><use href="#i-arrow"/></svg></a>
    </div>
  </div>
  <div class="container about-photo">
    <img src="images/apropos-diplomes.jpg" alt="Remise des diplômes des stagiaires de l’école hôtelière EchoResta à Abidjan" {taille("apropos-diplomes.jpg")} loading="lazy" decoding="async">
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

<section class="banner" style="padding:110px 0 120px">
  <div class="container">
    <h2>Prêt à lancer votre carrière ?</h2>
    <p>Les inscriptions pour la prochaine session sont ouvertes.</p>
    <a href="inscription.html" class="btn btn-red">S’inscrire à une session</a>
  </div>
</section>
'''
page('apropos.html', *seo.PAGES['apropos.html'], about, 'apropos.html', image='apropos-diplomes.jpg',
     schemas=[seo.fil_ariane(('Accueil', ''), ('À propos', 'apropos.html'))])

# =========================================================== Formations
cards = '\n'.join(f'''      <article class="course" id="{m['slug']}" data-cat="{m['cat']}">
        <a class="c-ico" href="{url(m)}" tabindex="-1" aria-hidden="true"><svg class="ic"><use href="#{m['icon']}"/></svg></a>
        <div class="body">
          <span class="tag">{CATEGORIES[m['cat']]}</span>
          <h3><a href="{url(m)}">{m['titre']}</a></h3>
          <p>{m['resume']}</p>
          <div class="meta">
            <span><svg class="ic"><use href="#i-level"/></svg>{m['niveau']}</span>
            <span><svg class="ic"><use href="#i-award"/></svg>Certifiante</span>
          </div>
          <div class="links"><a class="more" href="{url(m)}">Découvrir <svg class="ic"><use href="#i-arrow"/></svg></a><a class="more alt" href="inscription.html?formation={m['slug']}">S’inscrire</a></div>
        </div>
      </article>''' for m in METIERS)
steps = STEPS
faq = [('Quels sont les prérequis pour s’inscrire ?', 'La plupart de nos formations sont ouvertes dès 16 ans, sans diplôme exigé. Un entretien de motivation est réalisé avant l’inscription.'),
       ('Les formations sont-elles certifiantes ?', 'Oui. Chaque parcours donne lieu à une double certification internationale, reconnue en Côte d’Ivoire et en Australie.'),
       ('Le stage est-il vraiment garanti ?', 'Oui. Chaque stagiaire ayant validé sa formation effectue un stage de 6 mois garanti dans l’un des plus grands hôtels.'),
       ('Quels sont vos horaires ?', 'Nous vous accueillons du lundi au vendredi, de 8h à 17h. Selon la formation, les cours ont lieu le matin ou l’après-midi : contactez-nous pour connaître le prochain calendrier.'),
       ('Je ne sais pas quel métier choisir. Que faire ?', 'Faites notre test d’orientation en trois questions sur la page d’accueil, ou écrivez-nous sur WhatsApp : un conseiller vous aide à choisir.'),
       ('Peut-on payer en plusieurs fois ?', 'Oui, un échéancier peut être mis en place. Les modalités vous sont présentées lors de l’entretien d’inscription.')]
formations = page_hero('Formations en hôtellerie et restauration à Abidjan', 'Formations', 'images/formations-bandeau.jpg',
                       f'{len(METIERS)} métiers de l’hôtellerie et de la restauration, avec double certification internationale et stage de 6 mois garanti.') + f'''
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
page('formations.html', *seo.PAGES['formations.html'], formations, 'formations.html',
     schemas=[seo.fil_ariane(('Accueil', ''), ('Formations', 'formations.html')), seo.faq_schema(faq)])

# =========================================================== Pages métier
LADDER_LABELS = ['Après la formation', 'Avec l’expérience', 'Ensuite', 'À terme']
for old in OUT.glob('formation-*.html'):
    old.unlink()
for m in METIERS:
    paysage = m['photo'] and (lambda w, h: w / h >= 1.5)(*Image.open(OUT / 'images' / m['photo']).size)
    visual = (f'<img class="detail-img{"" if paysage else " crop"}" src="images/{m["photo"]}" alt="Formation {m["titre"].lower()} à Abidjan" {taille(m["photo"])} decoding="async">' if m['photo']
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
    meta = seo.METIERS_SEO[m['slug']]
    body = page_hero(meta['h1'], f'<a href="formations.html">Formations</a><span>/</span>{m["titre"]}',
                     f'images/{m["fond"]}', m['accroche']) + f'''
<section>
  <div class="container detail">
    <div class="detail-main">
      {visual}

      <div class="eyebrow" style="margin-top:40px">{CATEGORIES[m['cat']]}</div>
      <h2>Le métier en bref</h2>
      <div class="sep"></div>
      <p class="lead-p">{m['resume']} Une formation pratique, animée par des professionnels en activité, pour être opérationnel dès votre premier poste.</p>

      <h3 class="h3">Pourquoi suivre cette formation à Abidjan ?</h3>
      <p class="lead-p">{meta['pourquoi']}</p>

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
          <div><dt><svg class="ic"><use href="#i-level"/></svg>Niveau</dt><dd>{m['niveau']}</dd></div>
          <div><dt><svg class="ic"><use href="#i-users"/></svg>Public</dt><dd>{m['public']}</dd></div>
          <div><dt><svg class="ic"><use href="#i-award"/></svg>Certification</dt><dd>Double : Côte d’Ivoire &amp; Australie</dd></div>
          <div><dt><svg class="ic"><use href="#i-building"/></svg>Stage</dt><dd>6 mois garanti, grands hôtels</dd></div>
        </dl>
        <a href="inscription.html?formation={m['slug']}" class="btn btn-red" style="width:100%;justify-content:center">S’inscrire à cette formation</a>
        <a href="rendez-vous.html?formation={m['slug']}" class="btn btn-ghost side-rdv">Prendre rendez-vous</a>
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
      <a href="inscription.html?formation={m['slug']}" class="btn btn-red">Je m’inscris</a>
      <a href="formations.html" class="btn btn-ghost">Voir les autres formations</a>
    </div>
  </div>
</section>
'''
    page(url(m), meta['title'], meta['desc'], body, 'formations.html',
         f'Bonjour, je souhaite contacter le service commercial d’EchoResta au sujet de la formation {m["titre"]}.',
         schemas=[seo.cours_schema(m, meta), seo.fil_ariane(('Accueil', ''), ('Formations', 'formations.html'), (m['titre'], url(m)))],
         image=m['photo'] or 'hero-cuisine.jpg')

# =========================================================== Rendez-vous
MOTIFS = [('orientation', 'i-target', 'Entretien d’orientation', 'Être conseillé(e) pour choisir sa formation'),
          ('inscription', 'i-award', 'Inscription', 'Finaliser son inscription à une session'),
          ('visite', 'i-building', 'Visite de l’école', 'Découvrir nos locaux à Angré Star 14'),
          ('entreprise', 'i-case', 'Entreprise ou partenariat', 'Former vos équipes, accueillir nos stagiaires')]
CRENEAUX = [f'{h}h00 – {h + 1}h00' for h in range(8, 17)]
ETAPES_RDV = [('Choisissez votre créneau', 'Indiquez le motif, le jour et l’heure qui vous conviennent, du lundi au vendredi.'),
              ('Envoyez la demande', 'Remplissez vos coordonnées : votre demande nous est envoyée par e-mail.'),
              ('Recevez la confirmation', 'Notre équipe vous confirme le rendez-vous par e-mail ou par téléphone.'),
              ('Rencontrez un conseiller', 'À l’école, Angré Star 14, Cocody — ou par téléphone si vous préférez.')]
options_rdv = '\n'.join(
    f'              <optgroup label="{CATEGORIES[c]}">\n' +
    '\n'.join(f'                <option value="{m["slug"]}">{m["titre"]}</option>' for m in BY_CAT[c]) +
    '\n              </optgroup>' for c in CATEGORIES)
motifs_html = '\n'.join(f'''            <label class="choice"><input type="radio" name="motif" value="{t}" required{' checked' if i == 0 else ''}>
              <span><svg class="ic"><use href="#{ic}"/></svg><b>{t}</b><small>{d}</small></span></label>''' for i, (v, ic, t, d) in enumerate(MOTIFS))
creneaux_html = '\n'.join(f'            <label class="slot"><input type="radio" name="creneau" value="{c}" required><span>{c}</span></label>' for c in CRENEAUX)

rdv = page_hero('Prendre rendez-vous avec notre école à Abidjan', 'Rendez-vous', 'images/hero-cuisine.jpg',
                'Entretien d’orientation, inscription ou visite de l’école : choisissez votre créneau, nous vous confirmons le rendez-vous par e-mail.') + f'''
<section>
  <div class="container rdv-grid">
    <aside class="rdv-side">
      <div class="eyebrow">Comment ça se passe ?</div>
      <h2>Votre rendez-vous en 4 étapes</h2>
      <div class="sep"></div>
      <ol class="rdv-steps">
{chr(10).join(f'        <li><b>{t}</b><span>{d}</span></li>' for t, d in ETAPES_RDV)}
      </ol>
      <div class="info-box rdv-info">
        <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-pin"/></svg></div><div><strong>Adresse</strong><span>Angré Star 14, Cocody — Abidjan<br>Code de localisation : <a href="{MAPS_OUVRIR}" target="_blank" rel="noopener">{PLUS_CODE}</a></span></div></div>
        <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-clock"/></svg></div><div><strong>Horaires</strong><span>Lundi – Vendredi : 8h00 – 17h00</span></div></div>
        <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-mail"/></svg></div><div><strong>E-mail</strong><span>{EMAIL}</span></div></div>
        <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-phone"/></svg></div><div><strong>Téléphone</strong><span>{PHONE}</span></div></div>
        <a class="btn btn-ghost" href="{MAPS_ITINERAIRE}" target="_blank" rel="noopener">Itinéraire jusqu’à l’école</a>
      </div>
    </aside>

    <div class="form rdv-form" id="rendez-vous" style="scroll-margin-top:140px">
      <form id="form-rdv" data-mail="{EMAIL}" novalidate>
        <div class="eyebrow">Formulaire de rendez-vous</div>
        <h3>Réservez votre créneau</h3>

        <fieldset>
          <legend>1. Motif du rendez-vous</legend>
          <div class="choices">
{motifs_html}
          </div>
        </fieldset>

        <fieldset>
          <legend>2. Formation qui vous intéresse</legend>
          <select id="rdv-formation" name="formation" aria-label="Formation qui vous intéresse">
            <option value="">— Je ne sais pas encore —</option>
{options_rdv}
          </select>
        </fieldset>

        <fieldset>
          <legend>3. Jour et heure</legend>
          <label for="rdv-date">Date souhaitée * <small>(du lundi au vendredi)</small></label>
          <input id="rdv-date" name="date" type="date" required>
          <p class="field-error" id="rdv-date-err" hidden>Nous recevons du lundi au vendredi : choisissez un autre jour.</p>
          <p class="slot-label">Créneau horaire *</p>
          <div class="slots">
{creneaux_html}
          </div>
          <p class="field-error" id="rdv-slot-err" hidden>Choisissez un créneau horaire.</p>
        </fieldset>

        <fieldset>
          <legend>4. Vos coordonnées</legend>
          <div class="row">
            <div><label for="rdv-nom">Nom complet *</label><input id="rdv-nom" name="nom" required autocomplete="name"></div>
            <div><label for="rdv-tel">Téléphone *</label><input id="rdv-tel" name="tel" type="tel" required autocomplete="tel" placeholder="+225"></div>
            <div><label for="rdv-email">E-mail *</label><input id="rdv-email" name="email" type="email" required autocomplete="email"></div>
            <div><label for="rdv-conf">Confirmation par</label>
              <select id="rdv-conf" name="confirmation"><option>E-mail</option><option>Appel téléphonique</option></select></div>
            <div class="full"><label for="rdv-msg">Message (facultatif)</label><textarea id="rdv-msg" name="message" placeholder="Une question, une précision…"></textarea></div>
          </div>
        </fieldset>

        <button type="submit" class="btn btn-red rdv-submit"><svg class="ic"><use href="#i-mail"/></svg>Envoyer ma demande de rendez-vous</button>
        <p class="rdv-note">Votre demande est envoyée par e-mail à {EMAIL}. Vous pouvez aussi nous appeler au {PHONE}.</p>
        <p class="field-error" id="rdv-err" hidden></p>
      </form>

      <div class="form-ok" id="rdv-ok" hidden>
        <h3>Votre demande de rendez-vous est envoyée</h3>
        <p class="muted">Merci ! Nous vous confirmons le rendez-vous par e-mail ou par téléphone dans les meilleurs délais.</p>
        <pre class="rdv-recap" id="rdv-recap"></pre>
        <div class="quiz-actions" style="justify-content:center">
          <button type="button" class="btn btn-outline" id="rdv-again">Faire une autre demande</button>
        </div>
      </div>
    </div>
  </div>
</section>
''' + MAP
page('rendez-vous.html', *seo.PAGES['rendez-vous.html'], rdv, 'rendez-vous.html',
     schemas=[seo.ecole_schema(PHONE, LAT, LNG, PLUS_CODE), seo.fil_ariane(('Accueil', ''), ('Rendez-vous', 'rendez-vous.html'))])

# =========================================================== Contact
PIECES_DOSSIER = ['2 photos d’identité récentes', '1 copie de la pièce d’identité', '1 CV']
options = '\n'.join(
    f'              <optgroup label="{CATEGORIES[c]}">\n' +
    '\n'.join(f'                <option value="{m["slug"]}">{m["titre"]}</option>' for m in BY_CAT[c]) +
    '\n              </optgroup>' for c in CATEGORIES)
contact = page_hero('Contact et inscription : votre école hôtelière à Abidjan', 'Contact', 'images/audit-nuit.jpg') + f'''
<section>
  <div class="container contact-grid">
    <aside class="contact-side">
      <div class="info-box">
      <h3>Parlons de votre projet</h3>
      <p>Une question sur nos formations ou une inscription ? Notre équipe vous répond sous 48 h.</p>
      <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-pin"/></svg></div><div><strong>Adresse</strong><span>Angré Star 14, Cocody<br>Abidjan, Côte d’Ivoire<br>Code de localisation : <a href="{MAPS_OUVRIR}" target="_blank" rel="noopener">{PLUS_CODE}</a></span></div></div>
      <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-phone"/></svg></div><div><strong>Téléphone</strong><span>{PHONE}</span></div></div>
      <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-chat"/></svg></div><div><strong>WhatsApp</strong><span><a href="{wa_link('Bonjour EchoResta')}" target="_blank" rel="noopener">{WHATSAPP_AFFICHE}</a></span></div></div>
      <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-mail"/></svg></div><div><strong>E-mail</strong><span>contact@echoresta.ci</span></div></div>
      <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-clock"/></svg></div><div><strong>Horaires</strong><span>Lundi – Vendredi : 8h00 – 17h00</span></div></div>
      <a href="rendez-vous.html" class="btn btn-ghost info-rdv">Prendre rendez-vous</a>
      </div>
    </aside>

    <div class="form" id="formulaire" style="scroll-margin-top:140px">
      <form id="form-contact" data-mail="{EMAIL}" novalidate>
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
        <p class="field-error" id="contact-err" hidden></p>
      </form>
      <div class="form-ok" id="form-ok" hidden>
        <h3>Merci, votre demande est envoyée !</h3>
        <p class="muted">Notre équipe vous recontactera sous 48 h.</p>
      </div>
    </div>
  </div>
</section>
''' + MAP
page('contact.html', *seo.PAGES['contact.html'], contact, 'contact.html',
     schemas=[seo.ecole_schema(PHONE, LAT, LNG, PLUS_CODE), seo.fil_ariane(('Accueil', ''), ('Contact', 'contact.html'))])

# =========================================================== Inscription
NIVEAUX_ETUDES = ['Sans diplôme', 'CEPE', 'BEPC', 'BAC', 'BTS / BAC+2', 'Licence / BAC+3', 'Master / BAC+5 et plus']
SITUATIONS = ['Élève ou étudiant(e)', 'Sans emploi', 'En poste dans l’hôtellerie ou la restauration', 'En poste dans un autre secteur', 'Entrepreneur(e)']
EXPERIENCES = ['Aucune', 'Moins d’un an', '1 à 3 ans', 'Plus de 3 ans']
CONNU = ['Facebook', 'Instagram', 'TikTok', 'WhatsApp', 'Google', 'Bouche-à-oreille', 'Affiche ou flyer', 'Autre']
LIENS_PARENTE = ['Père', 'Mère', 'Tuteur / tutrice', 'Frère / sœur', 'Autre']
GLOBE = '<svg class="flag flag-globe" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/></svg>'


def liste_drapeaux(champ, label, mode='pays', requis=True, defaut=''):
    """Liste déroulante avec drapeaux, gérée par assets/main.js.
    mode 'pays' : choix d'un pays ; mode 'indicatif' : indicatif téléphonique (drapeau + code)."""
    if mode == 'pays':
        lignes = [(code, pays, tel, f'{drapeaux.drapeau(code)}<span class="fs-name">{pays}</span>') for code, pays, _, tel in drapeaux.PAYS]
        autre = ('autre', 'Autre pays', '', f'{GLOBE}<span class="fs-name">Autre pays</span>')
    else:
        lignes = [(code, tel, tel, f'{drapeaux.drapeau(code)}<span class="fs-name">{pays}</span><span class="fs-code">{tel}</span>') for code, pays, _, tel in drapeaux.PAYS]
        autre = ('autre', 'Autre', '', f'{GLOBE}<span class="fs-name">Autre indicatif</span><span class="fs-code">+…</span>')
    options = '\n'.join(
        f'            <li role="option" id="{champ}-{code.lower()}" data-value="{valeur}" data-tel="{tel}" aria-selected="false">{contenu}</li>'
        for code, valeur, tel, contenu in lignes + [autre])
    autre_txt = (f'\n          <input class="fs-other" id="{champ}-autre-txt" name="{champ}_autre" placeholder="Précisez le pays" aria-label="Précisez le pays" hidden>'
                 if mode == 'pays' else '')
    erreur = f'\n          <p class="field-error" id="{champ}-err" hidden>Choisissez dans la liste.</p>' if requis else ''
    return f'''<div class="flag-select{' tel-select' if mode == 'indicatif' else ''}" data-field="{champ}" data-default="{defaut}">
            <button type="button" class="fs-btn" id="{champ}-btn" aria-haspopup="listbox" aria-expanded="false" aria-labelledby="{label} {champ}-btn">
              <span class="fs-current">{GLOBE}<span class="fs-text">Sélectionnez votre pays</span></span><svg class="ic fs-chev"><use href="#i-down"/></svg>
            </button>
            <ul class="fs-list" role="listbox" id="{champ}-list" aria-labelledby="{label}" tabindex="-1" hidden>
{options}
            </ul>
            <input type="hidden" name="{champ}" id="{champ}">
          </div>{erreur}{autre_txt}'''


def telephone(champ, label, requis):
    etoile = ' *' if requis else ''
    return f'''<div><span class="flab" id="{champ}-label">{label}{etoile}</span>
              <div class="tel-field">
                {liste_drapeaux(champ + '_ind', champ + '-label', 'indicatif', requis=False, defaut='+225')}
                <input id="{champ}" name="{champ}" type="tel" inputmode="tel"{' required' if requis else ''} autocomplete="{'tel-national' if requis else 'off'}" placeholder="01 02 03 04 05" aria-labelledby="{champ}-label">
              </div></div>'''


def choix_radio(nom, valeurs, requis=True):
    return '<div class="pills">' + ''.join(
        f'<label class="pill"><input type="radio" name="{nom}" value="{v}"{" required" if requis else ""}><span>{v}</span></label>' for v in valeurs) + '</div>'


def options(valeurs):
    return ''.join(f'<option>{v}</option>' for v in valeurs)


options_formations = '\n'.join(
    f'              <optgroup label="{CATEGORIES[c]}">\n' +
    '\n'.join(f'                <option value="{m["slug"]}">{m["titre"]}</option>' for m in BY_CAT[c]) +
    '\n              </optgroup>' for c in CATEGORIES)

DOCS_HTML = f'''      <div class="info-box docs-box">
        <h3><svg class="ic"><use href="#i-award"/></svg>Pièces à joindre au dossier</h3>
        <ul class="docs-list">
{chr(10).join(f'          <li><svg class="ic"><use href="#i-check"/></svg>{d}</li>' for d in PIECES_DOSSIER)}
        </ul>
      </div>'''

# Nationalité proposée automatiquement selon le pays et le sexe
NATIONALITES = {pays: {'Féminin': nat, 'Masculin': masc} for (_, pays, nat, _), masc in zip(drapeaux.PAYS, drapeaux.NATIONALITES_MASC)}

FORMULAIRE_INSCRIPTION = f'''      <form id="form-inscription" data-mail="{EMAIL}" data-nationalites='{json.dumps(NATIONALITES, ensure_ascii=False).replace("'", "&#39;")}' novalidate>
        <h3 class="ins-title">Formulaire de candidature</h3>
        <div class="sep"></div>
        <p class="muted ins-intro">Les champs marqués d’un * sont obligatoires.</p>

        <fieldset>
          <legend>1. Informations personnelles</legend>
          <div class="row">
            <div><label for="ins-nom">Nom de famille *</label><input id="ins-nom" name="nom" required autocomplete="family-name" placeholder="Nom"></div>
            <div><label for="ins-prenoms">Prénom(s) *</label><input id="ins-prenoms" name="prenoms" required autocomplete="given-name" placeholder="Prénoms"></div>
            <div><label for="ins-naissance">Date de naissance *</label><input id="ins-naissance" name="naissance" type="date" required autocomplete="bday"></div>
            <div><label for="ins-lieu">Lieu de naissance *</label><input id="ins-lieu" name="lieu_naissance" required placeholder="Lieu"></div>
            <div><span class="flab" id="pays-label">Pays *</span>
          {liste_drapeaux('pays', 'pays-label')}</div>
            <div><span class="flab">Sexe *</span>{choix_radio('sexe', ['Masculin', 'Féminin'])}</div>
            <div class="full"><label for="ins-nationalite">Nationalité *</label><input id="ins-nationalite" name="nationalite" required placeholder="Ex. Ivoirienne" aria-describedby="ins-nat-aide"><p class="field-hint" id="ins-nat-aide">Remplie automatiquement quand vous choisissez votre pays et votre sexe.</p></div>
            <div><label for="ins-piece">Type de pièce d’identité</label>
              <select id="ins-piece" name="piece"><option value="">—</option>{options(['CNI', 'Passeport', 'Attestation d’identité', 'Carte consulaire', 'Autre'])}</select></div>
            <div><label for="ins-piece-num">Numéro de la pièce</label><input id="ins-piece-num" name="piece_numero"></div>
          </div>
        </fieldset>

        <fieldset>
          <legend>2. Coordonnées de contact</legend>
          <div class="row">
            <div class="full"><label for="ins-adresse">Adresse résidentielle *</label><input id="ins-adresse" name="adresse" required autocomplete="street-address" placeholder="Adresse"></div>
            <div><label for="ins-ville">Ville / Commune *</label><input id="ins-ville" name="ville" required autocomplete="address-level2" placeholder="Ville"></div>
            <div><label for="ins-email">Adresse e-mail *</label><input id="ins-email" name="email" type="email" required autocomplete="email" placeholder="Email"></div>
            {telephone('tel', 'Numéro de téléphone principal', True)}
            {telephone('tel2', 'Numéro de téléphone secondaire', False)}
          </div>
        </fieldset>

        <fieldset>
          <legend>3. Niveau d’études</legend>
          <div class="row">
            <div><label for="ins-niveau">Dernier niveau d’études atteint *</label>
              <select id="ins-niveau" name="niveau" required><option value="">Sélectionnez votre niveau</option>{options(NIVEAUX_ETUDES)}</select></div>
            <div><label for="ins-diplome">Dernier diplôme obtenu</label><input id="ins-diplome" name="diplome" placeholder="Ex. BEPC, BAC A2…"></div>
          </div>
        </fieldset>

        <fieldset>
          <legend>4. Formation souhaitée</legend>
          <div class="row">
            <div class="full"><label for="ins-formation">Formation *</label>
              <select id="ins-formation" name="formation" required>
                <option value="">— Choisissez une formation —</option>
{options_formations}
              </select></div>
            <div><label for="ins-situation">Situation actuelle *</label>
              <select id="ins-situation" name="situation" required><option value="">— Choisissez —</option>{options(SITUATIONS)}</select></div>
            <div><label for="ins-exp">Expérience en hôtellerie / restauration</label>
              <select id="ins-exp" name="experience">{options(EXPERIENCES)}</select></div>
          </div>
        </fieldset>

        <fieldset class="tuteur" id="ins-tuteur" hidden>
          <legend>5. Parent ou tuteur <small>(obligatoire pour les moins de 18 ans)</small></legend>
          <div class="row">
            <div><label for="ins-tut-nom">Nom et prénoms *</label><input id="ins-tut-nom" name="tuteur_nom" data-req></div>
            <div><label for="ins-tut-lien">Lien de parenté *</label>
              <select id="ins-tut-lien" name="tuteur_lien" data-req><option value="">— Choisissez —</option>{options(LIENS_PARENTE)}</select></div>
            <div class="full"><label for="ins-tut-tel">Téléphone du parent ou tuteur *</label><input id="ins-tut-tel" name="tuteur_tel" type="tel" data-req placeholder="+225 01 02 03 04 05"></div>
          </div>
        </fieldset>

        <fieldset>
          <legend><span class="num-tuteur">5</span>. Pour finir</legend>
          <div class="row">
            <div class="full"><label for="ins-urgence">Personne à prévenir en cas d’urgence (nom et téléphone)</label><input id="ins-urgence" name="urgence"></div>
            <div class="full"><label for="ins-connu">Comment avez-vous connu EchoResta ?</label>
              <select id="ins-connu" name="connu"><option value="">—</option>{options(CONNU)}</select></div>
            <div class="full"><label for="ins-motivation">Votre projet professionnel</label><textarea id="ins-motivation" name="motivation" placeholder="Quel métier visez-vous ? Pourquoi cette formation ?"></textarea></div>
          </div>
        </fieldset>

        <label class="consent"><input type="checkbox" id="ins-consent" required> Je certifie l’exactitude des informations et j’accepte d’être recontacté(e) par EchoResta au sujet de ma candidature.</label>
        <button type="submit" class="btn btn-red">Envoyer ma candidature</button>
        <p class="rdv-note">Votre candidature est envoyée par e-mail à {EMAIL}.</p>
        <p class="field-error" id="ins-err" hidden></p>
      </form>'''


inscription = page_hero('Inscription à une formation en hôtellerie et restauration à Abidjan', 'Inscription', 'images/hero-cuisine.jpg',
                        'Remplissez votre fiche d’inscription en quelques minutes : notre équipe vous recontacte pour finaliser votre dossier.') + f'''
<section>
  <div class="container contact-grid ins-grid">
    <aside class="contact-side">
{DOCS_HTML}
      <div class="info-box ins-after">
        <h3>Après votre inscription</h3>
        <ol class="rdv-steps on-dark">
          <li><b>Étude de votre fiche</b><span>Notre équipe vérifie votre demande.</span></li>
          <li><b>Entretien d’inscription</b><span>Nous vous appelons pour fixer un entretien à l’école.</span></li>
          <li><b>Dossier complet</b><span>Vous remettez les pièces demandées et confirmez votre place.</span></li>
        </ol>
        <div class="info-item"><div class="ico"><svg class="ic"><use href="#i-phone"/></svg></div><div><strong>Une question ?</strong><span>{PHONE}<br>{EMAIL}</span></div></div>
      </div>
    </aside>

    <div class="form ins-form" id="formulaire" style="scroll-margin-top:140px">
{FORMULAIRE_INSCRIPTION}

      <div class="form-ok" id="ins-ok" hidden>
        <h3>Votre candidature est envoyée</h3>
        <p class="muted">Merci ! Notre équipe vous recontacte pour fixer votre entretien d’inscription. Pensez à préparer les pièces de votre dossier.</p>
        <pre class="rdv-recap" id="ins-recap"></pre>
      </div>
    </div>
  </div>
</section>
'''
page('inscription.html', *seo.PAGES['inscription.html'], inscription, '',
     schemas=[seo.fil_ariane(('Accueil', ''), ('Inscription', 'inscription.html'))])

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
''', '', robots='noindex, follow')

# =========================================================== Données pour la recherche et le test
index = [{'t': 'Accueil', 'u': 'index.html', 'd': 'Présentation de l’école EchoResta'},
         {'t': 'À propos', 'u': 'apropos.html', 'd': 'Histoire, mission, valeurs et formateurs'},
         {'t': 'Nos formations', 'u': 'formations.html', 'd': 'Les 10 formations, étapes d’inscription et FAQ'},
         {'t': 'Test d’orientation', 'u': 'index.html#quiz', 'd': 'Quel métier est fait pour vous ? Trois questions'},
         {'t': 'Contact & inscription', 'u': 'contact.html', 'd': 'Coordonnées, formulaire et plan d’accès'},
         {'t': 'Prendre rendez-vous', 'u': 'rendez-vous.html', 'd': 'Entretien d’orientation, inscription ou visite de l’école'},
         {'t': 'Inscription', 'u': 'inscription.html', 'd': 'Fiche d’inscription en ligne et pièces à joindre au dossier'}]
for m in METIERS:
    kw = ' '.join([CATEGORIES[m['cat']], *(t for t, _ in m['modules']), *m['carriere'], *m['lieux']])
    index.append({'t': m['titre'], 'u': url(m), 'd': m['resume'], 'k': kw})
data = {
    'SEARCH_INDEX': index,
    'METIERS': [{'slug': m['slug'], 'titre': m['titre'], 'icon': m['icon'], 'accroche': m['accroche']} for m in METIERS],
    'QUIZ': [{'q': q['q'], 'r': [[label, pts] for label, pts in q['r']]} for q in QUIZ],
}
(OUT / 'assets' / 'data.js').write_text(''.join(f'window.{k}={json.dumps(v, ensure_ascii=False)};\n' for k, v in data.items()))
old_index = OUT / 'assets' / 'search-index.js'
if old_index.exists():
    old_index.unlink()
print('ok :', len(list(OUT.glob('*.html'))), 'pages')

# =========================================================== Plan du site (sitemap.xml) et robots.txt
import datetime  # noqa: E402
jour = datetime.date.today().isoformat()
PRIORITE = {'index.html': '1.0', 'formations.html': '0.9', 'rendez-vous.html': '0.8', 'inscription.html': '0.9', 'contact.html': '0.8', 'apropos.html': '0.7'}
urls = '\n'.join(
    f'  <url><loc>{seo.BASE_URL}{"" if f == "index.html" else f}</loc><lastmod>{jour}</lastmod>'
    f'<priority>{PRIORITE.get(f, "0.8")}</priority></url>'
    for f, robots in PAGES_PUBLIEES if robots.startswith('index'))
(OUT / 'sitemap.xml').write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
''')
(OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {seo.BASE_URL}sitemap.xml\n')
