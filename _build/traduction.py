"""Version anglaise du site (dossier en/).

Chaque page française générée est traduite à partir du dictionnaire _build/traduction_en.json
(texte français → texte anglais), puis écrite dans en/ avec des liens adaptés.
Les scripts ont aussi leur version anglaise : assets/main-en.js et assets/data-en.js.
Un texte absent du dictionnaire reste en français : la liste est écrite dans _build/traduction_manquante.json
et le nombre s'affiche à la fin de la construction. Pour le traduire, ajoutez-le au dictionnaire.
"""
import html as _h
import re as _r
from bs4 import BeautifulSoup, NavigableString, Comment, Tag

EN = json.loads((S / 'traduction_en.json').read_text())
MANQUANT = {}
EN_DIR = OUT / 'en'
EN_DIR.mkdir(exist_ok=True)

INLINE = {'a', 'strong', 'b', 'em', 'i', 'span', 'small', 'br', 'svg', 'use', 'sup', 'sub', 'u', 'abbr', 'time', 'mark', 's'}
SANS_TEXTE = {'script', 'style', 'noscript', 'svg', 'template'}
ATTRIBUTS = ['placeholder', 'aria-label', 'alt', 'title', 'data-label', 'data-requis']
METAS = {'description', 'twitter:title', 'twitter:description', 'og:title', 'og:description', 'og:image:alt'}


def _norm(t):
    return _r.sub(r'\s+', ' ', t).strip()


def _a_traduire(t):
    return _r.search(r'[A-Za-zÀ-ÿ]{2,}', _r.sub(r'<[^>]+>', '', t))


def tr(t, source='page'):
    """Traduction d'un texte (ou d'un fragment HTML) ; le texte d'origine s'il manque au dictionnaire."""
    k = _norm(t)
    if not k or not _a_traduire(k):
        return t
    debut, fin = t[:len(t) - len(t.lstrip())], t[len(t.rstrip()):]
    for cle in (k, _h.escape(k, quote=False), _h.unescape(k)):
        if cle in EN:
            return debut + EN[cle] + fin
    MANQUANT.setdefault(k, source)
    return t


def _bloc_simple(el):
    return all(isinstance(d, NavigableString) or (isinstance(d, Tag) and d.name in INLINE) for d in el.descendants)


def _traduire_corps(el, source):
    for c in list(el.children):
        if isinstance(c, Comment):
            continue
        if isinstance(c, NavigableString):
            t = str(c)
            if _a_traduire(t):
                debut, fin = t[:len(t) - len(t.lstrip())], t[len(t.rstrip()):]
                c.replace_with(debut + tr(t, source) + fin)
        elif isinstance(c, Tag) and c.name not in SANS_TEXTE and 'langs' not in c.get('class', []):
            contenu = c.decode_contents()
            if _bloc_simple(c) and _a_traduire(contenu):
                en = tr(contenu, source)
                if en is not contenu:
                    c.clear()
                    c.append(BeautifulSoup(en, 'html.parser'))
            else:
                _traduire_corps(c, source)


def _url_en(u):
    """URL absolue d'une page du site → son équivalent anglais."""
    if u.startswith(seo.BASE_URL) and not u.startswith(seo.BASE_URL + 'en/'):
        reste = u[len(seo.BASE_URL):]
        if reste == '' or reste.split('#')[0].endswith('.html'):
            return seo.BASE_URL + 'en/' + reste
    return u


LD_TEXTES = {'name', 'description', 'text', 'alternateName', 'educationalCredentialAwarded'}


def _json_ld(v, source, cle=None):
    """Données structurées : on traduit les textes lisibles, on adapte les adresses des pages."""
    if isinstance(v, dict):
        return {k: ('en' if k == 'inLanguage' else _json_ld(x, source, k)) for k, x in v.items()}
    if isinstance(v, list):
        return [_json_ld(x, source, cle) for x in v]
    if isinstance(v, str):
        if v.startswith('http'):
            return _url_en(v)
        if cle in LD_TEXTES and _a_traduire(v):
            return _h.unescape(_r.sub(r'<[^>]+>', '', tr(v, source)))
    return v


def _relatif(u):
    """Lien relatif vers un fichier du site (pas une page) : il faut remonter d'un dossier depuis en/."""
    if not u or _r.match(r'^([a-z][a-z0-9+.-]*:|#|/|\.\./)', u):
        return False
    return not u.split('#')[0].split('?')[0].endswith('.html')


