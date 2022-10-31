import sqlalchemy as db

# db setup
engine = db.create_engine("sqlite:///creds.db")
conn = engine.connect()
metadata = db.MetaData()
# tables setup
members = db.Table('members', metadata,
          db.Column('usrname_col', db.CHAR(64),primary_key=True),
          db.Column('passwd_col', db.CHAR(64), nullable=False),
          )
metadata.create_all(engine)

# insert new member (still in testing)
def insert(entered_usrname, entered_passwd):
    query = db.insert(members).values(usrname_col=entered_usrname, passwd_col=entered_passwd)
    result = conn.execute(query)
    if result.is_insert:
        print(f'''
        {entered_usrname} was inserted as the hashed_usrname to the db
        {entered_passwd} was inserted as the hashed_passwd to the db
        ''')
    else:
        print("No values were inserted.")
        return

# category types are queried_usrname, queried_passwd
def db_query(hash, category):
    if category == "queried_usrname":
        output = conn.execute(
            f"SELECT EXISTS(SELECT 1 FROM members WHERE usrname_col = ? LIMIT 1)", (hash,)
            )
        result = output.fetchall()
        if result[0][0] == 1:
            print("is 1")
            return True
        else:
            return False

    if category == "queried_passwd":
        output = conn.execute(
            f"SELECT EXISTS(SELECT 1 FROM members WHERE passwd_col = ? LIMIT 1)", (hash,)
            )
        result = output.fetchall()
        if result[0][0] == 1:
            print("is 1")
            return True
        else:
            return False
    else:
        print("Malformed Query category error")

if __name__ == '__main__':
    # insert(hashed_usrname, hashed_passwd)
    if db_query("03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4", "queried_usrname") == True:
        print("TRUEEEE")
    else:
        print("FALSE")
