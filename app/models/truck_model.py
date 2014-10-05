import random

class Food_Truck:
    """
    Representation of a truck document.
    """
    type_name = "truck"

    def __init__(self):
        self._id = self.generate_id()
        self.name = None
        self.latitude = None
        self.longitude = None
        self.schedule = None
        self.approved = False

    def generate_id(self):
        ID_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        num = random.getrandbits(122)
        encoding = ''
        for x in xrange(21):
            num, rem = divmod(num, 62)
            encoding += ID_ALPHABET[rem]
        return '{}_{}'.format(self.type_name, encoding)