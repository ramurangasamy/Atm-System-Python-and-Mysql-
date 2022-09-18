from tabulate import tabulate
import mysql.connector
con = mysql.connector.connect(
  host="localhost",
  user="root",
  password="priyaramu",
  database="banking_system"
)
res=con.cursor()

# Mysql Query:
"""
create database banking_system;
use banking_system; 
CREATE TABLE bank (
	id	int primary key auto_increment,
	username varchar(52) NOT NULL UNIQUE,
	pin	int NOT NULL,
	amount	float NOT NULL DEFAULT 1252.00,
	phone	long NOT NULL,
	email	varchar(120),
	address	varchar(225) NOT NULL
);
"""

def create_new_user(name,phone,mail,address):
    sql="insert into bank(username,phone,email,address) values(%s,%s,%s,%s)"
    data=(name,phone,mail,address)
    res.execute(sql,data)
    con.commit()
    print(f"New User {name} Createdd Successfully")

def delete_user(id):
    sql="select id from bank where id=%s"
    res.execute(sql,(id,))
    check_data=res.fetchone()
    if check_data is None:
        print("Customer ID Not Found")
    else:
        sql_del_query="delete from bank where id=%s"
        res.execute(sql_del_query,(id,))
        con.commit()
        print(f"Customer {id} Deleted Successfully")

def show_customers():
    sql="select id,username,amount,phone,email,address from bank"
    res.execute(sql)
    result=res.fetchall()
    print(tabulate(result,headers=["ID","USERNAME","AMOUNT","PHONE","EMAIL","ADDRESS"]))

def update_customer(name,phone,mail,address,id):
    sql="select id from bank where id=%s"
    res.execute(sql,(id,))
    check_data=res.fetchone()
    if check_data is None:
        print("Customer ID Not Found")
    else:
        sql_update_query="update bank set username=%s,phone=%s,email=%s,address=%s where id=%s"
        data=(name,phone,mail,address,id)
        res.execute(sql_update_query,data)
        con.commit()
        print(f"Customer {id} Updated Successfully")

def change_pin(id):
    sql="select id from bank where id=%s"
    data=(id,)
    res.execute(sql,data)
    check_data=res.fetchone()
    if check_data is None:
        print("Customer ID Not Found")
    else:
        new_pin=int(input("Enter New Pin : "))
        c_pin_sql="update bank set pin=%s where id=%s"
        c_data=(new_pin,id)
        res.execute(c_pin_sql,c_data)
        con.commit()
        print(f"Customer Pin Updated Successfully")

def deposit_initial():
    id=int(input("Enter Customer ID : "))
    sql_query="select id from bank where id=%s"
    res.execute(sql_query,(id,))
    check_data=res.fetchone()
    if check_data is not None:
        pin=int(input("Enter Pin Number : "))
        sql_query_pin="select pin,amount from bank where id=%s"
        res.execute(sql_query_pin,(id,))
        check_pin_data=res.fetchone()
        previous_bal=check_pin_data[1]
        if(int(check_pin_data[0])==pin):
            deposit(previous_bal,id)
        else:
            print("Wrong Pin! Enter Right Pin")
    else:
        print("Customer ID Doesn't Found")
   
def deposit(previous_bal,id):
    money=float(input("Enter Ammount To Deposit : "))
    money+=previous_bal
    sql_money_query="update bank set amount=%s where id=%s"
    res.execute(sql_money_query,(money,id))
    con.commit()
    if money is not None:
        sql_money_bal="select amount from bank where id=%s"
        res.execute(sql_money_bal,(id,))
        acc_bal=res.fetchone()
        print(f"Your Account Balance : {float(acc_bal[0])} ")
    else:
        print("Something Went Wrong! Try Again")
   
def withdraw_initial():
    id=int(input("Enter Customer ID : "))
    sql_query="select id from bank where id=%s"
    res.execute(sql_query,(id,))
    check_data=res.fetchone()
    if check_data is not None:
        pin=int(input("Enter Pin Number : "))
        sql_query_pin="select pin,amount from bank where id=%s"
        res.execute(sql_query_pin,(id,))
        check_pin_data=res.fetchone()
        previous_bal=check_pin_data[1]
        if(int(check_pin_data[0])==pin):
            withdraw(previous_bal,id)
        else:
            print("Wrong Pin! Enter Right Pin")
    else:
        print("Customer ID Doesn't Found")

def withdraw(previous_bal,id):
    money=float(input("Enter Ammount To Withdraw : "))
    previous_bal-=money
    sql_money_query="update bank set amount=%s where id=%s"
    res.execute(sql_money_query,(previous_bal,id))
    con.commit()
    if money is not None:
        sql_money_bal="select amount from bank where id=%s"
        res.execute(sql_money_bal,(id,))
        acc_bal=res.fetchone()
        print(f"Your Account Balance : {float(acc_bal[0])} ")
    else:
        print("Something Went Wrong! Try Again")

def check_balance(id):
    sql="select id from bank where id=%s"
    data=(id,)
    res.execute(sql,data)
    check_data=res.fetchone()
    if check_data is None:
        print("Customer ID Not Found")
    else:
        sql_bal="select pin,amount from bank where id=%s"
        data1=(id,)
        res.execute(sql_bal,data1)
        check_data1=res.fetchone()
        u_pin=int(input("Enter Your Pin : "))
        if(check_data1[0]==u_pin):
            print(f"Your Balance Amount : Rs.{check_data1[1]}")
        else:
            print("Something Went Wrong! Try Again")

def send_money():
    pass

