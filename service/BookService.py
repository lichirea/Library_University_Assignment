from domain.Book import Book
from repo.Files import Files
from service.UndoService import FunctionCall, Operation


class BookService:

    def __init__(self, undo_service, rental_service, repo):
        self._repo = repo
        self._rental_service = rental_service
        self._undo_service = undo_service
        self._files = Files()

    def readpickle(self, file):
        result = self._files.readpickle(file)
        for i in result:
            self.create(i.id, i.title, i.author, False)

    def writepickle(self, file):
        self._files.writepickle(file, self._repo)

    def readtext(self, file):
        result = self._files.readtext(file)
        for i in result:
            i = i.strip.split("|")
            self.create(i[0], i[1], i[2], False)

    def writetext(self, file):
            self._files.writepickle(file, self._repo)


    def create(self, book_id, title, author, undo):
        book = Book(book_id, title, author)
        self._repo.store(book)
        if undo == True:
            undo_fun = FunctionCall(self._repo.delete, int(book_id))
            redo_fun = FunctionCall(self._repo.store, book)
            self._undo_service.record(Operation(undo_fun, redo_fun))

        return book

    def delete(self, book_id):
        book = self._repo.delete(book_id)

        rentals = self._rental_service.filter_rentals(book_id, None)

        for rent in rentals:
            self._rental_service.delete_rental(rent.id)

        undo_fun = FunctionCall(self._repo.store, book)
        redo_fun = FunctionCall(self._repo.delete, book_id)
        self._undo_service.record(Operation(undo_fun, redo_fun))

        return book

    def update(self, book_id, title, author, a):
        titlee = 0
        authorr = 0
        found = False
        for book in self._repo.getAll():
            if book.id == book_id:
                titlee = book.title
                authorr = book.author
                book.title = title
                book.author = author
                found = True
        if not found:
            raise ValueError("Book with given ID not found")
        if a is not False:
            undo_fun = FunctionCall(self.update, book_id, titlee, authorr, False)
            redo_fun = FunctionCall(self.update, book_id, title, author, False)
            self._undo_service.record(Operation(undo_fun, redo_fun))

    def filter_books(self, book_id):
        result = []
        for book in self._repo.getAll():
            if book_id is None or book.id == book_id:
                result.append(book)
        return result

    def format_book(self, book):
        return str(book.id) + " | " + book.title + " | " + book.author
