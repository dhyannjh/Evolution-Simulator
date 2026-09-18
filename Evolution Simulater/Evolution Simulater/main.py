# Evolution Simulator Post HYE project

import pygame
import random
import matplotlib.pyplot as plt
import ttkbootstrap as ttk

from config import Configuration
from Astatistics import Statistics
from simulation import Simulation
from gui import GUI


cnf = Configuration()

stats = Statistics(cnf)

sim = Simulation(cnf)
sim.create_entities(100)

root = ttk.Window(themename="darkly")

gui = GUI(root, sim, stats)

root.mainloop()

'''

print(stats.time_data)
print(stats.average_speed_data)
print(stats.population_data)

pygame.quit()

# Plotting stuff

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

'''