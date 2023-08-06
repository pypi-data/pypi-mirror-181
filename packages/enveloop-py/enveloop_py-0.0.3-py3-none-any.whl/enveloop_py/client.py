class Client:
    """Client class."""

    def __init__(self, name=None, **kwargs):
        """Initialize the client."""
        self._name = name

    @property
    def name(self):
        """Return the name of the client."""
        return self._name

    def run(self):
        """Run the client."""
        print("Running client: {}".format(self.name))

def client(name):
    """Return an instance of Client."""
    return Client()
