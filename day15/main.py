class Constants:
    MULTIPLIER = 17

class Sequence:
    def __init__(self, sequences, operator, focal_length=0):
        self.sequence = sequences
        self.operator = operator
        self.focal_length = focal_length

    @property
    def box(self):
        return self._calculate_box()
    
    def _calculate_box(self):
        value = 0
        for letter in self.sequence:
            value = ((value + ord(letter)) * Constants.MULTIPLIER) % 256
        return value

    @classmethod
    def from_string(cls, string):
        focal_length = 0
        if "=" in string:
            sequence, focal_length = string.split("=")
            operator = "="
        else:
            sequence = string.split("-")[0]
            operator = "-"
        return cls(sequence, operator, int(focal_length))

with open("day15/input.txt") as file:
    sequences = []
    for line in file:
        splitted_line = line.split(",")
        sequences = [Sequence.from_string(sequence) for sequence in splitted_line]


print(sequences[0].box)
answer_1 = sum([sequence.box for sequence in sequences])


class Boxes():
    def __init__(self):
        self._boxes = [[]] * 256
    
    def fill_boxes(self, sequences: list[Sequence]):
        for sequence in sequences:
            if sequence.operator == "=":
                self.add_to_box(sequence)
            if sequence.operator == "-":
                self.remove_from_box(sequence)
    
    def add_to_box(self, sequence: Sequence):
        if self._boxes[sequence.box] == []:
            self._boxes[sequence.box] = [sequence]
        else:
            list_position = self.get_list_position(sequence)
            if list_position:
                self._boxes[sequence.box][list_position-1] = sequence
            else:
                self._boxes[sequence.box].append(sequence)
    
    def remove_from_box(self, sequence: Sequence):
        list_position = self.get_list_position(sequence)
        if list_position:
            del self._boxes[sequence.box][list_position-1]

    def get_list_position(self, sequence: Sequence) -> int:
        listed_sequence: Sequence
        for index, listed_sequence in enumerate(self._boxes[sequence.box]):
            if listed_sequence.sequence == sequence.sequence:
                return index + 1
        return 0
    
    def focus_power(self):
        sequence: Sequence
        power = 0
        for box_index, box in enumerate(self._boxes):
            for sequence_index, sequence in enumerate(box):
                power += (box_index +1) * (sequence_index + 1) * sequence.focal_length
        return power
                
    
boxes = Boxes()
boxes.fill_boxes(sequences)
answer_2 = boxes.focus_power()
print("test")
