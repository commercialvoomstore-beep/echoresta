# EchoResta — site vitrine

Site statique (HTML, CSS, JavaScript) du cabinet de formation EchoResta, Hôtellerie & Restauration, Abidjan.

## Voir le site sur son ordinateur

Ouvrir le fichier `index.html` dans un navigateur (double-clic).

## Pages

| Fichier | Page |
| --- | --- |
| `index.html` | Accueil |
| `apropos.html` | À propos |
| `formations.html` | Catalogue des formations |
| `formation-*.html` | Fiche détaillée de chacune des 10 formations métiers |
| `contact.html` | Contact et inscription |
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

## À compléter

- Remplacer les photos de `images/` par les originales (mêmes noms de fichiers).
- Vérifier les durées, niveaux et rythmes des formations dans `_build/metiers.py`.
- Remplacer le numéro de téléphone provisoire (+225 07 00 00 00 00). Le WhatsApp est le +225 07 68 84 20 38.
- Brancher le formulaire de contact sur un service d'envoi (voir le commentaire dans `assets/main.js`).
