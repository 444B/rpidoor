import hashlib
#from gpiozero import LED
print("\n")

def get_usr(cleartext_usrname):
    global hashed_usrname 
    hashed_usrname = hashlib.sha256(cleartext_usrname.encode()).hexdigest()
    return hashed_usrname
    # print(hashed_usrname)

def get_passwd(cleartext_passwd):
    global hashed_passwd
    hashed_passwd = hashlib.sha256(cleartext_passwd.encode()).hexdigest()
    print(hashed_passwd)
    

if __name__ == "__main__":
    fuckups = 0
    hashed_passwd = ""
    hashed_passwd = ""

    while True:    
        get_usr(input("Please enter your username\n"))
        # compare username to db
        # if username correct:
        # light up user LED GREEN
        get_passwd(input("What is your password?\n"))
        # elif global fuckups == 3:
        #   print("Too many incorrect attempts, pls wait 30s and try again")
        #   light up user LED RED 
        #   sleep 30
        # else:
        #   print("Incorrect user, try again")
        #   global fuckups += 1
        #   light up user LED RED
        

    
    

# if (usrname == True and password == True):
#     opendoor()
# else:
#     print("try again")
