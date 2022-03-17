from domain.Rental import Rental
from repo.Files import Files
from service.UndoService import FunctionCall, Operation


class RentalService:

    def __init__(self, undo_service, rental_repo, book_repo, client_repo):
        self._repository = rental_repo
        self._book_repo = book_repo
        self._client_repo = client_repo
        self._undo_service = undo_service
        self._files = Files()

    def readpickle(self, file):
        result = self._files.readpickle(file)
        for i in result:
            self.create_rental(i.id, i.book_id, i.client_id, i.rented_date, i.returned_date, False)

    def writepickle(self, file):
        self._files.writepickle(file, self._repository)

    def readtext(self, file):
        result = self._files.readtext(file)
        for i in result:
            i = i.strip.split("|")
            self.create_rental(i[0], i[1], i[2], i[3], i[4], False)

    def writetext(self, file):
        self._files.writepickle(file, self._repository)

    def create_rental(self, rental_id, book, client, start, end, undo):
        rental = Rental(rental_id, book, client, start, end)
        self._repository.store(rental)
        if undo == True:
            undo_fun = FunctionCall(self._repository.delete, int(rental_id))
            redo_fun = FunctionCall(self._repository.store, rental_id, book, client, start, end)
            self._undo_service.record(Operation(undo_fun, redo_fun))

        return rental

    def filter_rentals(self, book, client):
        result = []
        for rental in self._repository.getAll():
            if book == rental.book_id or client == rental.client_id or (book is None and client is None):
                result.append(rental)
        return result

    def delete_rental(self, rental_id):
        rental = self._repository.delete(rental_id)

        undo_fun = FunctionCall(self._repository.store, rental)
        redo_fun = FunctionCall(self._repository.delete, rental_id)
        self._undo_service.record(Operation(undo_fun, redo_fun))

        return rental

    def return_rental(self, rental_id, return_date):
        returnn = 0
        for i in self._repository.getAll():
            if i.id == rental_id:
                returnn = i.returned_date
                i.returned_date = return_date

        undo_fun = FunctionCall(self.return_rental, rental_id, returnn)
        redo_fun = FunctionCall(self.return_rental, rental_id, return_date)
        self._undo_service.record(Operation(undo_fun, redo_fun))

    def format_rental(self, rental):
        return str(rental.id) + " | " + str(rental.book_id) + " | " + str (rental.client_id) + " | " + str(rental.rented_date) + " | " + str(rental.returned_date)


