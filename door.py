import hashlib
from gpiozero import LED
import sqlalchemy as db
from random import randint

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
    













if __name__ == "__main__":
    fuckups = 0
    hashed_passwd = ""
    hashed_passwd = ""



    engine = db.create_engine("sqlite:///dylanz.db")
    conn = engine.connect()
    metadata = db.MetaData()

    Users = db.Table('Users', metadata,
                db.Column('username', db.Integer(),primary_key=True),
                db.Column('password', db.CHAR(128), nullable=False),
              )

    metadata.create_all(engine)



    def insert():
        # insert:
        query = db.insert(Users).values(username=randint(1000, 10000), password=11223344)
        result = conn.execute(query)
        if result.is_insert:
            print(f"inserted")
        else:
            print("not inserted.")
            return
:

def query(uname: int):
    # query
    output = conn.execute(f"SELECT * FROM Users WHERE username = {uname}")
    print(output.fetchall())


    while True:
        get_usr(input("Please enter your username\n"))
        # if get_usr == <"magic sha256 hash">
        #   door_open()
        # else:
        #   
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
        
    # insert()
    # query(8645)

    
    





    # insert()
    # query(8645)

