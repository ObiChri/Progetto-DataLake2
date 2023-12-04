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
                tickets = concert['biglietti']  # Accesso alla lista di biglietti

                print(f"\nConcerto {i}:")
                for ticket in tickets:
                    ticket_type = ticket['tipo']
                    availability = ticket['disponibili']
                    price = ticket['prezzo']
                    if availability == 0:
                        availability = 'sold-out'

                    print(f"{ticket_type.capitalize()}: Disp: {availability}, Prezzo: {price}€")

                # Chiedi all'utente di selezionare il tipo di biglietto da acquistare
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
                    updated_availability = availability - tickets_to_buy
                    collection.update_one({"_id": concert["_id"]},
                                          {"$set": {"biglietti.$[elem].disponibili": updated_availability}},
                                          array_filters=[{"elem.tipo": ticket_type}])

                    print(
                        f"Hai acquistato {tickets_to_buy} biglietti {ticket_type.capitalize()} per il concerto '{concert['nome']}'")
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
