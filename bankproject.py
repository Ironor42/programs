import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
mydb = mysql.connector.connect(host="localhost",user="root",passwd="")
mycursor = mydb.cursor()
#creating database
mycursor.execute("create database if not exists bank")
mycursor.execute("use bank")
#creating required tables 
mycursor.execute("create table if not exists\
                 bank_master(\
                     acno char(4) primary key,\
                     name varchar(30),\
                     city char(20),\
                     mobileno char(10),\
                     balance int(6))\
                 ")
mycursor.execute("create table if not exists\
                 bank_data(acno char (4),\
                 amount int(6),\
                 dot date,\
                 ttype char(1),\
                 foreign key (acno) references bank_master(acno))\
                 ")
mydb.commit()

def chart():
        mycursor.execute("select * from bank_master")
        col_list = [field[0] for field in mycursor.description]
        records = mycursor.fetchall()
        num_rec = mycursor.rowcount
        if num_rec > 0:
                df = pd.DataFrame(records, columns = col_list,
                                  index = range(1, num_rec + 1) )
                bal = df['BALANCE']
                acc = df['ACCNO']
                
                plt.bar(np.array(acc), np.array(bal))
                plt.xticks(np.array(acc))
                plt.title("chart of deposit vs. a/c")
                plt.ylabel("DOP")
                plt.xlabel("Amount")
                plt.grid(True) 
                plt.show()
        else:
                
                print("No records to display chart.")

def new_account():
        print("\t\t\t\t| NEW ACCOUNT OPENING WINDOW |")
        print("-"*111)
        print("\t\tAll information prompted are mandatory to be filled.",end="\n\n")
        mycursor.execute("select * from bank_master")
        col_list = [field[0] for field in mycursor.description]
        records = mycursor.fetchall()
        num_rec = mycursor.rowcount
        if num_rec > 0:
            df = pd.DataFrame(records, columns = col_list,index = range(1, num_rec + 1) )
            print(df,end="\n\n")
            while True:
                acno=int(input("\t\tEnter a new A/C No. (0 to main menu)=> "))
                if acno == 0:
                    print("+","-"*109,"+",end="\n\n",sep="")
                    break
                ndf = df[df['ACCNO'] == acno]
                if ndf.empty:
                    name = input("\t\tEnter name(limit 35 characters)=> ")
                    addrs = str(input("\t\tEnter your address=> "))
                    mn = str(input("\t\tEnter mobile no.=> "))
                    bal = 5000
                    query= "insert into bank_master values({},'{}','{}',{},{})".\
                           format(acno,name,addrs,mn,bal)
                    mycursor.execute(query)
                    mydb.commit()
                    print("\n\t\tAccount is successfully created!!!")
                else:

                    print("\n\t\tWARNING! This Account already exit, please re-\t\tEnter\n")

            
        return

def deposit():
        print("\t\t\t\t| DEPOSIT WINDOW |")
        print("-"*111)
        mycursor.execute("select * from bank_master")
        col_list = [field[0] for field in mycursor.description]
        records = mycursor.fetchall()
        num_rec = mycursor.rowcount
        if num_rec > 0:
            df = pd.DataFrame(records, columns = col_list,
                              index = range(1, num_rec + 1) )
            print(df,end='\n\n')
            while True:
                acno=int(input("\t\tEnter an A/C No. to deposit (0 to main menu)=> "))
                if acno == 0:
                    print("+","-"*109,"+",end="\n\n",sep="")
                    break
                ndf = df[df['ACCNO'] == acno]
                if ndf.empty:
                    print("\t\tNo such Account, please re-Enter\n")
                else:
                    amt=int(input("\t\tEnter amount to be deposited:"))
                    dot=str(input("\t\tEnter date of transaction yyyy-mm-dd=> "))
                    ttype="D"
                    mycursor.execute("insert into bank_data values('{}',{},{},'{}')".\
                                     format(dot,acno,amt,ttype))
                    mycursor.execute("update bank_master set balance = balance + {} where accno={}".\
                                     format(amt,acno))
                    mydb.commit()
                    print("\t\tmoney has been deposited successully!!!\n")
        else:
            print("\t\tno customers, please create an account first")
        return

