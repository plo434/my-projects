import sqlite3 
def connect_db():
    return sqlite3.connect('bank_system.db')

def create_tables():
    with connect_db() as conn:
        cursor = conn.cursor()
        # جدول العملاء
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            first_name TEXT NOT NULL,
                            last_name TEXT NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            phone TEXT,
                            address TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        # جدول الحسابات
        cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            customer_id INTEGER,
                            account_type TEXT NOT NULL,
                            balance REAL DEFAULT 0.0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(customer_id) REFERENCES customers(id))''')

        # جدول المعاملات
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            account_id INTEGER,
                            type TEXT NOT NULL,
                            amount REAL,
                       branch_id INTEGER,
                            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(account_id) REFERENCES accounts(id))''')

        # جدول الفروع
        cursor.execute('''CREATE TABLE IF NOT EXISTS branches (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            address TEXT NOT NULL,
                            phone TEXT,
                            vault_balance REAL DEFAULT 0.0,  -- رصيد الخزنة
                            total_deposits REAL DEFAULT 0.0,  -- إجمالي الإيداعات
                            total_withdrawals REAL DEFAULT 0.0  -- إجمالي السحوبات
                          )''')

        # جدول القروض
        cursor.execute('''CREATE TABLE IF NOT EXISTS loans (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            customer_id INTEGER,
                            amount REAL NOT NULL,
                            interest_rate REAL NOT NULL,
                            duration INTEGER NOT NULL,  -- المدة بالاشهر
                            start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(customer_id) REFERENCES customers(id))''')

        # جدول البطاقات
        cursor.execute('''CREATE TABLE IF NOT EXISTS cards (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            account_id INTEGER,
                            card_type TEXT NOT NULL,  -- ائتمان أو خصم
                            card_number TEXT UNIQUE NOT NULL,
                            expiration_date TEXT NOT NULL,
                            cvv TEXT NOT NULL,
                            FOREIGN KEY(account_id) REFERENCES accounts(id))''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS employees  (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    job_title TEXT NOT NULL,  -- Corrected from jop_title to job_title
                    salary REAL DEFAULT 0.0,
                    role TEXT NOT NULL,
                    branch_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(branch_id) REFERENCES branches(id))''')
        # جدول الإحصائيات
        cursor.execute('''CREATE TABLE IF NOT EXISTS stats (
                            id INTEGER PRIMARY KEY CHECK (id = 1),  -- id يجب أن يكون دائمًا 1
                            branch_count INTEGER DEFAULT 1,
                            employee_count INTEGER DEFAULT 1,
                            customer_count INTEGER DEFAULT 1,
                            accounts_count INTEGER DEFAULT 1,
                       
    
                            total_deposits REAL DEFAULT 0.0,  -- إجمالي الإيداعات على مستوى البنك
                            total_withdrawals REAL DEFAULT 0.0,  -- إجمالي السحوبات على مستوى البنك
                            total_vault_balance REAL DEFAULT 0.0  -- إجمالي مبالغ الخزنات على مستوى البنك
                          )''')
         # إدخال سجل الإحصائيات الأول إذا لم يكن موجودًا
        cursor.execute('''INSERT OR IGNORE INTO stats (id, branch_count, employee_count, customer_count, total_deposits, total_withdrawals, total_vault_balance) 
                          VALUES (1, 0, 0, 0, 0.0, 0.0, 0.0)''')


if __name__ == "__main__":
    create_tables()