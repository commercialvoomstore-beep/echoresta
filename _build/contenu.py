"""Textes ajoutés aux pages pour enrichir le contenu (référencement et information des visiteurs).

Règles de rédaction :
- uniquement des faits déjà présents sur le site (adresse, horaires, certification, stage, niveaux, modules) ou des
  connaissances générales sur les métiers : aucun chiffre, partenaire, salaire, durée ni témoignage inventé ;
- « double certification internationale (Côte d’Ivoire et Australie) » et « stage de 6 mois garanti » s'écrivent toujours ainsi ;
- pas de durée de formation, de rythme ni de « public » (retirés du site à la demande de l'école).
"""

# ============================================================== Pages des 10 formations
# Par formation : titre de la section « au quotidien », description du métier, déroulement et 3 questions en plus.
CONTENU_METIERS = {
    'valet-femme-chambre': {
        'titre_quotidien': 'Que fait une femme de chambre ou un valet au quotidien ?',
        'quotidien': 'Le valet ou la femme de chambre prépare les chambres avant l’arrivée des clients et les remet en état après leur départ : lits, salle de bain, poussière, produits d’accueil, minibar. C’est un travail physique et très encadré, où la régularité compte autant que la rapidité : une chambre doit être irréprochable à n’importe quelle heure et identique à celle d’à côté. Vous travaillez en équipe, sous la responsabilité de la gouvernante, et vous êtes souvent le premier à repérer un équipement défectueux ou un objet oublié.',
        'deroulement': 'Vous apprenez en pratiquant : les ateliers en chambre occupent chaque séance, et chaque geste est montré, répété puis corrigé par un formateur du métier. Le programme couvre l’organisation du chariot et l’ordre de travail, les standards des hôtels 3 à 5 étoiles, le nettoyage de chaque surface, la réfection des lits et le pliage du linge, la couverture du soir et les règles d’hygiène et de sécurité. Vous apprenez aussi à communiquer avec la gouvernante et la réception, car une chambre se prépare en lien avec toute l’équipe.',
        'faq': [
            ('Faut-il de l’expérience pour devenir femme de chambre ou valet d’hôtel ?',
             'Non. La formation est de niveau débutant : elle part des gestes de base (organisation du chariot, nettoyage, lit « au carré ») et les répète en atelier jusqu’à ce qu’ils deviennent naturels. Les hôtels recherchent avant tout de la rigueur, de la ponctualité et de la discrétion.'),
            ('Quelle est la différence entre une femme de chambre et une gouvernante ?',
             'La femme de chambre (ou le valet) prépare les chambres. La gouvernante organise le travail de toute l’équipe, contrôle chaque chambre avant l’arrivée des clients et gère le linge et les produits. C’est l’évolution naturelle après quelques années d’expérience.'),
            ('Le métier de femme de chambre est-il physiquement exigeant ?',
             'Oui, c’est un métier actif : on reste debout, on se déplace et on porte du linge et du matériel. La formation enseigne les bons gestes et les bonnes postures pour limiter la fatigue, et la bonne condition physique fait partie des qualités recherchées par les hôtels.'),
        ],
    },
    'gouvernante': {
        'titre_quotidien': 'Que fait une gouvernante d’hôtel au quotidien ?',
        'quotidien': 'La gouvernante est le chef d’orchestre des étages. Chaque matin, elle répartit les chambres entre les valets et les femmes de chambre selon les arrivées et les départs, puis contrôle les chambres terminées avant de les libérer à la réception. Elle gère aussi le linge, les produits d’entretien et les objets trouvés, signale les pannes à la maintenance et prépare en priorité les chambres des clients VIP. Son rôle associe exigence de qualité, organisation et management d’équipe.',
        'deroulement': 'La formation s’adresse à des personnes qui connaissent déjà le travail d’étage et veulent le diriger. Elle porte sur l’organisation des étages (répartition des chambres, priorités, clients VIP), le contrôle qualité avec check-lists et audits de chambres, la gestion du linge et des stocks, le management d’équipe (briefer, motiver, recadrer, former), les plannings et indicateurs, et la coordination avec la réception, la maintenance et la direction. Les ateliers pratiques sont animés par des professionnels de l’hébergement.',
        'faq': [
            ('Faut-il avoir été femme de chambre pour devenir gouvernante ?',
             'Ce n’est pas obligatoire, mais le niveau demandé est intermédiaire : connaître le travail d’étage aide beaucoup à contrôler les chambres et à encadrer une équipe. Si vous débutez, la formation Valet / Femme de chambre est un bon point de départ.'),
            ('Quelle est la différence entre une gouvernante d’étage et une gouvernante générale ?',
             'La gouvernante d’étage encadre une équipe sur un ou plusieurs étages. La gouvernante générale dirige l’ensemble du service des étages : plannings, budgets, linge, relations avec la réception et la direction. C’est une étape naturelle de l’évolution de carrière.'),
            ('Quels outils de gestion apprend-on à utiliser ?',
             'Les outils du quotidien d’une gouvernante : feuille de répartition des chambres, check-lists de contrôle qualité, inventaires de linge et de produits, planning de l’équipe et suivi des anomalies. Ils sont pratiqués en atelier pour être utilisables dès la prise de poste.'),
        ],
    },
    'audit-nuit': {
        'titre_quotidien': 'Que font un réceptionniste et un auditeur de nuit ?',
        'quotidien': 'Le réceptionniste est le premier visage de l’hôtel : il accueille les clients, enregistre les arrivées et les départs, gère les réservations et répond à leurs demandes. L’auditeur de nuit prend le relais quand l’hôtel s’endort : il accueille les arrivées tardives, veille à la sécurité, vérifie les encaissements de la journée et effectue la clôture comptable (« night audit ») dans le logiciel hôtelier avant le changement de date. C’est un métier de rigueur et de sang-froid, qui demande beaucoup d’autonomie.',
        'deroulement': 'Le programme couvre le front office (arrivées, départs et prise en main d’un logiciel hôtelier), la caisse et la facturation, la procédure de clôture pas à pas, les rapports et indicateurs (taux d’occupation, prix moyen, RevPAR), la sécurité de nuit et l’anglais de la réception. Il prépare aussi aux situations courantes du poste : arrivée sans réservation, erreur de facturation, demande particulière d’un client.',
        'faq': [
            ('Qu’est-ce que le « night audit » ?',
             'C’est la clôture comptable de la journée de l’hôtel, réalisée la nuit par l’auditeur dans le logiciel hôtelier : contrôle des factures et des encaissements, vérification des chambres occupées, édition des rapports, puis passage à la date du lendemain.'),
            ('Faut-il travailler de nuit toute sa carrière ?',
             'Non. L’audit de nuit est souvent une première expérience en réception. Avec l’expérience, on évolue vers un poste de réceptionniste confirmé de jour, puis chef de réception et responsable front office.'),
            ('L’anglais est-il nécessaire pour travailler à la réception d’un hôtel ?',
             'Il est très utile : les hôtels d’affaires et d’aéroport accueillent une clientèle internationale. Le programme comprend un module d’anglais de la réception, et la formation Anglais tourisme & hôtellerie permet d’aller plus loin.'),
        ],
    },
    'directeur-hotel': {
        'titre_quotidien': 'Que fait un directeur d’hôtel au quotidien ?',
        'quotidien': 'Le directeur d’hôtel est responsable de l’ensemble de l’établissement : chiffre d’affaires, qualité de service, équipes et réputation. Il suit chaque jour les indicateurs (taux d’occupation, prix moyen, avis des clients), réunit les chefs de service, rencontre les clients entreprises et arbitre les investissements. Il doit penser stratégie tout en restant présent sur le terrain, et savoir dialoguer avec les propriétaires, les équipes et les clients.',
        'deroulement': 'La formation de management s’adresse aux personnes qui ont déjà une première base : un niveau BAC+2 ou une expérience en hôtellerie. Elle combine les apports de gestion (stratégie et marketing hôtelier, revenue management, gestion financière, ressources humaines, qualité et e-réputation, réglementation) et des travaux pratiques à partir de tableaux de bord et de cas d’exploitation.',
        'faq': [
            ('Peut-on devenir directeur d’hôtel sans diplôme supérieur ?',
             'Le niveau demandé est BAC+2 ou une expérience en hôtellerie : une expérience solide dans un hôtel peut remplacer le diplôme. Un entretien de motivation avant l’inscription permet de vérifier que la formation correspond à votre parcours.'),
            ('Quelles compétences un directeur d’hôtel doit-il maîtriser ?',
             'La stratégie commerciale, le revenue management (prix et canaux de vente), la gestion financière, le management des équipes, la qualité de service et la réputation en ligne, ainsi que la réglementation d’hygiène et de sécurité. Ce sont les six modules du programme.'),
            ('Qu’est-ce que le revenue management ?',
             'C’est la gestion des prix et de la disponibilité des chambres pour maximiser le chiffre d’affaires : les tarifs sont ajustés selon la demande, la saison, les événements et les canaux de réservation (site de l’hôtel, plateformes en ligne, entreprises).'),
        ],
    },
    'serveur-hotesse': {
        'titre_quotidien': 'Que font un serveur et une hôtesse au quotidien ?',
        'quotidien': 'Le serveur ou la serveuse accueille les clients, les installe, présente la carte, prend la commande, la transmet en cuisine, sert les plats et les boissons, puis encaisse. L’hôtesse d’accueil reçoit les clients à leur arrivée, gère les réservations et les place en salle. Le métier se pratique en équipe, souvent en soirée et le week-end, avec des moments de forte affluence qui demandent de l’endurance, une bonne mémoire et le sourire.',
        'deroulement': 'Les ateliers se déroulent en salle : mise en place et art de la table, accueil et relation client, prise de commande et annonce en cuisine, service à l’assiette, au plat et au plateau, service des boissons et bases de l’œnologie, encaissement avec un logiciel de caisse. Chaque séance fait pratiquer les gestes du service sous le regard d’un formateur du métier.',
        'faq': [
            ('Quelle est la différence entre un serveur et une hôtesse d’accueil ?',
             'Le serveur ou la serveuse s’occupe du service à table : commande, plats, boissons, encaissement. L’hôtesse d’accueil reçoit les clients à leur arrivée, gère les réservations et les place en salle. Les deux métiers sont complémentaires dans un restaurant ou un hôtel et se travaillent ensemble dans la formation.'),
            ('Comment évoluer après avoir été serveur ?',
             'Avec l’expérience, un serveur devient chef de rang, puis maître d’hôtel et directeur de salle. La formation Maître d’hôtel est conçue pour franchir cette étape : service au guéridon, accords mets et vins, direction de salle.'),
            ('Faut-il parler anglais pour travailler en salle ?',
             'Ce n’est pas obligatoire pour débuter, mais c’est un vrai atout dans les hôtels et les restaurants qui reçoivent une clientèle internationale. La formation Anglais tourisme & hôtellerie existe pour cela ; pour un parcours associant plusieurs formations, contactez-nous.'),
        ],
    },
    'maitre-hotel': {
        'titre_quotidien': 'Que fait un maître d’hôtel au quotidien ?',
        'quotidien': 'Le maître d’hôtel dirige la salle pendant le service. Il vérifie les réservations et le plan de table, accueille les clients de marque, répartit les rangs entre les chefs de rang et les commis, surveille le rythme du service et intervient en cas de difficulté. Il conseille aussi les clients sur les plats et les vins et réalise des préparations devant eux, au guéridon. Élégance, diplomatie et sang-froid sont indispensables.',
        'deroulement': 'La formation prolonge l’expérience du service : direction du service (organiser la salle, répartir les rangs, gérer le rythme), service au guéridon (découpe, flambage, préparations devant le client), accords mets et vins, protocole pour les clients VIP, réservations et plans de table, encadrement de l’équipe de salle. Elle est animée par des professionnels de la salle.',
        'faq': [
            ('Quelle expérience faut-il avoir avant de devenir maître d’hôtel ?',
             'Une expérience en service est conseillée : la formation s’adresse aux serveurs et aux chefs de rang qui veulent diriger une salle. Si vous débutez, la formation Serveur / Hôtesse est le bon point de départ.'),
            ('En quoi consiste le service au guéridon ?',
             'Il s’agit de préparer ou de terminer un plat devant le client, sur une table roulante (le guéridon) : découpe, flambage, assaisonnement. C’est un savoir-faire de la grande restauration et des hôtels haut de gamme, qui demande de la précision et de l’aisance relationnelle.'),
            ('Quelle est la différence entre un maître d’hôtel et un directeur de restaurant ?',
             'Le maître d’hôtel dirige la salle et le service. Le directeur de restaurant gère l’ensemble de l’établissement : achats, carte, rentabilité, équipes de salle et de cuisine, marketing. Le maître d’hôtel peut évoluer vers ce poste avec la formation Directeur de restaurant.'),
        ],
    },
    'cuisinier': {
        'titre_quotidien': 'Que fait un cuisinier au quotidien ?',
        'quotidien': 'Le cuisinier réceptionne et contrôle les produits, prépare les légumes, les viandes et les poissons, réalise les plats de la carte selon les fiches techniques et dresse les assiettes. Il travaille en brigade, avec un chef et des commis, dans le respect strict des règles d’hygiène et de la chaîne du froid. Le « coup de feu » du service demande rapidité, organisation et résistance au stress, mais aussi un vrai plaisir à faire goûter.',
        'deroulement': 'L’apprentissage se fait en cuisine, encadré par des chefs en activité : hygiène et sécurité alimentaire (normes HACCP), techniques de base (taillage des légumes, fonds, sauces et cuissons), cuisine ivoirienne et africaine, cuisine internationale, pâtisserie, puis organisation de la brigade (mise en place, fiches techniques, coût matière).',
        'faq': [
            ('Apprend-on la cuisine ivoirienne en plus de la cuisine internationale ?',
             'Oui. Le programme comprend un module de cuisine ivoirienne et africaine (garba, kedjenou, sauce graine, attiéké revisités) et un module de cuisine internationale (classiques français, méditerranéens et asiatiques), pour pouvoir travailler en restaurant, en hôtel ou en traiteur.'),
            ('Peut-on devenir cuisinier sans diplôme ni expérience ?',
             'Oui. Le niveau demandé est débutant : la formation commence par l’hygiène et les techniques de base. Une grande partie du métier s’apprend en pratiquant, d’où l’importance des ateliers en cuisine.'),
            ('Qu’est-ce que la méthode HACCP ?',
             'Le HACCP est la méthode de maîtrise de l’hygiène alimentaire utilisée dans les restaurants, les hôtels et chez les traiteurs : elle identifie les risques à chaque étape (réception, stockage, préparation, service) et fixe les contrôles pour les éviter. Elle fait partie du premier module de la formation.'),
        ],
    },
    'bar-mixology': {
        'titre_quotidien': 'Que fait un barman au quotidien ?',
        'quotidien': 'Le barman ou la barmaid prépare et sert les boissons : cocktails classiques et créations, boissons chaudes et sans alcool, spiritueux, vins et bières. Il organise la mise en place du bar (fruits, sirops, glace, garnitures), conseille les clients, encaisse, tient les stocks et veille à un service responsable. Le bar est un lieu d’ambiance : le métier mêle dextérité, créativité et sens du contact.',
        'deroulement': 'Les ateliers se tiennent au bar : connaissance des produits (spiritueux, vins, bières, boissons sans alcool), mise en place, cocktails classiques, création de cocktails signatures avec les saveurs locales (bissap, gingembre, mangue), gestion des stocks et des coûts, service responsable. Aucun niveau n’est exigé pour commencer.',
        'faq': [
            ('Quelle est la différence entre un barman et un mixologue ?',
             'Le barman prépare et sert les boissons avec rapidité. Le mixologue met l’accent sur la création : il compose des cocktails originaux en travaillant les saveurs, les techniques et la présentation. La formation Bar & mixologie couvre les deux : les cocktails classiques de référence et les cocktails signatures.'),
            ('Sert-on uniquement des boissons alcoolisées ?',
             'Non. Le bar prépare aussi des boissons sans alcool, des boissons chaudes et des cocktails sans alcool, de plus en plus demandés. Le programme inclut un module de service responsable : accueil, conseil, animation et prévention.'),
            ('Où peut travailler un barman à Abidjan ?',
             'Dans les bars d’hôtel, les lounges et les rooftops, les restaurants et l’événementiel. Avec l’expérience, on évolue vers les postes de chef barman, puis de bar manager.'),
        ],
    },
    'directeur-restaurant': {
        'titre_quotidien': 'Que fait un directeur de restaurant au quotidien ?',
        'quotidien': 'Le directeur de restaurant pilote l’établissement au quotidien : il analyse les ventes, travaille avec les fournisseurs, suit le coût matière, construit la carte avec le chef, recrute et planifie les équipes de salle et de cuisine, et veille à la qualité de l’accueil. Il est aussi responsable de la visibilité du restaurant (réseaux sociaux, plateformes de livraison, avis clients) et du respect des règles d’hygiène et de sécurité.',
        'deroulement': 'Le programme est centré sur la gestion : lecture d’un compte d’exploitation et du seuil de rentabilité, achats, stocks et fiches techniques, conception d’une carte qui plaît et qui rapporte, management des équipes (recrutement, plannings, motivation), marketing et avis clients, réglementation. Il s’adresse aux responsables de salle, aux restaurateurs et aux porteurs de projet.',
        'faq': [
            ('La formation convient-elle pour ouvrir son propre restaurant ou maquis ?',
             'Oui. Elle donne les bases de gestion nécessaires pour ouvrir un établissement : calcul du coût matière, prix de vente, seuil de rentabilité, organisation des équipes et marketing. Elle s’adresse aussi bien aux salariés qu’aux porteurs de projet.'),
            ('Qu’est-ce que le coût matière ?',
             'C’est la part du prix de vente d’un plat qui correspond au coût des ingrédients. Le calculer plat par plat, à partir des fiches techniques, permet de fixer des prix rentables et de limiter les pertes : c’est l’un des premiers indicateurs d’un restaurant bien géré.'),
            ('Faut-il savoir cuisiner pour diriger un restaurant ?',
             'Ce n’est pas obligatoire, mais connaître le fonctionnement d’une cuisine et d’une salle aide à dialoguer avec le chef et les équipes. La formation, de niveau BAC ou expérience en restauration, se concentre sur la gestion : achats, carte, rentabilité et management.'),
        ],
    },
    'anglais-tourisme-hotellerie': {
        'titre_quotidien': 'À quoi sert l’anglais dans l’hôtellerie et le tourisme ?',
        'quotidien': 'En hôtellerie, en restauration et dans le tourisme, l’anglais sert à tout : accueillir un client à la réception, répondre au téléphone, présenter une carte, expliquer un tarif, traiter une réclamation avec tact, conseiller sur les sites à visiter à Abidjan. Le vocabulaire est précis et les situations reviennent souvent : on progresse en les travaillant par thèmes, avec des jeux de rôle.',
        'deroulement': 'Les séances sont organisées autour de situations professionnelles : accueil et conversation, réception et réservations, restaurant et bar, téléphone et e-mails, réclamations, tourisme à Abidjan. Chaque séance alterne vocabulaire du jour, jeu de rôle, correction et expressions clés à retenir, avec une mission à préparer pour la séance suivante. Tous les niveaux sont acceptés.',
        'faq': [
            ('Faut-il déjà parler anglais pour suivre la formation ?',
             'Non. Tous les niveaux sont acceptés. Le programme part de situations simples (se présenter, accueillir, répondre au téléphone) et monte progressivement vers les cas plus délicats, comme les réclamations.'),
            ('L’anglais est-il vraiment utile pour travailler dans un hôtel d’Abidjan ?',
             'Oui. Les hôtels d’affaires, les hôtels d’aéroport, les agences de voyage et les compagnies aériennes reçoivent une clientèle internationale. Parler anglais ouvre des postes de réceptionniste, de concierge ou d’agent d’accueil bilingue, et facilite l’évolution de carrière.'),
            ('Peut-on suivre l’anglais en plus d’une formation métier ?',
             'L’anglais est un bon complément d’une formation métier (réception, service, bar) pour être à l’aise avec une clientèle étrangère. Pour organiser un parcours associant plusieurs formations, contactez-nous : un conseiller vous renseigne.'),
        ],
    },
}

