import re
from math import lcm

class Route:
    instances = []
    def __init__(self, id, left, right):
        self.id = id
        self.left_id = left
        self.recht_id = right
        self.l = None
        self.r = None
        self.end_sequence_route = None
        self.instances.append(self)
        self.create_start_nodes()

    def define_next_hops(self):
        self.l = Route.get(self.left_id)
        self.r = Route.get(self.recht_id)

    def create_start_nodes(self):
        if self.is_node_type(self.id, "A"):
            _ = Node(self)

    @staticmethod
    def is_node_type(id,type):
        return id[2] == type
    
    @classmethod
    def from_string(cls, string):
        id, directions = string.split(" = ")
        left, right = re.findall(r"(\w+)", directions)
        return cls(id, left, right)

    @classmethod
    def get(cls, id):
        return [inst for inst in cls.instances if inst.id == id].pop()
    
class Node:
    instances = []
    def __init__(self, start: Route):
        self.start = start
        self.last_steps = start
        self.counter = 0
        self.sequence = 0
        self.instances.append(self)

    def walk(self,instruction: str):
        hop = Route.get(self.last_steps.__dict__[instruction.lower()])
        self.last_steps = hop

    def walk_sequences(self):
        hop = self.last_steps.end_sequence_route
        self.counter += 1
        self.last_steps = hop

    @property
    def end_node_type(self):
        return self.last_steps.id[-1] == "Z"

    

class Instruction:
    def __init__(self, instructions):
        self.instructions = instructions
        self.instructions_count = len(instructions)
        self.steps = []
        # self.walk_part1(Route.get("AAA"))

        self.nodes = Node.instances
        self.counter = 0
        

    def walk_part1(self, base: Route):
        hop = base
        for instruction in self.instructions:
            
            hop = hop.__dict__[instruction.lower()]
            self.steps.append(hop)

            if hop.id == "ZZZ":
                break

        if hop.id != "ZZZ":
            self.walk_part1(hop)

    def define_next_hops_on_routes(self):
        for route in Route.instances:
            route.define_next_hops()

    def set_step_sequence_on_routes(self):
        for route in Route.instances:
            hop = route
            for instruction in self.instructions:
                hop = hop.__dict__[instruction.lower()]

            route.end_sequence_route = hop

    def get_lcm_by_defining_route_multiplier(self):
        # diddnt come up with using lcm myself- least common multiple - via reddit
        # offcourse I tried bruut forcing it at first, but after 6 hours i gave up

        sequence_steps_for_reaching_end_node = []
        for node in self.nodes:
            while not node.end_node_type:
                node.walk_sequences()
            sequence_steps_for_reaching_end_node.append(node.counter)
        return self.get_lcm(sequence_steps_for_reaching_end_node)

    @staticmethod
    def get_lcm(multipliers):
        common_multiplier = lcm(*multipliers)
        return common_multiplier

     
    
routes = []
with open("day8/input.txt") as file:
    for line in file:
        routes.append(Route.from_string(line.replace("\n", "")))

instructions = Instruction("LRLRLLRLRLRRLRLRLRRLRLRLLRRLRRLRLRLRLLRRRLRRRLLRRLRLRLRRRLRRLRRRLRLRLRRLRLLRLRLRRLRRRLRLRRLRRRLLRLRLRRRLRRRLRLRRRLRLRRRLLRRLLLRRRLLRRRLRRRLRRRLRLRLRLLRLRRLRLRLLLRRLRRLRRLRLRRLRRLLRRLRLRRRLRLRLLRRRLRRRLRRRLLLRRRLRLRLRRLRRRLRRRLRLRRRLRRLRRRLRLRRLLRRRLRRRLLLRRLRLRLRRLRRRLRRLRRLRLRRRR")

# answer_1 = len(instructions.steps)
# print(answer_1)

instructions.define_next_hops_on_routes()
instructions.set_step_sequence_on_routes()
answer_2 = instructions.get_lcm_by_defining_route_multiplier() * instructions.instructions_count
print(answer_2)


