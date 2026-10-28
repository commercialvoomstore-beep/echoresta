"""Référencement (SEO) : titres, descriptions, données structurées et textes locaux.

Les mots-clés visés sont les recherches courantes en Côte d'Ivoire, surtout à Abidjan :
« école hôtelière Abidjan », « formation hôtellerie / restauration Abidjan », « formation cuisinier »,
« formation serveur », « formation femme de chambre », « formation réceptionniste », « formation barman »…
"""
import json

# Adresse publique du site. À changer si le site passe sur un nom de domaine (ex. https://www.echoresta.ci/).
BASE_URL = 'https://commercialvoomstore-beep.github.io/echoresta/'
SITE_NAME = 'EchoResta'
# Code fourni par Google Search Console (méthode « Balise HTML »), par ex. 'AbCdEf123…'. Vide = pas de balise.
GOOGLE_VERIFICATION = ''


def verification():
    return f'\n<meta name="google-site-verification" content="{GOOGLE_VERIFICATION}">' if GOOGLE_VERIFICATION else ''

ADRESSE = {
    '@type': 'PostalAddress',
    'streetAddress': 'Angré Star 14',
    'addressLocality': 'Abidjan',
    'addressRegion': 'Cocody',
    'addressCountry': 'CI',
}
ECOLE_ID = BASE_URL + '#ecole'


def ecole_schema(phone, lat, lng, plus_code):
    """Fiche de l'école pour Google (nom, adresse, position, horaires, téléphone)."""
    return {
        '@context': 'https://schema.org',
        '@type': 'EducationalOrganization',
        '@id': ECOLE_ID,
        'name': 'EchoResta — École de l’Hôtellerie & Restauration',
        'alternateName': ['EchoResta', 'École hôtelière EchoResta Abidjan'],
        'description': 'École de l’hôtellerie et de la restauration à Abidjan (Cocody, Angré) : formations '
                       'certifiantes en cuisine, service en salle, réception, hébergement, bar et management, avec double certification internationale (Côte d’Ivoire et Australie) et stage de 6 mois garanti.',
        'url': BASE_URL,
        'logo': BASE_URL + 'images/logo-512.png',
        'image': BASE_URL + 'images/hero-cuisine.jpg',
        'telephone': phone,
        'email': 'contact@echoresta.ci',
        'address': ADRESSE,
        'geo': {'@type': 'GeoCoordinates', 'latitude': lat, 'longitude': lng},
        'hasMap': f'https://www.google.com/maps/search/?api=1&query={plus_code.replace("+", "%2B")}%20Abidjan',
        'openingHours': 'Mo-Fr 08:00-17:00',
        'areaServed': [{'@type': 'City', 'name': 'Abidjan'}, {'@type': 'Country', 'name': 'Côte d’Ivoire'}],
        'knowsLanguage': ['fr', 'en'],
    }


def site_schema():
    return {'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE_NAME, 'url': BASE_URL,
            'inLanguage': 'fr', 'publisher': {'@id': ECOLE_ID}}


def fil_ariane(*etapes):
    """etapes : (nom, chemin) depuis l'accueil."""
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': nom, 'item': BASE_URL + chemin}
                                for i, (nom, chemin) in enumerate(etapes)]}


def faq_schema(questions):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': r}}
                           for q, r in questions]}


def cours_schema(m, meta):
    return {
        '@context': 'https://schema.org', '@type': 'Course',
        'name': meta['h1'], 'description': meta['desc'], 'url': BASE_URL + f'formation-{m["slug"]}.html',
        'inLanguage': 'fr', 'educationalCredentialAwarded': 'Double certification internationale (Côte d’Ivoire et Australie)',
        'provider': {'@type': 'EducationalOrganization', '@id': ECOLE_ID, 'name': SITE_NAME, 'url': BASE_URL},
        'hasCourseInstance': {'@type': 'CourseInstance', 'courseMode': 'Onsite',
                              'location': {'@type': 'Place', 'name': 'EchoResta, Angré Star 14', 'address': ADRESSE}},
    }


