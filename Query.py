from pymongo import MongoClient
from datetime import datetime
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import time


# Funzione per connettersi al database TicketTwo e alla collezione Concerti
def connect_to_mongodb():
    try:
        # Inserisci la tua connection string
        client = MongoClient("mongodb+srv://cbuondonno:yrQEJgK9SCFSQ5hp@cluster0.zvij7cy.mongodb.net/")

        # Seleziona il database TicketTwo
        db = client.TicketTwo

        # Seleziona la collezione Concerti
        collection = db.Concerti

        return collection
    except Exception as e:
        print("Errore durante la connessione a MongoDB:", str(e))
        return None


# Funzione per trovare i concerti per nome dell'artista
def find_concerts_by_artist(artist, collection):
    try:
        query = {"artisti.nome": {"$regex": artist, "$options": "i"}}
        results = collection.find(query)

        concerts = list(results)
        num_concerts = len(concerts)

        if num_concerts > 0:
            print(f"Concerti trovati: {num_concerts}")
            for i, concert in enumerate(concerts, start=1):
                print(f"\nConcerto {i}:")
                print(f"Nome: {concert['nome']}")
                print(f"Data: {concert['data'].strftime('%d-%m-%Y')}")
                print(f"Luogo: {concert['luogo']}")
                for ticket in concert['biglietti']:
                    ticket_type = ticket['tipo'].capitalize()
                    price = ticket['prezzo']
                    availability = ticket['disponibili']
                    print(f"{ticket_type}: Prezzo: {price}€, Disponibili: {availability}")

            choice = int(input(f"Scegli il concerto da acquistare (1-{num_concerts}): "))
            selected_concert = concerts[choice - 1]  # Indice inizia da 0
            buy_tickets(selected_concert, collection)
        else:
            print("Nessun concerto trovato.")
    except Exception as e:
        print("Errore durante la ricerca per nome dell'artista:", str(e))


# Funzione per trovare i concerti per nome del concerto
def find_concerts_by_name(name, collection):
    try:
        query = {"nome": {"$regex": name, "$options": "i"}}
        results = collection.find(query)

        concerts = list(results)
        num_concerts = len(concerts)

        if num_concerts > 0:
            print(f"Concerti trovati: {num_concerts}")
            for i, concert in enumerate(concerts, start=1):
                print(f"\nConcerto {i}:")
                print(f"Nome: {concert['nome']}")
                print(f"Data: {concert['data'].strftime('%d-%m-%Y')}")
                print(f"Luogo: {concert['luogo']}")
                for ticket in concert['biglietti']:
                    ticket_type = ticket['tipo'].capitalize()
                    price = ticket['prezzo']
                    availability = ticket['disponibili']
                    print(f"{ticket_type}: Prezzo: {price}€, Disponibili: {availability}")

            choice = int(input(f"Scegli il concerto da acquistare (1-{num_concerts}): "))
            selected_concert = concerts[choice - 1]  # Indice inizia da 0
            buy_tickets(selected_concert, collection)
        else:
            print("Nessun concerto trovato.")
    except Exception as e:
        print("Errore durante la ricerca per nome del concerto:", str(e))


# Funzione per trovare i concerti nell'intervallo di date specificato
def find_concerts_by_date_interval(start_date, end_date, collection):
    try:
        # Converti le stringhe in oggetti datetime
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Query per trovare i concerti nell'intervallo di date
        query = {
            "data": {
                "$gte": start_date,
                "$lte": end_date
            }
        }

        # Esegui la query nella collezione Concerti
        results = collection.find(query)

        # Stampa i risultati trovati
        concerts = list(results)
        num_concerts = len(concerts)

        if num_concerts > 0:
            print(
                f"Concerti trovati nell'intervallo di date ({start_date.strftime('%d-%m-%Y')} - {end_date.strftime('%d-%m-%Y')}):")
            for i, concert in enumerate(concerts, start=1):
                print(f"\nConcerto {i}:")
                print(f"Nome: {concert['nome']}")
                print(f"Data: {concert['data'].strftime('%d-%m-%Y')}")
                print(f"Luogo: {concert['luogo']}")
                for ticket in concert['biglietti']:
                    ticket_type = ticket['tipo'].capitalize()
                    price = ticket['prezzo']
                    availability = ticket['disponibili']
                    print(f"{ticket_type}: Prezzo: {price}€, Disponibili: {availability}")

            # Chiedi all'utente di selezionare un concerto
            choice = int(input(f"Scegli il concerto da acquistare (1-{num_concerts}): "))
            selected_concert = concerts[choice - 1]  # Indice inizia da 0
            buy_tickets(selected_concert, collection)
        else:
            print("Nessun concerto trovato nell'intervallo di date specificato")
    except Exception as e:
        print("Errore durante la ricerca per intervallo di date:", str(e))


