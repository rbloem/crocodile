import shelve

db=shelve.open("persondb")
for object in (bob, sue, tom):
	db[object.name]=object
db.close()