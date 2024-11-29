


//



//using System;
//using System.Collections.Generic;
//using System.Data.SqlClient;

//class TYp
//{
//   public static void Mainn()
//    {
//        string connectionString = "Data Source=(local);Initial Catalog=BankDB;Integrated Security=True";

//        using (SqlConnection connection = new SqlConnection(connectionString))
//        {
//            connection.Open();

//            BankDataRepository repository = new BankDataRepository(connection);

//            // إنشاء جدول لبيانات العملاء إذا لم يكن موجودًا بالفعل
//            repository.CreateBankDataTable();

//            // حفظ بيانات العملاء في قاعدة البيانات
//            List<BankData> bankDataList = new List<BankData>
//            {
//                new BankData("123456789", "محمد علي", 5000.00m),
//                new BankData("987654321", "أحمد خالد", 10000.00m),
//                new BankData("456789123", "سارة أحمد", 7500.00m)
//            };
//            repository.SaveBankData(bankDataList);

//            // قراءة بيانات العملاء من قاعدة البيانات
//            List<BankData> loadedBankDataList = repository.ReadBankData();

//            // عرض بيانات العملاء
//            foreach (BankData bankData in loadedBankDataList)
//            {
//                Console.WriteLine("رقم الحساب: " + bankData.AccountNumber);
//                Console.WriteLine("صاحب الحساب: " + bankData.AccountHolder);
//                Console.WriteLine("الرصيد: " + bankData.Balance.ToString("C"));
//                Console.WriteLine();
//            }

//            // البحث عن بيانات عميل معين
//            string accountNumberToSearch = "987654321";
//            BankData searchedBankData = repository.SearchBankData(accountNumberToSearch);

//            if (searchedBankData != null)
//            {
//                Console.WriteLine("تم العثور على بيانات العميل:");
//                Console.WriteLine("رقم الحساب: " + searchedBankData.AccountNumber);
//                Console.WriteLine("صاحب الحساب: " + searchedBankData.AccountHolder);
//                Console.WriteLine("الرصيد: " + searchedBankData.Balance.ToString("C"));
//            }
//            else
//            {
//                Console.WriteLine("لم يتم العثور على بيانات العميل.");
//            }
//        }
//    }
//}

//class BankData
//{
//    public string AccountNumber { get; set; }
//    public string AccountHolder { get; set; }
//    public decimal Balance { get; set; }

//    public BankData(string accountNumber, string accountHolder, decimal balance)
//    {
//        AccountNumber = accountNumber;
//        AccountHolder = accountHolder;
//        Balance = balance;
//    }
//}

//class BankDataRepository
//{
//    private SqlConnection _connection;

//    public BankDataRepository(SqlConnection connection)
//    {
//        _connection = connection;
//    }

//    public void CreateBankDataTable()
//    {
//        string createTableQuery = "CREATE TABLE IF NOT EXISTS BankData (AccountNumber VARCHAR(50), AccountHolder VARCHAR(100), Balance DECIMAL(18, 2))";
//        using (SqlCommand command = new SqlCommand(createTableQuery, _connection))
//        {
//            command.ExecuteNonQuery();
//        }
//    }

//    public void SaveBankData(List<BankData> bankDataList)
//    {
//        foreach (BankData bankData in bankDataList)
//        {
//            string insertQuery = "INSERT INTO BankData (AccountNumber, AccountHolder, Balance) VALUES (@AccountNumber, @AccountHolder, @Balance)";
//            using (SqlCommand command = new SqlCommand(insertQuery, _connection))
//            {
//                command.Parameters.AddWithValue("@AccountNumber", bankData.AccountNumber);
//                command.Parameters.AddWithValue("@AccountHolder", bankData.AccountHolder);
//                command.Parameters.AddWithValue("@Balance", bankData.Balance);
//                command.ExecuteNonQuery();
//            }
//        }

//        Console.WriteLine("تم حفظ بيانات البنك في قاعدة البيانات.");
//    }

//    public List<BankData> ReadBankData()
//    {
//        List<BankData> bankDataList = new List<BankData>();

//        string selectQuery = "SELECT AccountNumber, AccountHolder, Balance FROM BankData";
//        using (SqlCommand command = new SqlCommand(selectQuery, _connection))
//        {
//            using (SqlDataReader reader = command.ExecuteReader())
//            {
//                while (reader.Read())
//                {
//                    string accountNumber = reader.GetString(0);
//                    string accountHolder = reader.GetString(1);
//                    decimal balance = reader.GetDecimal(2);

//                    bankDataList.Add(new BankData(accountNumber, accountHolder, balance));
//                }
//            }
//        }

//        return bankDataList;
//    }

//    public BankData SearchBankData(string accountNumber)
//    {
//        List<BankData> bankDataList = ReadBankData();

//        foreach (BankData bankData in bankDataList)
//        {
//            if (bankData.AccountNumber == accountNumber)
//            {
//                return bankData;
//            }
//        }

//        return null;
//    }
//}