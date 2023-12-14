
pipes = {
    "|": { "connections": {8:8,2:2}, "sides": [[1,4,7],[3,6,9]] },
    "-": { "connections": {4:4,6:6}, "sides": [[7,8,9],[1,2,3]] },
    ".": { "connections": {}, "sides": [[1,3,7,9],[2,4,6,8]]},
    "L": { "connections": {2:6,4:8}, "sides": [[7,4,1,2,3],[9]] },
    "J": { "connections": {6:8,2:4}, "sides": [[7],[1,2,3,6,9]] },
    "7": { "connections": {6:2,8:4}, "sides": [[7,8,9,6,3],[1]] },
    "F": { "connections": {8:6,4:2}, "sides": [[1,4,7,8,9],[3]] },
    "S": { "connections": {}, "sides": [[1,2,3,4,6,7,8,9],[]] },
}

directions = {
    4: (0,-1),
    6: (0,1),
    8: (-1,0),
    2: (1,0)
}

slides = {
    4: (9,6),
    6: (7,1),
    8: (3,1),
    2: (9,7)
}




class Matrix:
    def __init__(self, matrix: list, start_type_symbol):
        self.matrix = matrix
        self.start_type_symbol = start_type_symbol
        self.target_matrix = self.build_target_matrix()
        self.matrix_row_size = len(matrix)
        self.matrix_column_size = len(matrix[0])

        self.start = self.find_start()
        self.starting_pipes = self.find_start_neighbours(self.start)
        self.walking(self.starting_pipes)

        self.define_outer_vs_inner_pipe()
        self.replace_dots_with_inner_outer()

    def define_outer_vs_inner_pipe(self):
        self.outers = self.matrix.copy()

        self.set_sides_starting_position()

        #todo fix starting point
        

        for r in range(0, self.matrix_row_size):
            for c in range(0, self.matrix_column_size):
                symbol = self.target_matrix[r][c]
                outer = []
                if r < 1 or c < 1:
                    outer = True
                else:
                    outer = self.outers[r][c-1]['slides'][9-1] == 0
                    
                self.outers[r][c] = {"symbol": symbol, "slides": self.get_slides(outer, self.get_pipe(symbol))}
                    
    
    def replace_dots_with_inner_outer(self):
        self.my_counter = 0
        self.inner_outers = self.target_matrix.copy()
        for r in range(0, self.matrix_row_size):
            for c in range(0, self.matrix_column_size):
                if self.target_matrix[r][c] == ".":
                    
                    type = "0"
                    if r < 1 or c < 1 or r > self.matrix_row_size-2 or c > self.matrix_column_size-2:
                        type = "0"
                    elif not self.test_edges((r,c)):
                        self.my_counter += 1
                        type = "1"

                    self.inner_outers[r][c] = type

    def test_edges(self, coordinate):
        r,c = coordinate
        results = []
        if self.outers[r+1][c]['symbol'] != ".":
            results.append(self.outers[r+1][c]['slides'][8-1] == 0)
        if self.outers[r][c-1]['symbol'] != ".":
            results.append(self.outers[r][c-1]['slides'][6-1] == 0)
        if self.outers[r][c+1]['symbol'] != ".":
            results.append(self.outers[r][c+1]['slides'][4-1] == 0)
        if self.outers[r-1][c]['symbol'] != ".":
            results.append(self.outers[r-1][c]['slides'][2-1] == 0)

        if len(results) == 0:
            results.append(self.inner_outers[r][c-1] == "0")
        return any(results)    

    
    def set_sides_starting_position(self):

        r,c = self.start
        positions = []
        for start_pipe in self.starting_pipes:
            r_relavtive,c_new = (start_pipe[0][i] - self.start[i] for i in range(0,len(self.start)))
            positions.append([d for d,v in directions.items() if v == (r_relavtive,c_new)].pop())
        start_symbol = [k for k,v in pipes.items() if set(v['connections'].values()).issubset(set(positions)) and k != "S" and k != "."].pop()
        print(start_symbol)
        self.target_matrix[r][c] = start_symbol

    
    @staticmethod
    def get_pipe(symbol):
        return pipes[symbol]

    def get_slides(self,outers, pipe):
        slides = [1,1,1,1,-1,1,1,1,1]
        for connection in pipe["connections"].values():
            slides[connection-1] = -1

        sides = pipe["sides"]
        for o in sides[0]:
            slides[o-1] = 0 if outers else 1
        for o in sides[1]:
            slides[o-1] = 1 if outers else 0

        return slides

    def find_start(self):
        for index, row in enumerate(self.matrix):
            if "S" in row:
                coordinates = (index, row.index("S"))
                self.replace_in_target_matrix(coordinates, "S")
                return coordinates
            
    def replace_in_target_matrix(self, coordinates, symbol):
        x, y = coordinates        
        self.target_matrix[x][y] = symbol
            
    def walking(self, starting_pipes):
        counter = 1
        coordinates_1, direction_1 = starting_pipes[0]
        coordinates_2, direction_2 = starting_pipes[1]
        found = False

        while not found:
            counter += 1
            new_coordinate_1, new_direction_1, symbol = self.walk_border(coordinates_1, direction_1)
            self.replace_in_target_matrix(new_coordinate_1, symbol)
            new_coordinate_2, new_direction_2, symbol = self.walk_border(coordinates_2, direction_2)
            self.replace_in_target_matrix(new_coordinate_2, symbol)
            found = (new_coordinate_1 == coordinates_2 and new_coordinate_2 == coordinates_1) or (new_coordinate_1 == new_coordinate_2)
            coordinates_1, direction_1 = new_coordinate_1, new_direction_1
            coordinates_2, direction_2 = new_coordinate_2, new_direction_2

        print(counter)

    def build_target_matrix(self):
        target_matrix = []
        for row in matrix:
            new_row = ["." for c in row]
            target_matrix.append(new_row)
        return target_matrix
    

    def walk_border(self, coordinate, direction):
        x, y = coordinate
        walk_x, walk_y = directions[direction]
        x += walk_x
        y += walk_y
        symbol = self.matrix[x][y]
        return [(x,y), pipes[symbol]["connections"][direction], symbol]

    
    def find_start_neighbours(self, coordinate):
        x, y = coordinate
        neighbours = []

        origin = 0
        for walk_x in reversed(range(x-1, x+2)):
            for walk_y in range(y-1, y+2):
                origin += 1
                if not 0 <= walk_x  <= (self.matrix_row_size-1) or not 0 <= walk_y <= (self.matrix_column_size-1):
                    continue
                
                symbol = self.matrix[walk_x][walk_y]
                print(walk_x,origin,walk_y,symbol)
                if origin in pipes[symbol]["connections"]:
                    coordinates = (walk_x,walk_y)
                    self.replace_in_target_matrix(coordinates,symbol)
                    neighbours.append([(walk_x,walk_y),pipes[symbol]["connections"][origin]])
        return neighbours




with open("day10/input.txt") as file:
    matrix = []
    for line in file:
        matrix.append([*line.replace("\n", "")])


matrix = Matrix(matrix, "7")

with open("day10/out.txt","w") as file:
    for row in matrix.target_matrix:
        file.write("".join(row)+"\n")

with open("day10/out_outers.txt","w") as file:
    for row in matrix.inner_outers:
        file.write("".join(row)+"\n")

amount = matrix.my_counter
print("test")
