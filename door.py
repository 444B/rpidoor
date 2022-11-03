import hashlib
from time import sleep
from gpiozero import LED
from db import db_query, db_query_match, db_insert, db_reset
from nfc_reader import nfc_setup, nfc_loop


print("\n")

MAX_ATTEMPTS = 3
TIMEOUT_SECONDS = 30
OPEN_SECONDS = 5


# hash the username
def hash_username(cleartext_username):
    hashed_username = hashlib.sha256(cleartext_username.encode()).hexdigest()
    return hashed_username

# hash the password
def hash_password(cleartext_password):
    hashed_password = hashlib.sha256(cleartext_password.encode()).hexdigest()
    return hashed_password


# function to open/close the door. in testing, just prints
def open_door():
    username_led.on()
    password_led.on()
    print("Door has been opened")

def close_door():
    print("Door has been closed")
    username_led.off()
    password_led.off()


# flashes both LEDs
def flash_both_led(time):
    for num in range(time):
        print(f"Locked out for {time - num} more seconds")
        username_led.on()
        password_led.on()
        sleep(0.5)
        username_led.off()
        password_led.off()
        sleep(0.5)


# TODO figure out how to add color to this logic
def change_led(category, action):
    if category == username_led:
        if action == 1:
            username_led.on()
        if action == 0:
            username_led.off()
    if category == password_led:
        if action == 1:
            password_led.on()
        if action == 0:
            password_led.off()


# main program runs from here
if __name__ == "__main__":

    # initial variables setup
    attempts = 0
    hashed_password = ""
    username_check = False
    password_check = False
    match_check = False
    username_led = LED(12)
    password_led = LED(5)
    change_led(username_led, 0)
    change_led(password_led, 0)
    

    # running program in a loop

    nfc_setup()
    while True:

        # card UID check loop
        attempts = 0
        while not username_check:
            uid = nfc_loop()
            if not uid:
                continue

            # compare card UID to creds.db
            if db_query(uid, "query_username"):
                change_led(username_led, 1)
                username_check = True
                print("Username is correct")

            # incorrect card
            elif attempts < MAX_ATTEMPTS:
                attempts += 1
                print(f"Incorrect card UID, try again.You have {MAX_ATTEMPTS - attempts} attempts left")
                flash_both_led(1)
                username_check = False

            # timeout after 3 incorrect cards
            else:
                print("Too many incorrect attempts, pls wait {TIMEOUT_SECONDS} seconds and try again")
                flash_both_led(TIMEOUT_SECONDS)
                sleep(TIMEOUT_SECONDS)
                username_check = False
                attempts = 0

        # password check loop
        attempts = 0
        while not password_check:
            hashed_password = hash_password(input("Please enter your password: "))

            # compare password to creds in the db
            if db_query(hashed_password, "query_password"):
                print("Password is correct")
                change_led(password_led, 1)
                password_check = True

            # incorrect input
            elif attempts < MAX_ATTEMPTS:
                attempts += 1
                print(f"Incorrect password, try again.You have {MAX_ATTEMPTS - attempts} attempts left")
                flash_both_led(1)
                password_check = False

            # timeout after MAX_ATTEMPTS of incorrect inputs
            else:
                print("Too many incorrect attempts, pls wait {TIMEOUT_SECONDS} seconds and try again")
                flash_both_led(5)
                attempts = 0
                username_check = False
                password_check = False

        # check that username and password match
        if db_query_match(uid, hashed_password):
            match_check = True
        else:
            print("Username and password do not match. Try again.")
            password_check = False
            username_check = False
            match_check = False
            attempts = 0

        # opens the door. 
        if username_check and password_check and match_check:
            open_door()
            sleep(OPEN_SECONDS)
            close_door()
            username_check = False
            password_check = False
            match_check = False
            attempts = 0
