import os
import pickle


from repo.Repository import Repository, RepositoryException
from service.BookService import BookService
from service.ClientService import ClientService
from service.RentalService import RentalService
import random

from service.UndoService import UndoService


class Console:

    def __init__(self, repository, books, clients, rentals):
        self._1 = repository
        self._2 = books
        self._3 = clients
        self._4 = rentals

    def initialize(self):
        self._undo_service = UndoService()

        self._client_repo = Repository()
        self._book_repo = Repository()
        self._rental_repo = Repository()

        self._rental_service = RentalService(self._undo_service, self._rental_repo, self._book_repo, self._client_repo)
        self._client_service = ClientService(self._undo_service, self._rental_service, self._client_repo)
        self._book_service = BookService(self._undo_service, self._rental_service, self._book_repo)


        if self._1 == "inmemory":
            self.initialize_inmemory()
        elif self._1 == "textfiles":
            self.initialize_textfiles()
        elif self._1 == "pickle":
            self.initialize_pickle()


    def initialize_pickle(self):

        self._book_service.readpickle(self._2)
        self._client_service.readpickle(self._3)
        self._rental_service.readpickle(self._4)

    def initialize_textfiles(self):

        self._book_service.readtext(self._2)
        self._client_service.readtext(self._3)
        self._rental_service.readtext(self._4)

    def initialize_inmemory(self):
        name = ['Statu-Palma', 'Barba-Cot', 'Pasari', 'Lati-Lungila', 'Setila', 'Fomila', 'Fat-Frumos', 'Fecioara',
                'Stefan', 'Barosu', 'Dragonu Roshu', 'Dragonu Verde']
        for i in range(10):
            id_ = random.randint(100, 999)
            found = False
            for client in self._client_repo.getAll():
                if id_ == client.id:
                    found = True
            if not found:
                self._client_service.create(id_, name[random.randint(1, 11)], False)

        title = ['Mistborn: The Final Empire', 'Wheel of Time', 'Stormlight Archives', 'Intercocalar', 'UFO Sightings',
                 'Search and Rescue Horror Stories', 'Stairs in the woods', 'Night in the woods', 'Life is Strange',
                 'How to train your cat', 'The Reptilian Deep State', 'Deep Space Religions', 'The Art of the Deal'
                                                                                              'How to boil eggs: A commentary on modern cooking',
                 'Red bean stuck at the bottom of a tin can']
        author = ['Tom Scott', 'God Himself', 'Jesus Christ of Nazareth', 'Captain Beefheart', 'Donald J. Trump',
                  'Natalie Wynn', 'Brandino', 'Faker', 'Wendys', 'Captain America', 'Plato', 'Leonardo Davinci']
        for i in range(10):
            id_ = random.randint(100, 999)
            found = False
            for book in self._book_repo.getAll():
                if id_ == book._id:
                    found = True
            if not found:
                self._book_service.create(id_, title[random.randint(1, 13)], author[random.randint(1, 11)], False)

        for i in range(9):
            self._rental_service.create_rental(i, self._book_repo.getAll()[i].id, self._client_repo.getAll()[i].id,
                                               random.randint(1, 30), random.randint(31, 60), False)

    def finish(self):

        # If using files, this function will write back all the changes in the files

        if self._1 == "textfiles":
            self._book_service.writetext(self._2)
            self._client_service.writetext(self._3)
            self._rental_service.writetext(self._4)

        elif self._1 == "pickle":
            self._book_service.writepickle(self._2)
            self._client_service.writepickle(self._3)
            self._rental_service.writepickle(self._4)
        else:
            pass

    def menu(self):
        print("\n~~~~~~~~~~~~~~~~~~~~~\nAB add book")
        print("AC add client")
        print("UB update book")
        print("UC update client")
        print("RB remove book")
        print("RC remove client")
        print("LB list books")
        print("LC list clients")
        print("AR add rental")
        print("RR return rental")
        print("LR list rentals")
        print("undo")
        print("redo")

        print("x to save and exit")

    def start(self):
        print("Console initialized")
        done = False
        while not done:
            try:
                self.menu()
                command = input("Enter command index: ").lower().strip()
                if command == "lb":
                    self.lb()
                elif command == "lc":
                    self.lc()
                elif command == "lr":
                    self.lr()
                elif command == "ac":
                    self.ac()
                elif command == "ab":
                    self.ab()
                elif command == "ar":
                    self.ar()
                elif command == "rb":
                    self.rb()
                elif command == "rc":
                    self.rc()
                elif command == "rr":
                    self.rr()
                elif command == "uc":
                    self.uc()
                elif command == "ub":
                    self.ub()
                elif command == "undo":
                    self.undo()
                elif command == "redo":
                    self.redo()
                elif command == "x":
                    self.finish()
                    done = True
                else:
                    print("Invalid index")
            except ValueError as ve:
                print(ve)
            except TypeError as ve:
                print(ve)
            except RepositoryException as ve:
                print(ve)



    def redo(self):
        a = self._undo_service.redo()
        if a == False:
            print("Can't redo anymore")

    def undo(self):
        a = self._undo_service.undo()
        if a == False:
            print("Can't undo anymore")

    def ub(self):
        idd = int(input("Enter book id to change: "))
        title = input("Enter new title: ")
        author = input("Enter new author: ")
        self._book_service.update(idd, title, author, True)

    def rb(self):
        book_id = input("Enter book id to remove: ")
        book_id = int(book_id)
        self._book_service.delete(book_id)

    def uc(self):
        idd = int(input("Enter client id to change: "))
        name = input("Enter new name: ")
        self._client_service.update(idd, name, True)

    def rc(self):
        client_id = input("Enter client id to remove: ")
        client_id = int(client_id)
        self._client_service.delete(client_id)

    def rr(self):
        rental_id = input("Enter rental id to return: ")
        return_date = input("Enter return date: ")
        rental_id = int(rental_id)
        return_date = int(return_date)
        self._rental_service.return_rental(rental_id, return_date)


    def lb(self):
        """
                Lists all book objects in the book object list:
                :return:
        """
        books = self._book_service.filter_books(None)
        for i in books:
            print(self._book_service.format_book(i))

    def lc(self):
        clients = self._client_service.filter_clients(None)
        for i in clients:
            print(self._client_service.format_client(i))

    def lr(self):
        rentals = self._rental_service.filter_rentals(None, None)
        for i in rentals:
            print(self._rental_service.format_rental(i))

    def ac(self):
        client_id = input("Enter client id: ")
        client_name = input("Enter client name: ")
        self._client_service.create(client_id, client_name, True)

    def ab(self):
        book_id = input("Enter book id: ")
        book_title = input("Enter book title: ")
        book_author = input("Enter book author: ")
        self._book_service.create(book_id, book_title, book_author, True)

    def ar(self):
        rental_id = input("Enter rental id: ")
        book_id = input("Enter book id: ")
        client_id = input("Enter client id: ")
        start = input("Enter start date: ")
        self._rental_service.create_rental(rental_id, book_id, client_id, start, 0, True)