def withdraw():
        print("\t\t\t\t| WITHDRAWL WINDOW |")
        print("-"*111)
        mycursor.execute("select * from bank_master")
        col_list = [field[0] for field in mycursor.description]
        records = mycursor.fetchall()
        num_rec = mycursor.rowcount
        if num_rec > 0:
            df = pd.DataFrame(records, columns = col_list, index = range(1, num_rec + 1) )
            print(df,end='\n\n')
            while True:
                acno=int(input("\t\tEnter an A/C No. to withdraw (0 to main menu)=> "))
                ndf = df[df['ACCNO'] == acno]
                if acno == 0:
                    print("+","-"*109,"+",end="\n\n",sep="")
                    break
                if ndf.empty:
                    print("\t\tNo such Account, please re-Enter")
                else:
                    while True:
                            amt=int(input("\t\tEnter amount to withdrawl=> "))
                            avail = (df.query(("ACCNO == {}").format(str(acno))))
                            idx= avail.index.values
                            balnce = list(df.loc[idx,"BALANCE"])
                            if amt <= balnce[0]:
                                    dot=str(input("\t\tEnter date of transaction yyyy-mm-dd=> "))
                                    ttype="W"
                                    mycursor.execute("insert into bank_data values('{}',{},{},'{}')".\
                                                     format(dot,acno,amt,ttype))
                                    mycursor.execute("update bank_master set balance = balance - {} \
                                                        where accno={}".format(amt,acno))
                                    mydb.commit()
                                    print("\t\tmoney has been withdrawl successully!!!\n")
                                    break
                            else:
                                print("\t\tInsufficient balance ,re-Enter amount.\n")
        else:
            print("\t\tno customers exist, please create an account first.\n")
        return
def update():
        print("\t\t\t\t| UPDATE DETAILS WINDOW |")
        print("-"*111)
        mycursor.execute("select * from bank_master")
        col_list = [field[0] for field in mycursor.description]
        records = mycursor.fetchall()
        num_rec = mycursor.rowcount
        df = pd.DataFrame(records, columns = col_list, index = range(1, num_rec + 1) )
        print(df,end='\n\n')
        while True:
                acno=int(input("\t\tEnter an A/C no. to update (0 to main menu)=> "))
                if acno == 0:
                        print("+","-"*109,"+",end="\n\n",sep="")
                        break
                ndf = df[df['ACCNO'] == acno]
                if ndf.empty:
                        print("\t\tNo such Account, please re-Enter\n")
                else:        
                    nm= str(input("\t\tEnter new name=> "))                    
                    ad= input("\t\tEnter new address=> ")
                    mb= int(input("\t\tEnter new mobile no.=> "))                    
                    mycursor.execute("update bank_master set name='{}' where accno={}".\
                                                     format(nm,str(acno)))
                    mycursor.execute("update bank_master set address='{}' where accno={}".\
                                                     format(ad,str(acno)))
                    mycursor.execute("update bank_master set mobno='{}'where accno={}".\
                                                     format(mb,str(acno)))
                    print("\t\tYour details has been updated successfully!!\n")
                                        
                
        return 
def passbook():
        print("\t\t\t\t| PASSBOOK WINDOW |")
        print("-"*111)
        mycursor.execute("select * from bank_master")
        col_list = [field[0] for field in mycursor.description]
        records = mycursor.fetchall()
        num_rec = mycursor.rowcount
        if num_rec > 0:
            df = pd.DataFrame(records, columns = col_list, index = range(1, num_rec + 1) )
            print(df,end='\n\n')
            while True:
                acno=int(input("\t\tEnter an A/C no. to display passbook (0 to main menu)=> "))
                if acno == 0:
                        print("+","-"*109,"+",end="\n\n",sep="")
                        break
                ndf = df[df['ACCNO'] == acno]
                if ndf.empty:
                    print("\t\tNo such Account, please re-Enter\n")
                else:
                    print(ndf)
                    #mycursor.execute("select * from bank_master where acno = '"+acno+"';")
                    #for i in mycursor:
                    #    print(i)
                    #print("--------------------------------------------------")
                    mycursor.execute("select * from bank_data where accno= {}".format(acno))
                    col_list = [field[0] for field in mycursor.description]
                    records = mycursor.fetchall()
                    num_rec = mycursor.rowcount
                    if num_rec > 0:
                        pdf = pd.DataFrame(records, columns = col_list, index = range(1, num_rec + 1) )
                        print("-"*50)
                        print(pdf)
                        print("-"*50)
                       #pdf['amount'].plot(kind='hist', figsize=(8,5) )
                        mbal = list(pdf['AMOUNT'])
                        dt= list(pdf["DATE"])
                        #macc = pdf['index']
                        plt.plot(dt,mbal)
                        plt.title("Deposit & Withdraw Chart of Ac/no. "+ str(acno))
                        plt.xlabel("Sequence")
                        plt.ylabel("Amount")
                        plt.grid(True) 
                        plt.show()

                    else:
                        print("\t\tNo transaction found for this account\n")
        else:
            print("\t\t\t\tAccount Master is empty\n")
        return
