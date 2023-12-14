import re

class Races():
    def __init__(self,time,distance):
        self.race_time = int(time)
        self.distance = int(distance)
        last_time_distance_met, first_time_distance_met = self.find_outer_races()
        self.number_combies = last_time_distance_met - first_time_distance_met +1

    def find_outer_races(self):
        first_time_distance_met = self.validate_race(range(0,self.race_time))
        last_time_distance_met = self.validate_race(reversed(range(0,self.race_time)))
        return last_time_distance_met, first_time_distance_met
    
    def validate_race(self, range):
        for x in range:
            distance = self.calculate_distance(x)
            if distance > self.distance:
                return x
    
    def calculate_distance(self, press_button_time):
        distance = press_button_time * (self.race_time-press_button_time)
        return distance

    @classmethod
    def from_string(cls, times, distances):
        return [cls(time, distance) for time, distance in zip(times, distances)]


with open("day6/input.txt") as file:
    lines = file.readlines()

times = re.findall(r"\d+", lines[0])
distances = re.findall(r"\d+", lines[1])
races = Races.from_string(times, distances)

amount = 1
for race in races:
    amount *= race.number_combies

print(amount)