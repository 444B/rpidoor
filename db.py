import sqlalchemy as db

# sha256 of 1234
hashed_usrname = "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"
# sha256 of 5678
hashed_passwd = "f8638b979b2f4f793ddb6dbd197e0ee25a7a6ea32b0ae22f5e3c5d119d839e75"

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


def db_query(hash, category):
    output = conn.execute(f"SELECT EXISTS(SELECT 1 FROM members WHERE {category}={hash} LIMIT 1)")
    print(output.fetchall())
    # result = output.fetchall()
    # if result == str(hash):
    #     return True
    # else:
    #     return False


if __name__ == '__main__':
    insert(hashed_usrname, hashed_passwd)
    db_query("03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4", usrname_col)