
# Import and initialize the pygame library
import pygame

pygame.init()
# Set up the drawing window
screen = pygame.display.set_mode([1000, 1000])
# Run until the user asks to quit
running = True
font = pygame.font.Font("./Font/expression_font.ttf", 12)

while running:

    # Fill the background with white
    screen.fill((0, 0, 0))

    # Did the user click the window close button?

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    text = font.render("while (x!=3)", True, (0, 255, 0))
    screen.blit(text, (300, 400))
    # Flip the display
    pygame.display.flip()

pygame.quit()
