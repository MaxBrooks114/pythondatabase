import sqlite3

db = sqlite3.connect("contacts.sqlite")
new_email = 'emails@update.com'
phone = input("Enter another phone number")
update_sql = "Update contacts set email = ? where phone = ?"
update_cursor = db.cursor()
update_cursor.execute(update_sql, (new_email, phone))
print("{} rows were updated".format(update_cursor.rowcount))
update_cursor.connection.commit()
update_cursor.close()

for name, phone, email in db.execute("SELECT * FROM contacts"):
    print(name)
    print(phone)
    print(email)
    print("=" * 20)

db.close()