# ============================================================== Page Formations : choisir selon son profil
FORMATIONS_GUIDE_TITRE = 'Quelle formation choisir selon votre profil ?'
FORMATIONS_GUIDE_INTRO = 'Chaque fiche indique le niveau demandé. Voici les parcours qui correspondent le mieux à votre situation.'
# (icône, titre, texte avec liens vers les fiches : {slug} est remplacé par l'adresse de la formation)
FORMATIONS_GUIDE = [
    ('i-level', 'Je débute, sans diplôme',
     '<a class="link" href="{valet-femme-chambre}">Valet / Femme de chambre</a>, <a class="link" href="{serveur-hotesse}">Serveur / Hôtesse</a> et <a class="link" href="{cuisinier}">Cuisinier</a> sont de niveau débutant. <a class="link" href="{bar-mixology}">Bar &amp; mixologie</a> et <a class="link" href="{anglais-tourisme-hotellerie}">Anglais</a> acceptent tous les niveaux.'),
    ('i-clipboard', 'J’ai déjà de l’expérience',
     '<a class="link" href="{gouvernante}">Gouvernante</a> (niveau intermédiaire) pour encadrer une équipe d’étage, ou <a class="link" href="{maitre-hotel}">Maître d’hôtel</a> (expérience en service conseillée) pour diriger une salle.'),
    ('i-trend', 'Je vise un poste de direction',
     '<a class="link" href="{directeur-hotel}">Directeur d’hôtel</a> (BAC+2 ou expérience en hôtellerie) ou <a class="link" href="{directeur-restaurant}">Directeur de restaurant</a> (BAC ou expérience en restauration).'),
    ('i-lang', 'J’aime la clientèle internationale',
     '<a class="link" href="{audit-nuit}">Audit de nuit / Réceptionniste</a> (niveau BAC conseillé) et <a class="link" href="{anglais-tourisme-hotellerie}">Anglais tourisme &amp; hôtellerie</a> préparent à accueillir des clients du monde entier.'),
]
FORMATIONS_FAQ_PLUS = [
    ('Quelle formation choisir si je n’ai aucun diplôme ?',
     'Les formations de niveau débutant (Valet / Femme de chambre, Serveur / Hôtesse, Cuisinier) et celles ouvertes à tous les niveaux (Bar & mixologie, Anglais tourisme & hôtellerie) peuvent se suivre sans diplôme spécifique. Un entretien de motivation est réalisé avant l’inscription.'),
    ('Quels documents faut-il pour s’inscrire ?',
     '2 photos d’identité récentes, 1 copie de la pièce d’identité et 1 CV. Vous remplissez d’abord la fiche d’inscription en ligne ; notre équipe vous indique ensuite comment transmettre les pièces.'),
    ('Les formations sont-elles ouvertes aux candidats hors d’Abidjan ?',
     'Oui. Elles sont ouvertes aux candidats de toutes les communes d’Abidjan, de l’intérieur du pays et des pays d’Afrique de l’Ouest : la fiche d’inscription en ligne permet d’indiquer votre pays.'),
]