def balises_json_ld(schemas):
    return '\n'.join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)


# ---------------------------------------------------------------- Pages principales
PAGES = {
    'index.html': ('École hôtelière Abidjan : formation hôtellerie restauration',
        'École hôtelière à Abidjan, Cocody Angré : formations en cuisine, service en salle, réception, bar et hébergement pour travailler en hôtel et restaurant.'),
    'formations.html': ('Formations hôtellerie restauration Abidjan, Côte d’Ivoire',
        '10 formations hôtellerie et restauration à Abidjan : cuisinier, serveur, réceptionniste, femme de chambre, gouvernante, barman, directeur d’hôtel.'),
    'apropos.html': ('École d’hôtellerie et restauration à Cocody Angré, Abidjan',
        'École d’hôtellerie et de restauration à Cocody Angré, Abidjan : formateurs professionnels du métier, cours pratiques en cuisine, salle, bar et réception.'),
    'recrutement.html': ('Recrutement hôtellerie restauration Abidjan : emploi hôtel',
        'Recrutement en hôtellerie et restauration à Abidjan : employeurs, trouvez du personnel formé ; candidats, trouvez un emploi en hôtel ou en restaurant.'),
    'espace_client.html': ('Recrutement personnel hôtel et restaurant à Abidjan',
        'Recrutez serveurs, cuisiniers, réceptionnistes, femmes de chambre et gouvernantes à Abidjan : personnel formé pour hôtels et restaurants en Côte d’Ivoire.'),
    'espace_candidat.html': ('Offre d’emploi hôtel et restaurant Abidjan, Côte d’Ivoire',
        'Emploi en hôtellerie et restauration à Abidjan : serveur, cuisinier, réceptionniste, femme de chambre, barman. Déposez votre candidature en ligne.'),
    'inscription.html': ('Inscription école hôtelière Abidjan : formation hôtellerie',
        'Inscription en ligne aux formations hôtellerie et restauration à Abidjan : cuisine, service, réception, bar, étages. Dossier simple, réponse rapide.'),
    'rendez-vous.html': ('Rendez-vous école hôtelière Abidjan : orientation, visite',
        'Prenez rendez-vous avec notre école hôtelière à Abidjan : orientation, inscription ou visite. Angré Star 14, Cocody, du lundi au vendredi de 8h à 17h.'),
    'contact.html': ('Contact école hôtelière Abidjan Cocody : téléphone, WhatsApp',
        'Contactez l’école hôtelière d’Abidjan : Angré Star 14, Cocody. Téléphone et WhatsApp : +225 07 68 84 20 38. Formations hôtellerie et restauration.'),
}

