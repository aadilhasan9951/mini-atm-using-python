print("===== WELCOME TO PYTHON ATM =====")
bal=5000
while True:
    print(
        '''
    1. Check Balance
    2. Deposit Money
    3. Withdraw Money
    4. Exit
    '''
    )
    user=int(input("enter respective no. of your choice: "))
    if(user==1):
        print(f"current balance:{bal}")
    elif(user==2):
        n1=int(input("enter deposit amount: "))
        if(n1>0):
            bal+=n1
        else:
            print("invalid amount, please enter a valid amount")
        print(f"current updated balance:{bal}")
    elif(user==3):
        n2=int(input("enter withdrawal amount: "))
        if(n2>0 and n2<=bal):
                bal-=n2
                print(f"current updated balance:{bal}")
        elif(n2>bal):
            print("insufficient balance")
        else:
            print("invalid amount,please enter a valid amount")
    elif(user==4):
        print('''
        Thank you for using Python ATM!
                Have a nice day!
              ''')
        break
    else:
        print("Invalid choice! Please enter 1 to 4.")