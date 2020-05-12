import sqlite3
import pytz
import datetime

db = sqlite3.connect("accounts.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
db.execute("CREATE table IF NOT EXISTS accounts (name text primary key not "
           "null, balance integer not null)")
db.execute("CREATE table if not exists transactions (time timestamp not "
           "null, account text not null, amount "
           "integer "
           "not null, primary "
           "key (time, account))")
db.execute("CREATE VIEW IF NOT EXISTS localhistory AS SELECT strftime("
           "'%Y-%m-%d "
           "%H:%M:%f', "
           "transactions.time, 'localtime') AS localtime, "
           "transactions.account, transactions.amount FROM "
           "transactions ORDER BY transactions.time")


class Account:

    @staticmethod
    def _current_time():
        return pytz.utc.localize(datetime.datetime.utcnow())

    def __init__(self, name: str, opening_balance: int = 0):
        cursor = db.execute("select name, balance from accounts where (name "
                            "=?)", (name,))
        row = cursor.fetchone()

        if row:
            self.name, self._balance = row
            print("Retrieved record for {}. ".format(self.name), end='')
        else:
            self.name = name
            self._balance = opening_balance
            cursor.execute("Insert into accounts values(?, ?)", (name,
                                                                 opening_balance))
            cursor.connection.commit()
            print("Account created for {}. ".format(self.name), end='')
        self.show_balance()

    def deposit(self, amount: int) -> float:
        if amount > 0:
            self._save_update(amount)
            print("{:.2f} deposited".format(amount / 100))
        return self._balance

    def withdraw(self, amount: int) -> float:
        if 0 < amount <= self._balance:
            self._save_update(-amount)
            print("{:.2f} withdrawn".format(amount / 100))
            return amount / 100
        else:
            print("The amount must be greater than zero and less than your "
                  "current balance")

    def show_balance(self):
        print("Balance on account {} is {:.2f}".format(self.name,
                                                       self._balance / 100))

    def _save_update(self, amount):
        new_balance = self._balance + amount
        deposit_time = Account._current_time()
        try:
            db.execute("update accounts set balance = ? where (name = ?)",
                   (new_balance, self.name))
            db.execute("insert into transactions values(?, ?, ?)",
                   (deposit_time, self.name, amount))
        except sqlite3.Error:
            db.rollback()
        else:
            db.commit()
            self._balance = new_balance

if __name__ == '__main__':
    john = Account("John")
    john.deposit(1010)
    john.deposit(10)
    john.deposit(10)
    john.withdraw(30)
    john.withdraw(0)
    john.show_balance()
    terry = Account("Terry")
    Graham = Account("Graham", 9000)
    Eric = Account("Eric", 7000)

