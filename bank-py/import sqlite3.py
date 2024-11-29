import sqlite3

class DatabaseConnection:
    def __init__(self, db_name='bank_system.db'):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

class BankEntity:
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def execute_query(self, query, params=None):
        with self.db_connection as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.fetchone()

class Branch(BankEntity):
    def add(self, name, address, phone):
        self.execute_query("UPDATE stats SET branch_count = branch_count + 1 WHERE id = 1")
        id_num = self.execute_query("SELECT branch_count FROM stats")[0]
        self.execute_query("INSERT INTO branches (id, name, address, phone) VALUES (?, ?, ?, ?)",
                           (id_num, name, address, phone))

class Employee(BankEntity):
    def add(self, first_name, last_name, password, email, phone, job_title, salary, role, branch_id):
        self.execute_query("UPDATE stats SET employee_count = employee_count + 1 WHERE id = 1")
        id_num = self.execute_query("SELECT employee_count FROM stats")[0]
        self.execute_query("""INSERT INTO employees 
                              (id, first_name, last_name, password, email, phone, job_title, salary, role, branch_id)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                           (id_num, first_name, last_name, password, email, phone, job_title, salary, role, branch_id))

class Customer(BankEntity):
    def add(self, first_name, last_name, email, password, phone, address):
        self.execute_query("UPDATE stats SET customer_count = customer_count + 1 WHERE id = 1")
        id_num = self.execute_query("SELECT customer_count FROM stats")[0]
        self.execute_query("""INSERT INTO customers 
                              (id, first_name, last_name, email, password, phone, address)
                              VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                           (id_num, first_name, last_name, email, password, phone, address))

class Transaction(BankEntity):
    def deposit(self, account_id, branch_id, amount):
        self._perform_transaction(account_id, branch_id, amount, 'dep')

    def withdraw(self, account_id, branch_id, amount):
        self._perform_transaction(account_id, branch_id, amount, 'Withd')

    def _perform_transaction(self, account_id, branch_id, amount, transaction_type):
        self.execute_query("""INSERT INTO transactions 
                              (account_id, branch_id, type, amount)
                              VALUES (?, ?, ?, ?)""", 
                           (account_id, branch_id, transaction_type, amount))

        balance_change = amount if transaction_type == 'dep' else -amount
        self.execute_query("""UPDATE accounts 
                              SET balance = balance + ? 
                              WHERE id = ?""", 
                           (balance_change, account_id))

        self.execute_query("""UPDATE branches 
                              SET vault_balance = vault_balance + ?, 
                                  total_deposits = total_deposits + ? 
                              WHERE id = ?""", 
                           (balance_change, amount if transaction_type == 'dep' else 0, branch_id))

        self.execute_query("""UPDATE stats 
                              SET total_deposits = total_deposits + ?, 
                                  total_withdrawals = total_withdrawals + ?,
                                  total_vault_balance = total_vault_balance + ? 
                              WHERE id = 1""", 
                           (amount if transaction_type == 'dep' else 0,
                            amount if transaction_type == 'Withd' else 0,
                            balance_change))

class Bank:
    def __init__(self):
        self.branch = Branch()
        self.employee = Employee()
        self.customer = Customer()
        self.transaction = Transaction()

    def add_branch(self, name, address, phone):
        self.branch.add(name, address, phone)

    def add_employee(self, first_name, last_name, password, email, phone, job_title, salary, role, branch_id):
        self.employee.add(first_name, last_name, password, email, phone, job_title, salary, role, branch_id)

    def add_customer(self, first_name, last_name, email, password, phone, address):
        self.customer.add(first_name, last_name, email, password, phone, address)

    def deposit_to_branch(self, account_id, branch_id, amount):
        self.transaction.deposit(account_id, branch_id, amount)

    def withdraw_from_branch(self, account_id, branch_id, amount):
        self.transaction.withdraw(account_id, branch_id, amount)
    
    def display_selected_tables(self, selected_tables):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            
            for table_name in selected_tables:
                print(f"\n--- Table {table_name} ---")
                
                # الحصول على أسماء الأعمدة
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [column[1] for column in cursor.fetchall()]
                
                # طباعة أسماء الأعمدة
                print(" | ".join(columns))
                print("-" * (len(" | ".join(columns))))
                
                # الحصول على البيانات وطباعة النتائج
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                for row in rows:
                    print(" | ".join(map(str, row)))
                
                print(f"\nNumber of records in {table_name}: {len(rows)}")


    def display_all_tables(self):
            with DatabaseConnection() as conn:
                cursor = conn.cursor()
                
                # الحصول على قائمة بجميع الجداول
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                for table in tables:
                    table_name = table[0]
                    print(f"\n--- Table {table_name} ---")
                    
                    # Get column names
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = [column[1] for column in cursor.fetchall()]
                    
                    # Print column names
                    print(" | ".join(columns))
                    print("-" * (len(" | ".join(columns))))
                    
                    # Get and print data
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    for row in rows:
                        print(" | ".join(map(str, row)))
                    
                    print(f"\nNumber of records in {table_name}: {len(rows)}")

if __name__ == "__main__":
    bank = Bank()
    while True:
        print("\nChoose an operation:")
        print("1 - Add branch")
        print("2 - Add employee")
        print("3 - Add customer")
        print("4 - Deposit")
        print("5 - Withdraw")
        print("6 - Display all data")
        print("7 - Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter branch name: ")
            address = input("Enter branch address: ")
            phone = input("Enter branch phone: ")
            bank.add_branch(name, address, phone)
        elif choice == "2":
            first_name = input("Enter employee first name: ")
            last_name = input("Enter employee last name: ")
            password = input("Enter employee password: ")
            email = input("Enter employee email: ")
            phone = input("Enter employee phone: ")
            position = input("Enter employee position: ")
            salary = float(input("Enter employee salary: "))
            role = input("Enter employee role: ")
            branch_id = int(input("Enter branch ID: "))
            bank.add_employee(first_name, last_name, password, email, phone, position, salary, role, branch_id)
        elif choice == "3":
            first_name = input("Enter customer first name: ")
            last_name = input("Enter customer last name: ")
            email = input("Enter customer email: ")
            password = input("Enter customer password: ")
            phone = input("Enter customer phone: ")
            address = input("Enter customer address: ")
            bank.add_customer(first_name, last_name, email, password, phone, address)
        elif choice == "4":
            branch_id = int(input("Enter branch ID: "))
            customer_id = int(input("Enter customer ID: "))
            amount = float(input("Enter amount: "))
            bank.deposit_to_branch(branch_id, customer_id, amount)
        elif choice == "5":
            branch_id = int(input("Enter branch ID: "))
            customer_id = int(input("Enter customer ID: "))
            amount = float(input("Enter amount: "))
            bank.withdraw_from_branch(branch_id, customer_id, amount)
        elif choice == "6":
            bank.display_all_tables()
        elif choice == "7":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Try again.")
    
    
    # Examples of adding branches, employees, customers, deposits, and withdrawals
    #bank.add_branch("Main Branch", "123 Main St", "123-456-7890")
    #bank.add_employee("John", "Doe", "password123", "john.doe@example.com", "123-456-7890", "Manager", 50000, "Admin", 1)
    #bank.add_customer("Alice", "Smith", "alice.smith@example.com", "securepass", "987-654-3210", "456 Elm St")
    #bank.deposit_to_branch(1, 1, 1000.0)
    #bank.withdraw_from_branch(1, 1, 200.0)
    #bank.display_all_tables()