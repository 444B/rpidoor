# rpidoor - [Work In Progress]

## Background
This is a python script for a door lock system.  
Current work in progress is on main even though it is in testing.  
Once we have a working model, dev will move to a dev branch and this md will be updated to reflect

## Setup
Copy this command and paste into terminal. It will change your directory to your home directory, clone the repo, change directory to the repo, give the bash script execution permisson and then run the script. Read the [run.sh](https://github.com/444B/rpidoor/blob/master/run.sh) script for more info. Always read what you run :) 
``` shell
cd ~
 git clone https://www.github.com/444B/rpidoor.git
 cd rpidoor/
 apt update
 ```
 then run the next command individually
 ``` shell
 sudo apt install sqlite3 python3 -y
 ```
 then run the rest
  ``` shell
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
nohup python3 door.py
```
TODO - polish these commands


## Physical layout
```
          __________________   
         | ______________  |  
         |  |            | |               _______   
         |  |      []...........__________|       |  
         |  |      []...........          |      O|  
         |  |       |   (RPI)  |          |       |  
         +  +       |__________|          |_______|  
|7|8|9| (LEDs)        |     |               (door)  
|4|5|6|_______________|     |  
|1|2|3|                  ___|__  
|*|0|#|                 [>->X<-<]  
(Keypad)              (RFID Reader)  
```

## Design 
inpired by [IEEE paper](https://ieeexplore.ieee.org/document/8807588) and [c-base/raspberrylock](https://github.com/c-base/raspberrylock)

## Future plans TODO
- Set up a working model in python
- rewrite a working model in rust (for practise)
- organise red/blue team events to break the model, using open and black box methods
- add in RFID tag support for the usr cred and leaving the keypad for the passwd
