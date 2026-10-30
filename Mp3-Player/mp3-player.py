import sys
from pypresence import Presence
import subprocess
import select
import random
import vlc
import time
import os
from evdev import InputDevice, ecodes

time.sleep(2)

# Replace with your Application ID
APPLICATION_ID = '1565806266461458472'

# Initialize the RPC
RPC = Presence(APPLICATION_ID)
RPC.connect()

# def bluecheck():
#    result = subprocess.run(
#        ["bluetoothctl", "devices", "Connected"],
#        capture_output=True,
#        text=True,
#        timeout=5,
#    )
#    return bool(result.stdout.strip())

MOUSE_DEVICE = (
    "/dev/input/by-id/"
    "usb-YICHIP_Trust_Wireless_Silent_Mouse-if01-event-mouse"
)
mouse = InputDevice(MOUSE_DEVICE)
playlist = os.listdir("/home/Freek/mp3s/Mp3s/")
songnumbers = list(range(0,len(playlist)))
random.shuffle(songnumbers)
songnumber = 0


volume = 100

player = vlc.MediaPlayer()
player.audio_set_volume(volume)

def checkadapter():
    """Check if wlan0 interface exists"""
    try:
        result = subprocess.run(['iwconfig', 'wlan0'],
                              capture_output=True, text=True, timeout=3)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except FileNotFoundError:
        return False
def checkwifi():
    """Check internet connection by pinging Google"""
    try:
        # Ping Google's DNS server (8.8.8.8) with 1 packet
        result = subprocess.run(['ping', '-c', '1', '-W', '2', '8.8.8.8'],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False
print(checkwifi())
print(checkadapter())

useWifi = checkadapter()

def shutdown():
    print("shutdown")
    player.stop()
    mouse.close()
    try:
        subprocess.run(["sudo", "shutdown", "-P", "now"], check=True)
    except:
        sys.exit()

while True:
    print("new song")
    time.sleep(0.1)
    if songnumber > -1 or songnumber < 33:
        songnumber = songnumber + 1
    else:
        songnumber = 0
    media = vlc.Media("/home/Freek/mp3s/Mp3s/" + playlist[songnumbers[songnumber]])
    player = vlc.MediaPlayer()
    media.parse()
    player.set_media(media)
    player.play()
    player.audio_set_volume(0)
    time.sleep(2)
    player.audio_set_volume(volume)
    player.set_time(0)
    print(songnumber)
    print("Playing " + playlist[songnumbers[songnumber]])
    print("Press Middle Mouse Button to pause/resume, Left/Right Mouse Button to go forward/back song, or Q to quit.")
	
	if useWifi:
		RPC.update(
			state="Playing " + playlist[songnumbers[songnumber]],
			details="Custom mp3 player made with a raspberry pi 2"
		)
    running = True
    paused = False
    
    left_pressed = False
    right_pressed = False
    while running:
        if player.get_state() == vlc.State.Ended:
            running = False
        readable, _, _ = select.select([mouse.fd], [], [], 0.2)
        if readable:
            for event in mouse.read():
                if event.type == ecodes.EV_REL:
                    if event.code == ecodes.REL_WHEEL:
                        if event.value > 0:
                            volume = min(150, volume + 5)
                        elif event.value < 0:
                            volume = max(0, volume - 5)
                        player.audio_set_volume(volume)
                if event.type != ecodes.EV_KEY:
                    continue
                pressed = event.value == 1
                released = event.value == 0
                if event.code == ecodes.BTN_LEFT:
                    if pressed:
                        left_pressed = True
                        time.sleep(0.05)
                        if right_pressed:
                            shutdown()
                        songnumber = songnumber - 2
                        player.stop()
                        running = False
                    elif released:
                        left_pressed = False
                elif event.code == ecodes.BTN_RIGHT:
                    if pressed:
                        print("next pressed")
                        right_pressed = True
                        if left_pressed:
                            shutdown()
                        player.stop()
                        running = False
                    elif released:
                        right_pressed = False
                elif event.code == ecodes.BTN_MIDDLE and pressed:
                    player.pause()
            
