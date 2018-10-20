class User:
    # exceptions
    NOT_EXIST_USER = "Not exist user."

    def __init__(self, id, username, name, email, date_creation):
        self.id = id
        self.name = name
        self.email = email
        self.username = username
        self.date_creation = date_creation

    def to_dict(self):
        if (
            self.username != None
            and self.name != None
            and self.email != None
            and self.date_creation != None
        ):
            return {
                "id": self.id,
                "username": self.username,
                "name": self.name,
                "email": self.email,
                "date_creation": self.date_creation,
            }
        else:
            raise Exception(self.NOT_EXIST_USER)


if __name__ == "__main__":
    u = User("myusername", "My Name", "username@gmail.com")
    print(u.to_dict())
