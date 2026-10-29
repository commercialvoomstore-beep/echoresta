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

## Espace recrutement

- `recrutement.html` : page d'accueil du recrutement avec deux boutons, vers `espace_client.html`
  (fiche de besoin de personnel, pour les établissements) et `espace_candidat.html` (fiche d'inscription candidat).
- Ces pages sont générées par `_build/recrutement.py` et envoyées par e-mail via Web3Forms, comme les autres formulaires.
  Les pièces jointes (CV, photo, diplômes) ne passent pas par e-mail avec l'offre gratuite de Web3Forms :
  après l'envoi, le candidat les transmet en un clic sur WhatsApp.
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
