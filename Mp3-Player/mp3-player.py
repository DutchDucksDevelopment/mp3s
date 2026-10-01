import sys
import pygame
import random

songnumbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
playlist = ["Arctic Monkeys - 505", "LINKIN PARK - Crawling", "LINKIN PARK - Faint", "LINKIN PARK - Given Up", "LINKIN PARK - In The End", "LINKIN PARK - Numb", "LINKIN PARK - One Step Closer", "LINKIN PARK - The Emptiness Machine", "LINKIN PARK - What I've Done", "Nirvana - All Apologies", "Nirvana - Come As You Are", "Nirvana - Heart-Shaped Box", "Nirvana - Lithium", "Nirvana - Rape Me", "Nirvana - Smells Like Teen Spirit", "overtonight - elephant cage", "overtonight - ghost party", "overtonight - mirrors demo", "overtonight - poem", "overtonight - they'll post it online", "Penelope Scott - Rat", "Radiohead - Creep", "Radiohead - Exit Music (for a film)", "Radiohead - Let Down", "Radiohead - No Surprises", "s0rrow - fake ur face", "s0rrow - stalk ur socials", "s0rrow - unhappy", "The Killers - Mr. Brightside", "The Long Faces - Jane!", "TV Girl - it almost worked", "TV Girl - Lovers Rock", "TV Girl - Not Allowed"]
songnumber = random.choice(songnumbers)
songnumbers.remove(songnumber)


pygame.init()

# Initialize the music mixer
pygame.mixer.init()

# Create a window
screen = pygame.display.set_mode((500, 300), pygame.RESIZABLE)
pygame.display.set_caption("Mp3 Player")

while True:
    print(songnumber)
    print(playlist[songnumber])
    pygame.mixer.music.load("/home/Freek/mp3s/Mp3s/" + playlist[songnumber] + ".ogg")
    pygame.mixer.music.play()
    
    print("Playing " + playlist[songnumber])
    print("Press P to pause/resume, S to skip song, or Q to quit.")

    running = True
    paused = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if paused:
                        pygame.mixer.music.unpause()
                        paused = False
                    else:
                        pygame.mixer.music.pause()
                        paused = True

                elif event.key == pygame.K_s:
                    pygame.mixer.music.stop()

                elif event.key == pygame.K_q:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

    # Keep the program alive until the music finishes
        if not pygame.mixer.music.get_busy() and not paused:
            running = False
    if not len(songnumbers) == 0:
        songnumber = random.choice(songnumbers)
        songnumbers.remove(songnumber)
    else:
        songnumbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
        songnumber = random.choice(songnumbers)
        songnumbers.remove(songnumber)
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
