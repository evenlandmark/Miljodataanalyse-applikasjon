
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

def last_inn_data(filbane):
    """
    Leser inn værdata fra en CSV-fil og retuernerer en DataFrame.
    """
    return pd.read_csv(filbane)

def beregn_statistikk(df, variabelnavn, visningsnavn):
    """
    Beregn statistikk for en gitt variabel (gjennomsnitt, median, standardavvik)
    per by.
        
    Args:
    df (DataFrame): Pandas DataFrame med værdata.
    variabelnavn (str): Navnet på variabelen som skal analyseres (f.eks. "air_temperature P1D").
    visningsnavn (str): Navnet som skal vises i utskriften (f.eks. "lufttemperatur").
        
    Returns:
    None
    """
    data = df[df["variable"] == variabelnavn]
    
    if "by" in data.columns:
        gruppert = data.groupby("by")["value"].agg(
            gjennomsnitt="mean",
            median="median",
            standardavvik="std"
            )
        print(f"\nStatistiske værdata for {visningsnavn} per by:")
        print(gruppert.round(2))
        return gruppert
    else:
        print(f"Variabelen '{variabelnavn}' finnes ikke i datasettet.")
        return None

def plott_statistikk(statistikk_df, statistikk_type_list, variabelnavn):
    """
    Plotter valgt type statistikk (gjennomsnitt, median, standardavvik) for en variabel per by,
    og grupperer plottene horisontalt etter statistikk-type.
    
    Args:
    statistikk_df (DataFrame): DataFrame med statistikk per by (returnert fra beregn_statistikk).
    statistikk_type_list (list): Liste med statistikk-typer som skal vises, f.eks. ["gjennomsnitt", "standardavvik"].
    variabelnavn (str): Navn på værvariabelen (for tittel).
    """
    # Oppretter subplot med én rad og så mange kolonner som det er statistikk-typer
    fig, axes = plt.subplots(1, len(statistikk_type_list), figsize=(10 * len(statistikk_type_list), 6))

    # Dersom det bare er en type statistikk, gjør om til liste for konsistens
    if len(statistikk_type_list) == 1:
        axes = [axes]
    # Tilpasser y-aksen avhengig av variabelen
    if variabelnavn == "lufttemperatur":
        y_benevning = "grader celcius"
    elif variabelnavn == "nedbør":
        y_benevning = "mm nedbør"
    elif variabelnavn == "vindstyrke":
        y_benevning = "m/s"
    else:
        y_benevning = "verdi"

    #Går igjenom listen med statistikk-typer og lager plot for hver
    for i, statistikk_type in enumerate(statistikk_type_list):
        if statistikk_type not in statistikk_df.columns:
            print(f"Ugyldig statistikk-type: {statistikk_type}")
            continue

        # plotter
        statistikk_df[statistikk_type].plot(kind='bar', ax=axes[i], color='cyan', edgecolor='red')
        axes[i].set_title(f"{statistikk_type.capitalize()} for {variabelnavn} per by")
        axes[i].set_ylabel(y_benevning)
        axes[i].set_xlabel("By")
        axes[i].tick_params(axis='x', rotation=90)
        axes[i].grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()


# Funksjon for å undersøke korrelasjon mellom ulike parametere
def undersok_korrelasjon(df, var1, var2, by=None):
    """
    Undersøker sammenhengen mellom to værvariabler i datasettet for en spesifikk by.
    Beregner Pearsons korrelasjonskoeffisient og viser scatter-plot med regresjonslinje.
    """

    if by:
        df = df[df["by"] == by]

    # Henter ut verdiene for hver variabel
    df1 = df[df["variable"] == var1][["referenceTime", "value"]].rename(columns={"value": var1})
    df2 = df[df["variable"] == var2][["referenceTime", "value"]].rename(columns={"value": var2})

    # Slår sammen på dato
    felles = pd.merge(df1, df2, on="referenceTime")

    if felles.empty:
        print("Ingen overlappende data for valgte variabler.")
        return

    x = felles[var1]
    y = felles[var2]

    # Beregner korrelasjon
    r, p = pearsonr(x, y)
    print(f"\nKorrelasjon mellom '{var1}' og '{var2}' i {by or 'alle byer'}:")
    print(f"Korrelasjonskoeffisient (r): {r:.2f}")
    print(f"P-verdi: {p:.4f}")

    # Plotter scatter-plot med regresjonslinje
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 5))
    sns.regplot(x=x, y=y, scatter_kws={'alpha':0.6}, line_kws={'color':'red'})
    plt.xlabel(var1)
    plt.ylabel(var2)
    plt.title(f"Sammenheng mellom {var1} og {var2} ({by})")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

