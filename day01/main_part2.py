import re

class Calibration():
    def __init__(self, sequence):
        self.sequence = sequence
        self.numeric_sequence = self.replace_words_with_numbers(sequence)
        self.first_number, self.last_number = self.find_first_and_last_number(self.numeric_sequence)
        self.value = int(self.first_number[0] + self.last_number[-1])

    @staticmethod
    def find_first_and_last_number(seqence):
        numbers = re.findall(r'\d+', seqence)
        if numbers:
            return numbers[0], numbers[-1]
        else:
            return None, None
        
    @staticmethod
    def replace_words_with_numbers(text):
        replace_dict = {'one': '1', 'two': '2', 'three': '3','four':'4','five':'5','six':'6','seven':'7','eight':'8','nine':'9'}
        for key, value in replace_dict.items():
            text = text.replace(key, key + value + key)

        return text
        
calibrations = []
with open("day1/input.txt") as file:
    for line in file:
       calibrations.append(Calibration(line.replace("\n","")))

total_value = 0
for calibration in calibrations:
    total_value += calibration.value

print(total_value)