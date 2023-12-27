from typing import List, Tuple

class Constants():
    GALAXY_SYMBOL = "#"

class Galaxy():
    def __init__(self, coordinates: Tuple[int, int]):
        self.coordinates = coordinates
        self._distances = []

    @property
    def distances(self):
        return sum(self._distances)
    
    @distances.setter
    def distances(self, value: int):
        self._distances.append(value)

class Matrix():
    def __init__(self, matrix: List[List[str]]) -> None:
        self.matrix = matrix
        self.galaxies = []
        self.rows_to_extend = []
        self.columns_to_extend = []
        self.expand_matrix()  

    def process(self,extension_factor):
        self._extension_factor = extension_factor
        self.get_galaxies()
        self.get_galaxy_distances()

    def get_galaxy_distances(self):
        from_galaxy: Galaxy
        to_galaxy: Galaxy

        for i, from_galaxy in enumerate(self.galaxies):
            for to_galaxy in self.galaxies[i+1:]:
                from_galaxy.distances = self.get_distance(from_galaxy, to_galaxy)

    def get_distance(self, from_galaxy:Galaxy, to_galaxy:Galaxy):
        from_r, from_c = from_galaxy.coordinates
        to_r, to_c = to_galaxy.coordinates

        c_range, r_range = range(min(from_c, to_c), max(from_c, to_c)), range(min(from_r,to_r), max(to_r, from_r))
        c_extensions = len(set(c_range).intersection(set(self.columns_to_extend))) * self._extension_factor
        r_extensions = len(set(r_range).intersection(set(self.rows_to_extend))) * self._extension_factor

        return abs(from_r - to_r) + c_extensions + abs(from_c - to_c) + r_extensions

    def get_galaxies(self):
        self.galaxies = []
        for r in range(0, len(self.matrix)):
            for c in range(0, len(self.matrix[0])):
                if self.matrix[r][c] == Constants.GALAXY_SYMBOL:
                    self.galaxies.append(Galaxy((r,c)))

    def expand_matrix(self):
        for i, r in enumerate(self.matrix):
            if Constants.GALAXY_SYMBOL not in r:
                self.rows_to_extend.append(i)

        for c in range(0, len(self.matrix[0])):
            if Constants.GALAXY_SYMBOL not in [r[c] for r in self.matrix]:
                self.columns_to_extend.append(c)

    @classmethod
    def from_file(cls, lines: List[List[str]]):
        matrix = []
        for line in lines:
            matrix.append([*line.replace("\n", "")])
        return cls(matrix)


with open("day11/input.txt") as file:
    matrix = Matrix.from_file(file.readlines())

matrix.process(2-1)
answer_1 = sum([galaxy.distances for galaxy in matrix.galaxies])

matrix.process(1000000-1)
answer_2 = sum([galaxy.distances for galaxy in matrix.galaxies])

print(answer_1, answer_2)