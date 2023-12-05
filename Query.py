from pymongo import MongoClient
from datetime import datetime
from geopy.distance import geodesic


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


# Funzione per trovare i concerti di un artista specifico
def find_concerts_by_artist(artist_name, collection):
    try:
        # Query per trovare i concerti dell'artista specificato
        query = {"artisti.nome": artist_name}

        # Esegui la query nella collezione Concerti
        results = collection.find(query)

        concerts = list(results)
        num_concerts = len(concerts)

        if num_concerts > 0:
            print(f"Concerti trovati per l'artista '{artist_name}': {num_concerts}")
            for i, concert in enumerate(concerts, start=1):
                concert_name = concert['nome']
                concert_date = concert['data']
                tickets = concert['biglietti']

                print(f"\nConcerto {i}:")
                print(f"Nome: {concert_name}")
                print(f"Data: {concert_date.strftime('%d/%m/%y')}")

                # Mostra la disponibilità dei biglietti
                for ticket in tickets:
                    ticket_type = ticket['tipo']
                    available_tickets = ticket['disponibili']
                    price = ticket['prezzo']
                    print(f"{ticket_type.capitalize()}: Prezzo: {price}€, Disponibili: {available_tickets}")

                # Chiedi all'utente se desidera acquistare un biglietto per questo concerto
                ticket_choice = input(
                    f"Vuoi acquistare un biglietto (VIP/Standard) per questo concerto (sì/no)? ").lower()
                if ticket_choice == 'sì' or ticket_choice == 'si':
                    buy_tickets(concert, collection)
                    break
                else:
                    print("Operazione annullata.")
        else:
            print(f"Nessun concerto trovato per l'artista '{artist_name}'")
    except Exception as e:
        print("Errore durante la ricerca dei concerti dell'artista:", str(e))


# Funzione per trovare i concerti per nome
def find_concerts_by_name(concert_name, collection):
    try:
        # Query per trovare i concerti basati sul nome
        query = {"nome": concert_name}

        # Esegui la query nella collezione Concerti
        results = collection.find(query)

        concerts = list(results)
        num_concerts = len(concerts)

        if num_concerts > 0:
            print(f"Concerti trovati: {num_concerts}")
            for i, concert in enumerate(concerts, start=1):
                concert_name = concert['nome']
                concert_date = concert['data']
                tickets = concert['biglietti']

                print(f"\nConcerto {i}:")
                print(f"Nome: {concert_name}")
                print(f"Data: {concert_date.strftime('%d/%m/%y')}")

                # Mostra la disponibilità dei biglietti
                for ticket in tickets:
                    ticket_type = ticket['tipo']
                    available_tickets = ticket['disponibili']
                    price = ticket['prezzo']
                    print(f"{ticket_type.capitalize()}: Prezzo: {price}€, Disponibili: {available_tickets}")

            return concerts  # Restituisce la lista dei concerti trovati
        else:
            print(f"Nessun concerto trovato con il nome '{concert_name}'")
            return []
    except Exception as e:
        print("Errore durante la ricerca dei concerti per nome:", str(e))
        return []


from datetime import datetime


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


# Ricerca per vicinanza geografica
def find_concerts_by_location(latitude, longitude, radius, collection):
    try:
        # Coordiante del luogo dell'utente
        user_location = (latitude, longitude)

        # Query per trovare i concerti entro il raggio specificato
        all_concerts = collection.find({})  # Ottieni tutti i concerti

        concerts_within_radius = []
        for concert in all_concerts:
            # Coordiante del luogo del concerto
            concert_location = (concert['posizione']['coordinates'][1], concert['posizione']['coordinates'][0])

            # Calcola la distanza tra il luogo dell'utente e il luogo del concerto
            distance = geodesic(user_location, concert_location).kilometers

            # Aggiungi il concerto alla lista se è entro il raggio specificato
            if distance <= radius:
                concerts_within_radius.append(concert)

        num_concerts = len(concerts_within_radius)
        if num_concerts > 0:
            print(f"Concerti trovati entro {radius} km dal luogo specificato: {num_concerts}")
            # Visualizza o elabora i risultati come desiderato
            for concert in concerts_within_radius:
                # Mostra i dettagli del concerto
                print(f"Nome: {concert['nome']}, Data: {concert['data']}, Altro: ...")

        else:
            print(f"Nessun concerto trovato entro {radius} km dal luogo specificato")
    except Exception as e:
        print("Errore durante la ricerca dei concerti per vicinanza:", str(e))


# Funzione per acquistare i biglietti per un concerto
def buy_tickets(concert, collection):
    try:
        ticket_type = input("Quale tipo di biglietto vuoi acquistare (VIP/Standard)? ").lower()

        tickets = concert['biglietti']
        selected_ticket = next((ticket for ticket in tickets if ticket['tipo'].lower() == ticket_type), None)

        if selected_ticket:
            availability = selected_ticket['disponibili']
            price = selected_ticket['prezzo']

            if availability == 0:
                print(f"I biglietti {ticket_type.capitalize()} per questo concerto sono esauriti.")
            else:
                tickets_to_buy = int(input(
                    f"Quanti biglietti {ticket_type.capitalize()} vuoi acquistare? (Disponibili: {availability}): "))

                if tickets_to_buy > 0 and tickets_to_buy <= availability:
                    total_price = price * tickets_to_buy
                    updated_availability = availability - tickets_to_buy
                    collection.update_one(
                        {"_id": concert["_id"],
                         "biglietti": {"$elemMatch": {"tipo": ticket_type, "disponibili": {"$gte": tickets_to_buy}}}},
                        {"$inc": {"biglietti.$.disponibili": -tickets_to_buy}}
                    )

                    print(
                        f"Hai acquistato {tickets_to_buy} biglietti {ticket_type.capitalize()} per il concerto '{concert['nome']}'")
                    print(f"Costo totale: {total_price}€")
                    print(f"Disponibilità rimasta: {updated_availability}")
                else:
                    print("Quantità non valida o biglietti esauriti.")
        else:
            print(f"Tipo di biglietto '{ticket_type.capitalize()}' non disponibile per questo concerto.")

    except Exception as e:
        print("Errore durante l'acquisto dei biglietti:", str(e))


def main():
    # Connessione al database e alla collezione
    collection = connect_to_mongodb()

    if collection is not None:
        print("Seleziona l'opzione di ricerca:")
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
            # Input per la vicinanza geografica
            latitude = float(input("Inserisci la latitudine del tuo luogo: "))
            longitude = float(input("Inserisci la longitudine del tuo luogo: "))
            radius = float(input("Inserisci il raggio di ricerca in chilometri: "))
            # Trova i concerti entro la vicinanza geografica
            find_concerts_by_location(latitude, longitude, radius, collection)
        else:
            print("Opzione non valida. Si prega di selezionare un'opzione da 1 a 4.")


if __name__ == "__main__":
    main()
