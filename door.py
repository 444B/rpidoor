import hashlib
from time import sleep
from gpiozero import LED
from nfc_reader import nfc_setup, nfc_loop
import os
from display import *

from datastore import UserDB

# Datastore object
Datastore = UserDB("ProductionDB.csv")

display("\n")

MAX_ATTEMPTS = 3
TIMEOUT_SECONDS = 30
OPEN_SECONDS = 5

# function to open/close the door. in testing, just displays
def open_door():
    led.on()
    display("Door has been opened")
def close_door():
    display("Door has been closed")
    led.off()

# flashes both LEDs for the specified number of seconds
def lock_out_wait(time: int):
    for num in range(time):
        display(f"Locked out for {time - num} more seconds")
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)

def lock_out():
    display("Too many bad attempts")
    sleep(2)
    display(f"Wait {TIMEOUT_SECONDS} seconds and try again")
    sleep(2)
    lock_out_wait(TIMEOUT_SECONDS)
        


def register_tag(make_admin: bool):
    display("Please scan the new tag")
    uid: bytes = nfc_loop()
    while not uid:
        uid = nfc_loop()
    display("Please enter the new password")
    password: int = input("Please enter the new password: ")
    Datastore.change_user(uid=uid,pincode=password,is_admin=make_admin)
    if make_admin:
        display("Created Admin user Account")
    if not make_admin:
        display("Created regular user Account")
    sleep(2)
    return True

    


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
        display("Waiting for card")
        if not uid:
            continue
        display("Card found!")
        sleep(0.5)
        
        # if the SET_ADMIN environment variable is set or there are no admins,
        # then the first card scanned will be made an admin
        if os.environ.get("SET_ADMIN") or not Datastore.check_admin():
            display("No admins found.")
            sleep(1)
            display("Setting first card as admin")
            sleep(2)
            if register_tag(True):
                os.environ["SET_ADMIN"] = ""
                continue
        
        # get the password
        display("Please enter the password")
        password = input("Please enter your password: ")

        # if we have an admin card, go to the register tag function
        if Datastore.is_admin(uid, password):
            display("Admin card detected")
            sleep(2)
            display("Register a new tag?")
            sleep(2)
            display("1: Yes, 0: No")
            ans = input("Would you like to register a new tag? (1/0): ")
            if ans == "1":
                register_tag(False)
                continue
            else:
                display("Exiting admin mode")
                sleep(2)
        
        # check if the hash is in the database
        display("Checking UID + password")
        user_check = Datastore.get_user(uid, password)
        print(user_check)

        if(user_check):
            display("User found, welcome back")
            open_door()
            sleep(OPEN_SECONDS)
            close_door()
            user_check = False
            attempts = 0
            continue

        elif attempts < MAX_ATTEMPTS:
            # incorrect input
            attempts += 1
            if attempts == MAX_ATTEMPTS:
                lock_out()
                attempts = 0
                continue

            display("Incorrect tag/password.")
            sleep(1)
            if(MAX_ATTEMPTS - attempts == 1):
                display(f"You have {MAX_ATTEMPTS - attempts} attempt left.")
            else:
                display(f"You have {MAX_ATTEMPTS - attempts} attempts left.")
            sleep(1)
            continue
        
        else:
            lock_out()
            attempts = 0
            continue
