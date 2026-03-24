from great_tables import GT, md, style, loc
from IPython.display import HTML, display


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
        Header complet si TOUS les 3 fournis (avec icône 📅).
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
    
    # GESTION GRAS INTELLIGENTE
    if col_gras == "all":
        col_gras = list(df.columns)  # ← TOUTES les colonnes
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

    if note:
        gt = gt.tab_source_note(md(f"**{note}**"))

    df_cols = df.columns

    # POURCENTAGES
    for col in col_pourcentages:
        if col in df_cols:
            gt = gt.fmt_number(
                columns=col, 
                decimals=2, 
                scale_by=0.01, 
                pattern="{x}%",
                sep_mark=" ", 
                dec_mark=","
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
