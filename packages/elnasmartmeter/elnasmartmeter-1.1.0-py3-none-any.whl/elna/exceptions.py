# define Python user-defined exceptions
class Error(Exception):
    """ Base class for other exceptions """
    pass


class NewConnectionError(Error):
    """ Raised when failing to establish a new connection to the device. """
    def __init__(self, message="Failed to establish a new connection."):
        self.message = message
        super().__init__(self.message)

