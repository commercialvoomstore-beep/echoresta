"""Pays d'Afrique de l'Ouest : nom, nationalité, indicatif téléphonique et drapeau (SVG dessiné ici)."""
import math


def _etoile(cx, cy, r, couleur):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.382
        pts.append(f'{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}')
    return f'<polygon points="{" ".join(pts)}" fill="{couleur}"/>'


def _bandes_v(*couleurs):
    w = 30 / len(couleurs)
    return ''.join(f'<rect x="{i * w:.2f}" width="{w + 0.05:.2f}" height="20" fill="{c}"/>' for i, c in enumerate(couleurs))


def _bandes_h(*bandes):
    """bandes : (couleur, hauteur) de haut en bas, sur 20."""
    out, y = [], 0
    for c, h in bandes:
        out.append(f'<rect y="{y:.2f}" width="30" height="{h + 0.05:.2f}" fill="{c}"/>')
        y += h
    return ''.join(out)


def _cap_vert():
    u = 20 / 12
    s = '<rect width="30" height="20" fill="#003893"/>'
    s += _bandes_h(('#003893', 6 * u), ('#fff', u), ('#cf2027', u), ('#fff', u))
    s += ''.join(_etoile(11.5 + 4.6 * math.cos(math.radians(i * 36)), 12.5 + 4.6 * math.sin(math.radians(i * 36)), 0.9, '#f7d116')
                 for i in range(10))
    return s


def _liberia():
    h = 20 / 11
    s = ''.join(f'<rect y="{i * h:.2f}" width="30" height="{h + 0.05:.2f}" fill="{"#bf0a30" if i % 2 == 0 else "#fff"}"/>' for i in range(11))
    c = 5 * h
    return s + f'<rect width="{c:.2f}" height="{c:.2f}" fill="#002868"/>' + _etoile(c / 2, c / 2, c * 0.33, '#fff')


def _mauritanie():
    return ('<rect width="30" height="20" fill="#006233"/>'
            '<circle cx="15" cy="10" r="5.6" fill="#ffc400"/><circle cx="15" cy="7.7" r="5.3" fill="#006233"/>'
            + _etoile(15, 7.4, 2.2, '#ffc400')
            + '<rect width="30" height="3" fill="#d01c1f"/><rect y="17" width="30" height="3" fill="#d01c1f"/>')


def _togo():
    s = _bandes_h(('#006a4e', 4), ('#ffce00', 4), ('#006a4e', 4), ('#ffce00', 4), ('#006a4e', 4))
    return s + '<rect width="12" height="12" fill="#d21034"/>' + _etoile(6, 6, 3.8, '#fff')


DESSINS = {
    'BJ': '<rect width="12" height="20" fill="#008751"/><rect x="12" width="18" height="10" fill="#fcd116"/><rect x="12" y="10" width="18" height="10" fill="#e8112d"/>',
    'BF': _bandes_h(('#ef2b2d', 10), ('#009e49', 10)) + _etoile(15, 10, 4, '#fcd116'),
    'CV': _cap_vert(),
    'CI': _bandes_v('#f77f00', '#fff', '#009e60'),
    'GM': _bandes_h(('#ce1126', 6.67), ('#fff', 1.11), ('#0c1c8c', 4.44), ('#fff', 1.11), ('#3a7728', 6.67)),
    'GH': _bandes_h(('#ce1126', 6.67), ('#fcd116', 6.67), ('#006b3f', 6.67)) + _etoile(15, 10, 3.3, '#000'),
    'GN': _bandes_v('#ce1126', '#fcd116', '#009460'),
    'GW': '<rect width="10" height="20" fill="#ce1126"/><rect x="10" width="20" height="10" fill="#fcd116"/><rect x="10" y="10" width="20" height="10" fill="#009e49"/>' + _etoile(5, 10, 3, '#000'),
    'LR': _liberia(),
    'ML': _bandes_v('#14b53a', '#fcd116', '#ce1126'),
    'MR': _mauritanie(),
    'NE': _bandes_h(('#e05206', 6.67), ('#fff', 6.67), ('#0db02b', 6.67)) + '<circle cx="15" cy="10" r="2.6" fill="#e05206"/>',
    'NG': _bandes_v('#008751', '#fff', '#008751'),
    'SN': _bandes_v('#00853f', '#fdef42', '#e31b23') + _etoile(15, 10, 3.3, '#00853f'),
    'SL': _bandes_h(('#1eb53a', 6.67), ('#fff', 6.67), ('#0072c6', 6.67)),
    'TG': _togo(),
}

# code, pays, nationalité, indicatif — la Côte d'Ivoire en premier, puis ordre alphabétique
PAYS = [
    ('CI', 'Côte d’Ivoire', 'Ivoirienne', '+225'),
    ('BJ', 'Bénin', 'Béninoise', '+229'),
    ('BF', 'Burkina Faso', 'Burkinabè', '+226'),
    ('CV', 'Cap-Vert', 'Cap-verdienne', '+238'),
    ('GM', 'Gambie', 'Gambienne', '+220'),
    ('GH', 'Ghana', 'Ghanéenne', '+233'),
    ('GN', 'Guinée', 'Guinéenne', '+224'),
    ('GW', 'Guinée-Bissau', 'Bissau-guinéenne', '+245'),
    ('LR', 'Liberia', 'Libérienne', '+231'),
    ('ML', 'Mali', 'Malienne', '+223'),
    ('MR', 'Mauritanie', 'Mauritanienne', '+222'),
    ('NE', 'Niger', 'Nigérienne', '+227'),
    ('NG', 'Nigeria', 'Nigériane', '+234'),
    ('SN', 'Sénégal', 'Sénégalaise', '+221'),
    ('SL', 'Sierra Leone', 'Sierra-léonaise', '+232'),
    ('TG', 'Togo', 'Togolaise', '+228'),
]


def drapeau(code, titre=''):
    t = f'<title>{titre}</title>' if titre else ''
    return (f'<svg class="flag" viewBox="0 0 30 20" preserveAspectRatio="none" role="img" aria-hidden="{"false" if titre else "true"}">'
            f'{t}{DESSINS[code]}</svg>')
