from system import BankEntity
import inspect

methods = inspect.getmembers(BankEntity, predicate=inspect.isfunction)

for method in methods:
    print(method[0])
class User:
    def __init__(self, name, role):
        self.name = name 
        self.role = role


def check_access(user, required_role):
    
    if user.role == required_role:
        return True
    elif user.role == 'admin':
        return True
    else:
        return False


class Branches :
    def deposit_to_branch(branch_id, amount):
        with connect_db() as conn:
            cursor = conn.cursor()
            # تحديث رصيد الخزنة في الفرع المحدد
            
            cursor.execute('''UPDATE branches 
                            SET vault_balance = vault_balance + ? 
                            WHERE id = ?''', 
                        (amount, branch_id))
            conn.commit()

# مثال على إيداع مبلغ في خزنة الفرع رقم 1
deposit_to_branch(1, 1000.0)


def get_branch_vault_balance(branch_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT vault_balance FROM branches WHERE id = ?''', (branch_id,))
        balance = cursor.fetchone()
        return balance[0] if balance else None
    





    class Transaction(BankEntity):
    def deposit(self, account_id, branch_id, amount):
        self._perform_transaction(account_id, branch_id, amount, 'dep')

    def withdraw(self, account_id, branch_id, amount):
        # التحقق من توفر المبلغ في رصيد العميل
        account_balance = self.get_account_balance(account_id)
        if account_balance < amount:
            raise ValueError("رصيد الحساب غير كافٍ لإجراء هذه العملية")

        # التحقق من أن المبلغ المراد سحبه أقل من نصف مبلغ خزينة الفرع
        branch_vault_balance = self.get_branch_vault_balance(branch_id)
        if amount > branch_vault_balance / 2:
            raise ValueError("المبلغ المطلوب سحبه يتجاوز الحد المسموح به للفرع")

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

    def get_account_balance(self, account_id):
        result = self.execute_query("""SELECT balance FROM accounts WHERE id = ?""", (account_id,))
        return result[0][0] if result else 0

    def get_branch_vault_balance(self, branch_id):
        result = self.execute_query("""SELECT vault_balance FROM branches WHERE id = ?""", (branch_id,))
        return result[0][0] if result else 0