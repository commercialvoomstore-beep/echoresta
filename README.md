# EchoResta — site vitrine

Site statique (HTML, CSS, JavaScript) de l’école de formation EchoResta, École de l’Hôtellerie & Restauration, Abidjan.

## Voir le site sur son ordinateur

Ouvrir le fichier `index.html` dans un navigateur (double-clic).

## Pages

| Fichier | Page |
| --- | --- |
| `index.html` | Accueil |
| `apropos.html` | À propos |
| `formations.html` | Catalogue des formations |
| `formation-*.html` | Fiche détaillée de chacune des 10 formations métiers |
| `inscription.html` | Fiche d'inscription (pays et nationalités d'Afrique de l'Ouest avec drapeaux) |
| `rendez-vous.html` | Prise de rendez-vous |
| `contact.html` | Contact |
| `404.html` | Page introuvable |

Les styles sont dans `assets/style.css`, les scripts dans `assets/main.js` et les photos dans `images/`.

## Modifier le contenu

Les pages HTML sont générées par `_build/build.py`. Les textes des formations (durée, programme, journée type, évolution de carrière…) et le test d’orientation sont dans `_build/metiers.py`, le numéro WhatsApp en haut de `_build/build.py`.

Après une modification, régénérer les pages depuis la racine du dépôt :

```
python3 _build/build.py
```

Le dossier `_build` n’est pas mis en ligne sur Vercel (voir `.vercelignore`).

## Mise en ligne sur Vercel

Sur vercel.com : **Add New… → Project → Import Git Repository**, choisir ce dépôt, puis **Deploy**. Aucun réglage n'est nécessaire (pas de commande de build).

## Référencement (Google)

