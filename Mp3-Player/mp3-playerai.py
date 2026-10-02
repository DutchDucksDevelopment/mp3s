#!/usr/bin/env python3

import os
import sys
import time
import random
import signal
import select

import vlc
from evdev import InputDevice, ecodes


# Use the stable path from /dev/input/by-id/.
# Change this to match your mouse.
MOUSE_DEVICE = (
    "/dev/input/by-id/"
    "usb-YICHIP_Trust_Wireless_Silent_Mouse-if01-event-mouse"
)

MUSIC_DIR = "/home/Freek/mp3s/Mp3s"
VOLUME = 20


playlist = [
    "Arctic Monkeys - 505",
    "LINKIN PARK - Crawling",
    "LINKIN PARK - Faint",
    "LINKIN PARK - Given Up",
    "LINKIN PARK - In The End",
    "LINKIN PARK - Numb",
    "LINKIN PARK - One Step Closer",
    "LINKIN PARK - The Emptiness Machine",
    "LINKIN PARK - What I've Done",
    "Nirvana - All Apologies",
    "Nirvana - Come As You Are",
    "Nirvana - Heart-Shaped Box",
    "Nirvana - Lithium",
    "Nirvana - Rape Me",
    "Nirvana - Smells Like Teen Spirit",
    "overtonight - elephant cage",
    "overtonight - ghost party",
    "overtonight - mirrors demo",
    "overtonight - poem",
    "overtonight - they'll post it online",
    "Penelope Scott - Rat",
    "Radiohead - Creep",
    "Radiohead - Exit Music (for a film)",
    "Radiohead - Let Down",
    "Radiohead - No Surprises",
    "s0rrow - fake ur face",
    "s0rrow - stalk ur socials",
    "s0rrow - unhappy",
    "The Killers - Mr. Brightside",
    "The Long Faces - Jane!",
    "TV Girl - it almost worked",
    "TV Girl - Lovers Rock",
    "TV Girl - Not Allowed",
]


song_order = list(range(len(playlist)))
random.shuffle(song_order)

song_position = 0
running = True
left_pressed = False
right_pressed = False


def stop_program(signum=None, frame=None):
    global running
    running = False


def song_path():
    song_index = song_order[song_position]
    filename = playlist[song_index] + ".ogg"
    return os.path.join(MUSIC_DIR, filename)


def play_current_song(vlc_instance):
    global player

    path = song_path()
    print(f"Playing: {path}", flush=True)

    if not os.path.isfile(path):
        print(f"File not found: {path}", flush=True)
        return

    if player is not None:
        player.stop()
        player.release()

    player = vlc_instance.media_player_new()
    player.set_media(vlc_instance.media_new(path))
    player.audio_set_volume(VOLUME)
    player.play()

    # VLC needs a short moment before some state operations work reliably.
    time.sleep(0.2)


def next_song(vlc_instance):
    global song_position

    song_position = (song_position + 1) % len(song_order)
    play_current_song(vlc_instance)


def previous_song(vlc_instance):
    global song_position

    song_position = (song_position - 1) % len(song_order)
    play_current_song(vlc_instance)


# Handle Ctrl+C and systemd termination cleanly.
signal.signal(signal.SIGINT, stop_program)
signal.signal(signal.SIGTERM, stop_program)

if not os.path.exists(MOUSE_DEVICE):
    print(f"Mouse device not found: {MOUSE_DEVICE}", file=sys.stderr)
    print("Available devices:", file=sys.stderr)
    print(os.listdir("/dev/input/by-id"), file=sys.stderr)
    sys.exit(1)

try:
    mouse = InputDevice(MOUSE_DEVICE)
except PermissionError:
    print(
        "Permission denied reading the mouse. Add the service user to "
        "the input group.",
        file=sys.stderr,
    )
    sys.exit(1)

print(f"Using mouse: {mouse.name}", flush=True)

vlc_instance = vlc.Instance("--no-video")
player = None

play_current_song(vlc_instance)

try:
    while running:
        # Read mouse events without blocking forever. The timeout lets us
        # check whether the current VLC song has ended.
        readable, _, _ = select.select([mouse.fd], [], [], 0.2)

        if readable:
            for event in mouse.read():
                if event.type != ecodes.EV_KEY:
                    continue

                pressed = event.value == 1
                released = event.value == 0

                if event.code == ecodes.BTN_LEFT:
                    if pressed:
                        left_pressed = True

                        # Left + right quits.
                        if right_pressed:
                            print("Quit combination detected", flush=True)
                            running = False
                            break

                        previous_song(vlc_instance)

                    elif released:
                        left_pressed = False

                elif event.code == ecodes.BTN_RIGHT:
                    if pressed:
                        right_pressed = True

                        # Left + right quits.
                        if left_pressed:
                            print("Quit combination detected", flush=True)
                            running = False
                            break

                        next_song(vlc_instance)

                    elif released:
                        right_pressed = False

                elif event.code == ecodes.BTN_MIDDLE and pressed:
                    if player is not None:
                        state = player.get_state()

                        if state == vlc.State.Playing:
                            player.pause()
                            print("Paused", flush=True)
                        elif state == vlc.State.Paused:
                            player.play()
                            print("Resumed", flush=True)

        if not running:
            break

        # Automatically start the next song.
        if player is not None:
            state = player.get_state()

            if state in (vlc.State.Ended, vlc.State.Stopped):
                next_song(vlc_instance)

finally:
    print("Stopping player", flush=True)

    if player is not None:
        player.stop()
        player.release()

    mouse.close()
    vlc_instance.release()