# ============================================================== Page À propos
APROPOS_PEDAGOGIE_TITRE = 'Une pédagogie centrée sur la pratique'
APROPOS_PEDAGOGIE = [
    ('i-clipboard', 'Des cours pour comprendre',
     'Les bases du métier : normes d’hygiène et de sécurité, standards des établissements, vocabulaire professionnel, gestion et organisation.'),
    ('i-chef', 'Des ateliers pour pratiquer',
     'En cuisine, en salle, au bar et en chambre, vous répétez les gestes du métier en petits groupes, avec un formateur qui corrige en direct.'),
    ('i-building', 'Une immersion pour s’insérer',
     'Le stage de 6 mois garanti dans les plus grands hôtels vous met en situation réelle et prépare votre entrée dans l’emploi.'),
]
APROPOS_EMPLOI_TITRE = 'Un accompagnement vers l’emploi'
APROPOS_EMPLOI = [
    'La formation ne s’arrête pas à la remise de la double certification internationale (Côte d’Ivoire et Australie). Le stage de 6 mois garanti dans les plus grands hôtels est le premier pas vers l’emploi : vous y découvrez le rythme réel d’un établissement et vous faites connaître votre travail.',
    'EchoResta propose aussi un <a class="link" href="recrutement.html">espace recrutement</a> : les hôtels, restaurants et particuliers décrivent leur besoin en personnel, les professionnels de l’hôtellerie et de la restauration déposent leur fiche, et notre équipe les met en relation.',
    'L’école accueille des élèves et étudiants, des personnes sans emploi, des salariés de l’hôtellerie ou d’un autre secteur et des entrepreneurs. La fiche d’inscription accepte les candidats de toute l’Afrique de l’Ouest.',
]
APROPOS_FAQ = [
    ('Qu’est-ce qu’EchoResta ?',
     'EchoResta est une école de formation en hôtellerie et restauration située à Angré Star 14, dans la commune de Cocody, à Abidjan. Elle propose dix formations professionnelles, du métier de femme de chambre à celui de directeur d’hôtel, en passant par la cuisine, le service en salle, le bar et l’anglais.'),
    ('Qui peut s’inscrire à l’école ?',
     'Les élèves et étudiants, les personnes sans emploi, les salariés de l’hôtellerie ou d’un autre secteur et les entrepreneurs. Le niveau demandé est précisé sur chaque formation ; les candidats de moins de 18 ans s’inscrivent avec l’accord d’un parent ou d’un tuteur.'),
    ('Les formateurs sont-ils des professionnels du métier ?',
     'Oui. Les cours et les ateliers sont animés par des professionnels du secteur, chefs, maîtres d’hôtel, gouvernantes, qui exercent dans les établissements d’Abidjan.'),
    ('Puis-je visiter l’école avant de m’inscrire ?',
     'Oui. Prenez rendez-vous en ligne, du lundi au vendredi, pour une visite, un entretien d’orientation ou une inscription.'),
]

