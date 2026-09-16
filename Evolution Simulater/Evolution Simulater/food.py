
import random
import pygame



# Food Class -------------------------------------------------------------------------------------------

class Food(pygame.sprite.Sprite):

    def __init__(self, x, y, config):
        super().__init__()

        self.cnf = config

        self.x = x
        self.y = y

        self.base_color = self.cnf.food_color
        self.color = self.base_color

        self.energy = random.randint(100, 500)

        # Sprite image
        self.image = pygame.Surface(
            (self.cnf.food_width, self.cnf.food_height),
            pygame.SRCALPHA
        )

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        self.update_color()


    def update_color(self):

        factor = max(self.energy / 500, 0)

        r = int(self.base_color[0] * factor)
        g = int(self.base_color[1] * factor)
        b = int(self.base_color[2] * factor)

        self.color = (r, g, b)

        self.image.fill((0, 0, 0, 0))

        pygame.draw.rect(
            self.image,
            self.color,
            self.image.get_rect()
        )


    def update(self):
        #self.update_color()
        pass





