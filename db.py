import sqlalchemy as db

# db setup
engine = db.create_engine("sqlite:///creds.db")
conn = engine.connect()
metadata = db.MetaData()
# tables setup
members = db.Table('members', metadata,
                   db.Column('hash', db.CHAR(64), primary_key=True),
                   db.Column('is_admin', db.INTEGER, nullable=False)
                   )
metadata.create_all(engine)


def db_insert(entered_hash):
    # insert new member 
    query = db.insert(members).values(hash=entered_hash, is_admin=0)
    result = conn.execute(query)
    if result.is_insert:
        print("New member added")
        return True
    else:
        print("No values were inserted.")
        return False

def db_query(entered_hash):
    # check if hash is in database
    output = conn.execute(
        f"SELECT EXISTS(SELECT 1 FROM members WHERE hash = ? LIMIT 1)", (entered_hash,)
    )
    result = output.fetchall()
    if result[0][0] == 1:
        return True
    else:
        return False

def db_reset():
    # reset database
    conn.execute("DELETE FROM members")
    print("Database reset")
    return


def db_check_admin():
    # Check if there are any admins in the database
    output = conn.execute(
        f"SELECT EXISTS(SELECT 1 FROM members WHERE is_admin = 1 LIMIT 1)"
    )
    result = output.fetchall()
    if result[0][0] == 1:
        return True
    else:
        return False

def db_is_admin(entered_hash):
    # Check if the user is an admin
    output = conn.execute(
        f"SELECT EXISTS(SELECT 1 FROM members WHERE hash = ? AND is_admin = 1 LIMIT 1)", (entered_hash,)
    )
    result = output.fetchall()
    if result[0][0] == 1:
        return True
    else:
        return False

def db_make_admin(entered_hash):
    # Make a user an admin
    query = db.update(members).where(members.columns.hash == entered_hash).values(is_admin=True)
    result = conn.execute(query)
    print("Admin status set")
    return True



# if __name__ == '__main__':
#     # insert(hashed_usrname, hashed_passwd)
#     if db_query("03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4", "queried_usrname"):
#         print("TRUEEEE")
#     else:
#         print("FALSE")
