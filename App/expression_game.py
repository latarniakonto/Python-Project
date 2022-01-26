# Import and initialize the pygame library
import pygame
from expression import (
    Constant, Variable,
    Add, Subtract, Times, Divide,
    Instruction, Assign, While, If
)
from expression_formatter import decode_expression
from expression_data_base import (
    init,
    ArithmeticExpression,
    ProgrammingExpression,        
)

def get_expressions_from_data_base(session):    
    expressions = []

    for row in session.query(ArithmeticExpression):
        e = decode_expression(row.expression_encoding)        
        expressions.append(e)
    for row in session.query(ProgrammingExpression):        
        e = decode_expression(row.expression_encoding)        
        expressions.append(e)

    return expressions

def print_expressions():
    pos_x = 30
    pos_y = 40          

    e_iter = 0    
    for e in expressions: 
        e_text = str(e)        
        lines = []        
        line = ""
        # pygame doesn't support newlines :(, so here is solution for that
        for char in e_text:            
            if char == '\n':                
                lines.append(font.render(line, True, (0, 255, 0)))
                line = ""
            else:
                line += char
        if line != "":
            lines.append(font.render(line, True, (0, 255, 0)))                        
        
        for line in range(len(lines)):            
            screen.blit(lines[line],(pos_x, pos_y + ((e_iter + line) * 2 * font_size)))
        e_iter = len(lines) + 1

        


database_session = init()
pygame.init()
# Set up the drawing window
screen = pygame.display.set_mode([1000, 1000])
# Run until the user asks to quit
running = True
font_size = 12
font = pygame.font.Font("./Font/expression_font.ttf", font_size)
expressions = get_expressions_from_data_base(database_session)

while running:

    # Fill the background with white
    screen.fill((0, 0, 0))

    # Did the user click the window close button?

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    print_expressions()
    # Flip the display
    pygame.display.flip()

pygame.quit()
