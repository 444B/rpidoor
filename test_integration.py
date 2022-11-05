from datastore import UserDB

from os import urandom
import random
import logging

logging.basicConfig(filename='testlog.log', encoding='utf-8', level=logging.DEBUG)

ActiveDatabase = UserDB("testdb.csv")

sessionUID: bytes = urandom(7) # 7 random bytes for the test session
sessionPincode: int = random.randint(100_000,999_999) # 6 digit pseudorandom pincode

def test_authflow():
    # Create a non admin session user
    ActiveDatabase.change_user(uid=sessionUID,pincode=sessionPincode,is_admin=False)

    #Make 15 more random users
    for i in range(0,15):
        ActiveDatabase.change_user(urandom(24),random.randint(100_000,999_999_999),False)

    assert ActiveDatabase.get_user(sessionUID,sessionPincode) == (True,False)

def test_removal():
    assert ActiveDatabase.delete_user(urandom(32),random.randint(100_000,999_999_999)) == False
    assert ActiveDatabase.delete_user(sessionUID,sessionPincode) == True
        