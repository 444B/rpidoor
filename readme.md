# rpidoor

## Background
This is a python script for a door lock system.  
Current work in progress is on main even though it is in testing.  
Once we had a working model, dev will move to dev branch and this md will be updated

## Setup
cd ~ \
 git clone https://github.com/444B/rpidoor.git\
 cd rpidoor/\
 chmod u+x run.sh\
 ./run.sh\


## Rough Arch / Design
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


## Future plans TODO
- Set up a working model in python
- rewrite a working model in rust (for practise)
- organise red/blue team events to break the model, using open and black box methods
- add in RFID tag support for the usr cred and leaving the keypad for the passwd