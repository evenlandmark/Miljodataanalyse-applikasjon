import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_percentage_error
from sklearn.model_selection import train_test_split

# Har benyttet oss av docStrings for å kunne forklare hva de ulike funksjonene/metodene gjør. 

def hent_og_strukturer_data(filsti, by=None):
    """
    Leser værdata fra fil og strukturerer det for analyse.
    
    Parametere:
        filsti: Filsti til CSV-filen.
        by: Hvis by er oppgitt filtreres data kun for denne byen.
    
    Returnerer en DataFrame med kolonnene dato, temperatur, nedbør.
    """
    df = pd.read_csv(filsti)

    # Beholder bare relevante variabler
    df = df[df["variable"].isin(["air_temperature P1D", "precipitation_amount P1D"])]

    # Filtrer på by hvis ønskelig
    if by:
        df = df[df["by"] == by]

    # Pivotering for å få temperatur og nedbør som kolonner
    df_pivot = df.pivot_table(index="referenceTime",
                               columns="variable",
                               values="value",
                               aggfunc="mean").reset_index()

    df_pivot = df_pivot.rename(columns={
        "referenceTime": "dato",
        "air_temperature P1D": "temperatur",
        "precipitation_amount P1D": "nedbør"
    })

    df_pivot["dato"] = pd.to_datetime(df_pivot["dato"])

    # Fjerner rader med manglende verdier
    df_pivot = df_pivot.dropna(subset=["temperatur", "nedbør"])

    return df_pivot

def legg_til_manglende_verdier(df, andel_missing=0.1, seed=42):
    """
    Returnerer en kopi av datasettet der en andel av temperatur og nedbør er satt til NaN.
    Dette for å kunne bruke det returnerte datasettet til å vise hva manglende verdier gjør med en fremstilling
    """
    df_kopi = df.copy()
    np.random.seed(seed)
    
    antall_rader = len(df_kopi)
    indeks_mangler = np.random.choice(df_kopi.index, size=int(andel_missing * antall_rader), replace=False)

    df_kopi.loc[indeks_mangler, 'temperatur'] = np.nan
    df_kopi.loc[indeks_mangler, 'nedbør'] = np.nan
    
    return df_kopi

def vis_manglende_verdier(df_med_mangler):
    """
    Lager en linjegraf som viser hvordan manglende verdier påvirker temperatur- og nedbørstrender.
    """
    plt.figure(figsize=(12, 6))

    plt.plot(df_med_mangler["dato"], df_med_mangler["temperatur"], label="Temperatur (med manglende verdier)", color="orange")
    plt.plot(df_med_mangler["dato"], df_med_mangler["nedbør"], label="Nedbør (med manglende verdier)", color="blue")
    
    plt.title("Hvordan manglende verdier påvirker trendene")
    plt.xlabel("Dato")
    plt.ylabel("Verdi")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def tren_modell(data, maalvariabel):
    """
    Trener en lineær regresjonsmodell på valgt målvariabel.
    
    Parametere:
        data: DataFrame med kolonner: temperatur, nedbør og wind_speed P1D
        maalvariabel: Strengen 'temperatur' eller 'nedbør'
    
    Returnerer: modell, X_test, y_test, y_pred, r2, mape
    """

    X = data.drop(columns=[maalvariabel, 'dato'])  
    y = data[maalvariabel]

    # deler opp dataen vår i to deler, en for å trene modellen, og en for å teste den senere
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modell = LinearRegression()
    modell.fit(X_train, y_train)

    # regner ut r^2 og Mean Absolute Percentage Error (MAPE)
    y_pred = modell.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)

    return modell, X_test, y_test, y_pred, r2, mape

