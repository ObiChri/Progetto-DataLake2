from pymongo import MongoClient
from datetime import datetime


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
            concerts = find_concerts_by_name(concert_name, collection)
            if concerts:
                # Se vengono trovati concerti con quel nome, permette di selezionare e acquistare i biglietti
                num_concerts = len(concerts)
                print(f"\nScegli il concerto da acquistare (1-{num_concerts}):")
                for i, concert in enumerate(concerts, start=1):
                    print(f"{i}. Nome: {concert['nome']}, Data: {concert['data'].strftime('%d/%m/%y')}")

                while True:
                    try:
                        choice = int(input("Inserisci il numero corrispondente al concerto da acquistare: "))
                        if 1 <= choice <= num_concerts:
                            buy_tickets(concerts[choice - 1],
                                        collection)  # Acquista biglietti per il concerto selezionato
                            break
                        else:
                            print("Inserisci un numero valido.")
                    except ValueError:
                        print("Inserisci un numero valido.")
            else:
                print("Nessun concerto trovato con il nome specificato.")
        else:
            print("Opzione non valida. Si prega di selezionare 1 o 2.")


if __name__ == "__main__":
    main()
