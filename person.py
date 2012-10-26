from model import BasicModel


class Person(BasicModel):
    """Sample Implementation of BasicModel

    Person is a sample implementation of BasicModel to show how easy it is
    to get a Model working and pulling/adding data to a MongoDB server.

    """

    def __init__(self, data = {}):
        super(Person, self).__init__(data, collection="people", db="testing")

    @property
    def display_name(self):
        name_data = self.get("fname", "middle_name", "lname")
        name_data = filter(None, name_data)
        return " ".join(name_data)

    @property
    def display_info(self):
        name = self.display_name
        num, addr = self.get("phone_number", "address")
        info = "%s\n%s\n%s\n%s, %s    %s"
        info = info % (name, num, addr["street"], addr["city"], addr["state"], 
                       addr["zipcode"])
        return info