- Titres, descriptions, titres H1 et textes des pages : `_build/seo.py`.
- Chaque page contient une URL canonique, des balises de partage (Open Graph) et des données structurées
  (école, formations, fil d'Ariane, questions fréquentes).
- `sitemap.xml` (avec les images de chaque page) et `robots.txt` sont générés automatiquement.
- Code de vérification Google Search Console : `GOOGLE_VERIFICATION` dans `_build/seo.py`.
- Si le site change d'adresse (nom de domaine), modifier `BASE_URL` dans `_build/seo.py` puis régénérer.
- À faire hors du site : déclarer le site dans Google Search Console (envoyer `sitemap.xml`)
  et créer la fiche Google Business Profile de l'école (adresse 92JH+FW, Angré Star 14).

## À compléter

- Remplacer les photos de `images/` par les originales (mêmes noms de fichiers).
- Vérifier les durées, niveaux et rythmes des formations dans `_build/metiers.py`.
- Formulaires : voir « Réception des formulaires » ci-dessous. L'adresse affichée sur le site reste contact@echoresta.ci.

## Espace recrutement

- `recrutement.html` : page d'accueil du recrutement avec deux boutons, vers `espace_client.html`
  (fiche de besoin de personnel, pour les établissements) et `espace_candidat.html` (fiche d'inscription candidat).
- Ces pages sont générées par `_build/recrutement.py` ; leurs fiches sont reçues comme les autres formulaires.
  La fiche candidat envoie les documents (CV, photo, diplômes) avec la fiche : voir « Documents des candidats » ci-dessous.
- Le style vient de Tailwind CSS, compilé dans `assets/recrutement.css` (classes préfixées `tw-`).
  Après avoir modifié les classes de ces pages, recompiler :
  `npx tailwindcss@3.4.17 -c _build/tailwind.config.js -i _build/tailwind.css -o assets/recrutement.css --minify`

## Version anglaise (dossier `en/`)

- Le bouton **FR / EN** de la barre du haut passe d'une langue à l'autre sur la même page.
- Les pages anglaises sont créées automatiquement à chaque `python3 _build/build.py`, à partir des pages françaises
  et du dictionnaire `_build/traduction_en.json` (texte français → texte anglais). Voir `_build/traduction.py`.
- Après une modification d'un texte français, la construction affiche « N texte(s) à traduire » : la liste est dans
  `_build/traduction_manquante.json`. Ajoutez chaque texte et sa traduction dans `_build/traduction_en.json`, puis relancez.
  Tant qu'un texte n'est pas traduit, il reste en français sur la page anglaise.
- Les balises `hreflang`, l'adresse canonique et le plan du site (`sitemap.xml`) indiquent à Google les deux versions.

## Adresses sans « .html »

- Les pages s'ouvrent sans extension : `https://www.echoresta.ci/formations`, `https://www.echoresta.ci/en/formation-cuisinier`…
- `vercel.json` active `cleanUrls` : Vercel sert `formations.html` à l'adresse `/formations` et redirige
  définitivement les anciennes adresses en `.html` (les liens déjà partagés continuent de fonctionner).
- La construction retire `.html` de tous les liens internes, des adresses déclarées à Google et du `sitemap.xml`.
- Adresse du site déclarée à Google : `BASE_URL` dans `_build/seo.py` (actuellement `https://www.echoresta.ci/`).

## Contenu rédactionnel

- Les textes ajoutés aux pages (description des métiers, déroulement des formations, questions fréquentes, guide de choix,
  débouchés, étapes du recrutement) sont dans `_build/contenu.py`, à modifier pour changer le texte.
- Règles : uniquement des faits vérifiables (adresse, horaires, niveaux, programme, certification, stage) ; pas de chiffre,
  de salaire, de durée, de partenaire ni de témoignage inventé.
- Après une modification, relancer `python3 _build/build.py` : la version anglaise signale les textes à traduire
  (voir « Version anglaise »).

## Réception des formulaires (Neon Postgres + Microsoft 365)

Tous les formulaires (contact, rendez-vous, inscription, recherche du personnel, recherche d'emploi) sont envoyés à la
fonction Vercel `api/envoyer.js`, qui :
1. enregistre la demande dans la base **Neon Postgres**, table `demandes` (créée automatiquement au premier envoi) ;
2. l'envoie par e-mail dans la boîte **contact@voomnetformation.ci** (Microsoft 365, via Microsoft Graph, application
   « Echoresta » de Microsoft Entra ID, permission *Mail.Send* de type Application), avec « Répondre » vers le visiteur ;
3. note dans la colonne `envoi_email` si l'e-mail est parti.
Si rien n'a pu être enregistré ni envoyé, la page propose au visiteur d'envoyer sa demande sur WhatsApp.

Réglages, dans Vercel → projet → Settings → Environment Variables (puis **Redeploy**) :
- `MS_CLIENT_SECRET` : la **Valeur** du secret client (pas l'« ID du secret ») ;
- `DATABASE_URL` : ajoutée automatiquement quand la base Neon est reliée au projet (Storage → Neon) ;
- facultatif : `MS_TENANT_ID`, `MS_CLIENT_ID`, `MAIL_FROM`, `MAIL_TO` (valeurs par défaut dans `api/envoyer.js`).

Ce qui est enregistré pour chaque demande (table `demandes`) : les réponses complètes (`champs`), regroupées comme sur la
page (`sections`), et des colonnes lisibles pour chercher vite : `nom`, `telephone`, `email`, `societe`, `consentement`
(texte de la case cochée), `documents` (liste des documents avec leur lien), `envoi_email`, `accuse_email`.
Les tables sont créées et complétées automatiquement (`api/_base.js`) : aucune manipulation dans Neon.

Consulter les demandes : console Neon → SQL Editor → `SELECT * FROM demandes ORDER BY recue_le DESC;`
Les candidatures avec leurs documents :
`SELECT d.id, d.recue_le, d.nom, d.telephone, f.champ, f.nom AS fichier, f.lien FROM demandes d JOIN fichiers f ON f.demande_id = d.id ORDER BY d.id DESC;`
En cas de problème : Vercel → Logs, filtre `/api/envoyer` (les erreurs de Neon et de Microsoft y sont affichées).
Le secret client a une date d'expiration (Entra ID → Certificats et secrets) : le renouveler avant et mettre à jour Vercel.

### Documents des candidats (CV, photo, diplômes)

- La fiche candidat (`espace_candidat`) envoie chaque fichier à la fonction `api/fichier.js` avant la fiche elle-même :
  4 Mo au plus par fichier (limite de Vercel), formats PDF, Word, JPEG, PNG, WebP, HEIC (reconnus à leur contenu).
  Les photos sont réduites dans le navigateur (1600 px) : une photo de téléphone de 4 Mo arrive en 200 à 400 Ko.
- Les fichiers sont gardés dans la base Neon, table `fichiers` (contenu, nom, taille, type, demande liée, lien).
- L'e-mail de l'école joint les documents tant que le message reste sous la limite de Microsoft (4 Mo) ; chaque document
  a aussi un bouton « Ouvrir » (lien secret `https://www.echoresta.ci/api/fichier?n=…&k=…`), présent également dans le
  récapitulatif PDF de l'école. Le candidat reçoit la liste de ses documents, sans lien. La photo figure sur le PDF.
- Un fichier qui n'a pas pu être envoyé est signalé au candidat, qui peut alors l'envoyer sur WhatsApp.
- Place : l'offre gratuite de Neon donne 0,5 Go, soit plusieurs centaines de candidatures. Taille utilisée :
  `SELECT pg_size_pretty(pg_total_relation_size('fichiers'));`
