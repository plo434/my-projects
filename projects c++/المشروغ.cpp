#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include<cstdlib>
#include<map>
#include <iterator>
//#include "Source1.cpp"

using namespace std;
#define MIN_BALANCE 100
class deficient_funds {};
class Cl_Accounts
{
private:
	long Accnt_No;
	string client_fname;
	string client_lname;
	float client_balance;
	static long Nxt_Accnt_No;

public:
	Cl_Accounts() {}
	Cl_Accounts(string fname, string lname, float client_balance);
	long getAccNo() { return Accnt_No; }
	string getFName() { return client_fname; }
	string getLName() { return client_lname; }
	float getBlnce() { return client_balance; }
	void Deposit(float amount);
	void Withdraw(float amount);
	static void setLstAccntNo(long Accnt_No);
	static long getLstAccntNo();
	friend ofstream& operator<<(ofstream& ofs, Cl_Accounts& acc);
	friend ifstream& operator>>(ifstream& ifs, Cl_Accounts& acc);
	friend ostream& operator<<(ostream& os, Cl_Accounts& acc);
};
long Cl_Accounts::Nxt_Accnt_No = 0;

class Bank
{
private:
	map<long, Cl_Accounts> accounts_cl;
public:
	Bank();
	Cl_Accounts Cl_Open_Account(string fname, string lname, float balance);
	Cl_Accounts Cl_Balance_Enquiry(long Account_no);
	Cl_Accounts Deposit(long Account_no, float amt);
	Cl_Accounts Withdraw(long Account_no, float amt);
	void CloseAccount(long Account_no);
	void ShowAllAccounts();
	~Bank();
};
void jop2()
{
	string jop[11][2] = {

		"Generl Director","300000","Vice president","250000","Office Manager",
		"120000","Legal Affairs","250000","Cleaners","100000"
		,"Financial Officer","250000",
		"Receptionist","150000","Office clerk"
		,"20000","The guards","170000"
	   ,"Correspondents","120000" };

	for (int i = 0; i < 10; i++)
		cout << i + 1 << "-" << jop[i][0] << endl;
}
void jop(string& function, string& salery, int jp)
{
	string jop[11][2] = {

		"Generl Director","300000","Vice president","250000","Office Manager",
		"120000","Legal Affairs","250000","Cleaners","100000"
		,"Financial Officer","250000",
		"Receptionist","150000","Office clerk"
		,"20000","The guards","170000"
	   ,"Correspondents","120000" };

	cout << "****chose the jop\n****";

	function = jop[jp][0];
	salery = jop[jp][1];
}

string  Add(int i)
{
	string arr[8];
	arr[0] = "Enter the name";
	arr[1] = "Enter the ID_numbeur";
	arr[2] = "Enter the phone number";
	arr[3] = "Enter the function";
	arr[4] = "Enter the salary";
	arr[5] = "Enter the account_number";
	return arr[i];
}
void show1() {
	cout << "1-The salary:\n";
	cout << "2-Pay bills:\n";
	cout << "3-Customers account:\n";
	cout << "4-The informtion\n";
	cout << "\t\tChoose any othrt number to exit\n";
}
void salary() {
	cout << "1-Payment of salary:\n";
	cout << "2-Pay the salary:\n";
	cout << "0-To reurn to the previous menu\n";
	cout << "\t\tChoose any othrt number to exit\n";
}
void salary2() {
	cout << "1-Pay the salary in cash :\n";
	cout << "2-Pay the salary into the account:\n";
	cout << "0-To reurn to the previous menu\n";
	cout << "\t\tChoose any othrt number to exit\n";

}
void bills() {
	cout << "1-water Bills:\n";
	cout << "2-Electiricity Bills:\n";
	cout << "3-Phne Bills:\n";
	cout << "0-To reurn to the previous menu\n";
	cout << "\t\tChoose any othrt number to exit\n";
}

