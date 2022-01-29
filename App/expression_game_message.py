

def display_messages(screen, font, expressions, solve_for_number):
    text = "solve this expression for x = " + str(solve_for_number)
    message_1 = font.render(text, True, (0, 255, 0))
    screen.blit(message_1, (30, 15))

    text = "solve this expression" 
    message_2 = font.render(text, True, (0, 255, 0))
    screen.blit(message_2, (30, 85))

    text = "what is x value after running this code?"
    message_3 = font.render(text, True, (0, 255, 0))
    screen.blit(message_3, (30, 155))
    screen.blit(message_3, (30, 275))
    screen.blit(message_3, (30, 490))

    text = "type answers in order"
    message_4 = font.render(text, True, (0, 255, 0))
    screen.blit(message_4, (430, 740))

    text = "seperate answers using !"
    message_4 = font.render(text, True, (0, 255, 0))
    screen.blit(message_4, (430, 770))

    text = "exclude the last one"
    message_4 = font.render(text, True, (0, 255, 0))
    screen.blit(message_4, (430, 800))

    text = "press enter to submit"
    message_4 = font.render(text, True, (0, 255, 0))
    screen.blit(message_4, (430, 830))







    
    
