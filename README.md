#  Élections Présidentielles 2022 — Analyse avec Python


## Présentation

Ce dépôt contient l'ensemble du travail réalisé dans le cadre de l'évaluation intermédiaire du cours *Python pour la data science* en $2^{ème}$ année à l'ENSAI . L'objectif est d'explorer les données électorales du premier tour de l'élection présidentielle 2022 à l'aide de Python, en combinant analyse de données, visualisation et cartographie.

Les données sont issues de [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/r/182268fc-2103-4bcb-a850-6cf90b02a9eb) et contiennent les résultats commune par commune pour chaque candidat.

---

## Structure du dépôt

```
.
├── Notebook_final.ipynb   # Notebook principal (questions 1 à 8)
├── utils.py              # Fonctions réutilisables (tableaux, cartes, filtres)
├── app.py                # Application Streamlit interactive
├── requirements.txt      # Dépendances Python
├── ressources/
│   └── logo_ensai.png    # Logo ENSAI (utilisé dans l'app et pour la page de garde)
└── README.md
```

---

## Contenu du notebook

### Partie 1 — Explorations générales

- **Q1** — Construction du `code_commune` (code département + code commune) et création de la variable `candidat` (prénom + nom).
- **Q2** — Comptage du nombre de candidats au premier tour (hors votes blancs, nuls et abstentions).
- **Q3** — Calcul des scores nationaux de chaque candidat (votes et % des votes exprimés), mis en forme avec `great_tables`.

### Partie 2 — Comparaison des scores départements aux moyennes nationales

- **Q4** — Création d'un dataframe `score_departements` avec le nombre de votes et le score (%) pour chaque candidat et chaque département.
- **Q5** — Jointure avec les scores nationaux pour comparer les deux niveaux géographiques.
- **Q6** — Calcul d'une variable `surrepresentation` : écart relatif entre score départemental et score national (en %).
- **Q7** — Fonction de visualisation des principales surreprésentations (en valeur absolue) pour un candidat donné.

### Partie 3 — Un peu de cartographie

- **Q8** — Jointure des scores départementaux avec le fond de carte (via `cartiflette`) et production de cartes choroplèthes de la surreprésentation par candidat.

---

## Application Streamlit

Une application interactive a été développée à partir du notebook pour permettre d'explorer les résultats de manière dynamique.

### Lancer l'application

```bash
streamlit run app.py
```

### Pages disponibles

| Page | Contenu |
|------|---------|
|  Vue d'ensemble | KPIs, podium du premier tour, graphique général |
|  Partie 1 — Résultats nationaux | Tableau des scores, phrase Q2, visualisation en barres |
|  Partie 2 — Analyse territoriale | Surreprésentation par département, sélection du candidat et du nombre de départements |
|  Partie 3 — Cartographie | Carte choroplèthe par candidat, comparaison multi-candidats |

---

## Installation

### Prérequis

Python 3.10+ recommandé.

### Création de l'environnement

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# ou
.venv\Scripts\activate           # Windows
```

### Installation des dépendances

```bash
pip install -r requirements.txt
```

Les principales librairies utilisées sont `pandas`, `matplotlib`, `geopandas`, `great_tables`, `streamlit` et `cartiflette`.

---

## Reproductibilité

Le notebook est conçu pour s'exécuter de bout en bout via **Run all** sans intervention manuelle. Les données sont téléchargées automatiquement depuis data.gouv.fr au lancement. Le fond de carte est récupéré via `cartiflette` à la première exécution puis mis en cache.

---

## Auteurs

Groupe 4B — 2ème année ENSAI · Mars 2026
    
    AÏFA Aristidina

    KENNE Lesline

    ROSE Valentin