# ---------------------------------------------------------------- Pages métier
# h1 : titre visible de la page ; title / desc : ce qui s'affiche dans Google ; pourquoi : texte local.
METIERS_SEO = {
    'valet-femme-chambre': {
        'h1': 'Formation valet et femme de chambre à Abidjan',
        'title': 'Formation femme de chambre et valet de chambre Abidjan',
        'desc': 'Formation femme de chambre et valet à Abidjan aux standards des hôtels 3 à 5 étoiles : chambres, lits, salles de bain, linge. Sans diplôme exigé.',
        'pourquoi': 'Hôtels d’affaires, résidences hôtelières, resorts : à Abidjan comme dans toute la Côte d’Ivoire, '
                    'les établissements recrutent régulièrement des valets et femmes de chambre formés aux standards '
                    'internationaux. Notre formation de femme de chambre et de valet de chambre vous apprend les gestes '
                    'et l’organisation des étages attendus par les hôtels 3 à 5 étoiles, et vous permet d’évoluer ensuite '
                    'vers un poste de gouvernante.',
    },
    'gouvernante': {
        'h1': 'Formation gouvernante d’hôtel à Abidjan',
        'title': 'Formation gouvernante d’hôtel Abidjan, Côte d’Ivoire',
        'desc': 'Formation gouvernante d’hôtel à Abidjan : gestion des étages, contrôle qualité des chambres, linge, planning et management des femmes de chambre.',
        'pourquoi': 'Dans un hôtel, la gouvernante est garante de la propreté et du confort de chaque chambre : c’est un '
                    'poste clé, recherché par les hôtels et résidences d’Abidjan. Cette formation de gouvernante d’hôtel '
                    's’adresse aux femmes et valets de chambre expérimentés qui veulent encadrer une équipe et prendre des '
                    'responsabilités au service hébergement.',
    },
    'audit-nuit': {
        'h1': 'Formation réceptionniste et audit de nuit à Abidjan',
        'title': 'Formation réceptionniste d’hôtel et audit de nuit Abidjan',
        'desc': 'Formation réceptionniste d’hôtel et night audit à Abidjan : accueil, check-in, check-out, réservations, logiciel hôtelier, caisse et clôture de journée.',
        'pourquoi': 'La réception est le premier contact du client avec l’hôtel. Notre formation de réceptionniste d’hôtel '
                    'et d’auditeur de nuit (night auditor) prépare aux postes de front office des hôtels d’Abidjan : '
                    'accueil, réservations, logiciel hôtelier, facturation et clôture de la journée. Des compétences '
                    'recherchées de jour comme de nuit, et un bon point de départ pour devenir chef de réception.',
    },
    'directeur-hotel': {
        'h1': 'Formation directeur d’hôtel à Abidjan',
        'title': 'Formation directeur d’hôtel Abidjan : management hôtelier',
        'desc': 'Formation directeur d’hôtel à Abidjan : management hôtelier, revenue management, gestion financière, ressources humaines, qualité et service client.',
        'pourquoi': 'Le tourisme d’affaires et les grands événements internationaux accueillis à Abidjan créent des '
                    'besoins en managers capables de piloter un établissement. Cette formation en management hôtelier '
                    'vous donne les outils de la direction d’hôtel : stratégie commerciale, revenue management, gestion '
                    'financière, ressources humaines et qualité de service.',
    },
    'serveur-hotesse': {
        'h1': 'Formation serveur et hôtesse à Abidjan',
        'title': 'Formation serveur, serveuse et hôtesse à Abidjan',
        'desc': 'Formation serveur, serveuse et hôtesse d’accueil à Abidjan : service à table, prise de commande, vins, accueil client en hôtel et restaurant.',
        'pourquoi': 'Restaurants, hôtels, traiteurs et événementiel : le métier de serveur ou de serveuse est l’un des plus '
                    'demandés de la restauration à Abidjan. Notre formation de serveur et d’hôtesse vous apprend '
                    'l’accueil, le service à table et la vente, pour être opérationnel dès votre premier poste et évoluer '
                    'vers chef de rang ou maître d’hôtel.',
    },
    'maitre-hotel': {
        'h1': 'Formation maître d’hôtel à Abidjan',
        'title': 'Formation maître d’hôtel Abidjan : service en salle',
        'desc': 'Formation maître d’hôtel à Abidjan : direction de salle, service au guéridon, accords mets et vins, clientèle VIP, encadrement des serveurs.',
        'pourquoi': 'Les restaurants gastronomiques et les hôtels haut de gamme d’Abidjan recherchent des maîtres d’hôtel '
                    'capables de diriger une salle et d’accueillir une clientèle exigeante. Cette formation s’adresse aux '
                    'serveurs et chefs de rang qui veulent évoluer : direction du service, service au guéridon, accords '
                    'mets et vins et protocole.',
    },
    'cuisinier': {
        'h1': 'Formation cuisinier à Abidjan',
        'title': 'Formation cuisinier Abidjan : école de cuisine Côte d’Ivoire',
        'desc': 'Formation cuisinier à Abidjan : cuisine ivoirienne et internationale, pâtisserie, techniques de base, hygiène HACCP. École de cuisine à Cocody Angré.',
        'pourquoi': 'Vous cherchez une école de cuisine à Abidjan ? Notre formation de cuisinier associe les techniques de '
                    'la cuisine professionnelle, la cuisine ivoirienne et africaine, la cuisine internationale et la '
                    'pâtisserie. Vous apprenez en cuisine, encadré par des chefs, avec les règles d’hygiène HACCP '
                    'exigées par les restaurants, les hôtels et les traiteurs.',
    },
    'bar-mixology': {
        'h1': 'Formation barman et mixologie à Abidjan',
        'title': 'Formation barman et mixologie Abidjan : cocktails, bar',
        'desc': 'Formation barman et barmaid à Abidjan : cocktails classiques et signatures, mixologie, spiritueux, service et gestion du bar en hôtel et lounge.',
        'pourquoi': 'Bars d’hôtel, lounges, rooftops et restaurants : la vie nocturne d’Abidjan offre de nombreux '
                    'débouchés aux barmen et barmaids formés. Notre formation de barman et de mixologie vous apprend les '
                    'cocktails classiques, la création de cocktails signatures avec les saveurs locales et la gestion '
                    'd’un bar.',
    },
    'directeur-restaurant': {
        'h1': 'Formation directeur de restaurant à Abidjan',
        'title': 'Formation directeur et gestion de restaurant Abidjan',
        'desc': 'Formation directeur de restaurant à Abidjan : gestion, coût matière, carte, rentabilité, management d’équipe et marketing pour restaurateurs.',
        'pourquoi': 'Vous dirigez un restaurant ou vous voulez ouvrir le vôtre à Abidjan ? Cette formation en gestion de '
                    'restaurant vous apprend à piloter la rentabilité, maîtriser le coût matière, construire une carte, '
                    'encadrer vos équipes et attirer de nouveaux clients, notamment grâce aux réseaux sociaux et aux '
                    'plateformes de livraison.',
    },
    'anglais-tourisme-hotellerie': {
        'h1': 'Formation anglais tourisme et hôtellerie à Abidjan',
        'title': 'Formation anglais hôtellerie et tourisme Abidjan',
        'desc': 'Formation anglais pour l’hôtellerie et le tourisme à Abidjan : accueil, réception, restaurant, téléphone, gestion des réclamations. Tous niveaux.',
        'pourquoi': 'À Abidjan, les hôtels, les agences de voyage et les sites touristiques accueillent une clientèle '
                    'internationale. Parler anglais est un vrai atout pour décrocher un poste et évoluer. Nos cours '
                    'd’anglais pour l’hôtellerie et le tourisme sont centrés sur les situations du métier : accueil, '
                    'réception, restaurant, téléphone et réclamations.',
    },
}

