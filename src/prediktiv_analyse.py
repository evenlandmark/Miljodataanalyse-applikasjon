import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def forbered_data_for_by(df, by_navn, variabel="air_temperature P1D"):
    """
    Filtrerer datasettet for én by og én værvariabel (standard: temperatur),
    og lager en numerisk månedskolonne som brukes som funksjonsvariabel.
    Returnerer X (måned) og y (verdi).
    """
    data = df[(df["by"] == by_navn) & (df["variable"] == variabel)].copy()
    data["referenceTime"] = pd.to_datetime(data["referenceTime"])
    data["måned"] = data["referenceTime"].dt.month  # Bruker måned som funksjonsvariabel

    X = data[["måned"]]  # funksjonsvariabel
    y = data["value"]    # målvariabel (temperatur)
    
    return X, y, data  # Returnerer også originalen for plotting hvis ønsket


def tren_regresjonsmodell(X, y):
    """
    Trener en lineær regresjonsmodell på X og y.
    Returnerer modellen.
    """
    modell = LinearRegression()
    modell.fit(X, y)
    return modell


def evaluer_modell(modell, X, y):
    """
    Evaluerer modellen med MSE og R²-score.
    """
    y_pred = modell.predict(X)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R²-score: {r2:.2f}")

    return y_pred, mse, r2

import matplotlib.pyplot as plt

def plott_prediksjon(data, X, y, y_pred, by_navn):
    """
    Lager en linjegraf som sammenligner faktisk og predikert temperatur.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(data["referenceTime"], y, label="Faktisk temperatur", marker='o')
    plt.plot(data["referenceTime"], y_pred, label="Predikert temperatur", marker='x', linestyle='--')
    plt.title(f"Faktisk vs. Predikert temperatur – {by_navn}")
    plt.xlabel("Dato")
    plt.ylabel("Temperatur (°C)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

