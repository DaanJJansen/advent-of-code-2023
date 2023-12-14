import re

    
class Calibration():
    def __init__(self, sequence):
        self.sequence = sequence
        self.first_number, self.last_number = self.find_first_and_last_number(seqence=sequence)
        self.value = int(self.first_number[0] + self.last_number[-1])

    @staticmethod
    def find_first_and_last_number(seqence):
        numbers = re.findall(r'\d+', seqence)
        if numbers:
            return numbers[0], numbers[-1]
        else:
            return None, None

calibrations = []

# calibrations.append(Calibration("six3278xsddmnz"))
with open("day1/input.txt") as file:
    for line in file:
       calibrations.append(Calibration(line.replace("\n","")))

total_value = 0
for calibration in calibrations:
    total_value += calibration.value

print("test")