void account()
{
	cout << "\n\tSelect One Option Below ";
	cout << "\n\t1 Open an Account";
	cout << "\n\t2 Balance Enquiry";
	cout << "\n\t3 Deposit";
	cout << "\n\t4 Withdrawal";
	cout << "\n\t5 Close an Account";
	cout << "\n\t6 Show All Accounts";
	cout << "\n\t7 Quit";
	cout << "\t\tChoose any othrt number to exit\n";

}


void information()
{
	cout << "1-Adding  new employee data\n";
	cout << "2-Amenging  employee data\n ";
	cout << "3-Deleting  employee data\n ";
	cout << "0-To reurn to the previous menu\n";
	cout << "\t\tChoose any othrt number to exit\n";


}
void get_bill(string filname, int& line)
{
	ifstream file;
	file.open(filname);
	if (file.fail())
	{
		cout << "no\n";
	}
	vector<int> contents;
	while (!file.eof())
	{
		file >> line;
		contents.push_back(line);
	}
	file.close();
}

void pay_salary(int asd) {
	cout << "Enter the client'S ID:\n";

}

void add(string taxe)
{
	ofstream myfale;
	myfale.open("data.txt", ios::out | ios::app);
	myfale << taxe + "\n";
	myfale.close();
}
inline void ococo();
struct user {
	string username = "ali";
	int pasoerd = 1234;


}use;



void  clk(int mon, int& acc) {


	cout << "Enter 1 to confirm or any other number to cancel the operation\n";
	bool dr;
	cin >> dr;
	if (dr == true)
	{
		acc -= mon;

		cout << "The amount has been withdrawn successfully\n";
		cout << "Your remaining balance is\t :" << acc;
	}
}
void File(string txtt, string  all)
{
	string All = "data/" + all + ".txt";
	ofstream my;
	my.open(All, ios::app);
	my << txtt + "\n";
	my.close();
};
void File(int txtt, string  all)
{
	string All = "data/" + all + ".txt";

	ofstream my;
	my.open(All, ios::app);
	my << txtt + "\n";
	my.close();
};

void file_sarch(string line, string filename)
{
	ifstream my;
	my.open(filename);
	if (my.fail())
	{
		cout << "no\n";
	}
	int curtn_lin = 0;
	while (!my.eof())
	{
		curtn_lin++;
		getline(my, line);
		if (curtn_lin == 7)break;
		cout << line << endl;
	}
}
struct employee_information
{
	string  name;
	int ID_numbeur;
	int phone;
	string  salery;
	string function;
} employee;

