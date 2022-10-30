import time
import hashlib
import sqlalchemy as db
from random import randint
# from gpiozero import LED
print("\n")

# get usrname and save as a global string(hashed)
def get_usr(cleartext_usrname):
    global hashed_usrname 
    hashed_usrname = hashlib.sha256(cleartext_usrname.encode()).hexdigest()
    # print(hashed_usrname)

# get passwd and save as a global string(hashed)
def get_passwd(cleartext_passwd):
    global hashed_passwd
    hashed_passwd = hashlib.sha256(cleartext_passwd.encode()).hexdigest()
    # print(hashed_passwd)

# insert new member (still in testing)
def insert():
    query = db.insert(Users).values(usr=randint(1000, 9999), passwd=123456)
    result = conn.execute(query)
    if result.is_insert:
        print(f"inserted")
    else:
        print("not inserted.")
        return

# check if the usr is in the db
def query(uname: int):
    output = conn.execute(f"SELECT * FROM members WHERE usr = {uname}")
    print(output.fetchall())

# function to open the door. in testing, just prints 
def open_door():
    print("the door is OPEN\n")

# main program runs from hhere
if __name__ == "__main__":
    
    # initial variables setup
    fuckups = 0
    hashed_passwd = ""
    hashed_passwd = ""
    
    # db setup
    engine = db.create_engine("sqlite:///creds.db")
    conn = engine.connect()
    metadata = db.MetaData()
    
    # tables setup
    Users = db.Table('members', metadata,
                db.Column('usr', db.Integer(),primary_key=True),
                db.Column('passwd', db.CHAR(64), nullable=False),
              )
    metadata.create_all(engine)

    # running program in a loop
    while True:
        get_usr(input("Please enter your usrname\n"))
        # admin override using magic hash
        if get_usr == "936867247aef14d232e539bd3f08b2c6bc47afe56a774ede3488d66006cbeb95":
            open_door()
        else: 
        # compare username to db
        # if username correct:
        # light up user LED GREEN
            get_passwd(input("What is your passwrd?\n"))
        # elif global fuckups == 3:
        #   print("Too many incorrect attempts, pls wait 30s and try again")
        #   light up user LED RED 
        #   sleep 30
        # else:
        #   print("Incorrect user, try again")
        #   global fuckups += 1
        #   light up user LED RED
        
    # insert()
    # query(8645)

