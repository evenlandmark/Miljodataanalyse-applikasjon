
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt


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

def plott_trend_over_tid(df, variabelnavn, visningsnavn="værdata"):
    """
    Plotter en trendanalyse for en valgt værvariabel over tid per by, aggregert per måned.

    Args:
    df (DataFrame): Værdata.
    variabelnavn (str): Navnet på værvariabelen i kolonnen "variable".
    visningsnavn (str): Forståelig navn som vises i tittel istedet for kronglete variabelnavn.
    """
    
    data = df[df["variable"] == variabelnavn].copy()
    data["referenceTime"] = pd.to_datetime(data["referenceTime"])
    data["måned"] = data["referenceTime"].dt.to_period("M")
    
    # Regner ut gjennomsnitt per måned og by, slik at vi kan se utviklingen over tid i plottet
    trend = data.groupby(["måned", "by"])["value"].mean().reset_index()
    trend["måned"] = trend["måned"].dt.to_timestamp()

    #Tilpasser y-aksen avhengig av variabelen
    if variabelnavn == "air_temperature P1D":
        y_akse = "grader Celcius" 
    elif variabelnavn == "precipitation_amount P1D": 
        y_akse = "mm nedbør"
    elif variabelnavn == "wind_speed P1D": 
        y_akse = "m/s Vindstyrke"
    else: 
        y_akse = "Verdi"


    plt.figure(figsize=(12, 6))

    for by in trend["by"].unique():
        by_data = trend[trend["by"] == by]
        plt.plot(by_data["måned"], by_data["value"], label=by)

    plt.title(f"Trend for {visningsnavn.capitalize()} over tid (per måned)")
    plt.xlabel("Måned")
    plt.ylabel(y_akse)
    plt.legend(title="By")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

