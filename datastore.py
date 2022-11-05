from cryptography import encrypt_user

from dataclasses import dataclass, field
import csv
import logging

@dataclass
class UserDB:
    disk_path : str
    dictionary : dict = field(init=False)

    def __post_init__(self):
        self.loaddb()
        logging.info(f"Initiated Datastore at path {self.disk_path}")

    def loaddb(self):
        with open(self.disk_path, "r",newline='') as f:
            reader = csv.reader(f)
            self.dictionary = {key: value for key, value in reader}
    
    # could be faster with append/diff writes ¯\_(ツ)_/¯ but I know this wont break and writes are infrequent
    # change when tami goes over 10k new members hourly
    def savedb(self):
        with open(self.disk_path, "w",newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.dictionary.items())

    def change_user(self,uid:bytes,pincode:int,is_admin:bool):
        """
        Change of create new and existing user records
        """
        logging.info(f"Changed/Added user with UID:{uid} and {'Admin' if is_admin else 'Unpriviledged'} permissions")
        self.dictionary[encrypt_user(uid,pincode)] = is_admin
        self.savedb()

    # user lookups are not constant time, susceptible to timing attacks
    # change when cpython gets too fast and starts optimizing too well
    def get_user(self,uid:bytes,pincode:int):
        """
        Returns False if the user doesnt exist
        Returns tuple of (user_exists, is_admin) otherwise
        """
        logging.info(f"Tried lookup for UID:{uid}")
        lookup = self.dictionary.get(encrypt_user(uid,pincode))
        if lookup == None:
            return False
        elif lookup != None: 
            return True, lookup

    def is_admin(self,uid:bytes,pincode:int) -> bool:
        """
        Returns True if user is admin
        Returns False if user is not admin
        Returns False if user doesnt exist
        """
        logging.info(f"Tried admin lookup for UID:{uid}")
        lookup = self.dictionary.get(encrypt_user(uid,pincode))
        if lookup == None:
            return False
        elif lookup != None: 
            return lookup

    def check_admin(self) -> bool:
        """
        Returns True if there is at least one admin user
        Returns False if there are no admin users
        """
        logging.info("Checked if there are any admin users")
        return any(self.dictionary.values())
    
    def delete_user(self,uid:bytes,pincode:int) -> bool:
        """
        Delete user from db
        If user never existed returns False
        If user existed returns True
        """
        logging.info(f"Tried deletion for UID:{uid}")
        removed_user = self.dictionary.pop(encrypt_user(uid,pincode),None)
        if removed_user == None:
            return False
        if removed_user != None:
            logging.info(f"Removed {'Admin' if removed_user else 'Unpriviledged'} user {uid} from Datastore")
            return True
        self.savedb()
