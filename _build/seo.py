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
        'logo': BASE_URL + 'images/logo.png',
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
    'index.html': ('École hôtelière à Abidjan, Cocody Angré | EchoResta',
        'Tu veux travailler dans les hôtels et restaurants ? EchoResta, école hôtelière à Abidjan : cuisine, service, réception, bar. Stage de 6 mois garanti.'),
    'formations.html': ('Formation hôtellerie et restauration Abidjan | EchoResta',
        'Cuisine, serveur, femme de chambre, réception, bar, gouvernante… 10 formations à Abidjan pour trouver vite boulot dans les hôtels. Stage garanti.'),
    'apropos.html': ('EchoResta : l’école hôtelière d’Angré, Cocody Abidjan',
        'À Cocody Angré, EchoResta forme les jeunes aux métiers de l’hôtel et du restaurant : formateurs du terrain, double certification Côte d’Ivoire & Australie.'),
    'recrutement.html': ('Recrutement hôtel et restaurant à Abidjan | EchoResta',
        'Tu cherches du personnel ou du boulot en hôtellerie-restauration à Abidjan ? Employeurs et candidats, remplissez votre fiche, on vous met en relation.'),
    'espace_client.html': ('Recruter serveur, cuisinier, réceptionniste à Abidjan',
        'Hôtel, restaurant, maquis ou résidence à Abidjan : besoin de serveurs, cuisiniers, femmes de chambre ? Remplis la fiche, on te propose des profils formés.'),
    'espace_candidat.html': ('Offre d’emploi hôtel et restaurant Abidjan | EchoResta',
        'Tu cherches boulot à Abidjan ? Serveur, cuisinier, réceptionniste, femme de chambre, barman : inscris-toi, on te présente aux hôtels qui recrutent.'),
    'inscription.html': ('Inscription formation hôtellerie Abidjan | EchoResta',
        'Inscris-toi en ligne en 5 minutes : cuisine, service, réception, bar, femme de chambre… À Abidjan, double certification et stage de 6 mois garanti.'),
    'rendez-vous.html': ('Rendez-vous école hôtelière Abidjan | EchoResta Angré',
        'Passe nous voir à Angré Star 14 ! Prends rendez-vous pour ton orientation, ton inscription ou la visite de l’école, du lundi au vendredi de 8h à 17h.'),
    'contact.html': ('Contact EchoResta, école hôtelière à Cocody Angré',
        'On est à Angré Star 14, Cocody (Abidjan). Appelle ou écris-nous sur WhatsApp au 07 68 84 20 38 pour tes questions sur les formations et l’inscription.'),
}