def vis_regresjon_resultat_scatter(X_test, y_test, y_pred, df, variabelnavn):
    """
    Viser scatterplot av faktisk vs predikert verdi over tid med ekte datoer på x-aksen.

    Parametre:
        X_test: array-like, testverdier brukt til prediksjon
        y_test: array-like, faktiske verdier
        y_pred: array-like, predikerte verdier
        df: pandas DataFrame, opprinnelig datasett med 'dato'-kolonne
        variabelnavn: str, navn på variabelen som predikeres (f.eks. "temperatur")
    """

    datoer_test = df.iloc[X_test.index]['dato']

    # lager dataframe for plotting
    df_resultat = pd.DataFrame({
        'dato': datoer_test,
        'faktisk': y_test,
        'predikert': y_pred
    })
    # if-setninger for å tilpasse titel på y-aksen
    if variabelnavn == "temperatur":
        y_benevning = "Temperatur (°C)"
    elif variabelnavn == "nedbør":
        y_benevning = "mm nedbør"
    elif variabelnavn == "vindstyrke":
        y_benevning = "m/s"
    else:
        y_benevning = "verdi"

    # Plotter
    plt.figure(figsize=(12, 6))
    plt.scatter(df_resultat['dato'], df_resultat['faktisk'], label='Faktisk', alpha=0.6)
    plt.scatter(df_resultat['dato'], df_resultat['predikert'], label='Predikert', alpha=0.6)
    plt.title(f'Faktisk vs Predikert {variabelnavn.capitalize()} (Scatterplot)')
    plt.xlabel('Dato')
    plt.ylabel(f'{y_benevning}')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def vis_regresjon_resultat_søyle(X_test, y_test, y_pred, df, variabelnavn):
    """
    Viser søylediagram av faktisk vs predikert verdi over tid med datoer på x-aksen.

    Parametre:
        X_test: array-like, testverdier brukt til prediksjon
        y_test: array-like, faktiske verdier
        y_pred: array-like, predikerte verdier
        df: pandas DataFrame, opprinnelig datasett med 'dato'-kolonne
        variabelnavn: str, navn på variabelen som predikeres (f.eks. "temperatur")
    """
    datoer_test = df.iloc[X_test.index]['dato']

    df_resultat = pd.DataFrame({
        'dato': datoer_test,
        'faktisk': y_test,
        'predikert': y_pred
    })

    x = df_resultat['dato']
    width = 0.4

    # if-setninger for å tilpasse tittel på y-aksen
    if variabelnavn == "temperatur":
        y_benevning = "Temperatur (°C)"
    elif variabelnavn == "nedbør":
        y_benevning = "mm nedbør"
    elif variabelnavn == "vindstyrke":
        y_benevning = "m/s"
    else:
        y_benevning = "verdi"

    plt.figure(figsize=(12, 6))
    plt.bar(x - pd.Timedelta(days=0.2), df_resultat['faktisk'], width=width, label='Faktisk', align='center')
    plt.bar(x + pd.Timedelta(days=0.2), df_resultat['predikert'], width=width, label='Predikert', align='center')
    plt.title(f'Faktisk vs Predikert {variabelnavn.capitalize()} (Søylediagram)')
    plt.xlabel('Dato')
    plt.ylabel(f'{y_benevning}')

    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.grid(True)
    plt.show()

def vis_regresjon_resultat_linje(X_test, y_test, y_pred, df, variabelnavn):
    """
    Viser linjediagram av faktiske verdier vs predikerte verdi over tid med datoer på x-aksen.

    Parametre:
        X_test: array-like, testverdier brukt til prediksjon
        y_test: array-like, faktiske verdier
        y_pred: array-like, predikerte verdier
        df: pandas DataFrame, opprinnelig datasett med 'dato'-kolonne
        variabelnavn: str, navn på variabelen som predikeres (f.eks. "temperatur")
    """
    datoer_test = df.iloc[X_test.index]['dato']

    df_resultat = pd.DataFrame({
        'dato': datoer_test,
        'Faktisk': y_test,
        'Predikert': y_pred
    })

    # if-setninger for å tilpasse tittel på y-aksen
    if variabelnavn == "temperatur":
        y_benevning = "Temperatur (°C)"
    elif variabelnavn == "nedbør":
        y_benevning = "mm nedbør"
    elif variabelnavn == "vindstyrke":
        y_benevning = "m/s"
    else:
        y_benevning = "verdi"

    # Gjør dataframe "long format" for seaborn. 
    df_melted = df_resultat.melt(id_vars='dato', value_vars=['Faktisk', 'Predikert'],
                                 var_name='Type', value_name=variabelnavn.capitalize())

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_melted, x='dato', y=variabelnavn.capitalize(), hue='Type', marker='o')
    plt.title(f'Faktisk vs Predikert {variabelnavn.capitalize()} (Linjediagram)')
    plt.xlabel('Dato')
    plt.ylabel(f'{y_benevning}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def filtrer_byer(filsti):
    """
    Returnerer en liste med unike byer som finnes i datasettet.
    Kan brukes til å se hvilke byer man kan velge blant i analysen.
    
    Parametere:
        filsti: Filsti til CSV-filen.
    
    Returnerer:
        Liste med unike bynavn.
    """
    df = pd.read_csv(filsti)
    return df["by"].dropna().unique().tolist()