def show_my_account_initial():
    user=int(input("Enter Customer ID : "))
    sql_query="select id,pin from bank where id=%s"
    res.execute(sql_query,(user,))
    check_data=res.fetchone()
    if check_data is not None:
        pin=int(input("Enter Pin Number : "))
        if(int(check_data[1])==pin):
            show_my_account(user)
        else:
            print("Wrong Pin! Enter Right Pin")
    else:
        print("Customer ID Doesn't Found! ")

def show_my_account(id):
    sql="select id,username,pin,amount,phone,email,address from bank where id=%s"
    res.execute(sql,(id,))
    result=res.fetchall()
    print('\n')
    print(f"Welcome Mr/Ms/Mrs {result[0][1]},")
    print("-------------------------------------------------------------------------------------")
    print(tabulate(result,headers=["ID","USERNAME","PIN","AMOUNT","PHONE","EMAIL","ADDRESS"]))
    print("--------------------------------------------------------------------------------------")

def send_money_initial():
    id=int(input("Enter Your ID : "))
    sql="select id from bank where id=%s"
    data=(id,)
    res.execute(sql,data)
    check_data=res.fetchone()
    if check_data is None:
        print("Customer ID Not Found")
    else:
        sql_bal="select pin,amount from bank where id=%s"
        data1=(id,)
        res.execute(sql_bal,data1)
        check_data1=res.fetchone()
        # print(check_data1)
        u_pin=int(input("Enter Your Pin : "))
        if(check_data1[0]==u_pin):
            trans_amount=float(input("Enter Amount To Send : "))
            if(trans_amount<=check_data1[1]):
                send_money(trans_amount,check_data1[1],id)
            else:
                print(f"You Don't Have Enough Money To Make Transactions! Your Account Balance is Rs.{check_data1[1]}")
        else:
            print("Wrong Pin! Try Again")

def send_money(trans_amount,acc_bal,id):
    id1=int(input("Enter Recepient ID : "))
    sql="select id,amount from bank where id=%s"
    res.execute(sql,(id1,))
    check_data=res.fetchone()
    # print(check_data[0])
    if check_data is None:
        print("Customer ID Not Found")
    else:
        sql_bal_sender="update bank set amount=%s where id=%s"
        after_trans_bal_sender=acc_bal-trans_amount
        res.execute(sql_bal_sender,(after_trans_bal_sender,id))
        con.commit()
        sql_bal_rec="update bank set amount=%s where id=%s"
        after_trans_bal_rec=check_data[1]+trans_amount
        res.execute(sql_bal_rec,(after_trans_bal_rec,id1))
        con.commit()
        print("Transaction Completed Successfully!")
        
g_ch="""
1.Normal Users
2.Bank Users
3.Exit
"""
nu_ch="""
0.My Account
1.Check Balance
2.Change Pin
3.Deposit
4.Withdraw
5.Send Money
6.Exit
"""
bu_ch="""
0.My Account
1.Create Customers
2.Update Customer Details
3.List Customers Details
4.Delete Customers
5.Check Balance
6.Change Pin
7.Deposit
8.Withdraw
9.Send Money
10.Exit
"""

print(g_ch)
ch=int(input("Enter Your Choice : "))
if (ch==1):
    while True:
        print(nu_ch)
        ch1=int(input("Enter Your Choice : "))
        if(ch1==0):
            show_my_account_initial()
        elif(ch1==1):
            id=int(input("Enter Your ID : "))
            check_balance(id)
        elif(ch1==2):
            id=int(input("Enter Customer ID : "))
            change_pin(id)
        elif(ch1==3):
            deposit_initial()
        elif(ch1==4):
            withdraw_initial()
        elif(ch1==5):
            send_money_initial()
        elif(ch1==6):
            exit()
        else:
            print("Something Went Wrong! Try Again")
elif(ch==2):
    while True:
        print(bu_ch)
        ch2=int(input("Enter Your Choice : "))
        if(ch2==0):
            show_my_account_initial()
        elif(ch2==1):
            user=input("Enter New Customer Name : ")
            sql_query="select username from bank where username=%s"
            res.execute(sql_query,(user,))
            check_data=res.fetchone()
            if check_data is None:
                phone=int(input("Enter Phone Number : "))
                email=input("Enter Mail Address : ")
                address=input("Enter Address : ")
                create_new_user(user,phone,email,address)
            else:
                print("--------------------------------------------------------------------")
                print("Username Already Exists! Try Something Else Username Must Be Uniuqe")  
                print("--------------------------------------------------------------------")  
        elif(ch2==2):
            id=int(input("Enter Customer ID : "))
            sql_query="select id from bank where id=%s"
            res.execute(sql_query,(id,))
            check_data=res.fetchone()
            if check_data is not None:
                user=input("Enter New Customer Name : ")
                phone=int(input("Enter Phone Number : "))
                email=input("Enter Mail Address : ")
                address=input("Enter Address : ")
                update_customer(user,phone,email,address,id)
            else:
                print("Customer ID Doesn't Found")
        elif(ch2==3):
            show_customers()
        elif(ch2==4):
            id=int(input("Enter Customer ID : "))
            delete_user(id)
        elif(ch2==5):
            id=int(input("Enter Your ID : "))
            check_balance(id)
        elif(ch2==6):
            id=int(input("Enter Customer ID : "))
            change_pin(id)
        elif(ch2==7):
            deposit_initial()
        elif(ch2==8):
            withdraw_initial()
        elif(ch2==9):
            send_money_initial()
        elif(ch2==10):
            exit()
        else:
            print("Something Went Wrong! Try Again")
elif(ch==3):
    exit()
else:
    print("Something Went Wrong! Try Again")













































