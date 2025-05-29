import pygame
import os
import ctypes

def draw_linesR(screen, color, start, end, n, N):
    if n == 1:
        pygame.draw.line(screen, color, start, end, 3)
        n += 1

    elif n > 1 and n < N:
        n += 1

    elif (n > N):
        return
        
        
        


def main():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    #initialize pygame
    screen = pygame.display.set_mode((screen_width,screen_height), pygame.RESIZABLE)
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    clock = pygame.time.Clock()
    run = True

    print("w: " + str(screen_width) + "\n")
    print("h: " + str(screen_height) + "\n")

    x = screen_width / 2
    y = screen_height / 2

    print("x: " + str(x) + "\n")
    print("y: " + str(y) + "\n")


    #pygame.draw.line(screen, (57,255,20), (x,screen_height), (x, y), 3)
    color = (57,255,20)
    start = ((x,screen_height))
    end = (x, y)
    n = 1
    N = 5

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #close if ESC is pressed
                    run = False

        screen.fill("black")

        draw_linesR(screen, color, start, end, n, N)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
