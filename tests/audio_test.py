def playSound():
    print('playing sound')
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load("audio/single-dog-bark-king-charles-spaniel-41366.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    print('finished playing sound')

playSound()