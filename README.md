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
- Formulaires Contact, Rendez-vous et Inscription : envoyés par e-mail via Web3Forms (clé `WEB3FORMS_KEY` dans
  `_build/build.py`) à contact@voomnetformation.ci ; l'adresse affichée sur le site reste contact@echoresta.ci.
  En cas d'échec d'envoi, le visiteur peut transmettre sa demande sur WhatsApp.
