import streamlit as st
import pandas as pd

# ── Configuration ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Élections 2022 · G4B",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');

:root {
    --noir:   #0d0d0d;
    --or:     #c9a84c;
    --or2:    #f0d080;
    --clair:  #faf8f4;
    --gris:   #4a4a4a;
    --gris2:  #9a9a9a;
    --blanc:  #ffffff;
    --card:   #161616;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--noir);
    color: #e8e4dc;
}

[data-testid="stSidebar"] {
    background: #0a0a0a !important;
    border-right: 1px solid #2a2a2a;
}
[data-testid="stSidebar"] * { color: #e8e4dc !important; }
[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    letter-spacing: 0.03em;
    padding: 5px 0;
}
[data-testid="stSidebar"] hr { border-color: #2a2a2a; }

h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif;
    color: var(--or) !important;
    letter-spacing: 0.02em;
}

.hero {
    background: linear-gradient(135deg, #111 0%, #1a1a1a 100%);
    border: 1px solid #2a2a2a;
    border-left: 4px solid var(--or);
    border-radius: 12px;
    padding: 40px 48px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: "⚜";
    position: absolute;
    right: 48px; top: 24px;
    font-size: 5rem;
    color: var(--or);
    opacity: 0.08;
}
.hero h1 { font-size: 2.6rem; margin: 0 0 8px 0; line-height: 1.1; }
.hero p { color: var(--gris2); font-size: 0.95rem; margin: 0; }
.hero .badge {
    display: inline-block;
    background: transparent;
    border: 1px solid var(--or);
    color: var(--or);
    font-size: 0.7rem;
    padding: 3px 12px;
    border-radius: 20px;
    margin-bottom: 16px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.card {
    background: #111;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    padding: 24px;
    margin-bottom: 16px;
}
.card-gold { border-left: 3px solid var(--or); }

.metric {
    background: #111;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    padding: 20px 24px;
    text-align: center;
}
.metric .val {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--or);
    line-height: 1;
}
.metric .lbl {
    font-size: 0.72rem;
    color: var(--gris2);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 6px;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, var(--or), transparent);
    margin: 20px 0;
    opacity: 0.5;
}

.q-badge {
    display: inline-block;
    background: var(--or);
    color: #000;
    font-weight: 700;
    font-size: 0.72rem;
    padding: 2px 10px;
    border-radius: 4px;
    margin-bottom: 8px;
    letter-spacing: 0.06em;
}

.team-card {
    background: #111;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 28px 20px;
    text-align: center;
}
.team-card .nom {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--or);
    margin: 14px 0 4px 0;
}
.team-card .role { font-size: 0.78rem; color: var(--gris2); margin-bottom: 14px; }
.team-card .links a { color: var(--gris2) !important; margin: 0 6px; font-size: 1rem; text-decoration: none; }
.avatar-circle {
    width: 80px; height: 80px;
    border-radius: 50%;
    background: #1a1a1a;
    border: 2px solid var(--or);
    margin: 0 auto;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    color: var(--or);
    overflow: hidden;
}
.avatar-circle img { width: 100%; height: 100%; object-fit: cover; }

