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


database_session = init()
pygame.init()
# Set up the drawing window
screen = pygame.display.set_mode([1000, 1000])
# Run until the user asks to quit
running = True
font = pygame.font.Font("./Font/expression_font.ttf", 12)
expressions = get_expressions_from_data_base(database_session)

while running:

    # Fill the background with white
    screen.fill((0, 0, 0))

    # Did the user click the window close button?

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
    text = font.render(str(expressions[1]), True, (0, 255, 0))
    screen.blit(text, (30, 40))
    # Flip the display
    pygame.display.flip()

pygame.quit()
