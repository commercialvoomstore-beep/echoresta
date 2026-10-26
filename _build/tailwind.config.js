// Tailwind CSS des pages de l'espace recrutement (espace client, espace candidat, page de choix).
// Régénérer assets/recrutement.css après une modification de _build/recrutement.py :
//   npx tailwindcss@3.4.17 -c _build/tailwind.config.js -i _build/tailwind.css -o assets/recrutement.css --minify
module.exports = {
  content: ['./espace_client.html', './espace_candidat.html', './recrutement.html', './assets/main.js'],
  prefix: 'tw-',                       // aucune collision avec les classes du site
  corePlugins: { preflight: false },   // pas de remise à zéro des styles du site
  theme: { extend: {
    colors: { nuit: { 50: '#f2f5fb', 100: '#e3e9f6', 200: '#c4d0ea', 600: '#22408f', 700: '#1a3480', 800: '#13296b', 900: '#0f2260', 950: '#0a1640' } },
    fontFamily: { serif: ['Merriweather', 'Georgia', 'serif'], sans: ['"Open Sans"', 'system-ui', 'sans-serif'] }
  } }
};
