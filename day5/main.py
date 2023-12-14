from abc import ABC, abstractmethod
import re
from dataclasses import dataclass

class BaseMap(ABC):
    instances = []
    def __init__(self, start_destination, start_source, range):
        self.start_destination = start_destination
        self.end_destination = start_destination + range-1
        self.start_source = start_source
        self.end_source = start_source + range -1
        self.range = range
        self.diff = start_destination - start_source
        self.instances.append(self)

    @classmethod
    def get_my_instances(cls):
        return [inst for inst in cls.instances if cls == type(inst)]
    
    @classmethod
    def get_next_hop(cls, value):
        find_in_range = [inst for inst in cls.instances if inst.start_source <= value  <= (inst.start_source+inst.range) and cls == type(inst)]
        hop = 0
        if len(find_in_range):
            hop = find_in_range[0].diff
        return value+hop

    @classmethod
    def get(cls,value):
        found_instances = [inst for inst in cls.instances if inst.start_source <= value  < (inst.start_source+inst.range) and cls == type(inst)]
        if found_instances:
            return found_instances.pop()
        return None

    @classmethod
    def read_file(cls, file_name):
        with open(file_name, "r") as f:
            return [cls.from_string(line) for line in f.readlines()]

    @classmethod
    def from_string(cls, map_string: str):
        start_destination, start_source, range = map_string.split(" ")
        return cls(start_destination=int(start_destination), start_source=int(start_source), range=int(range))

class SeedToSoil(BaseMap):
    pass
class SoilToFertilizer(BaseMap):
    pass
class FertilizerToWater(BaseMap):
    pass
class WaterToLight(BaseMap):  
    pass
class LightToTemperature(BaseMap):
    pass
class TemperatureToHumidity(BaseMap):
    pass
class HumidityToLocation(BaseMap):
    pass

@dataclass
class Node():
    start: int
    end: int
    diff: int
    new_start: int
    new_end: int
    map: BaseMap


class Seeds():
    def __init__(self, seed_no, range):
        self.seed_no = int(seed_no)
        self.range = int(range)
        self.nodes = []
        self.hops = [seed_no]
        self.play_map()

    def play_map(self):
        self.nodes.append([Node(start=self.seed_no, end=self.seed_no+self.range-1, map=None, diff=0,new_start=self.seed_no+0, new_end=self.seed_no+self.range-1)])
        for x, map_type in enumerate(BaseMap.__subclasses__()):
            self.nodes.append(self.caculate_nodes(self.nodes[x],map_type))
        self.lowest_node = min(self.nodes[-1], key=lambda x: x.new_start)

    def caculate_nodes(self, nodes, map_type):
        successors = []
        for node in nodes:
            node_successors = []
            node_min = node.new_start
            node_max = node.new_end
            for instance in map_type.get_my_instances():
                if not self.calculate_overlapping_nodes(node_min,node_max, instance.start_source, instance.end_source):
                    continue
                
                end = min(node_max, (instance.end_source))
                start = max(node_min, (instance.start_source))

                successor_node = Node(start=start, end=end, map=instance, diff=instance.diff, new_start=start+instance.diff, new_end=end+instance.diff)
                node_successors.append(successor_node)

            if not node_successors:
                successor_node = Node(start=node_min, end=node_max, map=None, diff=0, new_start=node_min,new_end=node_max )
                node_successors.append(successor_node)
                successors.extend(node_successors)
                continue

            node_successors.sort(key=lambda x: x.start)
            first = node_min
            for successor_node in node_successors:
                if successor_node.start > first:
                    successor_node = Node(start=first, end=successor_node.start-1, map=None, diff=0, new_start=first, new_end=successor_node.start-1)
                    node_successors.append(successor_node)
                first = successor_node.end+1
            
            if first < node_max:
                successor_node = Node(start=first+1, end=node_max, map=None, diff=0, new_start=first, new_end=node_max)
                node_successors.append(successor_node)
            successors.extend(node_successors)
        return successors

    @staticmethod
    def calculate_overlapping_nodes(node_min,node_max, instance_min, instance_max):
        if (instance_min <= node_min <= instance_max) or (instance_min <= node_max <= instance_max):
            return True
        if (node_min <= instance_min <= node_max) or (node_min <= instance_max <= node_max):
            return True
        return False

    @classmethod
    def read_file(cls, file_name: str):
        with open(file_name, "r") as f:
            lines = f.readlines()
            return cls.from_string(lines[0])

    @classmethod
    def from_string(cls, line: str):
        seeds = line.split(" ")
        return [cls(seed_no=int(seed), range=int(0)) for seed in seeds]
    
    @classmethod
    def read_pairs(cls, file_name: str):
        with open(file_name, "r") as f:
            lines = f.readlines()
        
        all_numbers = re.findall(r"\d+", lines[0])
        start_numbers = all_numbers[0::2]
        range_numbers = all_numbers[1::2]
        return [cls(seed_no=seeds[0], range=seeds[1]) for seeds in zip(start_numbers, range_numbers)]

SeedToSoil.read_file("day5/seed-to-soil.txt")
SoilToFertilizer.read_file("day5/soil-to-fertilizer.txt")
FertilizerToWater.read_file("day5/fertilizer-to-water.txt")
WaterToLight.read_file("day5/water-to-light.txt")
LightToTemperature.read_file("day5/light-to-temperature.txt")
TemperatureToHumidity.read_file("day5/temperature-to-humidity.txt")
HumidityToLocation.read_file("day5/humidity-to-location.txt")


##Answer 1
seeds = Seeds.read_file("day5/seeds.txt")
for seed in seeds:
    for map in BaseMap.__subclasses__():
        seed.hops.append(map.get_next_hop(seed.hops[-1]))

answer = min([seed.hops[-1] for seed in seeds])

##Answer 2
seeds = Seeds.read_pairs("day5/seeds.txt")
answer_part2 = min([seed.lowest_node.new_start for seed in seeds])
print(answer_part2)



