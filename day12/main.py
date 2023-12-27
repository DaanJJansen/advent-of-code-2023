from typing import List
from itertools import product, groupby
from dataclasses import dataclass
from functools import cache

class Constants:
    UNKOWN = "?"
    OPERATINAL = "."
    DAMAGED = "#"
    REPLACE_VALUE = [OPERATINAL, DAMAGED]

@dataclass
class Version:
    condition: List
    damaged_spring: List
    valid: bool = True


class Condition:
    def __init__(self, condition: List, groups):
        self.condition = condition
        self.groups = tuple(map(int, groups.split(",")))

        # self.versions = self.create_verions()
        self.versions = self.calculate(self.groups*5, "?".join([self.condition] * 5) + ".")
        print("test")

    def extend(self, groups):

        group_groups = groups.copy()
        for x in range(0,4):
            group_groups.extend(groups.copy())

        return group_groups
    
    @cache
    def calculate(self, groups, condition, number_of_operational = 0):
        #stole solution from reddit.. tried to bruut force it by first creating all possible combinations and then checking if they are valid
        #but that was to slow, using recursive function is much faster due to fact that you close single out from the beginning
        #caching is also a must have
        
        if not condition:
            return not groups and not number_of_operational
        number_of_solutions = 0
        for letter in [Constants.DAMAGED, Constants.OPERATINAL] if condition[0] == Constants.UNKOWN else condition[0]:
            if letter == Constants.DAMAGED:
                number_of_solutions += self.calculate(groups, condition[1:], number_of_operational + 1)
            else:
                if number_of_operational:
                    #group is matching 
                    if groups and groups[0] == number_of_operational:
                        number_of_solutions += self.calculate(groups[1:], condition[1:])
                else:
                    number_of_solutions += self.calculate(groups, condition[1:])
        return number_of_solutions



                

    def create_verions(self):
        replace_condition = self.condition.copy()
        replace_condition.insert(0, Constants.UNKOWN)
        # replace_condition.extend(Constants.UNKOWN)
        unkowns = [index for index, c in enumerate(replace_condition) if c == Constants.UNKOWN]

        versions = []
        counterlvl_1 = 0
        counterlvl_2 = 0
        for products in product(range(2), repeat=len(unkowns)):
            counterlvl_1 += 1
            replace_condition = self.replace_value(replace_condition, unkowns, products)
            # for seperator_product in product(range(2), repeat=4):
            #     counterlvl_2 += 1
            #     complete_condition = []
            #     for i in range(0,4):
            #         complete_condition.extend(replace_condition)
            #         complete_condition.extend(Constants.REPLACE_VALUE[seperator_product[i]])
            #     complete_condition.extend(replace_condition)

            
                
                # print(condition)
            damaged_spring = [len(list(g)) for k, g in groupby(replace_condition) if k==Constants.DAMAGED]

            # versions.append(Version(complete_condition, damaged_spring, damaged_spring == self.group_groups))
            if damaged_spring == self.groups:
                print("new version")
                versions.append(Version(replace_condition, damaged_spring))

        print(counterlvl_1)
        print(counterlvl_2)
        return versions
    
    def create_versions_groups(self):
        counter = []
        for i in range(0,len(self.condition_groups)):
            versions = self.create_verions(self.condition_groups[i], self.group_groups[i])
            counter.append(len(versions))
        print(counter)
        return counter
            
    @staticmethod
    def replace_value(condition: List, unkowns, products):
        condition = condition.copy()
        for i, product in enumerate(products):
            condition[unkowns[i]] = Constants.REPLACE_VALUE[product]
        return condition




    @classmethod
    def from_string(cls, condition, groups):
        return cls(condition, groups)



conditions = []
with open("day12/input.txt") as file:
    for i, line in enumerate(file):
        condition, groups = (line.replace("\n", "")).split(" ")
        conditions.append(Condition.from_string(condition, groups))
        print(i)

answer_1 = sum([condition.versions for condition in conditions])

print ("test")


