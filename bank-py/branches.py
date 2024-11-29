from db import connect_db


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

# مثال لاسترجاع رصيد الخزنة للفرع رقم 1
vault_balance = get_branch_vault_balance(1)
print(f"The vault balance for branch 1 is: {vault_balance}")
