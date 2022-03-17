class Client:

    def __init__(self, client_id, name):
        try:
            client_id = int(client_id)
        except ValueError:
            raise ValueError("Invalid value for client id")
        if not isinstance(name, str):
            raise ValueError("Invalid value for name")
        self._id = client_id
        self._name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value < 1:
            raise ValueError("Client ID must be bigger than 0")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long")
        self._name = value


def test_client():
    a = Client(1, "Aaa")
    assert a._id == 1
    assert a.name == "Aaa"
    try:
        a = Client("a", "b")
        assert False
    except ValueError:
        assert True


test_client()
