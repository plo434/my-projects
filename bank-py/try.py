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

    def update_stat(self, stat_column):
        self.execute_query(f"UPDATE stats SET {stat_column} = {stat_column} + 1 WHERE id = 1")
        return self.execute_query(f"SELECT {stat_column} FROM stats WHERE id = 1")[0]

class Branch(BankEntity):
    def add(self, name, address, phone):
        branch_id = self.update_stat('branch_count')
        self.execute_query("INSERT INTO branches (id, name, address, phone) VALUES (?, ?, ?, ?)",
                           (branch_id, name, address, phone))

class Employee(BankEntity):
    def add(self, first_name, last_name, password, email, phone, job_title, salary, role, branch_id):
        employee_id = self.update_stat('employee_count')
        self.execute_query("""INSERT INTO employees 
                              (id, first_name, last_name, password, email, phone, job_title, salary, role, branch_id)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           (employee_id, first_name, last_name, password, email, phone, job_title, salary, role, branch_id))

class Customer(BankEntity):
    def add(self, first_name, last_name, email, password, phone, address):
        customer_id = self.update_stat('customer_count')
        self.execute_query("""INSERT INTO customers 
                              (id, first_name, last_name, email, password, phone, address)
                              VALUES (?, ?, ?, ?, ?, ?, ?)""",
                           (customer_id, first_name, last_name, email, password, phone, address))

class Transaction(BankEntity):
    def deposit(self, account_id, branch_id, amount):
        self._perform_transaction(account_id, branch_id, amount, 'dep')
       
    def withdraw(self, account_id, branch_id, amount):
        if self.get_account_balance(account_id) < amount:
            raise ValueError("رصيد الحساب غير كافٍ لإجراء هذه العملية")

        if amount > self.get_branch_vault_balance(branch_id) / 2:
            raise ValueError("المبلغ المطلوب سحبه يتجاوز الحد المسموح به للفرع")

        self._perform_transaction(account_id, branch_id, amount, 'Withd')
    
    def transfer(self, from_account_id, to_account_id, amount):
        from_account_balance = self.get_account_balance(from_account_id)
        
        if from_account_balance < amount:
            raise ValueError("رصيد الحساب غير كافٍ لإجراء هذه العملية")
        
        if not self.account_exists(to_account_id):
            raise ValueError("الحساب المستهدف غير موجود")

        # خصم المبلغ من الحساب الأول
        self._perform_transaction(from_account_id, None, amount, 'Withd')

        # إضافة المبلغ إلى الحساب الثاني
        self._perform_transaction(to_account_id, None, amount, 'dep')
    
    def account_exists(self, account_id):
        result = self.execute_query("""SELECT id FROM accounts WHERE id = ?""", (account_id,))

        return result is not None

    def transfer_money(self, from_account_id, to_account_id, amount):
        from_account = self.transaction.get_account_balance(from_account_id)
        to_account = self.transaction.get_account_balance(to_account_id)

        if from_account is not None and to_account is not None:
            try:
                self.transaction.withdraw(from_account_id, self.branch_id, amount)
                self.transaction.deposit(to_account_id, self.branch_id, amount)
                print("تم تحويل الأموال بنجاح.")
            except ValueError as e:
                print(f"Error: {e}")
        else:
            if from_account is None:
                self._register_new_customer_for_transfer(from_account_id, "sender")

            if to_account is None:
                self._register_new_customer_for_transfer(to_account_id, "receiver")

            print("تم تسجيل بيانات المرسل أو المستلم كعميل جديد، لأن الحساب غير موجود.")
    
    def _register_new_customer_for_transfer(self, account_id, role):
        print(f"Creating a new customer for the {role}.")
        first_name = input(f"Enter {role} first name: ")
        last_name = input(f"Enter {role} last name: ")
        email = input(f"Enter {role} email: ")
        password = input(f"Enter {role} password: ")
        phone = input(f"Enter {role} phone: ")
        address = input(f"Enter {role} address: ")
        self.add_customer(first_name, last_name, email, password, phone, address)

    def _perform_transaction(self, account_id, branch_id, amount, transaction_type):
        self.execute_query("""INSERT INTO transactions 
                              (account_id, branch_id, type, amount)
                              VALUES (?, ?, ?, ?)""",
                           (account_id, branch_id, transaction_type, amount))

        balance_change = amount if transaction_type == 'dep' else -amount
        self.execute_query("""UPDATE accounts SET balance = balance + ? WHERE id = ?""",
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

class Account(BankEntity):
    def add(self, customer_id, account_type, balance=0):
        account_id = self.update_stat('accounts_count')
        self.execute_query("""INSERT INTO accounts 
                              (id, customer_id, account_type, balance)
                              VALUES (?, ?, ?, ?)""",
                           (account_id, customer_id, account_type, balance))

class BankManager:
    def __init__(self):
        self.branch = Branch()
        self.employee = Employee()
        self.customer = Customer()
        self.account = Account()

    def add_branch(self, name, address, phone):
        self.branch.add(name, address, phone)

    def add_employee(self, first_name, last_name, password, email, phone, job_title, salary, role, branch_id):
        self.employee.add(first_name, last_name, password, email, phone, job_title, salary, role, branch_id)

    def delete_branch(self, branch_id):
        self.branch.delete(branch_id)

    def delete_employee(self, employee_id):
        self.employee.delete(employee_id)

    def delete_customer(self, customer_id):
        self.customer.delete(customer_id)

    def delete_account(self, account_id):
        self.account.delete(account_id)

    def display_selected_tables(self, selected_tables):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            for table_name in selected_tables:
                print(f"\n--- Table {table_name} ---")
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [column[1] for column in cursor.fetchall()]
                print(" | ".join(columns))
                print("-" * (len(" | ".join(columns))))
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                for row in rows:
                    print(" | ".join(map(str, row)))
                print(f"\nNumber of records in {table_name}: {len(rows)}")

    def display_all_tables(self):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            self.display_selected_tables([table[0] for table in tables])
class BranchManager:
    def __init__(self, branch_id):
        self.branch_id = branch_id
        self.customer = Customer()
        self.transaction = Transaction()
        self.accounts = Account()

    def add_customer(self, first_name, last_name, email, password, phone, address):
        self.customer.add(first_name, last_name, email, password, phone, address)

    def delete_customer(self, customer_id):
        self.customer.delete(customer_id)

    def add_account(self, customer_id, account_type):
        self.accounts.add(customer_id, account_type)

    def delete_account(self, account_id):
        self.accounts.delete(account_id)

    def deposit_to_branch(self, account_id, amount):
        self.transaction.deposit(account_id, self.branch_id, amount)

    def withdraw_from_branch(self, account_id, amount):
        self.transaction.withdraw(account_id, self.branch_id, amount)

    def transfer_between_accounts(self, from_account_id, to_account_id, amount):
        self.transaction.transfer(from_account_id, to_account_id, amount)

class Authentication(BankEntity):
    def verify_user(self, email, password):
        with self.db_connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, role, branch_id FROM employees WHERE email = ? AND password = ?", 
                           (email, password))
            result = cursor.fetchone()
            if result:
                user_id, role, branch_id = result
                return role, branch_id
            else:
                raise ValueError("بيانات الدخول غير صحيحة")
    
        
if __name__ == "__main__":
    auth = Authentication()

    try:
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        role, branch_id = auth.verify_user(email, password)

        if role == "Admin":
            bank = BankManager()
            while True:
                print("\nChoose an operation:")
                print("1 - Add branch")
                print("2 - Add employee")
                print("3 - Delete branch")
                print("4 - Delete employee")
                print("5 - Delete customer")
                print("6 - Delete account")
                print("7 - Display all data")
                print("8 - Exit")

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
                    branch_id = int(input("Enter branch ID to delete: "))
                    bank.delete_branch(branch_id)
                elif choice == "4":
                    employee_id = int(input("Enter employee ID to delete: "))
                    bank.delete_employee(employee_id)
                elif choice == "5":
                    customer_id = int(input("Enter customer ID to delete: "))
                    bank.delete_customer(customer_id)
                elif choice == "6":
                    account_id = int(input("Enter account ID to delete: "))
                    bank.delete_account(account_id)
                elif choice == "7":
                    bank.display_all_tables()
                elif choice == "8":
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif role == "employee":
            branch_manager = BranchManager(branch_id)
            while True:
                print("\nChoose an operation:")
                print("1 - Add customer")
                print("2 - Delete customer")
                print("3 - Add account")
                print("4 - Delete account")
                print("5 - Deposit to branch")
                print("6 - Withdraw from branch")
                print("7 - Transfer between accounts")
                print("8 - Exit")

                choice = input("Enter your choice: ")

                if choice == "1":
                    first_name = input("Enter customer first name: ")
                    last_name = input("Enter customer last name: ")
                    email = input("Enter customer email: ")
                    password = input("Enter customer password: ")
                    phone = input("Enter customer phone: ")
                    address = input("Enter customer address: ")
                    branch_manager.add_customer(first_name, last_name, email, password, phone, address)
                elif choice == "2":
                    customer_id = int(input("Enter customer ID to delete: "))
                    branch_manager.delete_customer(customer_id)
                elif choice == "3":
                    customer_id = int(input("Enter customer ID: "))
                    account_type = input("Enter account type: ")
                    branch_manager.add_account(customer_id, account_type)
                elif choice == "4":
                    account_id = int(input("Enter account ID to delete: "))
                    branch_manager.delete_account(account_id)
                elif choice == "5":
                    account_id = int(input("Enter account ID: "))
                    amount = float(input("Enter amount to deposit: "))
                    branch_manager.deposit_to_branch(account_id, amount)
                elif choice == "6":
                    account_id = int(input("Enter account ID: "))
                    amount = float(input("Enter amount to withdraw: "))
                    branch_manager.withdraw_from_branch(account_id, amount)
                elif choice == "7":
                    from_account_id = int(input("Enter from account ID: "))
                    to_account_id = int(input("Enter to account ID: "))
                    amount = float(input("Enter amount to transfer: "))
                    branch_manager.transfer_between_accounts(from_account_id, to_account_id, amount)
                elif choice == "8":
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Unauthorized role.")
    except ValueError as e:
        print(f"Error: {e}")