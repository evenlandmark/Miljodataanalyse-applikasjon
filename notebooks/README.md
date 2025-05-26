# notebooks/

Jupyter Notebooks som utfører steg for steg analyser og besvarer oppgavene i prosjektbeskrivelsen. 
 

Notebooksfolderen vår består av fem ulike notebooks: 

- `Oppgave1.ipynb` - Besvarelse av oppgave 1 i prosjektet -> å sette opp utviklingsmiljøet. 
- `HenteData.ipynb` - Henter data fra API hos Met.no. Her har vi lent oss på Met.no sin kode på å hente data fra dem. Bruker hente_data.py for å gjøre dette, og lagrer  data vi finner i data/VaerData.csv
- `DataAnalyse.ipynb` - Beregner statistiske data, implementering av enkle statistiske analyser for å undersøke sammenhengen mellom variabler og visualisering av dette. 
Denne nootebooken er dermed et "svar" på oppgave 4 og 5 i prosjektbeskrivelsen. 
- `DataBehandling.ipynb` - Utfører databehandling hvor vi renser data, gjør den mer lesbar og identifiserer "hull i dataen". I tillegg vises det hvordan ulike verktøy kan anvendes for å utføre diverse handlinger. Notebooken fungerer også som et svar på oppgave 3 i prosjektbeskrivelsen. 
- `PrediktivAnalyse.ipynb` - Ved hjelp av metoder i predaktiv_analyse.py utfører vi en predaktiv analyse med lineær regresjon. 


Notebooksene bruker funksjoner/metoder fra `src/` og lagrer data i mappen `data/`. 

## Hvordan kjøre notebookene
1. Kjør notebookene fra toppen ved å trykke på "run all cells".


## Informasjon om oppsettet 
    I prosjektet har vi valgt å ha "svarene" på oppgavene som notebooks, hvor notebookene består av en blanding av både markdown og kodeceller. 
    Kodecellene fungerer i hovedsak på den måten at de henter definerte metoder/funksjoner, og bruker de for å hente, rense, visualisere og utføre analyser. 
    Markdowncellene fungerer som et supplement, hvor de både forklarer teori, og hvilke metoder som er benyttet. Samt at de kommenterer resultatene vi finner. 
    Vi har ved hjelp av markdown celler kommentert vurderingskriteriene utifra hva vi har gjort.
