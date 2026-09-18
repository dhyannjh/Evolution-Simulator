
import ttkbootstrap as ttk
import os
import pygame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GUI:

    def __init__(self, root, simulation, stats):

        self.root = root
        self.simulation = simulation
        self.stats = stats

        self.seconds_counter = 0

        self.root.title("Evolution Simulator")
        self.root.geometry("1200x700")

        # Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Tabs
        self.simulation_tab = ttk.Frame(self.notebook, padding=10)
        self.graphs_tab = ttk.Notebook(self.notebook, padding=10)

        self.notebook.add(
            self.simulation_tab,
            text="Simulation"
        )

        self.notebook.add(
            self.graphs_tab,
            text="Graphs"
        )

        self.simulation_init()
        self.graphs_init()
        

        self.update()


    def graphs_init(self):

        self.population_time = ttk.Frame(self.graphs_tab)
        self.average_speed_time = ttk.Frame(self.graphs_tab)
        self.average_energy_time = ttk.Frame(self.graphs_tab)

        self.graphs_tab.add(
            self.population_time,
            text="Population-Time"
        )

        self.graphs_tab.add(
            self.average_speed_time,
            text="Average-speed-Time"
        )

        self.graphs_tab.add(
            self.average_energy_time,
            text="Average-energy-Time"
        )
        

        # Population-Time Graph
        self.fig1 = Figure(figsize=(9, 4), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.line_ref, =  self.ax1.plot(self.stats.time_data, self.stats.population_data, color="#20b2aa", linewidth=2)
        self.ax1.set_title("Population-Time(s) Graph")

        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.population_time)
        self.canvas1.draw()

        self.canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Average-speed-Time Graph
        self.fig2 = Figure(figsize=(9, 4), dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.line_ref2, =  self.ax2.plot(self.stats.time_data, self.stats.average_speed_data, color="#73449e", linewidth=2)
        self.ax2.set_title("Average-speed-Time(s) Graph")

        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.average_speed_time)
        self.canvas2.draw()

        self.canvas2.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Average-energy-Time Graph
        self.fig3 = Figure(figsize=(9, 4), dpi=100)
        self.ax3 = self.fig3.add_subplot(111)
        self.line_ref3, =  self.ax3.plot(self.stats.time_data, self.stats.average_energy_data, color="#bd2b76", linewidth=2)
        self.ax3.set_title("Average-energy-Time(s) Graph")

        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=self.average_energy_time)
        self.canvas3.draw()

        self.canvas3.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def simulation_init(self):

        # Simulation Tab

        self.control_frame = ttk.Frame(self.simulation_tab)
        self.pygame_frame = ttk.Frame(self.simulation_tab)

        self.control_frame.pack(
            side="left",
            fill="y"
        )

        self.pygame_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Emmbedding pygame window

        self.pygame_frame.update()

        os.environ["SDL_WINDOWID"] = str(
            self.pygame_frame.winfo_id()
        )

        pygame.init()

        self.screen = pygame.display.set_mode(
            (600, 600))

        self.last_time = pygame.time.get_ticks()
        self.now = self.last_time


    def graph_update(self):

        # Population-Time Graph
        self.line_ref.set_data(self.stats.time_data, self.stats.population_data)

        self.ax1.relim()
        self.ax1.autoscale_view()

        self.canvas1.draw_idle()

        # Average-speed-Time Graph
        self.line_ref2.set_data(self.stats.time_data, self.stats.average_speed_data)

        self.ax2.relim()
        self.ax2.autoscale_view()

        self.canvas2.draw_idle()

        # Average-energy-Time Graph
        self.line_ref3.set_data(self.stats.time_data, self.stats.average_energy_data)

        self.ax3.relim()
        self.ax3.autoscale_view()

        self.canvas3.draw_idle()


    def simulation_update(self):

         for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.root.destroy()

         self.now = pygame.time.get_ticks()

         self.simulation.update()

         if self.now - self.last_time >= 1000:
             #print("One second passed!")
             self.last_time = self.now
             self.seconds_counter += 1
        
             self.stats.record_data(self.simulation.entities, self.seconds_counter)

             self.graph_update()

         self.screen.fill((0, 0, 0))

         self.simulation.entities.draw(self.screen)
         self.simulation.food_items.draw(self.screen)

         pygame.display.flip()


    def update(self):

        self.simulation_update()

        self.root.after(16, self.update)