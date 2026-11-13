import json, datetime as dt

START = dt.date(2026, 11, 16)  # lundi S1

PH = {
 'BASE':   ('Base et force', 'Installer le renfo lourd 2×/sem, foncier Z2, une séance plaisir.'),
 'FETES':  ('Fêtes', 'Semaine allégée avant le départ.'),
 'JAPON':  ('Japon', 'Du 26/12 au 11/01. Entretien : marche, footing court si possible, renfo poids du corps.'),
 'RETOUR': ('Retour du Japon', 'Semaine tampon : décalage horaire, fatigue du voyage, reprise en douceur.'),
 'BASE2':  ('Base 2 et retest', 'Reprise après le Japon, retest labo, recalage des zones.'),
 'CONS':   ('Construction Forts', 'Volume et D+ en hausse, côtes longues, premiers back-to-back, renfo lourd maintenu.'),
 'SPE':    ('Spécifique Forts', 'Semaines pic façon S13 : gros week-ends, reco du parcours, nutrition complète.'),
 'AFF':    ('Affûtage Forts', 'Formule qui a marché : dernière grosse SL à J-14, jours off possibles, openers courts.'),
 'RACE1':  ('Trail des Forts', '72 km, 2800 m D+, sans bâtons. Samedi 8 mai, 7h, La Rodia.'),
 'RECUP':  ('Récup', 'Marche, vélo souple. Pas de course tant que descendre un escalier n\'est pas indolore.'),
 'MONT':   ('Construction montagne', 'Bâtons introduits, gros D+, back-to-back, SL jusqu\'à 6 h, renfo lourd 2×/sem.'),
 'SPE2':   ('Spécifique Wild', 'Altitude, nuit, très gros week-ends, sommeil et nutrition de 20 h+.'),
 'AFF2':   ('Affûtage Wild', 'Trois semaines, dernière SL longue à J-20, dernière moyenne à J-13.'),
 'RACE2':  ('Wildstrubel', 'Wild 110 : 113 km, 6600 m D+, vendredi 10 septembre 23h, Crans-Montana. Barrière 30 h.'),
}

R_A = 'Renfo Force jambes'
R_B = 'Renfo Excentrique descente'
R_A1 = 'Renfo Force jambes (1 série de moins)'

