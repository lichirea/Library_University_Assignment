class Rental:

    def __init__(self, rental_id, book_id, client_id, rented_date, returned_date):
        self._client_id = int(client_id)
        self._book_id = int(book_id)
        self._id = int(rental_id)
        self._rented_date = int(rented_date)
        self._returned_date = int(returned_date)

    @property
    def client_id(self):
        return self._client_id

    @property
    def id(self):
        return self._id

    @property
    def returned_date(self):
        return self._returned_date

    @returned_date.setter
    def returned_date(self, value):
        self._returned_date = value

    @property
    def book_id(self):
        return self._book_id

    @property
    def rented_date(self):
        return self._rented_date

