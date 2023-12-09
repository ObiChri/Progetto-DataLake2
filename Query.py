from pymongo import MongoClient
from datetime import datetime
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import time

def connessione_mongo():
    """
    Stabilisce una connessione a MongoDB e restituisce un oggetto di raccolta.
    Da modificare con la propria stringa di connessione e con i propri nomi del database e della collection
    """
    try:
        client = MongoClient("mongodb+srv://carlotta_mapelli:s2.Bb_%24%23m5P5Th_@cluster0.zhmcqeo.mongodb.net/") 

        db = client.Tickettwo

        collection = db.Concerti

        return collection
    except Exception as e:
        print("Errore durante la connessione a MongoDB:", str(e))
        return None

def concerto_per_artista(artista, raccolta):
    """La funzione cerca e visualizza informazioni sui concerti associati a un determinato artista all'interno di una raccolta di dati""" 
    try:
        query = {"artisti.nome": {"$regex": artista, "$options": "i"}}
        risultati = raccolta.find(query)

        concerti = list(risultati)
        num_concerti = len(concerti)

        if num_concerti > 0:
            print(f"Concerti trovati: {num_concerti}")
            for i, concerto in enumerate(concerti, start=1):
                print(f"\nConcerto {i}:")
                print(f"Nome: {concerto['nome']}")
                print(f"Data: {concerto['data'].strftime('%d-%m-%Y')}")
                print(f"Luogo: {concerto['luogo']}")
                for biglietto in concerto['biglietti']:
                    tipo_biglietto = biglietto['tipo'].capitalize()
                    prezzo = biglietto['prezzo']
                    disponibilita = biglietto['disponibili']
                    print(f"{tipo_biglietto}: Prezzo: {prezzo}€, Disponibili: {disponibilita}")

            scelta = int(input(f"Scegli il concerto da acquistare (1-{num_concerti}): "))
            concerto_selezionato = concerti[scelta - 1]  # Indice inizia da 0
            acquista_biglietti(concerto_selezionato, raccolta)
        else:
            print("Nessun concerto trovato.")
    except Exception as e:
        print("Errore durante la ricerca per nome dell'artista:", str(e))

def trova_concerti_per_nome(nome, raccolta):
    """ La funzione cerca e visualizza informazioni sui concerti associati a un determinato nome all'interno di una raccolta di dati.""" 
    try:
        query = {"nome": {"$regex": nome, "$options": "i"}}
        risultati = raccolta.find(query)

        concerti = list(risultati)
        num_concerti = len(concerti)

        if num_concerti > 0:
            print(f"Concerti trovati: {num_concerti}")
            for i, concerto in enumerate(concerti, start=1):
                print(f"\nConcerto {i}:")
                print(f"Nome: {concerto['nome']}")
                print(f"Data: {concerto['data'].strftime('%d-%m-%Y')}")
                print(f"Luogo: {concerto['luogo']}")
                for biglietto in concerto['biglietti']:
                    tipo_biglietto = biglietto['tipo'].capitalize()
                    prezzo = biglietto['prezzo']
                    disponibilita = biglietto['disponibili']
                    print(f"{tipo_biglietto}: Prezzo: {prezzo}€, Disponibili: {disponibilita}")

            scelta = int(input(f"Scegli il concerto da acquistare (1-{num_concerti}): "))
            concerto_selezionato = concerti[scelta - 1]  # Indice inizia da 0
            acquista_biglietti(concerto_selezionato, raccolta)
        else:
            print("Nessun concerto trovato.")
    except Exception as e:
        print("Errore durante la ricerca per nome del concerto:", str(e))

