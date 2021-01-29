

class ContactList():
    def __init__(self):
        self.contacts = {}

    def addContact(self, Id, username, addr, port):
        try:
            starting_contacts = self.contacts
            self.contacts[str(Id)] = [str(username), str(addr), int(port)]

        except Exception as e:
            print("Unable to add contact due to the following reason ...")
            print(e)

            # Ensure the contact list is unaltered in case of error
            self.contacts = starting_contacts

    def delContact(self, Id):
        try:
            starting_contacts = self.contacts
            if self.contacts.pop(str(Id), None) == None:
                raise Exception("No contact could be found with the given ID")

        except Exception as e:
            print("Unable to add contact due to the following reason ...")
            print(e)

            # Ensure the contact list is unaltered in case of error
            self.contacts = starting_contacts

    def findById(self, Id):
        try:
            assert str(Id) in self.contacts.keys(
            ), "No contact with the given ID"
            return self.contacts[str(Id)]

        except Exception as e:
            print("Unable to find contact due to the following reasons ...")
            print(e)

    def findByUsername(self, username):
        try:
            for key in self.contacts.keys():
                if self.contacts[key][0] == str(username):
                    return self.contacts[key]

            # if no contact was found with the given username, throw an error
            raise Exception("No contact with the given username")

        except Exception as e:
            print("Unable to find contact due to the following reasons ...")
            print(e)

    def all(self):
        return self.contacts

    def numContacts(self):
        return len(self.contacts.keys())

    def checkById(self, Id):
        return str(Id) in self.contacts.keys()

    def updateContacts(self, contacts):
        self.contacts = contacts


if __name__ == "__main__":
    contacts = ContactList()

    contacts.addContact("1234", "user1", "127.0.0.1", 6789)

    print(contacts.all())

    contact = contacts.findById("1234")
    print(contact)

    contacts.addContact("5678", "user2", "127.0.0.1", 6544)
    print(contacts.all())

    contact = contacts.findByUsername("user2")
    print(contact)

    contacts.delContact("1234")
    print(contacts.all())

    contacts.delContact("3456")
    print(contacts.all())
