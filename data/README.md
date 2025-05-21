
# data/  
Denne mappen inneholder datafiler brukt i prosjektet.

## Innhold

- `Byer.json`: En JSON-fil med informasjon om hvilke byer det skal hentes værdata for. Gjør det lettere ved at vi kan kalle på bynavn istedenfor værstasjonsnummer. 
- `VaerData.csv`: Rådata som er hentet fra Met.no sitt Frost API.
- `BehandletVaerData.csv`: Renset og strukturert data brukt i videre analyser.

## Merknader

- Dataene opprettes og overskrives automatisk av notebookene i `notebooks/`.
- Ikke rediger CSV-filene manuelt med mindre det er helt nødvendig.
- `VaerData.csv` opprettes etter kjøring av `HenteData.ipynb`.
- `BehandletVaerData.csv` opprettes etter kjøring av `DataBehandling.ipynb`.