# ============================================================== Page Contact
CONTACT_VOIES_TITRE = 'Trois façons de nous joindre'
CONTACT_VOIES = [
    ('i-phone', 'Par téléphone ou WhatsApp',
     'Appelez le +225 07 68 84 20 38 ou écrivez-nous sur WhatsApp du lundi au vendredi, de 8h à 17h : un conseiller vous répond.'),
    ('i-mail', 'Par le formulaire',
     'Décrivez votre projet dans le formulaire ci-dessus : notre équipe vous répond sous 48 h.'),
    ('i-pin', 'Sur place, sur rendez-vous',
     'Venez à l’école, Angré Star 14, Cocody, pour une visite ou un entretien d’orientation : prenez rendez-vous en ligne.'),
]
CONTACT_FAQ = [
    ('Comment venir à l’école ?',
     'L’école est à Angré Star 14, dans la commune de Cocody, à Abidjan. Le code de localisation Google 92JH+FW permet de lancer l’itinéraire depuis Google Maps : utilisez le bouton « Itinéraire » de la carte, plus bas sur cette page.'),
    ('Sous quel délai répondez-vous ?',
     'Notre équipe répond sous 48 h aux messages envoyés par le formulaire. Pour une réponse plus rapide, appelez-nous ou écrivez-nous sur WhatsApp du lundi au vendredi, de 8h à 17h.'),
    ('Puis-je visiter l’école avant de m’inscrire ?',
     'Oui. Prenez rendez-vous en ligne, du lundi au vendredi, de 9 h à 16 h, pour une visite, un entretien d’orientation ou une inscription.'),
    ('Comment m’inscrire si j’habite loin d’Abidjan ?',
     'Remplissez la fiche d’inscription en ligne depuis chez vous : notre équipe vous rappelle pour un entretien d’inscription. Les candidats d’une autre ville ou d’un autre pays peuvent aussi nous joindre par téléphone ou sur WhatsApp.'),
]