# ---------------------------------------------------------------- Pages métier
# h1 : titre visible de la page ; title / desc : ce qui s'affiche dans Google ; pourquoi : texte local.
METIERS_SEO = {
    'valet-femme-chambre': {
        'h1': 'Formation valet et femme de chambre à Abidjan',
        'title': 'Formation femme de chambre et valet à Abidjan | EchoResta',
        'desc': 'Pas besoin de diplôme ! Deviens femme de chambre ou valet dans les hôtels 3 à 5 étoiles d’Abidjan. Double certification et stage de 6 mois garanti.',
        'pourquoi': 'Hôtels d’affaires, résidences hôtelières, resorts : à Abidjan comme dans toute la Côte d’Ivoire, '
                    'les établissements recrutent régulièrement des valets et femmes de chambre formés aux standards '
                    'internationaux. Notre formation de femme de chambre et de valet de chambre vous apprend les gestes '
                    'et l’organisation des étages attendus par les hôtels 3 à 5 étoiles, et vous permet d’évoluer ensuite '
                    'vers un poste de gouvernante.',
    },
    'gouvernante': {
        'h1': 'Formation gouvernante d’hôtel à Abidjan',
        'title': 'Formation gouvernante d’hôtel à Abidjan | EchoResta',
        'desc': 'Deviens gouvernante d’hôtel à Abidjan : étages, contrôle des chambres, linge et équipe. Un poste qui recrute fort en Côte d’Ivoire. Stage garanti.',
        'pourquoi': 'Dans un hôtel, la gouvernante est garante de la propreté et du confort de chaque chambre : c’est un '
                    'poste clé, recherché par les hôtels et résidences d’Abidjan. Cette formation de gouvernante d’hôtel '
                    's’adresse aux femmes et valets de chambre expérimentés qui veulent encadrer une équipe et prendre des '
                    'responsabilités au service hébergement.',
    },
    'audit-nuit': {
        'h1': 'Formation réceptionniste et audit de nuit à Abidjan',
        'title': 'Formation réceptionniste hôtel Abidjan | Audit de nuit',
        'desc': 'Apprends la réception d’hôtel à Abidjan : accueil, check-in, réservations, caisse et audit de nuit. Les hôtels de Côte d’Ivoire recrutent. Stage garanti.',
        'pourquoi': 'La réception est le premier contact du client avec l’hôtel. Notre formation de réceptionniste d’hôtel '
                    'et d’auditeur de nuit (night auditor) prépare aux postes de front office des hôtels d’Abidjan : '
                    'accueil, réservations, logiciel hôtelier, facturation et clôture de la journée. Des compétences '
                    'recherchées de jour comme de nuit, et un bon point de départ pour devenir chef de réception.',
    },
    'directeur-hotel': {
        'h1': 'Formation directeur d’hôtel à Abidjan',
        'title': 'Formation directeur d’hôtel à Abidjan | EchoResta',
        'desc': 'Tu veux diriger un hôtel en Côte d’Ivoire ? Stratégie, revenue management, finances, RH et qualité : la formation des cadres de l’hôtellerie à Abidjan.',
        'pourquoi': 'Le tourisme d’affaires et les grands événements internationaux accueillis à Abidjan créent des '
                    'besoins en managers capables de piloter un établissement. Cette formation en management hôtelier '
                    'vous donne les outils de la direction d’hôtel : stratégie commerciale, revenue management, gestion '
                    'financière, ressources humaines et qualité de service.',
    },
    'serveur-hotesse': {
        'h1': 'Formation serveur et hôtesse à Abidjan',
        'title': 'Formation serveur et serveuse à Abidjan | EchoResta',
        'desc': 'Deviens serveur, serveuse ou hôtesse dans les hôtels et restaurants d’Abidjan : accueil, service à table, commandes, vins. Stage de 6 mois garanti.',
        'pourquoi': 'Restaurants, hôtels, traiteurs et événementiel : le métier de serveur ou de serveuse est l’un des plus '
                    'demandés de la restauration à Abidjan. Notre formation de serveur et d’hôtesse vous apprend '
                    'l’accueil, le service à table et la vente, pour être opérationnel dès votre premier poste et évoluer '
                    'vers chef de rang ou maître d’hôtel.',
    },
    'maitre-hotel': {
        'h1': 'Formation maître d’hôtel à Abidjan',
        'title': 'Formation maître d’hôtel à Abidjan | EchoResta Cocody',
        'desc': 'Serveur ou chef de rang, passe au niveau supérieur : direction de la salle, guéridon, accords mets-vins, clients VIP. Formation maître d’hôtel à Abidjan.',
        'pourquoi': 'Les restaurants gastronomiques et les hôtels haut de gamme d’Abidjan recherchent des maîtres d’hôtel '
                    'capables de diriger une salle et d’accueillir une clientèle exigeante. Cette formation s’adresse aux '
                    'serveurs et chefs de rang qui veulent évoluer : direction du service, service au guéridon, accords '
                    'mets et vins et protocole.',
    },
    'cuisinier': {
        'h1': 'Formation cuisinier à Abidjan',
        'title': 'Formation cuisine à Abidjan | École de cuisine EchoResta',
        'desc': 'Kédjénou, attiéké, sauce graine… et cuisine internationale ! Formation cuisinier à Abidjan : pâtisserie, hygiène HACCP, certification et stage garanti.',
        'pourquoi': 'Vous cherchez une école de cuisine à Abidjan ? Notre formation de cuisinier associe les techniques de '
                    'la cuisine professionnelle, la cuisine ivoirienne et africaine, la cuisine internationale et la '
                    'pâtisserie. Vous apprenez en cuisine, encadré par des chefs, avec les règles d’hygiène HACCP '
                    'exigées par les restaurants, les hôtels et les traiteurs.',
    },
    'bar-mixology': {
        'h1': 'Formation barman et mixologie à Abidjan',
        'title': 'Formation barman et mixologie à Abidjan | EchoResta',
        'desc': 'Deviens barman ou barmaid à Abidjan : cocktails, mocktails, spiritueux et gestion du bar pour hôtels, lounges et rooftops. Certification et stage garanti.',
        'pourquoi': 'Bars d’hôtel, lounges, rooftops et restaurants : la vie nocturne d’Abidjan offre de nombreux '
                    'débouchés aux barmen et barmaids formés. Notre formation de barman et de mixologie vous apprend les '
                    'cocktails classiques, la création de cocktails signatures avec les saveurs locales et la gestion '
                    'd’un bar.',
    },
    'directeur-restaurant': {
        'h1': 'Formation directeur de restaurant à Abidjan',
        'title': 'Formation gestion de restaurant à Abidjan | EchoResta',
        'desc': 'Tu veux ouvrir ou mieux gérer ton restaurant, ton maquis à Abidjan ? Coût matière, carte, rentabilité, équipe, marketing : la formation des restaurateurs.',
        'pourquoi': 'Vous dirigez un restaurant ou vous voulez ouvrir le vôtre à Abidjan ? Cette formation en gestion de '
                    'restaurant vous apprend à piloter la rentabilité, maîtriser le coût matière, construire une carte, '
                    'encadrer vos équipes et attirer de nouveaux clients, notamment grâce aux réseaux sociaux et aux '
                    'plateformes de livraison.',
    },
    'anglais-tourisme-hotellerie': {
        'h1': 'Formation anglais tourisme et hôtellerie à Abidjan',
        'title': 'Anglais hôtellerie et tourisme à Abidjan | EchoResta',
        'desc': 'Parle anglais avec les clients étrangers : accueil, réception, restaurant, téléphone, réclamations. Anglais pro pour l’hôtellerie à Abidjan, tous niveaux.',
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
