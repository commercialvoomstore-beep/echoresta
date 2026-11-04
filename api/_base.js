// Base de données Neon Postgres, partagée par api/envoyer.js (demandes) et api/fichier.js (documents joints).
// Les tables sont créées et mises à jour automatiquement au premier appel : rien à préparer à la main dans Neon.
//   demandes : une ligne par formulaire envoyé (réponses complètes dans « champs », colonnes lisibles pour les recherches)
//   fichiers : les documents envoyés avec une candidature (CV, photo, diplômes), avec leur lien de téléchargement
// Fichier préfixé par « _ » : Vercel ne le publie pas comme une adresse.

const { neon } = require('@neondatabase/serverless');

const BASE = process.env.DATABASE_URL || process.env.POSTGRES_URL || '';
const sql = BASE ? neon(BASE) : null;

let prete = null;
function preparer() {
  if (!prete) {
    prete = sql.transaction([
      sql`CREATE TABLE IF NOT EXISTS demandes (
        id bigserial PRIMARY KEY,
        recue_le timestamptz NOT NULL DEFAULT now(),
        formulaire text NOT NULL,
        sujet text NOT NULL,
        nom text,
        telephone text,
        email text,
        societe text,
        champs json NOT NULL,
        documents json,
        sections json,
        consentement text,
        page text,
        langue text,
        envoi_email text,
        accuse_email text)`,
      // Colonnes ajoutées depuis la première version de la table
      sql`ALTER TABLE demandes
        ADD COLUMN IF NOT EXISTS accuse_email text, ADD COLUMN IF NOT EXISTS nom text, ADD COLUMN IF NOT EXISTS telephone text,
        ADD COLUMN IF NOT EXISTS societe text, ADD COLUMN IF NOT EXISTS documents json, ADD COLUMN IF NOT EXISTS sections json,
        ADD COLUMN IF NOT EXISTS consentement text`,
      sql`CREATE TABLE IF NOT EXISTS fichiers (
        id bigserial PRIMARY KEY,
        recu_le timestamptz NOT NULL DEFAULT now(),
        demande_id bigint REFERENCES demandes (id) ON DELETE CASCADE,
        champ text NOT NULL,
        nom text NOT NULL,
        taille integer NOT NULL,
        type text NOT NULL,
        lien text,
        cle text NOT NULL,
        origine text,
        contenu bytea NOT NULL)`,
      sql`CREATE INDEX IF NOT EXISTS fichiers_demande_idx ON fichiers (demande_id)`,
      sql`CREATE INDEX IF NOT EXISTS fichiers_origine_idx ON fichiers (origine, recu_le)`,
    ]).catch(e => { prete = null; throw e; });
  }
  return prete;
}

module.exports = { sql, preparer };
