This project contains the code used to play songs on 8 glasses with different water levels. The project is demonstrated here (https://youtu.be/Sa5ojr7yw0I).

If you want to create anything like this, micro-python need to be flashed on to a micro sd card and inserted in to the EV3's as described here: https://pybricks.com/ev3-micropython/startinstall.html
This allows direct python programing to the hub via a usb cable, and enables more complexity than the official LEGO EV3CLASSROOM app.

**The project consist of some folders:**
1. Bluetooth_sync_test
2. tethering_test
3. threading_test

Each folder contains code used to the test refered to. Some of the code I've found online, and just used for testing whats possible with the system, which will be referred to in the respectively files.

**Main files:**
_1. universal files:_
- player.py
- wireless.py
- songs.py

These files are used for both hubs, and contains different aspects of the program. player.py contains a class that contains all the information about playing the songs and moving the motors. wireless.py is for all the protocalls used in the wireless connection. Songs just hold the programmed information about the songs. This part was tricky and this project was used for this part: https://github.com/KasperThorup25/musicgenerator

_2. local files:_
- main.py
- tuning.py
- test.py
- second_ev3.py

These files only run on 1 of the EV3's. But they all use the code fron the universal files (except test.py). second_ev3.py is for the second ev3 which is refeared to as client in this project (the main EV3 is refeared to as server). This program will adapt to what program is running on the server EV3. main.py is the program controlling the song choices and is only run on the server EV3. tuning.py isn't used in the YouTube video, but it's used to tune the glasses water levels and therefore their frequencies. The program allows for just on note to be played when center button is presses. test.py is just a simple test program that can run independent, and runs the motor once when the center button is pressed.

When using the main.py and tunning.py the program will only work if there is a hub running second_ev3.py. 
They will automatically connect, but its important that the second_ev3.py is always turned on last, otherwise the bluetooth connection will fail.

Remeber if the universal files are getting updated (such as adding a song), they need to get uploaded to both EV3's
