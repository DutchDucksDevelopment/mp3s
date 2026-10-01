import sys
import pygame
import random
import vlc
import time

songnumbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
random.shuffle(songnumbers)
playlist = ["Arctic Monkeys - 505", "LINKIN PARK - Crawling", "LINKIN PARK - Faint", "LINKIN PARK - Given Up", "LINKIN PARK - In The End", "LINKIN PARK - Numb", "LINKIN PARK - One Step Closer", "LINKIN PARK - The Emptiness Machine", "LINKIN PARK - What I've Done", "Nirvana - All Apologies", "Nirvana - Come As You Are", "Nirvana - Heart-Shaped Box", "Nirvana - Lithium", "Nirvana - Rape Me", "Nirvana - Smells Like Teen Spirit", "overtonight - elephant cage", "overtonight - ghost party", "overtonight - mirrors demo", "overtonight - poem", "overtonight - they'll post it online", "Penelope Scott - Rat", "Radiohead - Creep", "Radiohead - Exit Music (for a film)", "Radiohead - Let Down", "Radiohead - No Surprises", "s0rrow - fake ur face", "s0rrow - stalk ur socials", "s0rrow - unhappy", "The Killers - Mr. Brightside", "The Long Faces - Jane!", "TV Girl - it almost worked", "TV Girl - Lovers Rock", "TV Girl - Not Allowed"]
songnumber = 0

pygame.init()

# Initialize the music mixer
pygame.mixer.init()
player = vlc.MediaPlayer("/home/Freek/mp3s/Mp3s/" + playlist[songnumbers[songnumber]] + ".ogg")
player.play()
print(songnumber)
print("Playing " + playlist[songnumbers[songnumber]])
print("Press Middle Mouse Button to pause/resume, S to skip song, or Q to quit.")
# Create a window
screen = pygame.display.set_mode((1280, 1024), pygame.RESIZABLE)
pygame.display.set_caption("Mp3 Player")

while True:
    time.sleep(0.1)
    if player.get_state() == vlc.State.Ended or player.get_state() == vlc.State.Stopped:
        if not songnumber < 0:
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
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.stop()
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    player.pause()

                elif event.button == 3:
                    player.stop()
                    running = False
                    
                elif event.button == 1:
                    songnumber = songnumber - 2
                    player.stop()
                    running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player.stop
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    volume += 5
                elif event.button == 5:
                    volume -= 5

                volume = max(0, min(100, volume))
                player.audio_set_volume(volume)

player.stop
pygame.quit()
sys.exit()
