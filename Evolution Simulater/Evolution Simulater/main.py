# Evolution Simulator Post HYE project

import pygame
import random
import matplotlib.pyplot as plt

from entity import Entity
from food import Food
from config import Configuration
from Astatistics import Statistics


# Constants -------------------------------------------------------------------------------------------

cnf = Configuration()


# Data ---------------------------------------------------------------------------------------------------

stats = Statistics(cnf)

# Pygame Stuff -------------------------------------------------------------------------------------------

pygame.init()

screen = pygame.display.set_mode((cnf.width, cnf.height))
clock = pygame.time.Clock()

# Font Stuff:

pygame.font.init()

font = pygame.font.SysFont("Arial", 24)   # name, size

# Labels:
entity_counter = font.render("Entities: 0", True, (255, 255, 255))


# Creation Functions -------------------------------------------------------------------------------------------

def create_entities(number):

    for i in range(number):

        entity = Entity(
            random.randint(cnf.entity_radius, cnf.width - cnf.entity_radius),
            random.randint(cnf.entity_radius, cnf.height - cnf.entity_radius), 
            cnf
        )

        entities.add(entity)


def create_food_item():

    food = Food(
        random.randint(0, cnf.width - cnf.food_width),
        random.randint(0, cnf.height - cnf.food_height), 
        cnf
    )

    food_items.add(food)


# Sprite Groups -------------------------------------------------------------------------------------------

entities = pygame.sprite.Group()
food_items = pygame.sprite.Group()


create_entities(1000)# ------------------- NUMBER OF ENTITIES SPAWNED


# Main Loop -------------------------------------------------------------------------------------------

running = True
last_time = pygame.time.get_ticks()
seconds_counter = 0

while running:

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


    # Update entities + Store Data
    now = pygame.time.get_ticks()
    if now - last_time >= 1000:   # 1000 ms = 1 second
        #print("One second passed!")
        last_time = now
        seconds_counter += 1
        
        stats.record_data(entities, seconds_counter)


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


print(stats.time_data)
print(stats.average_speed_data)
print(stats.population_data)

pygame.quit()

plt.subplot(2, 1, 1)
plt.plot(stats.time_data, stats.average_speed_data)

plt.xlabel("Time")
plt.ylabel("Average Speed")

#plt.show()

plt.subplot(2, 1, 2)
plt.plot(stats.time_data, stats.population_data)

plt.xlabel("Time")
plt.ylabel("Population")

plt.show()