def trova_concerti_per_intervallo_date(data_inizio, data_fine, raccolta):
""" La funzione  ricerca e visualizza informazioni sui concerti compresi in un intervallo di date specificato"""
    try:
        # Conversione delle stringhe in oggetti datetime
        data_inizio = datetime.strptime(data_inizio, '%Y-%m-%d')
        data_fine = datetime.strptime(data_fine, '%Y-%m-%d')

        query = {
            "data": {
                "$gte": data_inizio,
                "$lte": data_fine
            }
        }

        risultati = raccolta.find(query)

        concerti = list(risultati)
        num_concerti = len(concerti)

        if num_concerti > 0:
            print(
                f"Concerti trovati nell'intervallo di date ({data_inizio.strftime('%d-%m-%Y')} - {data_fine.strftime('%d-%m-%Y')}):")
            for i, concerto in enumerate(concerti, start=1):
                print(f"\nConcerto {i}:")
                print(f"Nome: {concerto['nome']}")
                print(f"Data: {concerto['data'].strftime('%d-%m-%Y')}")
                print(f"Luogo: {concerto['luogo']}")
                for biglietto in concerto['biglietti']:
                    tipo_biglietto = biglietto['tipo'].capitalize()
                    prezzo = biglietto['prezzo']
                    disponibilita = biglietto['disponibili']
                    print(f"{tipo_biglietto}: Prezzo: {prezzo}€, Disponibili: {disponibilita}")

            scelta = int(input(f"Scegli il concerto da acquistare (1-{num_concerti}): "))
            concerto_selezionato = concerti[scelta - 1]  # Indice inizia da 0
            acquista_biglietti(concerto_selezionato, raccolta)
        else:
            print("Nessun concerto trovato nell'intervallo di date specificato")
    except Exception as e:
        print("Errore durante la ricerca per intervallo di date:", str(e))

def acquista_biglietti(concerto, raccolta):
""" La funzione gestisce il processo di acquisto dei biglietti per un concerto specificato""" 
    try:
        biglietti = concerto['biglietti']

        print(f"I tipi di biglietti disponibili per il concerto '{concerto['nome']}' sono:")
        for idx, biglietto in enumerate(biglietti, start=1):
            print(
                f"{idx}. {biglietto['tipo'].capitalize()}: Prezzo: {biglietto['prezzo']}€, Disponibili: {biglietto['disponibili']}")

        scelta_biglietto = int(input(f"Scegli il tipo di biglietto da acquistare (1-{len(biglietti)}): "))
        biglietto_selezionato = biglietti[scelta_biglietto - 1]

        disponibilita = biglietto_selezionato['disponibili']
        prezzo = biglietto_selezionato['prezzo']
        tipo_biglietto = biglietto_selezionato['tipo']

        if disponibilita == 0:
            print(f"I biglietti {tipo_biglietto.capitalize()} per questo concerto sono esauriti.")
        else:
            biglietti_da_acquistare = int(input(
                f"Quanti biglietti {tipo_biglietto.capitalize()} vuoi acquistare? (Disponibili: {disponibilita}): "))

            if 0 < biglietti_da_acquistare <= disponibilita:
                disponibilita_aggiornata = disponibilita - biglietti_da_acquistare
                raccolta.update_one({"_id": concerto["_id"]},
                                      {"$set": {"biglietti.$[elem].disponibili": disponibilita_aggiornata}},
                                      array_filters=[{"elem.tipo": tipo_biglietto}])

                prezzo_totale = prezzo * biglietti_da_acquistare
                print(
                    f"Hai acquistato {biglietti_da_acquistare} biglietti {tipo_biglietto.capitalize()} per il concerto '{concerto['nome']}'. "
                    f"Totale: {prezzo_totale}€")
                print(f"Disponibilità rimasta: {disponibilita_aggiornata}")
            else:
                print("Quantità non valida o biglietti esauriti.")

    except Exception as e:
        print("Errore durante l'acquisto dei biglietti:", str(e))

