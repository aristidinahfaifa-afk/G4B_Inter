from great_tables import GT, md, style, loc
from IPython.display import HTML, display
import pandas as pd
import matplotlib.pyplot as plt


def beau_tableau(
    df,
    col_entiers=None,
    col_pourcentages=None,
    col_gras=None,
    titre=None,
    sous_titre=None,
    date=None,
    note=None,
    police="Times New Roman",
    charger_icons=True,
):
    """
    Affiche un beau tableau avec great_tables (🇫🇷 élections compatible).

    Paramètres
    ----------
    df : pd.DataFrame
        Le dataframe à afficher (colonnes déjà nommées).
    col_entiers : list, optional
        Colonnes à formater en entiers (1 234).
    col_pourcentages : list, optional  
        Colonnes à formater en % (27,85%).
    col_gras : list or str, optional
        Colonnes à mettre en gras :
        - `["col1", "col2"]` → colonnes spécifiques
        - `"all"` → TOUTES les colonnes en gras
        - `None` → pas de gras
    titre/sous_titre/date : str, optional
        Header complet si TOUS les 3 fournis (avec icône calendrier comme dans l'exmple du rendu).
    note : str, optional
        Note en bas (en gras).
    police : str
        Police du tableau.
    charger_icons : bool
        Charge FontAwesome automatiquement.

    Exemple
    -------
    # Preview simple
    beau_tableau(df.head())
    
    # Tableau élections (Table 1 du sujet)
    beau_tableau(
        votes_national,
        col_entiers=["Nombre votes (total)"],
        col_pourcentages=["Score (% votes exprimés)"],
        col_gras=["Candidat"],  # ou "all" pour tout gras
        titre="Elections 🇫🇷",
        sous_titre="Résultats du premier tour",
        date="10 avril 2022",
        note="Table 1. Résultats du premier tour"
    )
    
    # Table 2/3 du sujet (sans header)
    beau_tableau(score_departements.head(10), col_gras="all")
    """
    
    col_entiers = col_entiers or []
    col_pourcentages = col_pourcentages or []
    
    # GESTION GRAS 
    if col_gras == "all":
        col_gras = list(df.columns)  #  TOUTES les colonnes
    else:
        col_gras = col_gras or []

    if charger_icons:
        try:
            display(HTML(
                '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
            ))
        except:
            pass

    gt = GT(df)

    if titre and sous_titre and date:
        gt = gt.tab_header(
            title=md(f"**{titre}**"),
            subtitle=md(
                f'{sous_titre} (<i class="fa fa-calendar-o" aria-hidden="true"></i>'
                f' <em>{date}</em>)'
            )
        )
    if titre and sous_titre and date==None:
        gt = gt.tab_header(
            title=md(f"**{titre}**"),
            subtitle=md(
                f'{sous_titre} '
                
            )
        )
    if note:
        gt = gt.tab_source_note(md(f"**{note}**"))

    df_cols = df.columns

    # POURCENTAGES
    for col in col_pourcentages:
        if col in df_cols:
            gt = gt.fmt_number(
                columns=col, 
                decimals=2, 
                scale_by=1, 
                pattern="{x}%",
                sep_mark=" ", 
                dec_mark="."
            )

    # ENTIERS
    for col in col_entiers:
        if col in df_cols:
            gt = gt.fmt_number(
                columns=col, 
                decimals=0,
                sep_mark=" ", 
                dec_mark=","
            )

    # GRAS
    for col in col_gras:
        if col in df_cols:
            gt = gt.tab_style(
                style=style.text(weight="bold"),
                locations=loc.column_labels(col)
            )

    gt = (
        gt
        .tab_style(style=style.fill(color="white"), locations=loc.body())
        .tab_options(
            row_striping_include_table_body=False,
            row_striping_include_stub=False,
            table_font_names=police,
            column_labels_background_color="white",
        )
    )

    return gt


def load_data(path):
    """
    Charge un fichier CSV contenant des données électorales et
    prépare les variables pour une utilisation ultérieure.

    Parameters
    ----------
    path : str
        Chemin vers le fichier CSV à charger.

    Returns
    -------
    pandas.DataFrame
        DataFrame contenant les données importées avec la colonne
        'code_departement' convertie en chaîne de caractères.

    Raises
    ------
    FileNotFoundError
        Si le fichier spécifié n'existe pas.

    KeyError
        Si la colonne 'code_departement' est absente du fichier.

   
    Examples
    --------
    >>> df = load_data("data/score_departements_test.csv")
    >>> df.dtypes
    """
    
    df = pd.read_csv(path)
    df["code_departement"] = df["code_departement"].astype(str)
    return df



def filtrer_candidat(df, nom_candidat):
    """
    Filtre un DataFrame pour ne conserver que les observations
    correspondant à un candidat donné.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame contenant les résultats électoraux par département.
        Doit contenir au minimum une colonne 'candidat'.

    nom_candidat : str
        Nom du candidat à sélectionner (ex: "Marine LE PEN").

    Returns
    -------
    pandas.DataFrame
        Nouveau DataFrame contenant uniquement les lignes associées
        au candidat spécifié.

    Raises
    ------
    ValueError
        Si aucun enregistrement ne correspond au candidat fourni.

    Examples
    --------
    >>> df_filtre = filtrer_candidat(df, "Marine LE PEN")
    >>> df_filtre.head()
    """
    
    df_filtre = df[df["Candidat"] == nom_candidat].copy()
    
    if df_filtre.empty:
        raise ValueError(f"Aucune donnée pour le candidat : {nom_candidat}")
    
    return df_filtre


