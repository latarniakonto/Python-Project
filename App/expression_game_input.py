import pygame

def get_user_input(event):
    input = ""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_0:
            input += "0"
        return input
    else:
        return input