def buy_tickets(concert, collection):
    try:
        tickets = concert['biglietti']

        print(f"I tipi di biglietti disponibili per il concerto '{concert['nome']}' sono:")
        for idx, ticket in enumerate(tickets, start=1):
            print(
                f"{idx}. {ticket['tipo'].capitalize()}: Prezzo: {ticket['prezzo']}€, Disponibili: {ticket['disponibili']}")

        ticket_choice = int(input(f"Scegli il tipo di biglietto da acquistare (1-{len(tickets)}): "))
        selected_ticket = tickets[ticket_choice - 1]

        availability = selected_ticket['disponibili']
        price = selected_ticket['prezzo']
        ticket_type = selected_ticket['tipo']

        if availability == 0:
            print(f"I biglietti {ticket_type.capitalize()} per questo concerto sono esauriti.")
        else:
            tickets_to_buy = int(input(
                f"Quanti biglietti {ticket_type.capitalize()} vuoi acquistare? (Disponibili: {availability}): "))

            if tickets_to_buy > 0 and tickets_to_buy <= availability:
                updated_availability = availability - tickets_to_buy
                collection.update_one({"_id": concert["_id"]},
                                      {"$set": {"biglietti.$[elem].disponibili": updated_availability}},
                                      array_filters=[{"elem.tipo": ticket_type}])

                total_price = price * tickets_to_buy
                print(
                    f"Hai acquistato {tickets_to_buy} biglietti {ticket_type.capitalize()} per il concerto '{concert['nome']}'. "
                    f"Totale: {total_price}€")
                print(f"Disponibilità rimasta: {updated_availability}")
            else:
                print("Quantità non valida o biglietti esauriti.")

    except Exception as e:
        print("Errore durante l'acquisto dei biglietti:", str(e))


def find_concerts_by_address(address, radius, collection):
    try:
        # Inizializza il geolocalizzatore
        geolocator = Nominatim(user_agent="concert_finder", timeout= 10)

        # Ottieni le coordinate geografiche dell'indirizzo specificato
        location = geolocator.geocode(address)

        if location is None:
            print("Indirizzo non trovato.")
            return

        user_coordinates = (location.latitude, location.longitude)

        # Trova tutti i concerti dal database
        all_concerts = list(collection.find())

        time.sleep(1)

        # Filtra i concerti entro 7 km dall'indirizzo specificato
        nearby_concerts = []
        for concert in all_concerts:
            concert_location = geolocator.geocode(concert['luogo'])
            if concert_location is None:
                continue

            concert_coordinates = (concert_location.latitude, concert_location.longitude)

            # Calcola la distanza tra l'indirizzo utente e il concerto
            distance = geodesic(user_coordinates, concert_coordinates).kilometers

            # Se il concerto è entro il raggio specificato, aggiungilo alla lista dei concerti vicini
            if distance <= 7:
                nearby_concerts.append(concert)

        num_nearby_concerts = len(nearby_concerts)
        if num_nearby_concerts > 0:
            print(f"Concerti trovati entro 7 km da '{address}': {num_nearby_concerts}")
            for i, concert in enumerate(nearby_concerts, start=1):
                print(f"\nConcerto {i}:")
                print(f"Nome: {concert['nome']}")
                print(f"Data: {concert['data'].strftime('%d-%m-%Y')}")
                print(f"Luogo: {concert['luogo']}")
                for ticket in concert['biglietti']:
                    ticket_type = ticket['tipo'].capitalize()
                    price = ticket['prezzo']
                    availability = ticket['disponibili']
                    print(f"{ticket_type}: Prezzo: {price}€, Disponibili: {availability}")

            choice = int(input(f"Scegli il concerto da acquistare (1-{num_nearby_concerts}): "))
            selected_concert = nearby_concerts[choice - 1]  # Indice inizia da 0
            buy_tickets(selected_concert, collection)
        else:
            print(f"Nessun concerto trovato entro 7 km da '{address}'.")
    except Exception as e:
        print("Errore durante la ricerca per indirizzo:", str(e))


def main():
    # Connessione al database e alla collezione
    collection = connect_to_mongodb()

    if collection is not None:
        total_concerts = collection.count_documents({})
        print(f"Seleziona l'opzione di ricerca tra {total_concerts} concerti disponibili:")
        print("1. Cerca per nome dell'artista")
        print("2. Cerca per nome del concerto")
        print("3. Cerca per intervallo di date")
        print("4. Cerca per vicinanza geografica")

        user_choice = input("Inserisci il numero corrispondente all'opzione desiderata: ")

        if user_choice == '1':
            # Input dell'artista da cercare
            artist_name = input("Inserisci il nome dell'artista da cercare: ")
            # Trova i concerti dell'artista specificato
            find_concerts_by_artist(artist_name, collection)
        elif user_choice == '2':
            # Input del nome concerto
            concert_name = input("Inserisci il nome del concerto da cercare: ")
            # Trova i concerti per nome
            concert = find_concerts_by_name(concert_name, collection)
            if concert:
                buy_tickets(concert, collection)
        elif user_choice == '3':
            # Input per l'intervallo di date
            start_date = input("Inserisci la data di inizio (YYYY-MM-DD): ")
            end_date = input("Inserisci la data di fine (YYYY-MM-DD): ")
            # Trova i concerti nell'intervallo di date
            find_concerts_by_date_interval(start_date, end_date, collection)
        elif user_choice == '4':
            # Input per l'indirizzo
            address = input("Inserisci l'indirizzo (via, città): ")
            radius = 7  # Raggio di 7 km
            # Trova i concerti entro il raggio di 7 km dall'indirizzo specificato
            find_concerts_by_address(address, radius, collection)
        else:
            print("Opzione non valida. Si prega di selezionare un'opzione da 1 a 4.")


if __name__ == "__main__":
    main()
