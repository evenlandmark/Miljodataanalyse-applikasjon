import requests
import time
# Kilde:
# Met.no. (u.å.). *Python-eksempel for Frost API*. Hentet fra https://frost.met.no/python_example.html
def hent_data_fra_frost(endpoint, params, client_id, maks_forsøk=3, ventetid=2):
    """
    Henter data fra Frost API med støtte for flere forsøk og feilhåndtering.

    Parametere:
    - endpoint (str): API-endepunkt (URL).
    - params (dict): Parametere til API-kallet.
    - client_id (str): API-nøkkel (client ID).
    - maks_forsøk (int): Antall ganger funksjonen prøver å hente data.
    - ventetid (int): Antall sekunder mellom hvert forsøk.

    Returnerer:
    - dict: JSON-data dersom forespørselen lykkes.
    - None: Hvis alle forsøk feiler.
    """

    for forsøk in range(1, maks_forsøk + 1):
        try:
            response = requests.get(endpoint, params=params, auth=(client_id, ''))

            if response.status_code == 200:
                try:
                    return response.json()
                except ValueError:
                    print("Klarte ikke å tolke svaret som JSON.")
                    break

            elif response.status_code == 401:
                print("Ugyldig client ID (401 Unauthorized).")
                break

            elif response.status_code == 403:
                print("Tilgang nektet (403 Forbidden).")
                break

            elif response.status_code == 429:
                print("For mange forespørsler (429 Too Many Requests). Venter og prøver igjen...")
                time.sleep(ventetid)

            elif 500 <= response.status_code < 600:
                print(f"Serverfeil ({response.status_code}). Forsøk {forsøk} av {maks_forsøk}...")
                time.sleep(ventetid)

            else:
                print(f"Forespørsel feilet med statuskode {response.status_code}.")
                break

        except requests.exceptions.RequestException as e:
            print(f"Nettverksfeil: {e}")
            time.sleep(ventetid)

    print("Kunne ikke hente data etter flere forsøk.")
    return None