# ============================================================== Page Recrutement
RECRUTEMENT_ETAPES_TITRE = 'Comment ça marche ?'
RECRUTEMENT_ETAPES_EMPLOYEURS = [
    ('Décrivez votre besoin', 'Remplissez la fiche : profils recherchés, tâches, niveau d’études, conditions de travail et salaire proposé.'),
    ('Nous étudions votre demande', 'Notre équipe analyse votre besoin et sélectionne des profils formés aux métiers de l’hôtellerie et de la restauration.'),
    ('Recevez des profils adaptés', 'Nous vous recontactons rapidement avec des candidats qui correspondent à votre établissement.'),
]
RECRUTEMENT_ETAPES_CANDIDATS = [
    ('Remplissez votre fiche', 'Indiquez votre identité, vos expériences, l’emploi recherché et vos conditions de travail.'),
    ('Envoyez vos justificatifs', 'Transmettez en un clic votre CV, votre photo et vos diplômes sur WhatsApp, depuis la page de confirmation.'),
    ('Soyez mis en relation', 'Notre équipe vous met en relation avec des hôtels et des restaurants qui recrutent.'),
]
RECRUTEMENT_ATOUTS_TITRE = 'Pourquoi passer par EchoResta ?'
RECRUTEMENT_ATOUTS = [
    ('i-award', 'Une école du métier', 'EchoResta forme aux métiers de l’hôtellerie et de la restauration : nous savons ce que recherchent les établissements.'),
    ('i-users', 'Un interlocuteur unique', 'Une seule équipe pour vos demandes, joignable par téléphone, WhatsApp ou e-mail du lundi au vendredi.'),
    ('i-target', 'Tous les services couverts', 'Réception, étages, salle, bar, cuisine, direction : la fiche couvre l’ensemble des métiers de l’hôtellerie-restauration.'),
]
RECRUTEMENT_FAQ = [
    ('Quels métiers peut-on recruter ?',
     'Tous les services de l’hôtellerie et de la restauration : réception et hébergement, étages et lingerie, restaurant et salle, bar, cuisine, direction et gestion, loisirs et services annexes. Vous les retrouvez dans la fiche de besoin.'),
    ('À qui s’adresse l’espace candidat ?',
     'Aux professionnels de l’hôtellerie et de la restauration qui cherchent un emploi : cuisine, salle, bar, réception, étages. La fiche d’inscription candidat se remplit en quelques minutes.'),
    ('Comment envoyer mon CV et mes diplômes ?',
     'Remplissez la fiche candidat en ligne, puis envoyez votre CV, votre photo et vos diplômes sur WhatsApp en un clic depuis la page de confirmation : le message est déjà rédigé.'),
    ('En combien de temps suis-je recontacté ?',
     'Notre équipe étudie votre demande et vous recontacte rapidement. Pour toute question, appelez le +225 07 68 84 20 38 ou écrivez-nous sur WhatsApp du lundi au vendredi, de 8h à 17h.'),
]

