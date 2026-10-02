import sys
import select
import random
import vlc
import time
from evdev import InputDevice, ecodes

MOUSE_DEVICE = (
    "/dev/input/by-id/"
    "usb-YICHIP_Trust_Wireless_Silent_Mouse-if01-event-mouse"
)
mouse = InputDevice(MOUSE_DEVICE)
songnumbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
random.shuffle(songnumbers)
playlist = ["Arctic Monkeys - 505", "LINKIN PARK - Crawling", "LINKIN PARK - Faint", "LINKIN PARK - Given Up", "LINKIN PARK - In The End", "LINKIN PARK - Numb", "LINKIN PARK - One Step Closer", "LINKIN PARK - The Emptiness Machine", "LINKIN PARK - What I've Done", "Nirvana - All Apologies", "Nirvana - Come As You Are", "Nirvana - Heart-Shaped Box", "Nirvana - Lithium", "Nirvana - Rape Me", "Nirvana - Smells Like Teen Spirit", "overtonight - elephant cage", "overtonight - ghost party", "overtonight - mirrors demo", "overtonight - poem", "overtonight - they'll post it online", "Penelope Scott - Rat", "Radiohead - Creep", "Radiohead - Exit Music (for a film)", "Radiohead - Let Down", "Radiohead - No Surprises", "s0rrow - fake ur face", "s0rrow - stalk ur socials", "s0rrow - unhappy", "The Killers - Mr. Brightside", "The Long Faces - Jane!", "TV Girl - it almost worked", "TV Girl - Lovers Rock", "TV Girl - Not Allowed"]
songnumber = 0
volume = 60

player = vlc.MediaPlayer()
player.audio_set_volume(volume)


while True:
    time.sleep(0.1)
    if songnumber > 0 or songnumber == 0:
        songnumber = songnumber + 1
    else:
        songnumber = 0
    player = vlc.MediaPlayer("/home/Freek/mp3s/Mp3s/" + playlist[songnumbers[songnumber]] + ".ogg")
    player.play()
    print(songnumber)
    print("Playing " + playlist[songnumbers[songnumber]])
    print("Press Middle Mouse Button to pause/resume, Left/Right Mouse Button to go forward/back song, or Q to quit.")

    running = True
    paused = False
    
    left_pressed = False
    right_pressed = False
    while running:
        readable, _, _ = select.select([mouse.fd], [], [], 0.2)
        if readable:
            if player.get_state() == "State.Ended":
                running = False
            for event in mouse.read():
                if event.type == ecodes.EV_REL:
                    if event.code == ecodes.REL_WHEEL:
                        if event.value > 0:
                            volume = min(100, volume + 5)
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
                        if right_pressed:
                            print("exiting")
                            player.stop()
                            mouse.close()
                            sys.exit()
                        songnumber = songnumber - 2
                        player.stop()
                        running = False
                    elif released:
                        left_pressed = False
                elif event.code == ecodes.BTN_RIGHT:
                    if pressed:
                        right_pressed = True
                        if left_pressed:
                            print("exiting")
                            player.stop
                            pygame.quit()
                            sys.exit()
                        player.stop()
                        running = False
                    elif released:
                        right_pressed = False
                elif event.code == ecodes.BTN_MIDDLE and pressed:
                    player.pause()
            