# (phase, heures, D+, [séances clés], note)
W = [
 ('BASE', 5.0, 800,  [R_A, R_B, 'SL 1h30 +400, FC < 150', 'Séance plaisir au choix'], "Démarrer le renfo à 2/3 des charges : les courbatures baissent dès la 2e exposition."),
 ('BASE', 5.5, 1000, [R_A, R_B, 'SL 1h45 +500', 'Côtes courtes 6 × 1\''], ''),
 ('BASE', 6.0, 1200, [R_A, R_B, 'SL 2h +600', 'Côtes courtes 8 × 1\''], ''),
 ('BASE', 4.5, 700,  [R_A1, R_B, 'SL 1h30 +400'], "Semaine allégée : pas de séance plaisir."),
 ('BASE', 6.5, 1400, [R_A, R_B, 'SL 2h15 +700', 'Côtes courtes 8 × 1\'15'], ''),
('FETES', 4.0, 600, [R_A, R_B, 'SL 1h45 +500', 'Pas de séance de qualité'], "Fêtes et départ le 26/12 : semaine allégée, priorité au sommeil."),
 ('JAPON', 3.0, 300, ['Renfo poids du corps 2× (fentes bulgares tempo, mollets, nordic)', 'Footings 30-45\' si possible'], "Japon du 26/12 au 11/01. Marcher beaucoup suffit, les onsen comptent comme récup."),
 ('JAPON', 3.0, 300, ['Renfo poids du corps 2×', 'Footings 30-45\' si possible'], "Retour le 11/01."),
 ('RETOUR', 4.0, 600, ['Renfo Force jambes léger (2/3 des charges)', 'Footings faciles uniquement, FC < 145'], "Décalage horaire et fatigue du voyage : rien de dur avant d'avoir retrouvé VFC et sommeil."),
 ('BASE2', 5.5, 1100, [R_A, R_B, 'SL 2h +700', 'Retest labo (cette semaine ou la suivante)'], "Arriver frais au labo : 48 h faciles avant."),
 ('BASE2', 6.5, 1500, [R_A, R_B, 'SL 2h30 +800', 'Seuil plat 2 × 10\''], "Recaler les zones et le plafond Z2 sur le retest."),
 ('CONS', 7.5, 1900, [R_A, R_B, 'SL 3h +1100', 'Côtes longues 3 × 8\''], "Nutrition : 60-70 g/h sur la SL."),
 ('CONS', 8.0, 2100, [R_A, R_B, 'B2B : SL 3h +1200, J2 1h30 +600', 'Côtes courtes 10 × 1\''], "Premier back-to-back : sanctuarisé avant le volume."),
 ('CONS', 5.5, 1200, [R_A1, R_B, 'SL 2h +700'], "Semaine allégée."),
 ('CONS', 8.5, 2300, [R_A, 'Renfo Excentrique descente + pliométrie légère', 'SL 3h30 +1400 : reco Forts partie 1', 'Côtes longues 3 × 10\''], ''),
 ('CONS', 9.0, 2500, [R_A, R_B, 'B2B : SL 3h30 +1500, J2 2h +800', 'Seuil 3 × 8\''], ''),
 ('CONS', 9.5, 2600, [R_A, 'Renfo Circuit endurance (remplace Excentrique)', 'SL 4h +1600 : reco Forts partie 2, descentes travaillées', 'Côtes longues 4 × 10\''], "Nutrition 80-90 g/h, sodium 580-690 mg/h."),
 ('CONS', 6.0, 1400, [R_A1, R_B, 'SL 2h30 +900'], "Semaine allégée."),
 ('CONS', 10.0, 2800, [R_A, R_B, 'B2B : SL 4h +1700, J2 2h +900', 'Côtes courtes 10 × 1\'15'], ''),
 ('CONS', 10.0, 2800, [R_A, 'Renfo Circuit endurance', 'SL 4h30 +1800 : reco fin de parcours Forts', 'Côtes longues allure course 3 × 12\''], "Tester le passage gels vers solide/salé à partir de 2h30."),
 ('SPE', 11.0, 3200, [R_A, 'Renfo Circuit endurance', 'WE choc : SL 5h +2000, J2 2h30 +1000', 'Côtes longues allure course'], "Semaine pic, modèle S13. Protocole nutrition complet."),
 ('SPE', 9.5, 2600, ['Renfo Force jambes : dernière séance lourde', 'B2B : SL 4h +1600, J2 1h30 +600', 'Seuil 2 × 10\''], ''),
 ('AFF', 7.0, 1600, ['Renfo Excentrique descente léger', 'Dernière grosse SL : 3h +1200, réellement facile (sam. 24/04)'], "Affûtage S1."),
 ('AFF', 5.0, 1000, ['Openers : 2 × 8\' seuil ou lignes', 'Renfo stop à J-10 (mer. 28/04)'], "2-3 jours off possibles sans perte."),
 ('RACE1', 3.0, 2800, ['Veille : 15-20\' plat + 3-4 lignes', 'COURSE : Trail des Forts, sam. 8 mai 7h00'], "Charge glucidique J-2/J-1 à 8-10 g/kg. Petit-déjeuner 3 h avant. Départ prudent, power-hike sans bâtons > 15 %."),
 ('RECUP', 2.5, 300, ['Marche et vélo souple', 'Aucune course avant escaliers indolores'], ''),
 ('RECUP', 4.0, 600, ['Footings faciles 30-45\'', 'Renfo léger en fin de semaine'], "Décision définitive Wild 110 ou 70 selon la course et la récup."),
 ('MONT', 7.0, 2000, [R_A, R_B, 'SL 3h +1300 en montagne', 'Introduire les bâtons en power-hike'], ''),
 ('MONT', 8.5, 2800, [R_A, R_B, 'SL 4h +1800', 'Côtes longues 3 × 12\' avec bâtons'], ''),
 ('MONT', 10.0, 3500, [R_A, R_B, 'B2B : SL 4h +2000, J2 2h30 +1200', 'Côtes courtes 10 × 1\''], ''),
 ('MONT', 6.0, 1800, [R_A1, R_B, 'SL 2h30 +1000'], "Semaine allégée."),
 ('MONT', 11.0, 4000, [R_A, 'Renfo Circuit endurance', 'SL 5h30 +2500 (Jura haut ou Alpes)', 'Côtes longues 4 × 12\' bâtons'], ''),
 ('MONT', 12.0, 4500, [R_A, R_B, 'B2B : SL 5h +2500, J2 3h +1500', 'Descente longue travaillée (1500 m D-)'], ''),
 ('MONT', 12.5, 4800, [R_A, 'Renfo Circuit endurance', 'SL 6h +3000 : test nutrition 6 h (gels puis solide/salé)'], "C'est l'heure 6-8 qui lasse : tester les textures salées."),
 ('MONT', 7.0, 2200, [R_A1, R_B, 'SL 3h +1200'], "Semaine allégée."),
 ('SPE2', 13.0, 5000, ['Renfo Force jambes (1×)', 'Bloc montagne : 3 jours de 4-6 h, 2000-2800 m'], "Idéalement en Valais ou dans les Alpes : altitude du parcours."),
 ('SPE2', 7.0, 2000, ['Renfo Force jambes (1×)', 'SL 3h +1200'], "Récup du bloc."),
 ('SPE2', 14.0, 5500, ['Renfo Excentrique descente (1×)', 'SL de nuit : départ 23h, 7-8 h +3500', 'J2 : 2h facile'], "Répétition du départ du Wild : sieste l'après-midi, frontale, alimentation de nuit."),
 ('SPE2', 15.0, 6000, ['Renfo Force jambes : dernière séance lourde', 'WE choc final : SL 6h +3000, J2 4h +2000'], "Dernier très gros week-end."),
 ('AFF2', 10.0, 3500, ['Renfo Excentrique descente léger', 'SL 5h +2500 (J-20, réellement facile)', 'Côtes longues 3 × 10\' bâtons'], ''),
 ('AFF2', 7.0, 2000, ['SL 3h30 +1500 facile (sam. 28/08)', 'Renfo stop à J-10 (mar. 31/08)'], ''),
 ('AFF2', 5.0, 1000, ['Openers courts', '2-3 jours off possibles', 'Décaler le sommeil : siestes'], ''),
 ('RACE2', 3.0, 6600, ['Veille : 15-20\' facile + lignes', 'COURSE : Wild 110, ven. 10 sept. 23h00, Crans-Montana (ou Wild 70, 7h00, Kandersteg)'], "Dormir le vendredi après-midi. Départ très prudent : la nuit et l'altitude font le tri."),
]

