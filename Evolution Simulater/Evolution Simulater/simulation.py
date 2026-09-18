
import pygame
import random

from entity import Entity
from food import Food

class Simulation:
    
    def __init__(self, config):

        # Sprite Groups -------------------------------------------------------------------------------------------

        self.entities = pygame.sprite.Group()
        self.food_items = pygame.sprite.Group()
        self.cnf = config


    # Creation Functions -------------------------------------------------------------------------------------------

    def create_entities(self, number):

        for i in range(number):

            entity = Entity(
                random.randint(self.cnf.entity_radius, self.cnf.width - self.cnf.entity_radius),
                random.randint(self.cnf.entity_radius, self.cnf.height - self.cnf.entity_radius), 
                self.cnf
            )

            self.entities.add(entity)


    def create_food_item(self):

        food = Food(
            random.randint(0, self.cnf.width - self.cnf.food_width),
            random.randint(0, self.cnf.height - self.cnf.food_height), 
            self.cnf
        )

        self.food_items.add(food)

    def update(self):

        self.entities.update()

        # Eat Food and reproduce:
        for entity in self.entities:
            if entity.can_reproduce:
                child = entity.reproduce()
                self.entities.add(child)

            collided_sprite = pygame.sprite.spritecollide(entity, self.food_items, True)

            for food in collided_sprite:
                entity.energy += food.energy

                if entity.energy > entity.max_energy:
                    entity.energy = entity.max_energy

        # Spawn food
        if random.randint(1, 10) == 7:
            self.create_food_item()


    





