
import random
import pygame


# Entity Class -------------------------------------------------------------------------------------------

class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y, config):
        super().__init__()

        self.cnf = config

        # Position
        self.x = x
        self.y = y

        # Gene Pool
        self.speed = 4
        self.max_energy = 500
        self.reproduction_rate = 500
        self.base_color = self.cnf.entity_color

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
            (self.cnf.entity_radius * 2, self.cnf.entity_radius * 2),
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
            (self.cnf.entity_radius, self.cnf.entity_radius),
            self.cnf.entity_radius
        )


    def move(self):

        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        # Bounce
        if self.x < self.cnf.entity_radius or self.x > self.cnf.width - self.cnf.entity_radius:
            self.dx *= -1

        if self.y < self.cnf.entity_radius or self.y > self.cnf.height - self.cnf.entity_radius:
            self.dy *= -1

        # Keep inside screen
        self.x = max(self.cnf.entity_radius, min(self.x, self.cnf.width - self.cnf.entity_radius))
        self.y = max(self.cnf.entity_radius, min(self.y, self.cnf.height - self.cnf.entity_radius))

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
        
        child = Entity(self.x, self.y, self.cnf)
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

        global speed_sum_this_frame

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
