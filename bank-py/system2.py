from db import connect_db
from system import DatabaseConnection

def increment_employee_count():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE stats SET employee_count = employee_count + 1 WHERE id = 1''')
        conn.commit()

def increment_customer_count():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE stats SET customer_count = customer_count + 1 WHERE id = 1''')
        conn.commit()

def add_branch(name, address, phone):
    with connect_db() as conn:
        cursor = conn.cursor()

        # إضافة فرع جديد
        cursor.execute('''UPDATE stats SET branch_count = branch_count + 1 WHERE id = 1''')
        id_num=cursor.execute('''SELECT branch_count FROM stats''')
        conn.commit()

        cursor.execute('''INSERT INTO branches (id,name,address,phone) 
                          VALUES (?,?,?,?)''', (id_num,name,address,phone))
        conn.commit()
        # زيادة عدد الفروع في جدول الإحصائيات
       

def add_employee(first_name, last_name, password, email, phone, job_title, salary, role, branch_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE stats SET employee_count = employee_count + 1 WHERE id = 1''')
        id_num=cursor.execute('''SELECT employee_count FROM stats''')
        conn.commit()
        # إضافة الموظف إلى جدول الموظفين
        cursor.execute('''INSERT INTO employees 
                          (id,first_name, last_name, password, email, phone, job_title, salary, role, branch_id)
                          VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (id_num,first_name, last_name, password, email, phone, job_title, salary, role, branch_id))

        conn.commit()

        # زيادة عدد الموظفين في جدول الإحصائيات
       

def add_customer(first_name, last_name, email, password, phone, address):
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute('''UPDATE stats SET customer_count = customer_count + 1 WHERE id = 1''')
        id_num=cursor.execute('''SELECT customer_count FROM stats''')
        conn.commit()
        # إضافة العميل إلى جدول العملاء
        cursor.execute('''INSERT INTO customers 
                          (id,first_name, last_name, email, password, phone, address)
                          VALUES (?,?, ?, ?, ?, ?, ?)''', 
                       (id_num,first_name, last_name, email, password, phone, address))
        conn.commit()

        # زيادة عدد العملاء في جدول الإحصائيات
     

def deposit_to_branch(account_id, branch_id, amount):
    with connect_db() as conn:
        cursor = conn.cursor()

        # إضافة معاملة إيداع
        cursor.execute('''INSERT INTO transactions 
                          (account_id, branch_id, type, amount)
                          VALUES (?, ?, 'dep', ?)''', 
                       (account_id, branch_id, amount))

        # تحديث رصيد الحساب
        cursor.execute('''UPDATE accounts 
                          SET balance = balance + ? 
                          WHERE id = ?''', 
                       (amount, account_id))

        # تحديث رصيد الخزنة في الفرع المحدد
        cursor.execute('''UPDATE branches 
                          SET vault_balance = vault_balance + ?, 
                              total_deposits = total_deposits + ? 
                          WHERE id = ?''', 
                       (amount, amount, branch_id))

        # تحديث إجمالي الإيداعات في جدول الإحصائيات
        cursor.execute('''UPDATE stats 
                          SET total_deposits = total_deposits + ?, 
                              total_vault_balance = total_vault_balance + ? 
                          WHERE id = 1''', 
                       (amount, amount))

        conn.commit()

def withdraw_from_branch(account_id, branch_id, amount):
    with connect_db() as conn:
        cursor = conn.cursor()

        # إضافة معاملة سحب
        cursor.execute('''INSERT INTO transactions 
                          (account_id, branch_id, type, amount)
                          VALUES (?, ?, 'Withd', ?)''', 
                       (account_id, branch_id, amount))

        # تحديث رصيد الحساب
        cursor.execute('''UPDATE accounts 
                          SET balance = balance - ? 
                          WHERE id = ?''', 
                       (amount, account_id))

        # تحديث رصيد الخزنة في الفرع المحدد
        cursor.execute('''UPDATE branches 
                          SET vault_balance = vault_balance - ?, 
                              total_withdrawals = total_withdrawals + ? 
                          WHERE id = ?''', 
                       (amount, amount, branch_id))

        # تحديث إجمالي السحوبات في جدول الإحصائيات
        cursor.execute('''UPDATE stats 
                          SET total_withdrawals = total_withdrawals + ?, 
                              total_vault_balance = total_vault_balance - ? 
                          WHERE id = 1''', 
                       (amount, amount))

        conn.commit()


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
if __name__ == "__main__":
    # أمثلة لإضافة الفروع، الموظفين، العملاء، الإيداع، والسحب
    add_branch("Main Branch", "123 Main St", "123-456-7890")
    add_employee("John", "Doe", "password123", "john.doe@example.com", "123-456-7890", "Manager", 50000, "Admin", 1)
    add_customer("Alice", "Smith", "alice.smith@example.com", "securepass", "987-654-3210", "456 Elm St")
    deposit_to_branch(1, 1, 1000.0)
    withdraw_from_branch(1, 1, 200.0)