int main()
{
	employee_information* ptr_em_inf = &employee;
	int id, plo;
	Bank b;
	Cl_Accounts acc;
	int option;
	string fname, lname, cinname;
	long account_no;
	float blnced;
	float amnts;
	string* allbill;
	int* chose, cinpasoerd;
	d:cout << "Enter the username\n";
		cin >> cinname;
		cout << "Enter the pasoerd \n";
		cin >> cinpasoerd;
		if (cinname != use.username && cinpasoerd != use.pasoerd)
		{

			cout << "                    The username or pasoerd is rong try agen\n";
			goto d;
			}

	chose = new int;
	do
	{

		show1();
		cin >> *chose;
		system("cls");
		switch (*chose)
		{
			delete chose;
			chose = new int;
		case 1:
		f:salary();
			cin >> *chose;
			system("cls");
			switch (*chose)
			{
				delete chose;

			case 1:
				cout << "jiouoio\n";

				break;
			case 2:
				salary2();
				cout << "chose the number \n ";
				chose = new int;
				cin >> *chose;
				system("cls");
				cout << "Enter the ID\n";
				string* id;
				allbill = new string;
				id = new string;
				cin.ignore();
				getline(cin, *id);
				int salary;
				*allbill = "salery/" + *id + ".txt";
				get_bill(*allbill, salary);
				cout << "your salery is:" << salary << endl;
				switch (*chose)
				{
				case 1:
					chose = new int;
					cout << "The amont is :" << salary << "\t1=yes , 0=no" << endl;
					cin >> *chose;
					if (*chose = 1)

					{
						cout << "Don";
					}
					else goto f;
					break;
				case 2:
					cout << "Enter Account Number:";
					cin >> account_no;
					cout << "The amont is :" << salary;
					acc = b.Deposit(account_no, salary);
					cout << endl << "Amount is Deposited" << endl;
					cout << acc;
					break;
				case 0:

					goto f;
					break;
				}

			}
			break;
		case 2:
			bills();
			delete chose;

			chose = new int;
			cin >> *chose;
			system("cls");
			switch (*chose)
			{
				delete chose;
			case 1:
				cout << "Enter your name from the bills\n";
				string* Bill;
				allbill = new string;
				Bill = new string;
				cin.ignore();
				getline(cin, *Bill);
				int bill;
				*allbill = "water/" + *Bill + ".txt";
				get_bill(*allbill, bill);
				cout << "your bill is:" << bill << endl;
				cout << "1-pay from accont\n2-pay a cach\n";
				chose = new int;
				cin >> *chose;
				system("cls");
				if (*chose == 2)
				{

					int pay;
				p:cout << "Enter the amount:";
				j:cin >> pay;
					if (pay > bill)
					{
						cout << "The amount is begger than the bill\tEnter the amount\n";

						goto j;
					}
					cout << "The amount is: " << pay << "\t1=yes , 0=no\n";
					chose = new int;
					cin >> *chose;
					system("cls");
					if (*chose == 1)
					{
						delete chose;
						bill -= pay;
						cout << "residual is:" << bill;
					}
					else

						goto p;
				}
				else if (*chose == 1)
				{
					cout << "Enter Account Number:";
					cin >> account_no;
					acc = b.Withdraw(account_no, bill);
					cout << endl << "Amount paed" << endl;
					cout << acc;
				}
				break;
			case 2:
				cout << "Enter your name from the bills\n";
				delete allbill;
				allbill = new string;
				delete Bill;
				Bill = new string;
				cin.ignore();
				getline(cin, *Bill);
				*allbill = "elctrin/" + *Bill + ".txt";
				get_bill(*allbill, bill);
				cout << "your bill is:" << bill << endl;
				cout << "1-pay from accont\n2-pay a cach\n";
				chose = new int;
				cin >> *chose;
				system("cls");
				if (*chose == 2)
				{

					int pay;
				s:cout << "Enter the amount:";
				r:cin >> pay;
					if (pay > bill)
					{
						cout << "The amount is begger than the bill\tEnter the amount\n";

						goto r;
					}
					cout << "The amount is: " << pay << "\t1=yes , 0=no\n";
					chose = new int;
					cin >> *chose;
					system("cls");
					if (*chose == 1)
					{
						delete chose;
						bill -= pay;
						cout << "residual is:" << bill;
					}
					else

						goto s;
				}
				else if (*chose == 1)
				{
					cout << "Enter Account Number:";
					cin >> account_no;
					acc = b.Withdraw(account_no, bill);
					cout << endl << "Amount paed" << endl;
					cout << acc;
				}


				break;
			case 3:
				string phone;
				allbill = new string;
				cout << "Enter your pone number\n";

				//cin.ignore();
				cin.ignore();
				//cin>>phone;
				getline(cin, phone);
				*allbill = "phone/" + phone + ".txt";

			u:cout << "Enter the amount:";
				int pay;
				cin >> pay;
				cout << "The amount is: " << pay << "\t1=yes , 0=no\n";
				chose = new int;
				cin >> *chose;
				system("cls");
				if (*chose == 1)
				{
					cout << "1-pay from accont\n2-pay a cach\n";
					delete chose;
					chose = new int;
					cin >> *chose;
					if (*chose == 2)
					{

						cout << "Payment don\n";
					}
					else if (*chose == 1)
					{
						cout << "Enter Account Number:";
						cin >> account_no;
						acc = b.Withdraw(account_no, pay);
						cout << endl << "Amount paed" << endl;
						cout << acc;
					}
					ofstream my;
					my.open(*allbill, ios::app);
					my << pay;
					my.close();
				}
				else goto u;



				break;

			}

			break;





			//الجساي 
		case 3:

			cout << "***Account Management System***" << endl;
			account();

			do
			{
				delete chose;
				chose = new int;
				cin >> *chose;
				switch (*chose)
				{
				case 1:
					cout << "Enter First Name: ";
					cin >> fname;
					cout << "Enter Last Name: ";
					cin >> lname;
					cout << "Enter Initial Balance: ";
					cin >> blnced;
					acc = b.Cl_Open_Account(fname, lname, blnced);
					cout << endl << "Congratulations Account is Created" << endl;
					cout << acc;
					break;
				case 2:
					cout << "Enter Account Number:";
					cin >> account_no;
					acc = b.Cl_Balance_Enquiry(account_no);
					cout << endl << "Your Account Details" << endl;
					cout << acc;
					break;
				case 3:
					cout << "Enter Account Number:";
					cin >> account_no;
					cout << "Enter Balance:";
					cin >> amnts;
					acc = b.Deposit(account_no, amnts);
					cout << endl << "Amount is Deposited" << endl;
					cout << acc;
					break;
				case 4:
					cout << "Enter Account Number:";
					cin >> account_no;
					cout << "Enter Balance:";
					cin >> amnts;
					acc = b.Withdraw(account_no, amnts);
					cout << endl << "Amount Withdrawn" << endl;
					cout << acc;
					break;
				case 5:
					cout << "Enter Account Number:";
					cin >> account_no;
					b.CloseAccount(account_no);
					cout << endl << "Account is Closed" << endl;
					cout << acc;
				case 6:
					b.ShowAllAccounts();
					break;
				case 7: break;
				default:
					cout << "\nEnter corret choice";
					exit(0);
				}


			} while (*chose != 7);

			break;
		el:case 4:
		fg:	information();
			chose = new int;
			cin >> *chose;
			cin.ignore();
			switch (*chose)
			{
			case 1:
				delete chose;
				cout << Add(0) << endl;
				getline(cin, ptr_em_inf->name);
				string all_name_file;

				cout << all_name_file;
				cout << Add(1) << endl;
				cin >> ptr_em_inf->ID_numbeur;

				cout << Add(2) << endl;
				cin >> ptr_em_inf->phone;

				cout << Add(3) << endl;
				jop2();
				chose = new int;
				cin >> *chose;
				jop(ptr_em_inf->function, ptr_em_inf->salery, *chose);

				delete chose;
				chose = new int;
				cout << "1-To add anether \n2-To show the informeshen\n";
				cin >> *chose;
				if (*chose == 2)


				{
					delete chose;
					cout << "\t*The informeshen abote new employee*\n";
					cout << "1-Name:" << ptr_em_inf->name << endl;
					cout << "2-ID :" << ptr_em_inf->ID_numbeur << endl;
					cout << "3-phone:" << ptr_em_inf->phone << endl;
					cout << "4-function:" << ptr_em_inf->function << endl;
					cout << "5-salre:" << ptr_em_inf->salery << endl;
					cout << "*DO you want to save them ( y=yes , n=no)\n";
					char* Chose;
					Chose = new char;
					cin >> *Chose;
					if (*Chose == 'y')
					{
						string namfile = "data/" + ptr_em_inf->name + ".txt";
						ofstream my;
						my.open(namfile, ios::app);
						my << ptr_em_inf->name + "\n";
						my << ptr_em_inf->ID_numbeur + "\n";
						my << ptr_em_inf->phone + "\n";
						my << ptr_em_inf->function + "\n";
						my << ptr_em_inf->salery + "\n";
						my.close();

					
					}
					else goto el;
				}
				else  if (*chose == 1)
				{
					delete chose;
					goto fg;
				}
				break;
			}

		}
		cout << "\n\tTO conct enter 1\n";
		cin >> plo;
	} while (plo == 1);
	return 0;

}
Cl_Accounts::Cl_Accounts(string fname, string lname, float client_balance)
{
	Nxt_Accnt_No++;
	Accnt_No = Nxt_Accnt_No;
	client_fname = fname;
	client_lname = lname;
	this->client_balance = client_balance;
}