def trova_concerti_per_indirizzo(indirizzo, raggio, raccolta):
    """ La funzione icerca e visualizza informazioni sui concerti nelle vicinanze di un indirizzo specificato, entro un determinato raggio in chilometri."""
    try:
        geolocalizzatore = Nominatim(user_agent="ricerca_concerti", timeout=10)

        posizione = geolocalizzatore.geocode(indirizzo)

        if posizione is None:
            print("Indirizzo non trovato.")
            return

        coordinate_utente = (posizione.latitude, posizione.longitude)

        tutti_concerti = list(raccolta.find())

        time.sleep(1)

        concerti_vicini = []
        for concerto in tutti_concerti:
            posizione_concerto = geolocalizzatore.geocode(concerto['luogo'])
            if posizione_concerto is None:
                continue

            coordinate_concerto = (posizione_concerto.latitude, posizione_concerto.longitude)

            # Calcola la distanza tra l'indirizzo utente e il concerto
            distanza = geodesic(coordinate_utente, coordinate_concerto).kilometers

            # Se il concerto è entro il raggio specificato, aggiungilo alla lista dei concerti vicini
            if distanza <= raggio:
                concerti_vicini.append(concerto)

        num_concerti_vicini = len(concerti_vicini)
        if num_concerti_vicini > 0:
            print(f"Concerti trovati entro {raggio} km da '{indirizzo}': {num_concerti_vicini}")
            for i, concerto in enumerate(concerti_vicini, start=1):
                print(f"\nConcerto {i}:")
                print(f"Nome: {concerto['nome']}")
                print(f"Data: {concerto['data'].strftime('%d-%m-%Y')}")
                print(f"Luogo: {concerto['luogo']}")
                for biglietto in concerto['biglietti']:
                    tipo_biglietto = biglietto['tipo'].capitalize()
                    prezzo = biglietto['prezzo']
                    disponibilita = biglietto['disponibili']
                    print(f"{tipo_biglietto}: Prezzo: {prezzo}€, Disponibili: {disponibilita}")

            scelta = int(input(f"Scegli il concerto da acquistare (1-{num_concerti_vicini}): "))
            concerto_selezionato = concerti_vicini[scelta - 1]  # Indice inizia da 0
            acquista_biglietti(concerto_selezionato, raccolta)
        else:
            print(f"Nessun concerto trovato entro {raggio} km da '{indirizzo}'.")
    except Exception as e:
        print("Errore durante la ricerca per indirizzo:", str(e))


if __name__ == "__main__":
    raccolta = connessione_mongo()

    if raccolta is not None:
        totale_concerti = raccolta.count_documents({})
        print(f"Seleziona l'opzione di ricerca tra {totale_concerti} concerti disponibili:")
        print("1. Cerca per nome dell'artista")
        print("2. Cerca per nome del concerto")
        print("3. Cerca per intervallo di date")
        print("4. Cerca per vicinanza geografica")

        scelta_utente = input("Inserisci il numero corrispondente all'opzione desiderata: ")

        if scelta_utente == '1': #ricerca per nome artista
            nome_artista = input("Inserisci il nome dell'artista da cercare: ")
            concerto_per_artista(nome_artista, raccolta)
        elif scelta_utente == '2': #ricerca per nome concerto
            nome_concerto = input("Inserisci il nome del concerto da cercare: ")
            trova_concerti_per_nome(nome_concerto, raccolta)
        elif scelta_utente == '3': #ricerca per intervallo di date
            data_inizio = input("Inserisci la data di inizio (YYYY-MM-DD): ")
            data_fine = input("Inserisci la data di fine (YYYY-MM-DD): ")
            trova_concerti_per_intervallo_date(data_inizio, data_fine, raccolta)
        elif scelta_utente == '4': #ricerca per indirizzo
            indirizzo = input("Inserisci l'indirizzo (via, città): ")
            raggio = 7  # Raggio di 7 km
            trova_concerti_per_indirizzo(indirizzo, raggio, raccolta)
        else:
            print("Opzione non valida. Si prega di selezionare un'opzione da 1 a 4.")


