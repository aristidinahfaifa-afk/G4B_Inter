from great_tables import GT, md, style, loc
from IPython.display import HTML, display


def charger_fontawesome():
    """Charge FontAwesome 4 dans le notebook (à appeler une fois en début de notebook)."""
    display(HTML(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">'
    ))


def beau_tableau(
    df,
    col_entiers=None,
    col_pourcentages=None,
    titre="Elections",
    sous_titre="Résultats du premier tour",
    date="10 avril 2022",
    note="",
    police="Times New Roman",
):
    """
    Affiche un beau tableau avec great_tables.

    Paramètres
    ----------
    df : pd.DataFrame
        Le dataframe à afficher (colonnes déjà nommées comme on veut les afficher).
    col_entiers : list, optional
        Noms des colonnes à formater en entiers avec séparateurs de milliers.
    col_pourcentages : list, optional
        Noms des colonnes à formater en pourcentages (2 décimales).
    titre : str
        Titre principal du tableau (en gras).
    sous_titre : str
        Texte du sous-titre avant la date.
    date : str
        Date affichée en italique avec icône calendrier.
    note : str
        Note de bas de tableau (ex: "Table 1. Description").
    police : str
        Police du tableau (défaut: Times New Roman).

    Exemple
    -------
    from utils import charger_fontawesome, beau_tableau
    charger_fontawesome()
    beau_tableau(
        votes_national,
        col_entiers=["Nombre votes (total)"],
        col_pourcentages=["Score (% votes exprimés)"],
        titre="Elections 🇫🇷",
        sous_titre="Résultats du premier tour",
        date="10 avril 2022",
        note="Table 1. Résultats du premier tour de l'élection présidentielle 2022"
    )
    """
    col_entiers = col_entiers or []
    col_pourcentages = col_pourcentages or []

    gt = (
        GT(df)
        .tab_header(
            title=md(f"**{titre}**"),
            subtitle=md(
                f'{sous_titre} (<i class="fa fa-calendar-o" aria-hidden="true"></i>'
                f' <em>{date}</em>)'
            ),
        )
    )

    if note:
        gt = gt.tab_source_note(md(f"**{note}**"))

    for col in col_entiers:
        gt = gt.fmt_number(columns=col, sep_mark=" ", dec_mark=",", decimals=0)

    for col in col_pourcentages:
        gt = gt.fmt_number(columns=col, decimals=2, sep_mark=" ", dec_mark=",")

    gt = (
        gt
        .tab_style(
            style=style.fill(color="white"),
            locations=loc.body()
        )
        .tab_options(
            row_striping_include_table_body=False,
            row_striping_include_stub=False,
            table_font_names=police,
            column_labels_background_color="white",
        )
    )

    return gt