void Cl_Accounts::Deposit(float amt)
{
	client_balance += amt;
}
void Cl_Accounts::Withdraw(float amt)
{
	if (client_balance - amt < MIN_BALANCE)
		throw deficient_funds();
	client_balance -= amt;
}
void Cl_Accounts::setLstAccntNo(long Accnt_No)
{
	Nxt_Accnt_No = Accnt_No;
}
long Cl_Accounts::getLstAccntNo()
{
	return Nxt_Accnt_No;
}
ofstream& operator<<(ofstream& ofs, Cl_Accounts& acc)
{
	ofs << acc.Accnt_No << endl;
	ofs << acc.client_fname << endl;
	ofs << acc.client_lname << endl;
	ofs << acc.client_balance << endl;
	return ofs;
}
ifstream& operator>>(ifstream& ifs, Cl_Accounts& acc)
{
	ifs >> acc.Accnt_No;
	ifs >> acc.client_fname;
	ifs >> acc.client_lname;
	ifs >> acc.client_balance;
	return ifs;
}
ostream& operator<<(ostream& os, Cl_Accounts& acc)
{
	os << "First Name:" << acc.getFName() << endl;
	os << "Last Name:" << acc.getLName() << endl;
	os << "Account Number:" << acc.getAccNo() << endl;
	os << "Balance:" << acc.getBlnce() << endl;
	return os;
}

