import sqlalchemy as db
from random import randint

engine = db.create_engine("sqlite:///creds.db")
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


def query(uname: int):
    # query
    output = conn.execute(f"SELECT * FROM Users WHERE username = {uname}")
    print(output.fetchall())


if __name__ == '__main__':
    # insert()
    query(8645)