def traduire_page(fichier):
    soup = BeautifulSoup((OUT / fichier).read_text(), 'html.parser')
    soup.html['lang'] = 'en'
    _traduire_corps(soup.body, fichier)
    soup.title.string = tr(soup.title.string, fichier)
    for el in soup.find_all(True):
        for a in ATTRIBUTS:
            if el.has_attr(a):
                el[a] = tr(el[a], fichier)
    for m in soup.find_all('meta'):
        if m.get('name') in METAS or m.get('property') in METAS:
            m['content'] = tr(m['content'], fichier)
        elif m.get('property') == 'og:locale':
            m['content'] = 'en_GB'
            m.insert_after(soup.new_tag('meta', attrs={'property': 'og:locale:alternate', 'content': 'fr_FR'}))
        elif m.get('property') == 'og:url':
            m['content'] = _url_en(m['content'])
    soup.find('link', rel='canonical')['href'] = _url_en(soup.find('link', rel='canonical')['href'])
    for s in soup.find_all('script', type='application/ld+json'):
        s.string = json.dumps(_json_ld(json.loads(s.string), fichier), ensure_ascii=False)
    # Nationalités proposées automatiquement (fiche d'inscription)
    for el in soup.find_all(attrs={'data-nationalites': True}):
        nat = json.loads(el['data-nationalites'])
        el['data-nationalites'] = json.dumps({p: {g: tr(n, fichier) for g, n in v.items()} for p, v in nat.items()}, ensure_ascii=False)
    # Scripts en anglais, puis liens vers les fichiers du dossier parent
    for s in soup.find_all('script', src=True):
        s['src'] = {'assets/data.js': 'assets/data-en.js', 'assets/main.js': 'assets/main-en.js'}.get(s['src'], s['src'])
    for el in soup.find_all(True):
        for a in ('href', 'src', 'poster'):
            if el.has_attr(a) and _relatif(el[a]):
                el[a] = '../' + el[a]
        if el.has_attr('style'):
            el['style'] = el['style'].replace("url('images/", "url('../images/")
    # Choix de la langue : FR renvoie vers la page française, EN est la page courante
    for a in soup.select('.langs a'):
        if a['data-lang'] == 'fr':
            a['href'] = '../' + fichier
            del a['aria-current']
        else:
            a['href'] = fichier
            a['aria-current'] = 'true'
    (EN_DIR / fichier).write_text(str(soup))


# Chaînes de assets/main.js affichées au visiteur (ou envoyées dans l'e-mail) : remplacées dans main-en.js
JS_CHAINES = [
    'Adresse', 'Autre', 'Bonjour EchoResta, voici les justificatifs de ma candidature (', ') : CV, photo et diplômes.',
    'Candidature : ', 'Cette date n’existe pas : vérifiez le jour et le mois.', 'Choisissez d’abord une date',
    'Choisissez une date à partir du ', 'Connu par', 'Contact en cas d’urgence', 'Date de naissance', 'Demande de rendez-vous : ',
    'Dernier diplôme', 'Emploi recherché', 'Envoi en cours…', 'Envoyer ma candidature', 'Envoyer ma demande', 'Expérience',
    'Fichier obligatoire', 'Formation', 'Formation souhaitée', 'Je cherche', 'Je ne sais pas encore', 'La date ne peut pas dépasser le ',
    'Lien de parenté', 'Lieu de naissance', 'L’envoi n’a pas abouti. <a class="link" href="', 'Message', 'Nationalité', 'Niveau d’études',
    'Nom', 'Nom et prénom', 'Non précisée', 'Objet', 'Parent ou tuteur', 'Pays', 'Pièce d’identité', 'Projet professionnel', 'Prénom(s)',
    'Prénoms', 'Remarques ou questions', 'Rendez-vous', 'Saisissez la date au format jj/mm/aaaa.', 'Sexe', 'Situation actuelle',
    'Téléphone', 'Téléphone / WhatsApp', 'Téléphone du tuteur', 'Téléphone principal', 'Téléphone secondaire', 'Ville / Commune',
    'Établissement ou société', '— Choisir l’heure —', '<li class="empty">Aucun résultat.</li>', ' ans)',
    '" target="_blank" rel="noopener">Envoyez la demande sur WhatsApp</a> (message déjà rédigé) ou appelez-nous au +225 07 68 84 20 38.',
]
JS_FRAGMENTS = ['>Votre résultat<', '>Découvrir la formation<', '>Refaire le test<']


def _js(t):
    return t.replace('\\', '\\\\').replace("'", "\\'")


js = (OUT / 'assets' / 'main.js').read_text()
for c in JS_CHAINES:
    if f"'{c}'" not in js:
        MANQUANT.setdefault(c, 'main.js (chaîne introuvable)')
    js = js.replace(f"'{c}'", f"'{_js(tr(c, 'main.js'))}'")
for c in JS_FRAGMENTS:
    js = js.replace(c, '>' + tr(c[1:-1], 'main.js') + '<')
js = js.replace("'fr-FR'", "'en-GB'").replace("' à '", "' at '").replace("' n° '", "' no. '")
(OUT / 'assets' / 'main-en.js').write_text(js)

data_en = {
    'SEARCH_INDEX': [dict(e, t=tr(e['t'], 'data.js'), d=tr(e['d'], 'data.js')) for e in data['SEARCH_INDEX']],
    'METIERS': [dict(m, titre=tr(m['titre'], 'data.js'), accroche=tr(m['accroche'], 'data.js')) for m in data['METIERS']],
    'QUIZ': [{'q': tr(q['q'], 'data.js'), 'r': [[tr(l, 'data.js'), p] for l, p in q['r']]} for q in data['QUIZ']],
}
for e in data_en['SEARCH_INDEX']:
    e['t'], e['d'] = _h.unescape(e['t']), _h.unescape(e['d'])
(OUT / 'assets' / 'data-en.js').write_text(''.join(f'window.{k}={json.dumps(v, ensure_ascii=False)};\n' for k, v in data_en.items()))

PAGES_EN = [f for f, robots in PAGES_PUBLIEES if robots.startswith('index')]
for f in PAGES_EN:
    traduire_page(f)
(S / 'traduction_manquante.json').write_text(json.dumps(MANQUANT, ensure_ascii=False, indent=1))
print('version anglaise :', len(PAGES_EN), 'pages,', len(MANQUANT), 'texte(s) à traduire (voir _build/traduction_manquante.json)')
