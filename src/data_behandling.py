import pandas as pd
import json
import numpy as np

class DataBehandler:
    def __init__(self, df, byer_dict):
        """
        Initialiserer DataBehandler-klassen med et datasett og et oppslagsverk for byer.

        Parametre:
        - df (DataFrame): Pandas DataFrame som inneholder værdata.
        - byer_dict (dict): Ordbok som kobler bynavn til stasjonskoder (f.eks. {"Oslo": "SN18700"}).

        Denne metoden lagrer datasettet og by-ordboken som attributter i klassen, slik at de kan brukes
        av andre metoder for behandling og analyse av dataene.
        """
        # Lagre datasettet og byordboken som attributter i objektet
        self.df = df
        self.byer = byer_dict
    
    def fyll_manglende_codequality(self):
        """
        Fyller inn manglende verdier i kolonnen 'codequality' med den mest brukte (modus) verdien.

        Returnerer:
        - DataFrame: Den oppdaterte DataFrame-en der alle NaN-verdier i 'codequality'-kolonnen er fylt inn
        med den mest forekommende verdien i kolonnen.

        Merk:
        - Hvis kolonnen 'codequality' ikke finnes i datasettet, vil metoden ikke gjøre noe.
        """
        if 'codequality' in self.df.columns:
            # Finn den mest vanlige verdien (modus) i kolonnen
            mest_vanlige = self.df['codequality'].mode()[0]
            # Fyll inn manglende verdier med modus
            self.df['codequality'] = self.df['codequality'].fillna(mest_vanlige)
        return self.df

    def finn_manglende_verdier(self):
        """
        Gir en oversikt over hvor mange manglende verdier (NaN) det finnes i hver kolonne i datasettet.

        Returnerer:
        - pandas.Series: En Series hvor indeksene er kolonnenavn og verdiene er antall manglende verdier.

        Eksempel:
        >>> behandler.finn_manglende_verdier()
        temperature     5
        humidity        0
        codequality     3
        dtype: int64
        """
        return self.df.isna().sum()

    def omstrukturerer_data(self):
        """
        Forbedrer lesbarheten og strukturen i datasettet:
        - Konverterer tidskolonnen 'referenceTime' til kun dato.
        - Splitter opp 'elementId' i to kolonner: 'statistikk' og 'variable'.
        - Legger til bynavn basert på 'sourceId'.
        - Reorganiserer kolonnene i en ny, mer ryddig rekkefølge.

        Returnerer:
            pd.DataFrame: Et oppdatert og forbedret DataFrame.
        """
        # Fjerner tidspunkt og beholder kun dato
        self.df['referenceTime'] = pd.to_datetime(self.df['referenceTime']).dt.date

        # Splitter 'elementId' inn i to separate kolonner: 'statistikk' og 'variable'
        self.df[['statistikk', 'variable']] = self.df['elementId'].str.extract(r'(\w+)\(([^)]+)')

        # Mapper 'sourceId' til bynavn basert på byer-dictionary
        self.df['by'] = self.df['sourceId'].map({v: k for k, v in self.byer.items()})

        # Reorganiserer kolonner for bedre struktur
        self.df = self.df[['by', 'sourceId', 'referenceTime', 'statistikk', 'variable', 'value', 'unit', 'codequality']]

        return self.df

    
    def lagre_data(self, filsti='../data/BehandletVaerData.csv'):
        """
        Lagrer den behandlede DataFrame-en til en CSV-fil.

        Parametere:
        - filsti (str): Filstien hvor CSV-filen skal lagres. Standard er '../data/BehandletVaerData.csv'.

        Returnerer:
        - None

        Skriver en bekreftelse hvis lagringen lykkes, eller en feilmelding hvis noe går galt.
        """
        try:
            self.df.to_csv(filsti, index=False)
            print(f"\nBehandlet data lagret i: {filsti}")
        except Exception as e:
            print(f"\nKlarte ikke å lagre data til {filsti}. Feil: {e}")


    def lagre_rådata(self, filsti='../data/VaerData.csv'):
        """
        Lagrer rådataen til en CSV-fil.

        Parametere:
        - filsti (str): Filstien hvor CSV-filen skal lagres. Standard er '../data/VaerData.csv'.

        Returnerer:
        - None

        Skriver en bekreftelse hvis lagringen lykkes, eller en feilmelding hvis noe går galt.
        """
        try:
            self.df.to_csv(filsti, index=False)
            print(f"\nRådata lagret i: {filsti}")
        except Exception as e:
            print(f"\nKlarte ikke å lagre rådata til {filsti}. Feil: {e}")


    def tell_kalde_dager(self):
        """
        Returnerer en DataFrame med rader for alle dager der temperaturen (air_temperature P1D) er under 0 grader,
        uavhengig av by eller stasjon.

        Returnerer:
        - DataFrame med kalde dager (rader der temperaturen er under 0 grader)
        """
        if 'variable' not in self.df.columns or 'value' not in self.df.columns:
            print("DataFrame mangler nødvendige kolonner.")
            return pd.DataFrame()

        kalde_dager = self.df[
            (self.df['variable'] == 'air_temperature P1D') &
            (self.df['value'] < 0)
        ]

        print(f"Fant {len(kalde_dager)} kalde dager.")
        return kalde_dager
    
    def klassifiser_codequality(self):
        """
        Gjør om numeriske 'codequality'-verdier til kategorier:
        - 0-2: God
        - 3-5: Middels
        - 6 og høyere: Dårlig

        Returnerer:
            DataFrame med oppdatert 'codequality'-kolonne som kategorisk tekst.
        """
        if 'codequality' not in self.df.columns:
            print("Kolonnen 'codequality' finnes ikke i DataFrame.")
            return self.df

        def vurder(x):
            if pd.isna(x):
                return x  # Behold NaN som NaN
            elif x in [0, 1, 2]:
                return "God"
            elif x in [3, 4, 5]:
                return "Middels"
            else:
                return "Dårlig"

        self.df['codequality'] = self.df['codequality'].apply(vurder)
        return self.df

    @staticmethod
    def les_byer_fra_fil(filbane):
        """
        Denne try-except-blokken håndterer filinnlasting og JSON-dekoding
        og gir tilbakemelding hvis noe går galt.
        Den prøver å åpne filen og lese innholdet som JSON.
        """
        try:
            with open(filbane, 'r', encoding='utf-8') as f:
                byer = json.load(f)
            return byer
        except FileNotFoundError:
            print(f"❌ Filen {filbane} ble ikke funnet.")
            return {}
        except json.JSONDecodeError:
            print(f"❌ Feil ved lesing av JSON-format i filen {filbane}.")
            return {}