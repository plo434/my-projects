from db import connect_db

class BankDatabase:
    def __init__(self):
        self.conn = connect_db()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def execute(self, query, params=None):
        with self.conn:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor.lastrowid

    def fetch_one(self, query, params=None):
        with self.conn:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()

class Stats:
    def __init__(self, db):
        self.db = db

    def increment_employee_count(self):
        self.db.execute('''UPDATE stats SET employee_count = employee_count + 1 WHERE id = 1''')

    def increment_customer_count(self):
        self.db.execute('''UPDATE stats SET customer_count = customer_count + 1 WHERE id = 1''')

    def increment_branch_count(self):
        self.db.execute('''UPDATE stats SET branch_count = branch_count + 1 WHERE id = 1''')

    def get_branch_count(self):
        return self.db.fetch_one('''SELECT branch_count FROM stats''')[0]

    def get_employee_count(self):
        return self.db.fetch_one('''SELECT employee_count FROM stats''')[0]

    def get_customer_count(self):
        return self.db.fetch_one('''SELECT customer_count FROM stats''')[0]

    def update_total_deposits(self, amount):
        self.db.execute('''UPDATE stats SET total_deposits = total_deposits + ?, 
                           total_vault_balance = total_vault_balance + ? WHERE id = 1''', 
                        (amount, amount))

    def update_total_withdrawals(self, amount):
        self.db.execute('''UPDATE stats SET total_withdrawals = total_withdrawals + ?, 
                           total_vault_balance = total_vault_balance - ? WHERE id = 1''', 
                        (amount, amount))

class Branch:
    def __init__(self, db):
        self.db = db

    def add(self, name, address, phone):
        stats = Stats(self.db)
        stats.increment_branch_count()
        id_num = stats.get_branch_count()
        self.db.execute('''INSERT INTO branches (id, name, address, phone) 
                           VALUES (?, ?, ?, ?)''', (id_num, name, address, phone))

    def update_balance(self, branch_id, amount, is_deposit):
        if is_deposit:
            self.db.execute('''UPDATE branches SET vault_balance = vault_balance + ?, 
                               total_deposits = total_deposits + ? WHERE id = ?''', 
                            (amount, amount, branch_id))
        else:
            self.db.execute('''UPDATE branches SET vault_balance = vault_balance - ?, 
                               total_withdrawals = total_withdrawals + ? WHERE id = ?''', 
                            (amount, amount, branch_id))

class Employee:
    def __init__(self, db):
        self.db = db

    def add(self, first_name, last_name, password, email, phone, job_title, salary, role, branch_id):
        stats = Stats(self.db)
        stats.increment_employee_count()
        id_num = stats.get_employee_count()
        self.db.execute('''INSERT INTO employees 
                           (id, first_name, last_name, password, email, phone, job_title, salary, role, branch_id)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                        (id_num, first_name, last_name, password, email, phone, job_title, salary, role, branch_id))

class Customer:
    def __init__(self, db):
        self.db = db

    def add(self, first_name, last_name, email, password, phone, address):
        stats = Stats(self.db)
        stats.increment_customer_count()
        id_num = stats.get_customer_count()
        self.db.execute('''INSERT INTO customers 
                           (id, first_name, last_name, email, password, phone, address)
                           VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                        (id_num, first_name, last_name, email, password, phone, address))

class Transaction:
    def __init__(self, db):
        self.db = db

    def deposit(self, account_id, branch_id, amount):
        self.db.execute('''INSERT INTO transactions 
                           (account_id, branch_id, type, amount)
                           VALUES (?, ?, 'dep', ?)''', 
                        (account_id, branch_id, amount))
        self.db.execute('''UPDATE accounts SET balance = balance + ? WHERE id = ?''', 
                        (amount, account_id))
        Branch(self.db).update_balance(branch_id, amount, True)
        Stats(self.db).update_total_deposits(amount)

    def withdraw(self, account_id, branch_id, amount):
        self.db.execute('''INSERT INTO transactions 
                           (account_id, branch_id, type, amount)
                           VALUES (?, ?, 'Withd', ?)''', 
                        (account_id, branch_id, amount))
        self.db.execute('''UPDATE accounts SET balance = balance - ? WHERE id = ?''', 
                        (amount, account_id))
        Branch(self.db).update_balance(branch_id, amount, False)
        Stats(self.db).update_total_withdrawals(amount)

if __name__ == "__main__":
    with BankDatabase() as db:
        Branch(db).add("Main Branch", "123 Main St", "123-4564444-7890")
        Employee(db).add("John", "Do4e", "passw4ord123", "john442.doe@example.com", "123-4546-7890", "Manager", 5044000, "Admin", 1)
        Customer(db).add("Alice", "Smith", "alice.s222mith@example.com", "securepass", "987-654-3210", "456 Elm St")
        Transaction(db).deposit(1, 1, 1000.0)
        Transaction(db).withdraw(1, 1, 200.0)