def plott_trend_over_tid(df, variabelnavn, visningsnavn="værdata"):
    """
    Plotter en trendanalyse for en valgt værvariabel over tid per by, aggregert per måned.
    Bruker Seaborn for visuell forbedring.

    Args:
    df (DataFrame): Værdata.
    variabelnavn (str): Navnet på værvariabelen i kolonnen "variable".
    visningsnavn (str): Forståelig navn som vises i tittel istedet for kronglete variabelnavn.
    """
    
    # Forbered Seaborn-stil
    sns.set_theme(style="whitegrid")

    # Filtrerer og forbereder data
    data = df[df["variable"] == variabelnavn].copy()
    data["referenceTime"] = pd.to_datetime(data["referenceTime"])
    data["måned"] = data["referenceTime"].dt.to_period("M")
    trend = data.groupby(["måned", "by"])["value"].mean().reset_index()
    trend["måned"] = trend["måned"].dt.to_timestamp()

    # Setter y-akse basert på type variabel
    if variabelnavn == "air_temperature P1D":
        y_akse = "Temperatur (°C)" 
    elif variabelnavn == "precipitation_amount P1D": 
        y_akse = "Nedbør (mm)"
    elif variabelnavn == "wind_speed P1D": 
        y_akse = "Vindstyrke (m/s)"
    else: 
        y_akse = "Verdi"

    # Lager selve plottet
    plt.figure(figsize=(14, 6))
    sns.lineplot(data=trend, x="måned", y="value", hue="by", marker="o")
    plt.title(f"Trend for {visningsnavn.capitalize()} over tid (per måned)", fontsize=14)
    plt.xlabel("Måned")
    plt.ylabel(y_akse)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title="By")
    plt.tight_layout()
    plt.show()

def interaktiv_trend_plot(df, variabelnavn, visningsnavn="Miljødata"):
    """
    Lager en interaktiv tidsserie-visualisering av en valgt værvariabel med Plotly.
    
    Parametre:
    - df (DataFrame): Datasettet som inneholder værdata
    - variabelnavn (str): Navnet på variabelen i 'variable'-kolonnen, f.eks. "air_temperature P1D"
    - visningsnavn (str): Tittel som vises i grafen
    
    Returnerer:
    - Interaktiv Plotly-graf
    """
    # Filtrer data basert på valgt variabel
    data = df[df["variable"] == variabelnavn].copy()
    data["referenceTime"] = pd.to_datetime(data["referenceTime"])
    
    # Tilpasser hva y-aksen skal vise basert på variabelnavn
    if variabelnavn == "air_temperature P1D":
        y_akse = "Temperatur (°C)"
    elif variabelnavn == "precipitation_amount P1D":
        y_akse = "Nedbør (mm)"
    elif variabelnavn == "wind_speed P1D":
        y_akse = "Vindstyrke (m/s)"
    else:
        y_akse = "Verdi"

    # Lager interaktiv figur
    fig = px.line(
        data,
        x="referenceTime",
        y="value",
        color="by",
        title=f"{visningsnavn.capitalize()} over tid",
        labels={
            "referenceTime": "Dato",
            "value": y_akse,
            "by": "By"
        }
    )
    
    fig.update_traces(mode="lines+markers", hovertemplate="Dato: %{x}<br>Verdi: %{y}")
    fig.update_layout(hovermode="x unified")
    
    fig.show()

def interaktiv_by_og_variabel_plot(df):
    """
    Lager en interaktiv Plotly-graf med to dropdown-menyer:
    - En for valg av by
    - En for valg av værvariabel (temperatur, nedbør, vind)
    """

    # Konverter dato
    df["referenceTime"] = pd.to_datetime(df["referenceTime"])

    # Variabler og visningsnavn
    variabler = {
        "air_temperature P1D": "Temperatur (°C)",
        "precipitation_amount P1D": "Nedbør (mm)",
        "wind_speed P1D": "Vindstyrke (m/s)"
    }

    byer = df["by"].unique()
    traces = []
    visibility_matrix = []

    # Lag en trace for hver (by, variabel)-kombinasjon
    for variabel in variabler:
        for by in byer:
            filtrert = df[(df["by"] == by) & (df["variable"] == variabel)]
            trace = go.Scatter(
                x=filtrert["referenceTime"],
                y=filtrert["value"],
                mode="lines+markers",
                name=f"{by} – {variabler[variabel]}",
                visible=False
            )
            traces.append(trace)

    # By default: første kombinasjon skal være synlig
    traces[0].visible = True

    # Opprett layout og figur
    fig = go.Figure(data=traces)

    # Lag synlighetsmatriser for dropdown-knappene
    total = len(variabler) * len(byer)

    # Dropdown for byvalg
    by_knapper = []
    for i, by in enumerate(byer):
        vis = [False] * total
        for j, variabel in enumerate(variabler):
            index = i * len(variabler) + j
            vis[index] = (variabel == "air_temperature P1D")  # standardvariabel
        by_knapper.append(dict(
            label=by,
            method="update",
            args=[{"visible": vis},
                  {"title": f"Temperatur over tid – {by}"}]
        ))

    # Dropdown for variabelvalg
    var_knapper = []
    for j, (variabel, navn) in enumerate(variabler.items()):
        vis = [False] * total
        for i, by in enumerate(byer):
            index = i * len(variabler) + j
            vis[index] = (by == byer[0])  # standardby
        var_knapper.append(dict(
            label=navn,
            method="update",
            args=[{"visible": vis},
                  {"title": f"{navn} over tid – {byer[0]}"}]
        ))

    # Oppdater layout med begge menyer
    fig.update_layout(
        updatemenus=[
            dict(buttons=by_knapper, direction="down", showactive=True, x=0.4, xanchor="left", y=1.15, yanchor="top"),
            dict(buttons=var_knapper, direction="down", showactive=True, x=0.65, xanchor="left", y=1.15, yanchor="top"),
        ],
        title=f"Temperatur over tid – {byer[0]}",
        xaxis_title="Dato",
        yaxis_title="Verdi",
        hovermode="x unified",
        template="plotly_white",
        height=600
    )

    fig.show()
