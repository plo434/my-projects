//using System;
//using System.IO;

//class Program
//{
//    static void Main()
//    {
//        // استلام معلومات الحساب من المستخدم
//        Console.WriteLine("Welcome to the Account Information Printing Program.");
        
//        Console.Write("Please enter the name of the account holder: ");
//        string accountHolder = null;
//        accountHolder = Console.ReadLine();

//        Console.Write("Please enter the account number: ");
//        string accountNumber = Console.ReadLine();

//        Console.Write("Please enter the account balance: ");
//        decimal accountBalance = decimal.Parse(Console.ReadLine());

//        Console.Write("Please enter the date of the operation: ");
//        DateTime transactionDate = DateTime.Parse(Console.ReadLine());

//        Console.Write("Please enter the name of the bank branch: ");
//        string bankName = Console.ReadLine();

//        Console.Write("Please enter the type of operation: ");
//        string transactionType = Console.ReadLine();

//        // إنشاء وفتح ملف للكتابة
//        string filePath = accountHolder+accountNumber+ ".txt";
//        using (StreamWriter writer = new StreamWriter(filePath))
//        {
//            // كتابة معلومات الحساب في الملف
//            writer.WriteLine("************************************");
//            writer.WriteLine("          معلومات الحساب          ");
//            writer.WriteLine("************************************");
//            writer.WriteLine("اسم صاحب الحساب: " + accountHolder);
//            writer.WriteLine("رقم الحساب: " + accountNumber);
//            writer.WriteLine("رصيد الحساب: " + accountBalance.ToString("C"));
//            writer.WriteLine("تاريخ العملية: " + transactionDate.ToString("dd/MM/yyyy"));
//            writer.WriteLine("اسم فرع البنك: " + bankName);
//            writer.WriteLine("نوع العملية: " + transactionType);
//            writer.WriteLine("************************************");
//        }

//        Console.WriteLine("تم طباعة معلومات الحساب وحفظها في الملف: " + filePath);
//    }
//}