import unittest


class Book:

    def __init__(self, book_id, title, author):
        try:
            book_id = int(book_id)
        except ValueError:
            raise ValueError("Invalid value for book id")
        if not isinstance(title, str):
            raise ValueError("Invalid value for title")
        if not isinstance(author, str):
            raise ValueError("Invalid value for author")
        self._id = book_id
        self._title = title
        self._author = author

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value < 1:
            raise ValueError("ID must be bigger than 0")
        self._id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if len(value) < 3:
            raise ValueError("Title must be at least 3 characters long")
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if len(value) < 3:
            raise ValueError("Author must be at least 3 characters long")
        self._author = value


class TestBookDomainMethods(unittest.TestCase):

    def test_book(self):
        l = Book(1,"Aaa", "Bbb")
        self.assertEqual(1, l.book_id)
        self.assertEqual("Aaa", l.title)
        self.assertEqual("Bbb", l.author)
        self.assertRaises(ValueError, l.__init__, "A", "Aaa", "Bbb")
        self.assertRaises(ValueError, l.__init__, 1, 1, "Bbb")
        self.assertRaises(ValueError, l.__init__, 1, "Aaa", 1)
