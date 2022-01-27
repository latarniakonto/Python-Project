class Button():
    def __init__(self, image, x_coord, y_coord, text, font):
        self.image = image
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.image_rect = self.image.get_rect(center=(self.x_coord, 
                                                      self.y_coord))
        self.text = text
        self.font = font
        self.display_text = self.font.render(self.text, True, (0, 255, 0))
        self.text_rect = self.display_text.get_rect(center=(self.x_coord, 
                                                            self.y_coord))
    def update(self, screen):
        screen.blit(self.image, self.image_rect)
        screen.blit(self.display_text, self.text_rect)

    def is_clicked(self, position):
        return (position[0] in range(self.image_rect.left, 
                                     self.image_rect.right) and
                position[1] in range(self.image_rect.top, 
                                     self.image_rect.bottom))

