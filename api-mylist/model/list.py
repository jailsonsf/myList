class List:
    # exceptions
    NOT_EXIST_LIST = "Not exist list."

    def __init__(self, id, id_user, title, date):
        self.id = id
        self.title = title 
        self.date = date
        self.link = self.create_link()
        self.id_user = id_user 

    def to_dict(self):
        if (self.id != None and self.title != None and self.date != None and self.link != None and self.id_user != None):
            return {'id':self.id, 'title':self. title, 'date': self.date, 'link':self.link, 'id_user': self.id_user}
        else:
            raise Exception(self.NOT_EXIST_LIST)

    def create_link(self):
        return "link 123"
        
    
    def create_id(self):
        return 1

# test 
if __name__ == '__main__':
    l = List(1, "Minha lista papae", '12/10/2018')
    print(l.to_dict())
