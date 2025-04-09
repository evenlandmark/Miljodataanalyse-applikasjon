import pandas as pd
import json
import numpy as np

class DataBehandler:
    def __init__(self, df, byer_dict):
        self.df = df
        self.byer = byer_dict
    
    def fyll_manglende_codequality(self):
        """Fyller inn manglende verdier i kolonnen 'codequality' med den mest brukte verdien"""
        if 'codequality' in self.df.columns:
            mest_vanlige = self.df['codequality'].mode()[0]
            self.df['codequality'] = self.df['codequality'].fillna(mest_vanlige)
        return self.df

    def finn_manglende_verdier(self):
        """Returnerer en oversikt over antall manglende verdier per kolonne"""
        return self.df.isna().sum()
    
    # Copilot foreslo denne funksjonen. Hva gjør den? 
    def fyll_manglende_verdier(self):
        """Fyller inn manglende verdier i kolonnene 'codequality' og 'lines_of_code'"""
        if 'codequality' in self.df.columns:
            mest_vanlige = self.df['codequality'].mode()[0]
            self.df['codequality'] = self.df['codequality'].fillna(mest_vanlige)
        
        if 'lines_of_code' in self.df.columns:
            median = self.df['lines_of_code'].median()
            self.df['lines_of_code'] = self.df['lines_of_code'].fillna(median)
        
        return self.df

    def omstrukturer_data(self):
        """Renser og strukturer rådataen til et mer lesbart format."""
        self.df['referenceTime'] = pd.to_datetime(self.df['referenceTime']).dt.date
        
        self.df[['statistikk', 'variable']] = self.df['elementId'].str.extract(r'(\w+)\(([^)]+)')

        self.df['by'] = self.df['sourceId'].map({v: k for k, v in self.byer.items()})

        self.df = self.df[[
            'by', 'sourceId', 'referenceTime',
            'statistikk', 'variable', 'value',
            'unit', 'codequality'
        ]]
        
        return self.df
    
    def lagre_data(self, filsti='../data/BehandletVaerData.csv'):
        """
        Lagrer den behandlede DataFrame-en til en CSV-filen BehandletVaerData.csv
        """
        self.df.to_csv(filsti, index=False)
        print(f"\nBehandlet data lagret i {filsti}")

    def lagre_rådata(self, filsti='../data/VaerData.csv'):
        """
        Lagrer rådataen til en CSV-filen VaerData.csv
        """
        self.df.to_csv(filsti, index=False)
        print(f"\nRådata lagret i {filsti}")

    def tell_kalde_dager(self):
        """
        Returnerer en liste over datoer for kalde dager i Trondheim, altså der temperaturen er under 0 grader. 
        """
        kalde_dager = self.df[
            (self.df['variable'] == 'air_temperature P1D') &
            (self.df['value'] < 0)
        ]
        return kalde_dager
    
    def klassifiser_codequality(self):
        """
        Gjør om numeriske codequality-verdier til kategorier: God, Middels, Dårlig.
        """
        self.df['codequality'] = [
            "God" if x in [0, 1, 2]
            else "Middels" if x in [3, 4, 5]
            else "Dårlig"
            for x in self.df['codequality']
        ]
        return self.df

    @staticmethod
    def les_byer_fra_fil(filbane):
        """Laster inn byer og tilhørende SN-koder fra json-filen Byer.json"""
        with open(filbane, 'r', encoding='utf-8') as f:
            byer = json.load(f)
        return byer