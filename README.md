## Versjonshåndtering

Prosjektet bruker Git for å holde oversikt over alle endringer i koden og for å støtte samarbeid.

- Vi bruker en hovedbranch `main` som inneholder stabile versjoner av prosjektet.
- Funksjoner og forbedringer utvikles i egne branches (f.eks. `Utvikler2`) og merges inn i `main` når de er klare.
- Alle commits har beskrivende meldinger som forklarer hvilke endringer som er gjort.
- Vi bruker GitHub for lagring og samarbeid, og henter/pusher jevnlig for å holde hverandres lokale repo oppdatert.

Eksempel på en utviklingsflyt:
1. `git checkout -b ny-funksjon`
2. Gjør endringer og test.
3. `git add .` og `git commit -m "Implementert ny funksjon"`
4. `git push origin ny-funksjon`
5. Opprett en Pull Request eller `git merge ny-funksjon` inn i `main`