div[data-testid="stMarkdownContainer"] p { color: #c8c4bc; }
</style>
""", unsafe_allow_html=True)


# ── Données ───────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(
        'https://www.data.gouv.fr/fr/datasets/r/182268fc-2103-4bcb-a850-6cf90b02a9eb'
    )
    df['code_departement'] = df['code_departement'].replace('fr_etranger', '99')
    df['code_commune'] = (
        df['code_departement'].astype(str).str[:2]
        + df['code_commune'].astype(str).str.zfill(3)
    )
    df['candidat'] = df['prenom'].astype(str) + ' ' + df['nom'].astype(str)
    return df


@st.cache_data
def compute_scores(df):
    df_exp = df[df['prenom'].notna()]
    votes_nat = df_exp.groupby('candidat')['voix'].sum().reset_index(name='votes_national')
    total_nat = votes_nat['votes_national'].sum()
    votes_nat['score_national'] = votes_nat['votes_national'] / total_nat * 100

    votes_dept = df_exp.groupby(['code_departement', 'candidat'])['voix'].sum().reset_index(name='votes_departement')
    total_dept = votes_dept.groupby('code_departement')['votes_departement'].sum().reset_index(name='total_dept')
    votes_dept = votes_dept.merge(total_dept, on='code_departement')
    votes_dept['score_departement'] = votes_dept['votes_departement'] / votes_dept['total_dept'] * 100

    score_dep = votes_dept.merge(votes_nat, on='candidat')
    score_dep['surrepresentation'] = (
        (score_dep['score_departement'] - score_dep['score_national'])
        / score_dep['score_national'] * 100
    ).round(2)
    return votes_nat, score_dep


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:12px 0 20px 0;'>
        <div style='font-family:Cormorant Garamond,serif;font-size:1.4rem;font-weight:700;color:#c9a84c;'>
            🗳️ Élections 2022
        </div>
        <div style='font-size:0.75rem;color:#666;margin-top:4px;'>Analyse territoriale · G4B</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio("", [
        "🏠  Accueil",
        "📋  Consignes",
        "🔍  Présentation des données",
        "📈  Partie 1 — Explorations",
        "📊  Partie 2 — Comparaisons",
        "🗺️  Partie 3 — Cartographie",
        "👥  Équipe",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.7rem;color:#444;line-height:1.8;'>
        Source : data.gouv.fr<br>
        Cours : Python data science<br>
        Deadline : 31 mars 2026
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# ACCUEIL
# ════════════════════════════════════════════════════════════════════════════════
if page == "🏠  Accueil":
    st.markdown("""
    <div class='hero'>
        <div class='badge'>Évaluation intermédiaire · 2026</div>
        <h1>Exploitation de données électorales avec Python</h1>
        <p>Analyse territoriale des résultats du 1er tour de l'élection présidentielle 2022</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl in zip([c1,c2,c3,c4],
        ["12", "10 avril 2022", "~35 000", "101"],
        ["Candidats", "Date du scrutin", "Communes", "Départements"]):
        col.markdown(f"<div class='metric'><div class='val'>{val}</div><div class='lbl'>{lbl}</div></div>",
                     unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='card card-gold'>
        <b style='color:#c9a84c;font-family:Cormorant Garamond,serif;font-size:1.1rem;'>À propos</b><br><br>
        Ce projet explore la richesse des données électorales fines à l'échelle communale.
        L'objectif est de visualiser les dynamiques territoriales de vote et les surreprésentations
        départementales pour chaque candidat.
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# CONSIGNES
# ════════════════════════════════════════════════════════════════════════════════
elif page == "📋  Consignes":
    st.markdown("# 📋 Consignes générales")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card card-gold'>
        <b style='color:#c9a84c;'>Livrable</b> : Dépôt Github avec un notebook Jupyter reproductible.<br>
        <b style='color:#c9a84c;'>Date limite</b> : 31 mars 2026 — envoyer par mail à votre chargé de TD.<br>
        <b style='color:#c9a84c;'>Critères</b> : lisibilité, reproductibilité (Run All), qualité des outputs.
    </div>
    """, unsafe_allow_html=True)

    parties = [
        ("📈 Partie 1 — Explorations générales", "📈  Partie 1 — Explorations", [
            ("Q1", "Créer/mettre à jour `code_commune` et `candidat`"),
            ("Q2", "Compter les candidats (hors votes non exprimés)"),
            ("Q3", "Scores nationaux — tableau mis en forme"),
        ]),
        ("📊 Partie 2 — Comparaisons départementales", "📊  Partie 2 — Comparaisons", [
            ("Q4", "Scores par département"),
            ("Q5", "Comparaison score départemental vs national"),
            ("Q6", "Variable `surrepresentation`"),
            ("Q7", "Graphique des surreprésentations par candidat"),
        ]),
        ("🗺️ Partie 3 — Cartographie", "🗺️  Partie 3 — Cartographie", [
            ("Q8", "Carte choroplèthe de la surreprésentation par candidat"),
        ]),
    ]

    for titre_partie, _, questions in parties:
        st.markdown(f"### {titre_partie}")
        for q, desc in questions:
            st.markdown(f"""
            <div class='card' style='margin-bottom:8px;padding:14px 20px;'>
                <span class='q-badge'>{q}</span>
                <span style='margin-left:10px;color:#c8c4bc;'>{desc}</span>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# PRÉSENTATION DES DONNÉES
# ════════════════════════════════════════════════════════════════════════════════
elif page == "🔍  Présentation des données":
    st.markdown("# 🔍 Présentation des données")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    with st.spinner("Chargement..."):
        df = load_data()

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='metric'><div class='val'>{df.shape[0]:,}</div><div class='lbl'>Lignes</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric'><div class='val'>{df.shape[1]}</div><div class='lbl'>Colonnes</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric'><div class='val'>{df['code_departement'].nunique()}</div><div class='lbl'>Départements</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### Aperçu des données")
    n = st.slider("Nombre de lignes", 5, 50, 10)
    st.dataframe(df.head(n), use_container_width=True, hide_index=True)

    st.markdown("### Description des colonnes")
    col_info = pd.DataFrame({
        "Colonne": df.columns,
        "Type": df.dtypes.values.astype(str),
        "Valeurs manquantes": df.isna().sum().values,
        "Exemple": [str(df[c].dropna().iloc[0]) if df[c].notna().any() else "—" for c in df.columns]
    })
    st.dataframe(col_info, use_container_width=True, hide_index=True)

    st.markdown("### Départements présents dans le jeu de données")
    st.write(sorted(df['code_departement'].unique().tolist()))


# ════════════════════════════════════════════════════════════════════════════════
# PARTIE 1
# ════════════════════════════════════════════════════════════════════════════════
elif page == "📈  Partie 1 — Explorations":
    st.markdown("# 📈 Partie 1 — Explorations générales")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    with st.spinner("Chargement..."):
        df = load_data()

    # Q1
    st.markdown("<div class='q-badge'>Q1</div>", unsafe_allow_html=True)
    st.markdown("### Création des variables `code_commune` et `candidat`")
    st.markdown("""
    <div class='card'>
        <b style='color:#c9a84c;'>code_commune</b> : 2 premiers caractères du département
        + code commune zero-paddé sur 3 chiffres.<br>
        <b style='color:#c9a84c;'>candidat</b> : prénom + espace + nom.
        Les votes non exprimés sont conservés (prenom = NaN).
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(
        df[['code_departement', 'code_commune', 'libelle_commune', 'candidat', 'voix']].head(10),
        use_container_width=True, hide_index=True
    )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Q2
    st.markdown("<div class='q-badge'>Q2</div>", unsafe_allow_html=True)
    st.markdown("### Nombre de candidats")
    candidats_n = df[df['prenom'].notna()]['candidat'].nunique()
    st.markdown(f"""
    <div class='card card-gold' style='font-family:Cormorant Garamond,serif;font-size:1.4rem;'>
        En 2022, il y avait
        <span style='color:#c9a84c;font-weight:700;'>{candidats_n}</span>
        candidats à l'élection présidentielle.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Q3
    st.markdown("<div class='q-badge'>Q3</div>", unsafe_allow_html=True)
    st.markdown("### Scores nationaux")
    votes_nat, _ = compute_scores(df)
    votes_nat_display = votes_nat.sort_values('votes_national', ascending=False).copy()
    votes_nat_display['score_national'] = votes_nat_display['score_national'].round(2)
    votes_nat_display.columns = ['Candidat', 'Nombre de votes', 'Score (%)']
    st.dataframe(votes_nat_display, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════════════
# PARTIE 2
# ════════════════════════════════════════════════════════════════════════════════
elif page == "📊  Partie 2 — Comparaisons":
    st.markdown("# 📊 Partie 2 — Comparaisons départementales")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    with st.spinner("Chargement..."):
        df = load_data()
    votes_nat, score_dep = compute_scores(df)

    # Q4
    st.markdown("<div class='q-badge'>Q4</div>", unsafe_allow_html=True)
    st.markdown("### Scores par département")
    dept_list = sorted(score_dep['code_departement'].unique())
    dept_sel = st.selectbox("Département", dept_list,
                            index=dept_list.index('11') if '11' in dept_list else 0,
                            key="dept_q4")
    df4 = score_dep[score_dep['code_departement'] == dept_sel][
        ['candidat', 'votes_departement', 'score_departement']
    ].sort_values('votes_departement', ascending=False).reset_index(drop=True)
    df4['score_departement'] = df4['score_departement'].round(2)
    df4.columns = ['Candidat', 'Votes', 'Score (%)']
    st.dataframe(df4, use_container_width=True, hide_index=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Q5
    st.markdown("<div class='q-badge'>Q5</div>", unsafe_allow_html=True)
    st.markdown("### Comparaison département / national")
    df5 = score_dep[score_dep['code_departement'] == dept_sel][
        ['candidat', 'votes_departement', 'score_departement', 'votes_national', 'score_national']
    ].sort_values('votes_departement', ascending=False).reset_index(drop=True)
    df5['score_departement'] = df5['score_departement'].round(2)
    df5['score_national'] = df5['score_national'].round(2)
    df5.columns = ['Candidat', 'Votes dépt', 'Score dépt (%)', 'Votes national', 'Score national (%)']
    st.dataframe(df5, use_container_width=True, hide_index=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Q6
    st.markdown("<div class='q-badge'>Q6</div>", unsafe_allow_html=True)
    st.markdown("### Variable surreprésentation")
    st.markdown("""
    <div class='card'>
        <b style='color:#c9a84c;'>Formule</b> :
        surreprésentation = (score_département − score_national) / score_national × 100<br>
        <i style='color:#9a9a9a;'>Exemple : score dépt = 30%, score national = 15% → surreprésentation = 100%</i>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Q7
    st.markdown("<div class='q-badge'>Q7</div>", unsafe_allow_html=True)
    st.markdown("### Graphique de surreprésentation par candidat")

    candidats_list = sorted(score_dep['candidat'].unique())
    cand_sel = st.selectbox("Candidat", candidats_list, key="cand_q7")
    n_top = st.slider("Nombre de départements", 5, 20, 10)

    df7 = score_dep[score_dep['candidat'] == cand_sel].copy()
    df7 = df7.reindex(df7['surrepresentation'].abs().sort_values(ascending=False).index).head(n_top)

    import matplotlib.pyplot as plt
    import matplotlib as mpl
    mpl.rcParams.update({'text.color': '#e8e4dc', 'axes.labelcolor': '#9a9a9a',
                         'xtick.color': '#9a9a9a', 'ytick.color': '#e8e4dc'})

    fig, ax = plt.subplots(figsize=(9, max(4, n_top * 0.45)))
    fig.patch.set_facecolor('#111')
    ax.set_facecolor('#111')
    colors = ['#c9a84c' if v >= 0 else '#555555' for v in df7['surrepresentation']]
    ax.barh(df7['code_departement'], df7['surrepresentation'], color=colors, height=0.6)
    ax.axvline(0, color='#444', linewidth=1)
    ax.set_xlabel("Surreprésentation (%)")
    ax.set_title(f"Top {n_top} surreprésentations — {cand_sel}",
                 color='#c9a84c', fontsize=13, pad=14,
                 fontfamily='serif')
    ax.spines[:].set_color('#2a2a2a')
    ax.grid(axis='x', color='#2a2a2a', linewidth=0.5)
    st.pyplot(fig)


# ════════════════════════════════════════════════════════════════════════════════
# PARTIE 3
# ════════════════════════════════════════════════════════════════════════════════
elif page == "🗺️  Partie 3 — Cartographie":
    st.markdown("# 🗺️ Partie 3 — Cartographie")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='q-badge'>Q8</div>", unsafe_allow_html=True)
    st.markdown("### Carte choroplèthe de la surreprésentation")
    st.info("⏳ Cette section sera complétée après l'intégration de cartiflette et geopandas.")
    st.markdown("""
    <div class='card'>
        Le code reposera sur :<br>
        • <b style='color:#c9a84c;'>cartiflette</b> — fond de carte des départements<br>
        • <b style='color:#c9a84c;'>geopandas</b> — jointure spatiale et cartographie<br>
        • Un sélecteur de candidat pour afficher la carte correspondante
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# ÉQUIPE
# ════════════════════════════════════════════════════════════════════════════════
elif page == "👥  Équipe":
    st.markdown("# 👥 L'équipe")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    if 'photos' not in st.session_state:
        st.session_state.photos = [None, None, None]

    membres = [
        {"nom": "Membre 1", "role": "Questions 1–3",
         "github": "#", "linkedin": "#", "email": "membre1@example.com"},
        {"nom": "Membre 2", "role": "Questions 4–6",
         "github": "#", "linkedin": "#", "email": "membre2@example.com"},
        {"nom": "Membre 3", "role": "Questions 7–8",
         "github": "#", "linkedin": "#", "email": "membre3@example.com"},
    ]

    cols = st.columns(3)
    for i, (col, m) in enumerate(zip(cols, membres)):
        with col:
            import base64
            initiales = "".join([p[0].upper() for p in m['nom'].split()])
            if st.session_state.photos[i] is not None:
                b64 = base64.b64encode(st.session_state.photos[i]).decode()
                avatar = f"<div class='avatar-circle'><img src='data:image/jpeg;base64,{b64}'/></div>"
            else:
                avatar = f"<div class='avatar-circle'>{initiales}</div>"

            st.markdown(f"""
            <div class='team-card'>
                {avatar}
                <div class='nom'>{m['nom']}</div>
                <div class='role'>{m['role']}</div>
                <div class='links'>
                    <a href='{m['github']}' title='GitHub'><i class='fa fa-github'></i></a>
                    <a href='{m['linkedin']}' title='LinkedIn'><i class='fa fa-linkedin'></i></a>
                    <a href='mailto:{m['email']}' title='Email'><i class='fa fa-envelope'></i></a>
                </div>
            </div>
            """, unsafe_allow_html=True)

            uploaded = st.file_uploader(
                f"📷 Photo de {m['nom']}", type=["jpg", "jpeg", "png"], key=f"photo_{i}"
            )
            if uploaded:
                st.session_state.photos[i] = uploaded.read()
                st.rerun()

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### 📄 README")
    st.markdown("""
    <div class='card'>
        Projet réalisé dans le cadre de l'évaluation intermédiaire du cours
        <b style='color:#c9a84c;'>Python pour la data science</b> (2026),
        encadré par Lino Galiana (INSEE).<br><br>
        <b style='color:#c9a84c;'>Source</b> : Résultats officiels du 1er tour — data.gouv.fr<br>
        <b style='color:#c9a84c;'>Librairies</b> : pandas · geopandas · great_tables · cartiflette · matplotlib · streamlit
    </div>
    """, unsafe_allow_html=True)
