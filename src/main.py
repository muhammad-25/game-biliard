import pygame #import pygame

# inisialisasi pygame
pygame.init()
pygame.display.set_mode((400, 500))
pygame.display.set_caption('Billiard Game')

def main():
    running = True

    while running:

        for event in pygame.event.get():
      
            if event.type == pygame.QUIT:
                running = False

if __name__=='__main__': main()