# ---------------------------------------------------------------- Accueil : texte local et questions fréquentes
ACCUEIL_FAQ = [
    ('Où se trouve l’école hôtelière EchoResta à Abidjan ?',
     'EchoResta se trouve à Angré Star 14, dans la commune de Cocody, à Abidjan (code de localisation Google : 92JH+FW). '
     'L’école vous accueille du lundi au vendredi, de 8h à 17h.'),
    ('Quelles formations en hôtellerie et restauration proposez-vous ?',
     'Dix formations : valet et femme de chambre, gouvernante, réceptionniste et audit de nuit, directeur d’hôtel, '
     'serveur et hôtesse, maître d’hôtel, cuisinier, barman et mixologie, directeur de restaurant, et anglais pour '
     'l’hôtellerie et le tourisme.'),
    ('Les formations sont-elles reconnues ?',
     'Chaque parcours donne lieu à une double certification internationale (Côte d’Ivoire et Australie) '
     'et se termine par un stage de 6 mois garanti dans les plus grands hôtels.'),
    ('Comment s’inscrire à une formation ?',
     'Remplissez la fiche d’inscription en ligne, appelez-nous ou écrivez-nous sur WhatsApp au +225 07 68 84 20 38. '
     'Un conseiller vous rappelle pour un entretien d’inscription.'),
]
