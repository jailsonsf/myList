class Task:
    # exceptions
    NOT_EXIST_TASK = "Not exist task."
    
    # constants
    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"

    def __init__(self, id_list, title, description, date):
        self.id = self.create_id()
        self.title = title 
        self.description = description
        self.date = date.datetime.utcnow()
        self.id_list = id_list 
        self.status = self.STATUS_OPEN

    def to_dict(self):
        if (self.id != None and self.title != None and self.date != None and self.id_list != None and self.status != None):
            return {'id':self.id, 'title':self. title, 'description': self.description, 'date': self.date, 'status':self.status, 'id_list': self.id_list}
        else:
            raise Exception(self.NOT_EXIST_LIST)
    
    def create_id(self):
        return 1

# test 
if __name__ == '__main__':
    t = Task(1, "Comprar leite", "Vá e compre leite, ué!", "12/10/2018")
    print(t.to_dict())