def report():
        print("\t\t\t\t| TRANSACTIONS REPORT WINDOW |")
        print("-"*111)
        while True:       
                dt = str(input("\tEnter date of transactions(yyyy-mm-dd) or (0 to main menu)=> "))
                if dt == "0":
                        print("+","-"*109,"+",end="\n\n",sep="")
                        break
                else:
                        mycursor.execute("select * from bank_data where date = '{}'".format(dt))
                        col_list = [field[0] for field in mycursor.description]
                        records = mycursor.fetchall()
                        num_rec = mycursor.rowcount
                        df = pd.DataFrame(records, columns = col_list, index = range(1, num_rec + 1) )
                        if df.empty:
                                print("\n\t\tNo records found.\n")
                        else:
                                
                                print(df,end="\n\n")
                                mycursor.execute("select * from bank_data where t_type='W' and date='{}'".\
                                         format(dt))
                                col_list = [field[0] for field in mycursor.description]
                                records = mycursor.fetchall()
                                num_rec = mycursor.rowcount
                                df = pd.DataFrame(records, columns = col_list, index = range(1, num_rec + 1) )
                                print("\t\tTotal amount withdrawn is: ",df.AMOUNT.sum(),end="\n\n")
                                mycursor.execute("select * from bank_data where t_type = 'D' and date='{}'".\
                                         format(dt))
                                col_list = [field[0] for field in mycursor.description]
                                records = mycursor.fetchall()
                                num_rec = mycursor.rowcount
                                df = pd.DataFrame(records, columns = col_list, index = range(1, num_rec + 1) )
                                print("\t\tTotal amount deposited is: ",df.AMOUNT.sum(),end="\n\n")
        return
print("\t\t\t\t|****   BANK MANAGEMENT SYSTEM  ****|")
print("="*111,end='\n\n')
# Main menu
while True:
    print("\t\t\t\t\t   |MAIN MENU|\n")
    print("\t\t\t\t1. Open new account")
    print("\t\t\t\t2. Deposit money")
    print("\t\t\t\t3. Withdraw money")
    print("\t\t\t\t4. Update details")
    print("\t\t\t\t5. Display passbook")
    print("\t\t\t\t6. Display Chart")
    print("\t\t\t\t7. Report of Transactions")
    print("\t\t\t\t8. Exit\n")
    ch = int(input("\t\t\t\tEnter your choice->> "))
    print("="*111,end="\n\n")
   
    if(ch==1):
        new_account() # FUNCTION CALL FOR opening A NEW ACCOUNT
    elif(ch==2): 
        deposit()   # FUNCTION CALL TO DEPOSIT MONEY IN AN ACCOUNT
    elif(ch==3): 
        withdraw()  # FUNCTION CALL TO WITHDRAW MONEY FROM AN ACCOUNT
    elif(ch==4):
        update()  # FUNCTION CALL TO UPDATE AN ACCOUNT
    elif(ch==5):
        passbook()   # FUNCTION CALL TO SHOW PASSBOOK OF AN ACCOUNT
    elif(ch==6):
        chart()       # FUNCTION CALL TO SHOW GRAPH OF ALL ACCOUNTS
    elif(ch==7):
        report()   #FUNCTION CALL TO SHOW REPORT OF TRANSACTIONS OF ACCOUNTS
    elif(ch==8):
        print("Thanks For Visiting Our Bank. |^_^|")
        break
    else:
        print("WRONG CHOICE")
    

    