# ============================================================== Page d'accueil
ACCUEIL_DEBOUCHES_TITRE = 'Où travailler après la formation ?'
ACCUEIL_DEBOUCHES_INTRO = 'Les métiers enseignés à l’école s’exercent dans des établissements très variés, à Abidjan comme dans toute la Côte d’Ivoire.'
ACCUEIL_DEBOUCHES = [
    ('i-building', 'Hôtels et résidences',
     'Réception, étages, salle, direction : hôtels d’affaires et d’aéroport, resorts, lodges et résidences hôtelières emploient tous les métiers de l’école.'),
    ('i-utensils', 'Restaurants et traiteurs',
     'Salle, cuisine, bar ou direction : restaurants indépendants et gastronomiques, chaînes de restauration, traiteurs et événementiel.'),
    ('i-cocktail', 'Bars, lounges et rooftops',
     'La vie nocturne d’Abidjan offre de nombreux débouchés aux barmen, barmaids et serveurs formés au service et aux cocktails.'),
    ('i-heart', 'Cliniques et résidences de standing',
     'Cliniques et hôpitaux privés, résidences de luxe et résidences diplomatiques recherchent des équipes d’étage et de service formées.'),
]
ACCUEIL_FAQ_PLUS = [
    ('Peut-on se former sans diplôme ?',
     'Oui, pour les formations de niveau débutant (valet / femme de chambre, serveur / hôtesse, cuisinier) et celles ouvertes à tous les niveaux (bar et mixologie, anglais). Les formations plus avancées demandent un niveau d’études ou une expérience précisés sur chaque fiche.'),
    ('L’école accueille-t-elle des candidats d’autres villes ou d’autres pays ?',
     'Oui. Les formations sont ouvertes aux candidats de toutes les communes d’Abidjan, de l’intérieur du pays et des pays d’Afrique de l’Ouest. Pour toute question sur votre situation, appelez-nous ou écrivez-nous sur WhatsApp.'),
    ('Comment trouver un emploi après la formation ?',
     'Chaque parcours se termine par un stage de 6 mois garanti dans les plus grands hôtels. EchoResta propose aussi un espace recrutement : les établissements y décrivent leur besoin en personnel et les candidats y déposent leur fiche.'),
    ('Comment choisir ma formation ?',
     'Faites le test d’orientation de la page d’accueil : trois questions vous suggèrent le métier qui vous correspond. Vous pouvez aussi prendre rendez-vous pour un entretien d’orientation à l’école.'),
]