Bank::Bank()
{
	Cl_Accounts acnt;
	ifstream infile;
	infile.open("Bank.data");
	if (!infile)
	{
		//cout<<"Error in Opening! File Not Found!!"<<endl;
		return;
	}
	while (!infile.eof())
	{
		infile >> acnt;
		accounts_cl.insert(pair<long, Cl_Accounts>(acnt.getAccNo(), acnt));
	}
	Cl_Accounts::setLstAccntNo(acnt.getAccNo());
	infile.close();
}
Cl_Accounts Bank::Cl_Open_Account(string fname, string lname, float balance)
{
	ofstream outfile;
	Cl_Accounts acnt(fname, lname, balance);
	accounts_cl.insert(pair<long, Cl_Accounts>(acnt.getAccNo(), acnt));
	outfile.open("Bank.data", ios::trunc);
	map<long, Cl_Accounts>::iterator itr;
	for (itr = accounts_cl.begin(); itr != accounts_cl.end(); itr++)
	{
		outfile << itr->second;
	}
	outfile.close();
	return acnt;
}
Cl_Accounts Bank::Cl_Balance_Enquiry(long Accnt_No)
{
	map<long, Cl_Accounts>::iterator itr = accounts_cl.find(Accnt_No);
	return itr->second;
}
Cl_Accounts Bank::Deposit(long Accnt_No, float amt)
{
	map<long, Cl_Accounts>::iterator itr = accounts_cl.find(Accnt_No);
	itr->second.Deposit(amt);
	return itr->second;
}
Cl_Accounts Bank::Withdraw(long Accnt_No, float amt)
{
	map<long, Cl_Accounts>::iterator itr = accounts_cl.find(Accnt_No);
	itr->second.Withdraw(amt);
	return itr->second;
}

void Bank::CloseAccount(long Accnt_No)
{
	map<long, Cl_Accounts>::iterator itr = accounts_cl.find(Accnt_No);
	cout << "Account Deleted" << itr->second;
	accounts_cl.erase(Accnt_No);
}

void Bank::ShowAllAccounts()
{
	map<long, Cl_Accounts>::iterator itr;
	for (itr = accounts_cl.begin(); itr != accounts_cl.end(); itr++)
	{
		cout << "Account " << itr->first << endl << itr->second << endl;
	}
}

Bank::~Bank()
{
	ofstream outfile;
	outfile.open("Bank.data", ios::trunc);
	map<long, Cl_Accounts>::iterator itr;
	for (itr = accounts_cl.begin(); itr != accounts_cl.end(); itr++)
	{
		outfile << itr->second;
	}
	outfile.close();
}
