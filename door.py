import hashlib
from time import sleep
from gpiozero import LED
from db import *
from nfc_reader import nfc_setup, nfc_loop
import os


print("\n")

MAX_ATTEMPTS = 3
TIMEOUT_SECONDS = 30
OPEN_SECONDS = 5


# hash function
def hash(cleartext):
    hashed = hashlib.sha256(cleartext.encode()).hexdigest()
    return hashed


# function to open/close the door. in testing, just prints
def open_door():
    led.on()
    print("Door has been opened")

def close_door():
    print("Door has been closed")
    led.off()


# flashes both LEDs for the specified number of seconds
def lock_out(time):
    for num in range(time):
        print(f"Locked out for {time - num} more seconds")
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)


def register_tag(make_admin):
    print("Please scan your tag")
    uid = nfc_loop()
    password = input("Please enter your password: ")
    hashed = hash(uid + password)
    if db_insert(hashed):
        print("Registration complete")
    else:
        print("Registration insert failed")
    if make_admin:
        print("Setting admin status")
        db_make_admin(hashed)
    


# main program runs from here
if __name__ == "__main__":

    # initial variables setup
    attempts = 0
    hashed_password = ""
    user_check = False
    led = LED(12)
    led.off()
    nfc_setup()

    while True:
        uid = nfc_loop()
        if not uid:
            continue
        
        # if the SET_ADMIN environment variable is set or there are no admins,
        # then the first card scanned will be made an admin
        if os.environ.get("SET_ADMIN") or not db_check_admin():
            print("No admins found or SET_ADMIN env variable is set. Setting first card as admin")
            if register_tag(True):
                os.environ["SET_ADMIN"] = ""
                continue
        
        # get the password
        password = input("Please enter your password: ")

        # hash the UID + password
        hashed = hash(uid + password)

        # if we have an admin card, go to the register tag function
        if db_is_admin(hashed):
            print("Admin card detected")
            ans = input("Would you like to register a new tag? (1/0): ")
            if ans == "1":
                register_tag(False)
                continue
            else:
                print("Exiting admin mode, the door will now be unlocked")
        
        # check if the hash is in the database
        print("Checking if UID + password is in database")
        user_check = db_query(hashed)

        if(user_check):
            print("User found, welcome back")
            open_door()
            sleep(OPEN_SECONDS)
            close_door()
            user_check = False
            attempts = 0

        elif attempts < MAX_ATTEMPTS:
            # incorrect input
            attempts += 1
            print(f"Incorrect tag/password, try again.You have {MAX_ATTEMPTS - attempts} attempts left")
            lock_out(1)

        else:
            # timeout after MAX_ATTEMPTS of incorrect inputs
            print("Too many incorrect attempts, pls wait {TIMEOUT_SECONDS} seconds and try again")
            lock_out(TIMEOUT_SECONDS)
            attempts = 0
