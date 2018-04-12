import pygame


def main():

    pygame.init()
    screen = pygame.display.set_mode((800,600))
    running = True
    screen.fill((0,0,0))

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        x_res = 5
        y_res = 5
        cell_width  = screen.get_width()/x_res
        cell_height = screen.get_height()/y_res

        for v in range(y_res):
            for u in range(x_res):
                color = pygame.Color(0)
                color.hsva = (v*u*(360/(y_res*x_res)), 50, 50, 50)
                pygame.draw.rect(screen, color, (v*cell_width, u*cell_height, cell_width, cell_height))

        pygame.display.flip()


if __name__=="__main__":
    main()
