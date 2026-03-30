import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ─── CONFIGURATION ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Élections Présidentielles 2022",
    page_icon="O",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── PALETTE ENSAI ────────────────────────────────────────────────────────────
ENSAI_BLUE   = "#003F7F"
ENSAI_LIGHT  = "#E8F0FB"
ENSAI_MID    = "#A8C0E0"
ENSAI_ACCENT = "#0066CC"
TEXT_DARK    = "#0A1628"
TEXT_MID     = "#4A5568"
TEXT_LIGHT   = "#718096"
WHITE        = "#FFFFFF"
BORDER       = "#C9D9EE"

# ─── STYLES ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [data-testid="stApp"] {{
    background-color: {ENSAI_LIGHT};
    color: {TEXT_DARK};
    font-family: 'Inter', sans-serif;
}}
[data-testid="stSidebar"] {{
    background-color: {ENSAI_BLUE} !important;
}}
[data-testid="stSidebar"] * {{ color: {WHITE} !important; }}
[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.15); }}

.page-title {{
    font-family: 'Source Serif 4', serif;
    font-size: 2rem; font-weight: 700;
    color: {ENSAI_BLUE}; margin-bottom: 0.1rem;
}}
.page-sub {{
    font-size: 0.78rem; letter-spacing: 0.12em;
    text-transform: uppercase; color: {TEXT_LIGHT};
    margin-bottom: 1.5rem; padding-bottom: 0.8rem;
    border-bottom: 2px solid {ENSAI_BLUE};
}}
.kpi-card {{
    background: {WHITE}; border: 1px solid {BORDER};
    border-top: 3px solid {ENSAI_BLUE};
    border-radius: 6px; padding: 1.2rem 1.4rem; text-align: center;
}}
.kpi-label {{ font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; color: {TEXT_LIGHT}; }}
.kpi-value {{ font-family: 'Source Serif 4', serif; font-size: 2.2rem; font-weight: 700; color: {ENSAI_BLUE}; line-height: 1; }}
.kpi-sub {{ font-size: 0.78rem; color: {TEXT_LIGHT}; margin-top: 0.3rem; }}
.podium-card {{
    background: {WHITE}; border: 1px solid {BORDER};
    border-radius: 6px; padding: 1.4rem; text-align: center;
}}
.podium-card .medal {{ font-size: 2rem; margin-bottom: 0.5rem; }}
.podium-card .name {{ font-family: 'Source Serif 4', serif; font-size: 1rem; font-weight: 600; color: {TEXT_DARK}; margin-bottom: 0.6rem; min-height: 2.5rem; }}
.podium-card .score {{ font-size: 1.9rem; font-weight: 700; color: {ENSAI_BLUE}; font-family: 'Source Serif 4', serif; }}
.podium-card .voix {{ font-size: 0.8rem; color: {TEXT_LIGHT}; margin-top: 0.3rem; }}
.section-label {{
    font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase;
    color: {TEXT_LIGHT}; margin-top: 1.5rem; margin-bottom: 0.5rem;
    border-left: 3px solid {ENSAI_ACCENT}; padding-left: 0.6rem;
}}
hr.divider {{ border: none; border-top: 1px solid {BORDER}; margin: 1.5rem 0; }}
</style>
""", unsafe_allow_html=True)

# ─── COULEURS CANDIDATS ───────────────────────────────────────────────────────
COULEURS = {
    "Emmanuel MACRON":       "#FFDD00",
    "Marine LE PEN":         "#003189",
    "Jean-Luc MÉLENCHON":   "#CC2529",
    "Éric ZEMMOUR":          "#1E3A5F",
    "Valérie PÉCRESSE":      "#0066CC",
    "Yannick JADOT":         "#2E8B57",
    "Jean LASSALLE":         "#FF8C00",
    "Fabien ROUSSEL":        "#B22222",
    "Nicolas DUPONT-AIGNAN": "#4169E1",
    "Anne HIDALGO":          "#E91E8C",
    "Philippe POUTOU":       "#DC143C",
    "Nathalie ARTHAUD":      "#8B0000",
}

# ─── CHARGEMENT ───────────────────────────────────────────────────────────────
DATA_URL = "https://www.data.gouv.fr/fr/datasets/r/182268fc-2103-4bcb-a850-6cf90b02a9eb"

@st.cache_data(show_spinner=False)
def load_raw():
    df = pd.read_csv(DATA_URL)
    df = df.convert_dtypes()
    df["code_commune"]     = df["code_commune"].astype("string")
    df["code_departement"] = df["code_departement"].astype("string")
    df["code_departement"] = df["code_departement"].replace("fr_etranger", "99")
    df["code_commune"] = (
        df["code_departement"].str[:2]
        + df["code_commune"].str[-3:].str.zfill(3)
    )
    mask_wallis = df['code_departement'].astype(str) == '986'
    df.loc[mask_wallis, 'code_commune'] = (
        '986' + df.loc[mask_wallis, 'code_commune'].str[-1:].str.zfill(2)
    )
    df["candidat"] = (df["prenom"].fillna("") + " " + df["nom"].fillna("")).str.strip()
    return df

@st.cache_data(show_spinner=False)
def compute_national(df):
    df_exp = df[df["prenom"].notna()]
    v = df_exp.groupby("candidat")["voix"].sum().reset_index()
    v.columns = ["Candidat", "votes_national"]
    v["score_national"] = v["votes_national"] / v["votes_national"].sum() * 100
    return v.sort_values("votes_national", ascending=False).reset_index(drop=True)

@st.cache_data(show_spinner=False)
def compute_departements(df, vnat):
    df_exp = df[df["prenom"].notna()]
    vd = df_exp.groupby(["code_departement", "candidat"])["voix"].sum().reset_index()
    vd.columns = ["code_departement", "Candidat", "votes_departement"]
    tot = vd.groupby("code_departement")["votes_departement"].sum().reset_index()
    tot.columns = ["code_departement", "total_dep"]
    vd = vd.merge(tot, on="code_departement")
    vd["score_departement"] = vd["votes_departement"] / vd["total_dep"] * 100
    sd = vd.merge(vnat[["Candidat", "votes_national", "score_national"]], on="Candidat", how="left")
    sd["surrepresentation"] = (sd["score_departement"] - sd["score_national"]) / sd["score_national"] * 100
    return sd

@st.cache_data(show_spinner=False)
def load_geodata():
    try:
        from cartiflette import carti_download
        return carti_download(
            values=["France"], crs=4326, borders="DEPARTEMENT",
            vectorfile_format="geojson", simplification=50,
            filter_by="FRANCE_ENTIERE_DROM_RAPPROCHES",
            source="EXPRESS-COG-CARTO-TERRITOIRE", year=2022,
        )
    except Exception:
        return None

with st.spinner("Chargement des données…"):
    df_raw         = load_raw()
    votes_national = compute_national(df_raw)
    score_dep      = compute_departements(df_raw, votes_national)

nb_candidats = df_raw[df_raw["prenom"].notna()]["candidat"].nunique()
total_voix   = int(votes_national["votes_national"].sum())
nb_communes  = df_raw["code_commune"].nunique()

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def style_ax(ax, fig):
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.tick_params(colors=TEXT_MID, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(BORDER)
    ax.xaxis.grid(True, color=BORDER, linewidth=0.5, linestyle="--")
    ax.set_axisbelow(True)

def style_colorbar(fig, main_ax):
    """Style les axes colorbar sans utiliser labelcolor."""
    for child_ax in fig.axes:
        if child_ax is not main_ax:
            child_ax.tick_params(labelsize=8, color=TEXT_MID, labelcolor=TEXT_MID)
            child_ax.yaxis.label.set_color(TEXT_MID)
            child_ax.yaxis.label.set_fontsize(9)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    logo_path = Path(__file__).parent / "ressources/logo_ensai.png"
    if logo_path.exists():
        st.image(str(logo_path), width=140)
    st.markdown("<hr>", unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        [" Vue d'ensemble",
         " Résultats nationaux",
         " Analyse territoriale",
         " Cartographie"],
        label_visibility="collapsed",
    )
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:0.7rem; opacity:0.5; line-height:1.9;'>"
        "Source : data.gouv.fr<br>Cours Python · Lino Galiana · INSEE"
        "</div>",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — VUE D'ENSEMBLE
# ══════════════════════════════════════════════════════════════════════════════
if page == " Vue d'ensemble":
    st.markdown("<div class='page-title'>Élections Présidentielles 2022</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Premier tour · 10 avril 2022</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, label, val, sub in [
        (c1, "Candidats", str(nb_candidats), "Au premier tour"),
        (c2, "Votes exprimés", f"{total_voix/1e6:.1f} M", "Bulletins comptabilisés"),
        (c3, "Communes", f"{nb_communes:,}", "Bureaux de vote"),
    ]:
        with col:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-value'>{val}</div>
                <div class='kpi-sub'>{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Podium</div>", unsafe_allow_html=True)

    top3 = votes_national.head(3)
    cols = st.columns(3)
    for col, medal, (_, row) in zip(cols, ["🥇", "🥈", "🥉"], top3.iterrows()):
        with col:
            st.markdown(f"""
            <div class='podium-card'>
                <div class='medal'>{medal}</div>
                <div class='name'>{row['Candidat']}</div>
                <div class='score'>{row['score_national']:.1f} %</div>
                <div class='voix'>{int(row['votes_national']):,} voix</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Résultats complets</div>", unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(10, 4.5))
    style_ax(ax, fig)
    df_plot = votes_national.sort_values("votes_national")
    bars = ax.barh(df_plot["Candidat"],
                   df_plot["score_national"],
                   color=[COULEURS.get(c, ENSAI_ACCENT) for c in df_plot["Candidat"]],
                   height=0.6, alpha=0.92)
    for bar, val in zip(bars, df_plot["score_national"]):
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", ha="left", color=TEXT_MID, fontsize=8.5)
    ax.set_xlabel("% des votes exprimés", color=TEXT_LIGHT, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — RÉSULTATS NATIONAUX
# ══════════════════════════════════════════════════════════════════════════════
elif page == " Résultats nationaux":
    st.markdown("<div class='page-title'>Résultats Nationaux</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Scores agrégés — Premier tour</div>", unsafe_allow_html=True)

    st.info(f"En 2022, il y avait **{nb_candidats} candidats** à l'élection présidentielle.")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Tableau des résultats</div>", unsafe_allow_html=True)

    df_display = pd.DataFrame({
        "Rang":       range(1, len(votes_national) + 1),
        "Candidat":   votes_national["Candidat"],
        "Votes":      votes_national["votes_national"].apply(lambda x: f"{int(x):,}"),
        "Score (%)":  votes_national["score_national"].apply(lambda x: f"{x:.2f}%"),
    })
    st.dataframe(df_display, use_container_width=True, hide_index=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Scores en barres</div>", unsafe_allow_html=True)

    fig2, ax2 = plt.subplots(figsize=(10, 4.5))
    style_ax(ax2, fig2)
    df_plot2 = votes_national.sort_values("score_national")
    bars2 = ax2.barh(df_plot2["Candidat"],
                     df_plot2["score_national"],
                     color=[COULEURS.get(c, ENSAI_ACCENT) for c in df_plot2["Candidat"]],
                     height=0.6, alpha=0.92)
    for bar, val in zip(bars2, df_plot2["score_national"]):
        ax2.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                 f"{val:.1f}%", va="center", ha="left", color=TEXT_MID, fontsize=8.5)
    ax2.set_xlabel("% des votes exprimés", color=TEXT_LIGHT, fontsize=9)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.yaxis.grid(False)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — ANALYSE TERRITORIALE
# ══════════════════════════════════════════════════════════════════════════════
elif page == " Analyse territoriale":
    st.markdown("<div class='page-title'>Analyse Territoriale</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Surreprésentation par département (Q6 & Q7)</div>", unsafe_allow_html=True)

    col_ctrl1, col_ctrl2 = st.columns([2, 1])
    with col_ctrl1:
        candidat_choisi = st.selectbox("Candidat", options=sorted(score_dep["Candidat"].unique()))
    with col_ctrl2:
        nb_dep = st.slider("Nb départements", 5, 20, 10)

    df_c = score_dep[score_dep["Candidat"] == candidat_choisi].copy()
    df_c["abs_surrep"] = df_c["surrepresentation"].abs()
    df_top = df_c.nlargest(nb_dep, "abs_surrep").sort_values("surrepresentation")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-label'>Top {nb_dep} surreprésentations — {candidat_choisi}</div>",
                unsafe_allow_html=True)

    fig3, ax3 = plt.subplots(figsize=(10, max(4, nb_dep * 0.55)))
    style_ax(ax3, fig3)
    colors3 = [ENSAI_ACCENT if v >= 0 else ENSAI_MID for v in df_top["surrepresentation"]]
    ax3.barh(df_top["code_departement"], df_top["surrepresentation"],
             color=colors3, height=0.65, alpha=0.9)
    ax3.axvline(0, color=TEXT_MID, linewidth=0.9, linestyle="--")
    for i, (_, row) in enumerate(df_top.iterrows()):
        val = row["surrepresentation"]
        ax3.text(val + (0.5 if val >= 0 else -0.5), i,
                 f"{val:+.1f}%", va="center",
                 ha="left" if val >= 0 else "right",
                 color=TEXT_MID, fontsize=8)
    ax3.set_xlabel("Surreprésentation (%)", color=TEXT_LIGHT, fontsize=9)
    ax3.set_ylabel("Département", color=TEXT_LIGHT, fontsize=9)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close()

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Tableau complet</div>", unsafe_allow_html=True)

    df_table = score_dep[score_dep["Candidat"] == candidat_choisi].copy()
    df_table = df_table.sort_values("score_departement", ascending=False).reset_index(drop=True)
    st.dataframe(pd.DataFrame({
        "Département":        df_table["code_departement"],
        "Votes":              df_table["votes_departement"].apply(lambda x: f"{int(x):,}"),
        "Score départ. (%)":  df_table["score_departement"].apply(lambda x: f"{x:.2f}%"),
        "Score national (%)": df_table["score_national"].apply(lambda x: f"{x:.2f}%"),
        "Surreprés. (%)":     df_table["surrepresentation"].apply(lambda x: f"{x:+.1f}%"),
    }), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — CARTOGRAPHIE
# ══════════════════════════════════════════════════════════════════════════════
elif page == " Cartographie":
    st.markdown("<div class='page-title'>Carte Électorale</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Score départemental par candidat (Q8)</div>", unsafe_allow_html=True)

    with st.spinner("Chargement du fond de carte…"):
        gdf = load_geodata()

    if gdf is None:
        st.error("Installe `cartiflette` (`pip install cartiflette`) puis relance l'app.")
        st.stop()

    insee_col = next((c for c in gdf.columns if "dep" in c.lower() or "insee" in c.lower()), None)
    if insee_col is None:
        st.error("Colonne département introuvable dans le GeoDataFrame.")
        st.stop()

    col_ctrl1, col_ctrl2 = st.columns([2, 1])
    with col_ctrl1:
        candidat_carte = st.selectbox("Candidat", options=sorted(score_dep["Candidat"].unique()), key="carto")
    with col_ctrl2:
        indicateur = st.radio(
            "Indicateur",
            ["score_departement", "surrepresentation"],
            format_func=lambda x: "Score (%)" if x == "score_departement" else "Surreprésentation (%)",
        )

    df_filtre = score_dep[score_dep["Candidat"] == candidat_carte].copy()
    df_filtre["code_departement"] = df_filtre["code_departement"].astype(str)
    carte = gdf.merge(df_filtre, left_on=insee_col, right_on="code_departement", how="left")

    if indicateur == "surrepresentation":
        cmap = "RdBu_r"
        lim  = max(carte[indicateur].abs().quantile(0.95), 1)
        vmin, vmax = -lim, lim
        label_cb = "% vs. moyenne nationale"
    else:
        cmap = "Blues"
        vmin = carte[indicateur].quantile(0.05)
        vmax = carte[indicateur].quantile(0.95)
        label_cb = "Score départemental (%)"

    fig4, ax4 = plt.subplots(figsize=(12, 9))
    fig4.patch.set_facecolor(WHITE)
    ax4.set_facecolor(WHITE)

    carte.plot(
        column=indicateur,
        cmap=cmap, vmin=vmin, vmax=vmax,
        legend=True,
        linewidth=0.6, edgecolor=BORDER,
        missing_kwds={"color": "#EEEEEE", "label": "Pas de données"},
        legend_kwds={"shrink": 0.5, "aspect": 20, "label": label_cb},
        ax=ax4,
    )

    # ← Styler la colorbar APRÈS le plot, sans passer labelcolor à Colorbar.__init__
    for child_ax in fig4.axes:
        if child_ax is not ax4:
            child_ax.tick_params(labelsize=8, labelcolor=TEXT_MID)
            child_ax.yaxis.label.set_color(TEXT_MID)
            child_ax.yaxis.label.set_fontsize(9)

    ax4.set_title(f"{candidat_carte} — {label_cb}", fontsize=13,
                  color=ENSAI_BLUE, pad=15, fontfamily="serif")
    ax4.axis("off")
    plt.tight_layout()
    st.pyplot(fig4)
    plt.close()

    # Comparaison multi-candidats
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Comparaison multi-candidats</div>", unsafe_allow_html=True)

    candidats_multi = st.multiselect(
        "Sélectionner 2 à 4 candidats",
        options=sorted(score_dep["Candidat"].unique()),
        default=[], max_selections=4,
    )

    if candidats_multi:
        n     = len(candidats_multi)
        nrows = (n + 1) // 2
        fig5, axes = plt.subplots(nrows, 2, figsize=(14, 6 * nrows))
        fig5.patch.set_facecolor(WHITE)
        axes_flat = np.array(axes).flatten()

        for ax_i, cand in zip(axes_flat, candidats_multi):
            df_c2 = score_dep[score_dep["Candidat"] == cand].copy()
            df_c2["code_departement"] = df_c2["code_departement"].astype(str)
            carte2 = gdf.merge(df_c2, left_on=insee_col, right_on="code_departement", how="left")
            ax_i.set_facecolor(WHITE)
            lim2 = max(carte2["surrepresentation"].abs().quantile(0.95), 1)
            carte2.plot(
                column="surrepresentation", cmap="RdBu_r",
                vmin=-lim2, vmax=lim2, legend=False,
                linewidth=0.4, edgecolor=BORDER, ax=ax_i,
            )
            ax_i.set_title(cand, color=ENSAI_BLUE, fontsize=10, fontfamily="serif")
            ax_i.axis("off")

        for ax_extra in axes_flat[n:]:
            ax_extra.set_visible(False)

        plt.suptitle("Surreprésentation par candidat",
                     color=ENSAI_BLUE, fontsize=13, fontfamily="serif", y=1.01)
        plt.tight_layout()
        st.pyplot(fig5)
        plt.close()