weeks = []
for i, (ph, h, dp, keys, note) in enumerate(W):
    d0 = START + dt.timedelta(days=7 * i)
    weeks.append({'n': i + 1, 'start': d0.isoformat(), 'phase': ph, 'h': h, 'dp': dp, 'keys': keys, 'note': note})


import re
JOURS = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
JAPON = (dt.date(2026, 12, 26), dt.date(2027, 1, 11))

def mins(txt, pre=''):
    m = re.search(pre + r'(\d+)h(\d{2})?', txt)
    if m: return int(m.group(1)) * 60 + int(m.group(2) or 0)
    m = re.search(pre + r"(\d+)'", txt)
    return int(m.group(1)) if m else None

def r5(x): return int(round(x / 5.0) * 5)

def work_days(i):
    # S1 (sem. ISO 47, impaire) : travail mer jeu ven ; alternance continue ensuite
    return {2, 3, 4} if i % 2 == 0 else {0, 2, 3}

def qual_min(k):
    if 'Côtes longues' in k: return 85
    if 'Côtes courtes' in k: return 65
    if 'Seuil' in k: return 60
    if 'Descente' in k: return 90
    if 'Openers' in k: return 40
    return 60

# Progression HIIT, dehors en priorité (piste ou côte), Zwift seulement si météo
HIIT_SEQ = [
    # base : intervalles courts, on apprend à aller vite sans casser
    "HIIT piste : 2 × 8 × 30/30 à VMA (3:30/km), 3' entre séries",
    "HIIT piste : 2 × 10 × 30/30 à VMA, 3' entre séries",
    "HIIT piste : 3 × 8 × 30/30 à VMA, 3' entre séries",
    # base 2 : reprise puis on allonge
    "HIIT piste : 2 × 10 × 30/30 à VMA (reprise après le Japon)",
    "HIIT côte : 10 × 45\" en côte 6-8 %, récup descente trottinée",
    "HIIT piste : 6 × 2' à 3:35/km, récup 2' trot",
    # construction : intervalles longs, VO2max
    "HIIT côte : 6 × 2' en côte 8-10 % (FC > 170), récup descente",
    "HIIT piste : 5 × 3' à 3:40/km, récup 2'30 trot",
    "HIIT côte : 5 × 3' en côte 6-8 %, récup descente",
    "HIIT piste : 4 × 4' (FC 170-177), récup 3' trot",
    "HIIT côte : 5 × 3'30 en côte 6-8 %, récup descente",
    "HIIT piste : 5 × 4' (FC 170-177), récup 3' trot",
    "HIIT côte : 4 × 5' en côte 6-8 %, récup descente",
    # montagne : entretien, en côte longue
    "HIIT côte : 5 × 3' en côte raide avec bâtons, récup descente",
    "HIIT côte : 4 × 4' en côte avec bâtons, récup descente",
]
def hiit_weeks():
    out = []
    for i, w in enumerate(weeks):
        if w['phase'] not in ('BASE', 'BASE2', 'CONS', 'MONT') or i == 0: continue
        if 'allégée' in (w['note'] or ''): continue
        if w['phase'] == 'MONT' and i % 2: continue
        out.append(i)
    return out
