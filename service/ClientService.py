from domain.Client import Client
from repo.Files import Files
from service.UndoService import FunctionCall, Operation


class ClientService:
    def __init__(self, undo_service, rental_service, repository):
        self._repository = repository
        self._rental_service = rental_service
        self._undo_service = undo_service
        self._files = Files()

    def readpickle(self, file):
        result = self._files.readpickle(file)
        for i in result:
            self.create(i.id, i.name, False)

    def writepickle(self, file):
        self._files.writepickle(file, self._repository)

    def readtext(self, file):
        result = self._files.readtext(file)
        for i in result:
            i = i.strip.split("|")
            self.create(i[0], i[1], False)

    def writetext(self, file):
        self._files.writepickle(file, self._repository)


    def create(self, client_id, client_name, undo):
        client = Client(client_id, client_name)
        self._repository.store(client)
        if undo == True:
            undo_fun = FunctionCall(self._repository.delete, int(client_id))
            redo_fun = FunctionCall(self._repository.store, client_id, client_name)
            self._undo_service.record(Operation(undo_fun, redo_fun))

        return client

    def delete(self, client_id):

        client = self._repository.delete(client_id)

        rentals = self._rental_service.filter_rentals(None, client_id)

        for rent in rentals:
            self._rental_service.delete_rental(rent.id)

        undo_fun = FunctionCall(self._repository.store, client)
        redo_fun = FunctionCall(self._repository.delete, client.id)
        self._undo_service.record(Operation(undo_fun, redo_fun))

        return client

    def get_client_count(self):
        return len(self._repository)

    def update(self, client_id, name, a):
        namee = 0
        found = False
        for client in self._repository.getAll():
            if client.id == client_id:
                namee = client.name
                client.name = name
                found = True
        if not found:
            raise ValueError("Found no client with such an ID")
        if a is not False:
            undo_fun = FunctionCall(self.update, client_id, namee, False)
            redo_fun = FunctionCall(self.update, client_id, name, False)
            self._undo_service.record(Operation(undo_fun, redo_fun))

    def filter_clients(self, client_id):
        result = []
        for client in self._repository.getAll():
            if client_id is None or client.id == client_id:
                result.append(client)
        return result

    def format_client(self, client):
        return str(client.id) + " | " + client.name