def merge_carte(df_scores, df_geo, left_id="INSEE_DEP", right_id="code_departement"):
    """
    Effectue la jointure entre les scores électoraux
    et le fond de carte des départements.

    Parameters
    ----------
    df_scores : pandas.DataFrame
        Données électorales filtrées (un candidat).

    df_geo : geopandas.GeoDataFrame
        Fond de carte des départements.

    Returns
    -------
    geopandas.GeoDataFrame
        Données fusionnées prêtes à être visualisées.
    """

    df_scores["code_departement"] = df_scores["code_departement"].astype(str)

    carte = df_geo.merge(
        df_scores,
        left_on=left_id,   
        right_on=right_id,
        how="left"
    )

    return carte



def plot_carte(df_geo, colonne, titre,epais_lim= 0.8, long_legend= 25):
    """
    Affiche une carte choroplèthe à partir d'un GeoDataFrame.

    Parameters
    ----------
    df_geo : geopandas.GeoDataFrame
        Données géographiques contenant la variable à représenter.

    colonne : str
        Nom de la colonne à afficher sur la carte.

    titre : str
        Titre de la carte.

    Returns
    -------
    None
        Affiche directement la carte.
    """
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    df_geo.plot(
        column=colonne,
        cmap="RdBu_r",
        legend=True,
        linewidth=epais_lim,           
        edgecolor="black",
        missing_kwds={
            "color": "lightgrey",
            "label": "Pas de données"
        },
        legend_kwds={
            "shrink": 0.6,       # taille de la barre 
            "aspect": long_legend,        # finesse de la barre de légende
            "label": "Score (%) par rapport à la moyenne nationale" # titre de la légende
        },
        ax=ax
    )

    

    ax.set_title(titre, fontsize=14, y=-0.05)  
    ax.axis("off")

    plt.show()


def carte_par_candidat(df, df_geo, nom_candidat, indicateur="Score (% votes exprimés)",epais_lim=0.8,long_legend= 25):
    """
    Génère la carte des scores départementaux
    pour un candidat donné.

    Parameters
    ----------
    df : pandas.DataFrame
        Base complète des résultats électoraux.

    df_geo : geopandas.GeoDataFrame
        Fond de carte des départements.

    nom_candidat : str
        Nom du candidat à analyser.

    Returns
    -------
    None
        Affiche la carte correspondante.
    """

   
    df_filtre = filtrer_candidat(df, nom_candidat)

    carte = merge_carte(df_filtre, df_geo)

    titre = f"Score départemental - {nom_candidat}"

    plot_carte(carte, indicateur, titre,epais_lim, long_legend)


def cartes_plusieurs_candidats(df, df_geo, liste_candidats, indicateur="Score (% votes exprimés)", epais_lim = 0.8, long_legend= 25):
    """
    Génère les cartes pour plusieurs candidats.

    Parameters
    ----------
    df : pandas.DataFrame
        Base complète des résultats électoraux.

    df_geo : geopandas.GeoDataFrame
        Fond de carte des départements.

    liste_candidats : list of str
        Liste des candidats à afficher.

    Returns
    -------
    None
        Affiche les cartes une par une.
    """

    for candidat in liste_candidats:
        carte_par_candidat(
            df=df,
            df_geo=df_geo,
            nom_candidat=candidat,
            indicateur=indicateur,
            epais_lim=epais_lim,
            long_legend=long_legend
        )



def diagnostic_qualite(df, colonnes_cle=None):

    # =========================
    # 1. Valeurs manquantes
    # =========================
    manquant = df.isna().sum()
    manquant_pct = (manquant / len(df) * 100).round(2)

    table_manquant = (
        pd.DataFrame({
            "Variable": manquant.index,
            "Nombre de valeurs manquantes": manquant.values,
            "Part (%)": manquant_pct.values
        })
        .query("`Nombre de valeurs manquantes` > 0")
        .sort_values("Part (%)", ascending=False)
    )

    if len(table_manquant) > 0:
        display(beau_tableau(
            table_manquant,
            col_entiers=["Nombre de valeurs manquantes"],
            col_pourcentages=["Part (%)"],
            titre="Variables avec les valeurs manquantes",
            sous_titre="Qualité des données"
        ))

    # =========================
    # 2. Doublons
    # =========================
    n_doublons = df.duplicated().sum()

    n_doublons_key = (
        df.duplicated(subset=colonnes_cle).sum()
        if colonnes_cle else 0
    )

    doublons = pd.DataFrame({
        "Type de doublon": ["Doublons exacts"],
        "Nombre": [n_doublons]
    })

    display(beau_tableau(
        doublons,
        col_entiers=["Nombre"],
        col_gras="all",
        titre="Doublons",
        sous_titre="Vérification"
    ))

    # =========================
    # 3. Variable voix
    # =========================
    stats_voix = df["voix"].describe().to_frame().reset_index()
    stats_voix.columns = ["Indicateur", "Valeur"]

    display(beau_tableau(
        stats_voix,
        col_entiers=["Valeur"],
        titre="Distribution des votes",
        sous_titre="Statistiques descriptives"
    ))


    # =========================
    # 4. Zéro votes global
    # =========================
    votes_par_personne = (
        df.groupby(["nom", "prenom"], dropna=False)["voix"]
        .sum()
        .reset_index()
    )

    zero_votes = votes_par_personne[votes_par_personne["voix"] == 0]

    resume_zero = pd.DataFrame({
        "Indicateur": ["Candidats sans aucun vote"],
        "Nombre": [len(zero_votes)]
    })

    display(beau_tableau(
        resume_zero,
        col_entiers=["Nombre"],
        col_gras="all",
        titre="Candidats sans aucun vote sur le territoire",
 
    ))

    if len(zero_votes) > 0:
        display(beau_tableau(
            zero_votes,
            titre="Liste des candidats ayant 0 votes sur tout le territoire"
        ))