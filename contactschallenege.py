import sqlite3

db = sqlite3.connect("contacts.sqlite")
get_name = input("Who do you want to see?")
statement = "SELECT * FROM contacts where name LIKE ?"
for row in db.execute(statement, (get_name,)):
    print(row)
#
# for name, phone, email in db.execute("SELECT * FROM contacts"):
#     print(name)
#     print(phone)
#     print(email)
#     print("=" * 20)

db.close()
