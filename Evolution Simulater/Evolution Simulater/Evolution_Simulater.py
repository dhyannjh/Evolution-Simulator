# Evolution Simulator Post HYE project

import pygame
import random
import math


# Constants -------------------------------------------------------------------------------------------

# Colors
ENTITY_COLOR = (130, 180, 120)
FOOD_COLOR = (14, 240, 108)

# Dimensions
HEIGHT, WIDTH = 600, 600

ENTITY_RADIUS = 10
FOOD_WIDTH = 8
FOOD_HEIGHT = 15


# Data 


# Pygame Stuff -------------------------------------------------------------------------------------------

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Font Stuff:

pygame.font.init()

font = pygame.font.SysFont("Arial", 24)   # name, size

# Labels:
entity_counter = font.render("Entities: 0", True, (255, 255, 255))


# Entity Class -------------------------------------------------------------------------------------------

class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        # Position
        self.x = x
        self.y = y

        # Gene Pool
        self.speed = 4
        self.max_energy = 500
        self.reproduction_rate = 500
        self.base_color = ENTITY_COLOR

        # Appearance
        self.color = self.base_color

        # Movement
        self.dx = random.choice([-1, 0, 1])
        self.dy = random.choice([-1, 0, 1])

        # Energy
        self.energy = self.max_energy
        self.alive = True

        # Reproduction
        self.can_reproduce = True
        self.reproduction_cooldown = 120
        self.reproduction_timer = random.randint(0, self.reproduction_cooldown)

        # Sprite image
        self.image = pygame.Surface(
            (ENTITY_RADIUS * 2, ENTITY_RADIUS * 2),
            pygame.SRCALPHA
        )

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.update_color()


    def update_color(self):
        # Scale brightness based on energy
        factor = max(self.energy / self.max_energy, 0)

        r = int(self.base_color[0] * factor)
        g = int(self.base_color[1] * factor)
        b = int(self.base_color[2] * factor)

        self.color = (r, g, b)

        # Rebuild sprite image
        self.image.fill((0, 0, 0, 0))

        pygame.draw.circle(
            self.image,
            self.color,
            (ENTITY_RADIUS, ENTITY_RADIUS),
            ENTITY_RADIUS
        )


    def move(self):

        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        # Bounce
        if self.x < ENTITY_RADIUS or self.x > WIDTH - ENTITY_RADIUS:
            self.dx *= -1

        if self.y < ENTITY_RADIUS or self.y > HEIGHT - ENTITY_RADIUS:
            self.dy *= -1

        # Keep inside screen
        self.x = max(ENTITY_RADIUS, min(self.x, WIDTH - ENTITY_RADIUS))
        self.y = max(ENTITY_RADIUS, min(self.y, HEIGHT - ENTITY_RADIUS))

        # Update sprite position
        self.rect.center = (self.x, self.y)

        # Energy loss
        self.energy -= 1


    def get_color(self, mutation):
        (r, g, b) = self.base_color

        r += mutation * -5

        if r < 0:
            r = 0
        if r > 255:
            r = 255

        return (r, g, b)
        

    def reproduce(self):
        
        child = Entity(self.x, self.y)
        choice = random.choice([-1, 0, 1])

        if choice == -1:
            child.speed = self.speed - random.uniform(0, 1)

            child.max_energy = self.max_energy - random.uniform(0, 1)
            if child.max_energy <= 0:
                child.max_energy = 100

            child.reproduction_rate = self.reproduction_rate + random.randint(1, 100)


        elif choice == 1:
            child.speed = self.speed + random.uniform(0, 1)

            child.max_energy = self.max_energy + random.uniform(0, 1)

            child.reproduction_rate = self.reproduction_rate - random.randint(1, 100)
            if child.reproduction_rate <= 0:
                child.reproduction_rate = 100


        else:
            child.speed = self.speed

            child.max_energy = self.max_energy

            child.reproduction_rate = self.reproduction_rate


        child.base_color = self.get_color(choice)

        child.energy = child.max_energy
        child.update_color()
        self.energy *= 3/5
        return child

    def update(self):

        # Die
        if self.energy <= 0:
            self.alive = False
            self.kill()
            return

        # Occasionally change direction
        if random.randint(1, 30) == 5:

            if self.dx == 0:
                self.dx = random.choice([1, -1])

            self.dx *= random.choice([-1, 0])


        if random.randint(1, 30) == 7:

            if self.dy == 0:
                self.dy = random.choice([1, -1])

            self.dy *= random.choice([-1, 0])


        # Reproduce
        if self.energy > (self.max_energy / 2) and random.randint(1, self.reproduction_rate) == 7 and self.reproduction_timer <= 0:
            self.can_reproduce = True
            self.reproduction_timer = self.reproduction_cooldown
        else:
            self.can_reproduce = False

        self.reproduction_timer -= 1
        self.move()
        self.update_color()


# Food Class -------------------------------------------------------------------------------------------

class Food(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

        self.base_color = FOOD_COLOR
        self.color = self.base_color

        self.energy = random.randint(100, 500)

        # Sprite image
        self.image = pygame.Surface(
            (FOOD_WIDTH, FOOD_HEIGHT),
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


# Creation Functions -------------------------------------------------------------------------------------------

def create_entities(number):

    for i in range(number):

        entity = Entity(
            random.randint(ENTITY_RADIUS, WIDTH - ENTITY_RADIUS),
            random.randint(ENTITY_RADIUS, HEIGHT - ENTITY_RADIUS)
        )

        entities.add(entity)


def create_food_item():

    food = Food(
        random.randint(0, WIDTH - FOOD_WIDTH),
        random.randint(0, HEIGHT - FOOD_HEIGHT)
    )

    food_items.add(food)


# Sprite Groups -------------------------------------------------------------------------------------------

entities = pygame.sprite.Group()
food_items = pygame.sprite.Group()


create_entities(200)# ------------------- NUMBER OF ENTITIES SPAWNED


# Main Loop -------------------------------------------------------------------------------------------

running = True

while running:

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


    # Update entities
    entities.update()

    # Update food
    #food_items.update()

    # Eat Food and reproduce:
    for entity in entities:
        if entity.can_reproduce:
            child = entity.reproduce()
            entities.add(child)

        collided_sprite = pygame.sprite.spritecollide(entity, food_items, True)

        for food in collided_sprite:
            entity.energy += food.energy

            if entity.energy > entity.max_energy:
                entity.energy = entity.max_energy


    # Spawn food
    if random.randint(1, 10) == 7:
        create_food_item()


    # Labels
    entity_counter = font.render("Entities: " + str(len(entities)), True, (255, 255, 255))

    # Drawing
    screen.fill((0, 0, 0))

    entities.draw(screen)
    food_items.draw(screen)

    screen.blit(entity_counter, (10, 10))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()