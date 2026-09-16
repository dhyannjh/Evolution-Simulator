

class Statistics:
     
    def __init__(self, cnf):

        self.time_data = []
        self.population_data = []
        self.average_speed_data = []
        self.average_energy_data = []

        self.speed_sum_this_frame = 0
        self.energy_sum_this_frame = 0


    def calculate_data(self, entities):
        Speed_sum_this_frame = 0
        Energy_sum_this_frame = 0

        for entity in entities:
            Speed_sum_this_frame += entity.speed

        for entity in entities:
            Energy_sum_this_frame += entity.energy

        return (Speed_sum_this_frame, Energy_sum_this_frame)

    def record_data(self, entities, seconds):
        self.speed_sum_this_frame, self.energy_sum_this_frame = self.calculate_data(entities)

        average_speed_this_frame = self.speed_sum_this_frame / len(entities)
        average_energy_this_frame = self.energy_sum_this_frame / len(entities)

        self.time_data.append(seconds)
        self.population_data.append(len(entities))
        self.average_speed_data.append(average_speed_this_frame)
        self.average_energy_data.append(average_energy_this_frame)









