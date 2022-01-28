# Import and initialize the pygame library
import queue
import pygame
import time
import random
from threading import Thread
from expression import (
    Constant, Variable,
    Add, Subtract, Times, Divide,
    Instruction, Assign, While, If
)
from expression_data_base import (
    init,
    ArithmeticExpression,
    ProgrammingExpression,
    get_expressions_from_data_base

)
from expression_game_input import get_user_input
from expression_game_button import Button
from expression_game_message import display_messages


def get_expressions_lines():        
    expressions_lines = [[]]
    
    for e in expressions: 
        e_text = str(e)  
        lines = []
        line = ""
        # pygame font doesn't support newlines :(, so here is solution for that
        for char in e_text:
            if char == '\n':                
                lines.append(font.render(line, True, (0, 255, 0)))
                line = ""                
            else:
                line += char
        if line != "":            
            lines.append(font.render(line, True, (0, 255, 0)))
        lines.append(font.render(" ", True, (0, 255, 0)))
        lines.append(font.render(" ", True, (0, 255, 0)))
        expressions_lines.append(lines)
    return expressions_lines


def get_expressions_solution():
    global expressions_solution, solve_for_number

    print(solve_for_number)
    for e in expressions:
        if e.class_name == "Instruction":
            x_dict = {}
            e.run(x_dict)
            expressions_solution += str(int(x_dict["x"]))
            expressions_solution += "!"
        else:   
            x_value = e.evaluate({"x" : solve_for_number})
            expressions_solution += str(int(x_value))
            expressions_solution += "!"
    print(expressions_solution)
    expressions_solution = expressions_solution[:-1]
    expressions_solution += "\n"        
    solve_for_number = random.randint(1, 10)    


def display_expressions():
    pos_x = 30
    pos_y = 40

    e_iter = 0    
    for lines in expressions_lines:                 
        # pygame font doesn't support newlines :(, so here is solution for that                
        for line in range(len(lines)):
            screen.blit(lines[line],(pos_x, pos_y + ((e_iter + line) * 2 * font_size)))        
        e_iter += len(lines)


def display_flickering_dots():    
    global first_dot, second_dot, third_dot, fourth_dot
        
    if first_dot is False:
        first_dot = True
        screen.blit(dots[0], (30, 740))
    elif second_dot is False:
        second_dot = True
        screen.blit(dots[0], (46, 740))
    elif third_dot is False:
        third_dot = True
        screen.blit(dots[0], (62, 740))
    elif fourth_dot is False:
        fourth_dot = True

    if fourth_dot is True:
        first_dot = False
        screen.blit(dots[1], (30, 700))
        second_dot = False
        screen.blit(dots[1], (46, 740))
        third_dot = False
        screen.blit(dots[1], (62, 740))
        fourth_dot = False
        return

    if first_dot is True:
        screen.blit(dots[0], (30, 740))
    if second_dot is True:
        screen.blit(dots[0], (46, 740))
    if third_dot is True:
        screen.blit(dots[0], (62, 740))


def display_input():
    global first_dot, second_dot, third_dot, fourth_dot

    if first_dot is True:
        first_dot = False
        screen.blit(dots[0], (30, 740))
    if second_dot is True:
        second_dot = False
        screen.blit(dots[0], (46, 740))
    if third_dot is True:
        third_dot = False
        screen.blit(dots[0], (62, 740))
    if fourth_dot is True:
        fourth_dot = False

    display_input = font.render(input, True, (0, 255, 0))
    screen.blit(display_input, (30, 740))


def menu_scene():
    global running
    while running:
        # Fill the background with black
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_clicked = play_button.is_clicked(pygame.mouse.get_pos())
                if play_clicked:
                    return False
                # running = is_clicked() was laggy
                exit_clicked = exit_button.is_clicked(pygame.mouse.get_pos())
                if exit_clicked:
                    running = False

        play_button.update(screen)
        exit_button.update(screen)
        pygame.display.flip()
    return False


def game_scene():
    global running, input, expressions_lines, expression_solution_thread
    global expressions_solution
    expressions_lines = get_expressions_lines()
    expression_solution_thread = Thread(target=get_expressions_solution)
    expression_solution_thread.start()
    while running:
    # Fill the background with black
        screen.fill((0, 0, 0))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu_clicked = menu_button.is_clicked(pygame.mouse.get_pos())                
                if menu_clicked:
                    expression_solution_thread.join()                    
                    return False
            input = get_user_input(event, input)
            if len(input) > 0 and input[-1] == "\n":
                expression_solution_thread.join()
                if input == expressions_solution:                    
                    print("poprawne")
                expressions_solution = ""
                input = ""
                return False

        screen.blit(input_image, (25,740))
        display_expressions()        
        display_messages(screen, font)
        menu_button.update(screen)
        if input == "":
            if pygame.time.get_ticks() % 240 == 0:
                display_flickering_dots()
            else:
                continue
        else:
            display_input()
        # Flip the display
        pygame.display.flip()
    return False
    

## def start():
q = queue.Queue()
database_session = init()
pygame.init()
screen = pygame.display.set_mode([1000, 1000])
running = True
font_size = 12
font = pygame.font.Font("./Font/expression_font.ttf", font_size)
expressions = []
expressions_thread = Thread(target=get_expressions_from_data_base, args=(database_session, q))
expressions_thread.start()
expressions_lines = [[]]
expressions_solution = ""
expressions_solution_thread = None
dots = [font.render(".", True, (0, 255, 0)),        
        font.render(" ", True, (0, 255, 0))]
first_dot = False
second_dot = False
third_dot = False
fourth_dot = False
input = ""
input_image = pygame.image.load("./Sprites/input_sprite.png")
menu_active = True
game_active = False
button_image = pygame.image.load("./Sprites/button_sprite.png")
play_button = Button(button_image, 50, 40, "play", font)
exit_button = Button(button_image, 50, 72, "exit", font)
menu_button = Button(button_image, 75, 787, "menu", font)
solve_for_number = random.randint(1, 10)


## def update():
while running:
    if menu_active:
        menu_active = menu_scene()
        game_active = menu_active == False and running == True
        if len(expressions) == 0:
            expressions_thread.join()
            expressions = q.get()        
    if game_active:
        game_active = game_scene()
        menu_active = game_active == False and running == True
    

# def on_exit():
# expression_solution_thread.join()
pygame.quit()
database_session.close()
