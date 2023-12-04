from pymongo import MongoClient


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
            print(f"Concerti trovati: {num_concerts}")
            for i, concert in enumerate(concerts, start=1):
                availability = concert['biglietti']['disponibili']
                if availability == 0:
                    availability = 'sold-out'
                else:
                    availability = availability[0]  # Prende il primo elemento della lista di disponibilità

                concert_details = f"{i}: {concert['nome']}, {concert['data'].strftime('%d/%m/%y')}, disp:{availability}, {concert['biglietti']['prezzo']}€"
                print(concert_details)

            # Chiedi all'utente di selezionare un concerto per l'acquisto
            concert_index = int(input(f"Scegli il concerto da acquistare (1 - {num_concerts}): "))
            if 1 <= concert_index <= num_concerts:
                selected_concert = concerts[concert_index - 1]
                buy_tickets(selected_concert, collection)
            else:
                print("Selezione non valida.")
        else:
            print(f"Nessun concerto trovato per l'artista '{artist_name}'")
    except Exception as e:
        print("Errore durante la ricerca dei concerti dell'artista:", str(e))


# Funzione per acquistare i biglietti per un concerto
def buy_tickets(concert, collection):
    try:
        print("Dettagli del concerto:")
        print(f"Nome: {concert['nome']}")
        print(f"Data: {concert['data'].strftime('%d/%m/%y')}")
        print(f"Prezzo: {concert['biglietti']['prezzo']}€")
        availability = concert['biglietti']['disponibili']

        if isinstance(availability, list):  # Verifica se la disponibilità è una lista
            availability = availability[0]  # Prende il primo elemento della lista

        if availability > 0:
            tickets_to_buy = int(input(f"Quanti biglietti vuoi acquistare? (Disponibili: {availability}): "))
            if tickets_to_buy > 0 and tickets_to_buy <= availability:
                updated_availability = availability - tickets_to_buy
                collection.update_one({"_id": concert["_id"]},
                                      {"$set": {"biglietti.disponibili": updated_availability}})
                print(f"Hai acquistato {tickets_to_buy} biglietti per il concerto '{concert['nome']}'")
                print(f"Disponibilità rimasta: {updated_availability}")
            else:
                print("Quantità non valida o biglietti esauriti.")
        else:
            print("I biglietti per questo concerto sono esauriti.")

    except Exception as e:
        print("Errore durante l'acquisto dei biglietti:", str(e))


# Funzione per trovare un concerto per nome
def find_concert_by_name(concert_name, collection):
    try:
        # Query per trovare il concerto basato sul nome
        query = {"nome": concert_name}

        # Esegui la query nella collezione Concerti
        result = collection.find_one(query)

        # Stampa il risultato trovato
        if result:
            print("Dettagli del concerto:")
            print(result)
            return result
        else:
            print(f"Nessun concerto trovato con il nome '{concert_name}'")
            return None
    except Exception as e:
        print("Errore durante la ricerca del concerto per nome:", str(e))


def main():
    # Connessione al database e alla collezione
    collection = connect_to_mongodb()

    if collection is not None:
        print("Seleziona l'opzione di ricerca:")
        print("1. Cerca per nome dell'artista")
        print("2. Cerca per nome del concerto")

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
            concert = find_concert_by_name(concert_name, collection)
            if concert:
                buy_tickets(concert, collection)
        else:
            print("Opzione non valida. Si prega di selezionare 1 o 2.")


if __name__ == "__main__":
    main()
