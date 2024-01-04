from dataclasses import dataclass
import re


class Constants():
    S_ROCK = '#'
    R_ROCK = 'O'
    EMPTY = '.'
    CYCLES = 1000000000

class Rock():
    def __init__(self, type, row, column):
        self.type = type
        self.row = row
        self.column = column
    
    def find_above_rocks(self, row,column):
        if self.row > row and self.column == column:
            return True
        return False

    
class Platform():
    def __init__(self, input):
        self._platform = input        
        self._platform_transposed = list(map(list, zip(*self._platform)))
        self.cycle()

    def cycle(self):

        matrix = self._platform.copy()
        lst_of_cycles = []

        for x in range(0, Constants.CYCLES):
            for direction in ['N','W','S','E']:
                matrix = list(map(list, zip(*matrix)))

                if direction in ['S','E']:
                    [l.reverse() for l in matrix]

                matrix = self.calculate_r_rock_position(matrix)

            matrix.reverse()
            [l.reverse() for l in matrix]

            if matrix in lst_of_cycles:
                print(x,'found')
                break
                
            lst_of_cycles.append(matrix)


        first_found = lst_of_cycles.index(matrix)
        modulo = (Constants.CYCLES-(x+1)) % (x - first_found)
        end_result_matrix = lst_of_cycles[first_found + modulo]
        answer_2 = self.calculate_load(end_result_matrix)
        print(answer_2)

    
    def calculate_load(self,matrix):
        copied_matrix = matrix.copy()
        copied_matrix.reverse()
        points = 0

        for r in range(0, len(copied_matrix)):
            for c in range(0, len(copied_matrix[r])):
                if copied_matrix[r][c] == Constants.R_ROCK:
                    points += r


        return points

    
    def collect_rocks_per_column(self, rock_type, matrix):
        rocks_per_column = [[]] * len(matrix)

        for c,r in [(c,r) for r in range(0, len(matrix[0])) for c in range(0, len(matrix))]:
            if matrix[c][r] == rock_type:
                current_rocks = rocks_per_column[c].copy()
                current_rocks.append(Rock(rock_type, r,c))
                rocks_per_column[c] = current_rocks

        return rocks_per_column
    
    def calculate_r_rock_position(self, matrix):

        number_of_rows = len(matrix)
        s_rocks_per_column  = self.collect_rocks_per_column(Constants.S_ROCK, matrix)
        r_rocks_per_column  = self.collect_rocks_per_column(Constants.R_ROCK, matrix)
        
        for c in range(0,number_of_rows):

            if not r_rocks_per_column[c]:
                continue
            
            for s_rock in s_rocks_per_column[c]:
                find_next_s_rock_row = min([next_s_rock.row for next_s_rock in s_rocks_per_column[c] if next_s_rock.row > s_rock.row], default=number_of_rows)
                find_r_rocks_in_between = [r_rock for r_rock in r_rocks_per_column[c] if r_rock.row > s_rock.row and r_rock.row < find_next_s_rock_row]

                position = s_rock.row + 1
                for r_rock in find_r_rocks_in_between:
                    matrix[c][r_rock.row] = Constants.EMPTY
                    matrix[c][position] = Constants.R_ROCK
                    position += 1

        return matrix


with open("day14/input.txt") as file:
    input = []
    for line in file:
        str_line = line.replace("\n", "")
        input.append(f'#{str_line}#')
    input.insert(0, "#" * (len(line)+2))
    input.append("#" * (len(line)+2))

platform = Platform(input)
# answer_1 = sum(platform.points_per_column)
print('test')