_HW = None
def hiit_for(i, w):
    global _HW
    if _HW is None:
        _HW = hiit_weeks()
        mont = [j for j in _HW if weeks[j]['phase'] == 'MONT']
        _HW = {j: (HIIT_SEQ[13 + mont.index(j) % 2] if j in mont else HIIT_SEQ[min(n, 12)]) for n, j in enumerate([j for j in _HW if j not in mont])} | {j: HIIT_SEQ[13 + n % 2] for n, j in enumerate(mont)}
    t = _HW.get(i)
    return (t + " · Zwift si météo", 50) if t else None

def place(i, w):
    d0 = START + dt.timedelta(days=7 * i)
    dates = [d0 + dt.timedelta(days=k) for k in range(7)]
    work = work_days(i)
    winter = d0.month in (11, 12, 1, 2, 3)
    days = [[] for _ in range(7)]; flt = []
    def add(d, t, k, m=None, key=False): days[d].append({'t': t, 'k': k, 'm': m, 'key': key})
    T = w['h'] * 60; used = 0
    keys = w['keys']; ph = w['phase']
    in_japan = [JAPON[0] <= x <= JAPON[1] for x in dates]
    if ph == 'JAPON':
        for k in keys: flt.append({'t': k, 'k': 'renfo' if 'Renfo' in k else 'z2'})
        flt.append({'t': 'Beaucoup de marche, onsen = récup', 'k': 'info'})
        return days, flt
    race_day = None
    for k in keys:
        if 'COURSE' in k:
            race_day = 5 if 'Forts' in k else 4
    renfo = [k for k in keys if 'Renfo' in k and 'stop' not in k and 'fin de semaine' not in k]
    sl = [k for k in keys if re.search(r'^(SL|B2B|WE choc|Dernière grosse SL|Bloc)', k) or 'SL de nuit' in k]
    qual = [k for k in keys if re.search(r'Côtes|Seuil|Openers|Descente|plaisir', k)]
    other = [k for k in keys if k not in renfo + sl + qual]
    # course et veille
    if race_day is not None:
        for k in other:
            if 'COURSE' in k: add(race_day, k, 'race', None, True)
            elif 'Veille' in k: add(race_day - 1, k, 'z2', 20, True); used += 20
        other = [k for k in other if 'COURSE' not in k and 'Veille' not in k]
    # sortie longue
    sat_free = not in_japan[5]
    for k in sl:
        if k.startswith('Bloc'):
            for d, n in ((5, 'J1'), (6, 'J2')): add(d, 'Bloc montagne ' + n + ' : 4-6 h', 'sl', 300, True); used += 300
            flt.append({'t': 'Bloc montagne J3 : un 3e jour de 4-6 h, à caler sur un jour libre ou des congés', 'k': 'sl'})
            continue
        if 'SL de nuit' in k:
            add(5, k, 'sl', 450, True); used += 450; continue
        j2 = mins(k, r'J2 :? ?')
        main = mins(k.split('J2')[0]) or 120
        d = 5 if sat_free else 1
        add(d, k.split(', J2')[0].replace('B2B : ', 'B2B J1 : ').replace('WE choc : ', 'WE choc J1 : '), 'sl', main, True); used += main
        if j2:
            add(6, 'B2B J2 : ' + k.split('J2')[1].strip(' :'), 'sl', j2, True); used += j2
    for k in [k for k in other if k.startswith('J2')]:
        add(6, k, 'sl', mins(k) or 120, True); used += mins(k) or 120
    other = [k for k in other if not k.startswith('J2')]
    hx = hiit_for(i, w)
    if hx:
        add(0, hx[0], 'hiit', hx[1], True); used += hx[1]
    # qualité : seuil sur la piste le lundi (mardi si HIIT), le reste le mardi
    for k in qual:
        m = qual_min(k)
        if 'Seuil' in k: add(1 if hx else 0, k + (' (route plate ou piste)' if hx else ' (piste)'), 'qual', m, True)
        elif 'plaisir' in k: add(1, k, 'qual', m, True)
        else: add(1, k + '', 'qual', m, True)
        used += m
    # renfo : force le mardi soir (jour dur), le second le jeudi
    rdays = [1, 3] if not in_japan[1] else [3, 1]
    for n, k in enumerate(renfo):
        d = rdays[n % 2]
        if 'Circuit' in k: d = 3
        add(d, k, 'renfo', None, True)
    # infos du plan
    for k in other:
        m = re.search(r'\((?:sam|mer|mar)\. (\d+)/(\d+)\)', k)
        if 'Retest' in k or 'off' in k or 'sommeil' in k or 'Introduire' in k or 'Aucune' in k or 'Marche' in k:
            flt.append({'t': k, 'k': 'info'})
        elif 'fin de semaine' in k:
            add(5, k, 'renfo')
        elif 'Renfo stop' in k:
            dd = [x for x in range(7) if m and dates[x].day == int(m.group(1))]
            add(dd[0] if dd else 2, k, 'info')
        elif 'Footings faciles' in k and ph == 'RECUP':
            for d in (1, 3, 5): add(d, "Footing facile 35'", 'z2', 35); used += 35
        elif 'Openers' in k:
            add(1, k, 'qual', 40, True); used += 40
        else:
            flt.append({'t': k, 'k': 'info'})
    # jours bloqués
    blocked = set()
    for x in range(7):
        if in_japan[x]: blocked.add(x)
    if ph == 'RETOUR': blocked.add(0)
    if race_day is not None:
        blocked |= {d for d in range(7) if d >= race_day - 1}
    # footings pour compléter les heures
    rest = T - used if ph != 'RECUP' else 0
    slots = []  # (jour, plafond, type, libellé)
    mon_cap = 60 if 0 in work else 90
    slots.append((0, mon_cap, 'piste', 'Piste Z2'))
    slots.append((1, 75, 'z2', 'Footing Z2 vallonné'))
    slots.append((3, 50, 'tapis', 'Tapis Z2 (incliné 5-10 % pour le D+)'))
    slots.append((4, 45 if 4 in work else 75, 'tapis' if (4 in work and winter) else 'z2', 'Tapis Z2' if (4 in work and winter) else 'Footing Z2'))
    slots.append((6, 75, 'z2', 'Footing Z2'))
    slots.append((2, 40, 'tapis', 'Tapis facile (matin)'))
    free = []
    for d, cap, k, lab in slots:
        if d in blocked: continue
        if any(it['k'] in ('sl', 'race') for it in days[d]): continue
        have = sum(it['m'] or 0 for it in days[d] if it['k'] != 'renfo')
        if d == 2 and rest < 200: continue  # mercredi : repos sauf grosse semaine
        free.append([d, max(0, cap - have), k, lab, 0])
    # remplir : répartition proportionnelle aux plafonds, minimum 30'
    while True:
        tot = sum(f[1] for f in free)
        if not free or rest < 25 or tot <= 0: break
        for f in free: f[4] = min(f[1], r5(rest * f[1] / tot))
        small = [f for f in free if f[4] < 30]
        if not small: break
        free.remove(min(small, key=lambda f: f[1]))
    rest -= sum(f[4] for f in free)
    for d, cap, k, lab, m in free:
        if m >= 25:
            m = r5(m)
            q = [it for it in days[d] if it['k'] == 'qual']
            if q: q[0]['m'] += m; q[0]['t'] += " + %d' Z2" % m
            else: days[d].append({'t': "%s %s" % (lab, fmt_m(m)), 'k': k, 'm': m, 'key': False})
    # double si nécessaire
    if rest >= 25 and not (1 in blocked):
        m = r5(min(45, rest)); days[1].append({'t': '2e sortie : tapis facile %s' % fmt_m(m), 'k': 'tapis', 'm': m, 'key': False}); rest -= m
    order = {'race': 0, 'qual': 1, 'hiit': 1, 'sl': 1, 'piste': 2, 'z2': 2, 'tapis': 3, 'renfo': 4, 'info': 5}
    for d in range(7):
        days[d].sort(key=lambda it: order.get(it['k'], 9))
        if in_japan[d] and not days[d]: days[d].append({'t': 'Japon', 'k': 'info', 'm': None, 'key': False})
    return days, flt

def fmt_m(m):
    h, mm = divmod(int(m), 60)
    return ("%dh%02d" % (h, mm) if mm else "%dh" % h) if h else "%d'" % mm

for i, w in enumerate(weeks):
    w['work'] = sorted(work_days(i))
    w['days'], w['float'] = place(i, w)
    w['planned'] = sum((it['m'] or 0) for d in w['days'] for it in d if it['k'] != 'renfo') / 60

data = {'phases': {k: {'name': v[0], 'desc': v[1]} for k, v in PH.items()}, 'weeks': weeks}

if __name__ == '__main__':
    import sys
    json.dump(data, open(sys.argv[1], 'w'), ensure_ascii=False)
    print(len(weeks), weeks[24]['start'], weeks[-1]['start'])
