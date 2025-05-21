# MILJODATAANALYSE-APPLIKASJON

Et Python prosjekt i TDT4114 for å hente, analysere og visualisere miljødata fra Met.no sitt Frost API. 
Målet er å utforme en predikativ analyse basert på historiske værdata fra ulike norske byer. 

## Prosjektet vårt inneholder flere ulike mapper: 
- `data/`: Inneholder både rå og bearbeidede datafiler. Disse er hentet opprettet ved å hente data fra Frost API. 
- `docs/`: 
- `notebooks/`: Flere Jupyter Notebooks som tar for seg oppgavene i prosjektbeskrivelsen. Herunder gjøres det da datahenting, rensing, analyse og visualiseringer. 
- `src/`: - Python-funskjoner som anvendes i notebooks. 
- `tests/` - Tester som er laget for databehandlingsfunskjonene 
- `requirements.txt` - Det som kreves av biblioteker og tilsvarende for at applikasjonen skal fungere. 
- `.env` - API-nøkkel til dataen vi har hentet. 



# Utforsk applikasjonen 
1. Klon repoet: 
    ``` bash 
    git clone https://github.com/evenlandmark/Miljodataanalyse-applikasjon.git
2. Innstaler nødvendige biblioteker og tilsvarende: 
    pip install -r requirements.txt
3. Lag en env fil og legg inn API-nøkkel. 
    FROST_API_KEY = dinkeyher


Kjør notebooksene i følgende rekkefølge: 
- `Oppgave 1.ipynb` 
- `HenteData.ipynb`
- `DataBehandling.ipynb`
- `DataAnalyse.ipynb`
- `PrediktivAnalyse.ipynb`
(Det er også rekkefølgen på besvarelsene til prosjektbeskrivelsen)

NB! Viktig at hver notebook kjøres fra toppen. Da noen koder bygger videre på ting som er gjort tidligere i notebooken. I tillegg benytter de ulike cellene seg av biblioteker og tilsvarende som er importert i starten av notebooken. 


## Versjonshåndtering

Under prosjektet vårt har vi brukt Git for å holde oversikt over alle endringer i koden og for å støtte samarbeid.

- Vi bruker en hovedbranch `main` som inneholder stabile versjoner av prosjektet.
- Besvarelse av oppgaver, funksjoner og forbedringer har blitt utviklet i egne branches (f.eks. `Utvikler1`) og senere blitt merget inn i `main` når de er komplette.
- Vi har gitt alle commits beskrivende meldinger som forklarer hvilke endringer som er gjort.
- Vi har brukt GitHub for lagring og samarbeid, og pushet jevnlig for å holde hverandres lokale repo oppdatert.


