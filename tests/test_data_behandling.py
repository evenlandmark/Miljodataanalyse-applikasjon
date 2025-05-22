import pandas as pd
import pytest
import sys
import os 
# Legger til src-mappen i Python's søkesti
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from data_behandling import DataBehandler

def test_fyll_manglende_codequality():
    # Eksempeldata med én manglende verdi
    data = {
        'sourceId': ['SN18700', 'SN18700'],
        'referenceTime': ['2022-01-01', '2022-01-02'],
        'elementId': ['mean(air_temperature P1D)', 'mean(air_temperature P1D)'],
        'value': [3.5, -2.1],
        'unit': ['degC', 'degC'],
        'codequality': [0, None]
    }

    df = pd.DataFrame(data)
    byer = {'Oslo': 'SN18700'}

    behandler = DataBehandler(df, byer)
    behandler.fyll_manglende_codequality()

    # Nå skal det ikke være noen manglende verdier igjen i 'codequality'
    assert behandler.df['codequality'].isnull().sum() == 0

def test_finn_manglende_verdier():
    data = {
        'sourceId': ['SN18700', 'SN18700'],
        'referenceTime': ['2022-01-01', None],
        'elementId': ['mean(air_temperature P1D)', 'mean(air_temperature P1D)'],
        'value': [3.5, -2.1],
        'unit': ['degC', 'degC'],
        'codequality': [0, None]
    }

    df = pd.DataFrame(data)
    byer = {'Oslo': 'SN18700'}
    behandler = DataBehandler(df, byer)

    manglende = behandler.finn_manglende_verdier()

    assert manglende['referenceTime'] == 1
    assert manglende['codequality'] == 1

def test_klassifiser_codequality():
    data = {
        'sourceId': ['SN18700'] * 3,
        'referenceTime': ['2022-01-01', '2022-01-02', '2022-01-03'],
        'elementId': ['mean(air_temperature P1D)'] * 3,
        'value': [3.5, -2.1, 1.0],
        'unit': ['degC'] * 3,
        'codequality': [0, 4, 6]
    }

    df = pd.DataFrame(data)
    byer = {'Oslo': 'SN18700'}
    behandler = DataBehandler(df, byer)

    behandler.klassifiser_codequality()

    forventet = ['God', 'Middels', 'Dårlig']
    faktisk = list(behandler.df['codequality'])

    assert faktisk == forventet

def test_tell_kalde_dager():
    data = {
        'sourceId': ['SN68230', 'SN18700', 'SN50540'],
        'referenceTime': ['2022-01-01', '2022-01-02', '2022-01-03'],
        'elementId': ['mean(air_temperature P1D)'] * 3,
        'value': [1.5, -3.2, -0.5],
        'unit': ['degC'] * 3,
        'codequality': [0, 1, 2],
        'variable': ['air_temperature P1D'] * 3
    }

    df = pd.DataFrame(data)
    byer = {
        'Trondheim': 'SN68230',
        'Oslo': 'SN18700',
        'Bergen': 'SN50540'
    }
    behandler = DataBehandler(df, byer)

    kalde_dager = behandler.tell_kalde_dager()
    assert len(kalde_dager) == 2

def test_lagre_data(tmp_path):
    data = {
        'sourceId': ['SN18700'],
        'referenceTime': ['2022-01-01'],
        'elementId': ['mean(air_temperature P1D)'],
        'value': [3.5],
        'unit': ['degC'],
        'codequality': [0]
    }

    df = pd.DataFrame(data)
    byer = {'Oslo': 'SN18700'}
    behandler = DataBehandler(df, byer)

    filsti = tmp_path / "test_output.csv"
    behandler.lagre_data(filsti=str(filsti))

    assert filsti.exists()
    # Les inn og sjekk innhold
    innlest = pd.read_csv(filsti)
    assert len(innlest) == 1
    assert innlest.iloc[0]['value'] == 3.5
