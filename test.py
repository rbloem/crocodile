from person import Person, Manager
import shelve


def make_db(): 
    db=shelve.open("persondb")
    for object in (bob, sue, tom):
        db[object.name]=object
    db.close()

if __name__=="__main__":
    bob=Person("Bob Smith")
    sue=Person("Sue Jones", job="dev", pay=10)
    tom=Manager("Tom Jones", 20)


"""
import shelve




import shelve
db=shelve.open("persondb")

for key in sorted(db):
	print key, "\t=>", db[key]

sue=db["Sue Jones"]
sue.giveRaise(.10)
db["Sue Jones"]=sue
db.close()
"""