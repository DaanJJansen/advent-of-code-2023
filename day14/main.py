from dataclasses import dataclass
import re


class Constants():
    S_ROCK = '#'
    R_ROCK = 'O'
    EMPTY = '.'

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
        self._number_of_rows = len(self._platform_transposed)
        self._s_rocks_per_column  = self.collect_rocks_per_column(Constants.S_ROCK)
        self._r_rocks_per_column  = self.collect_rocks_per_column(Constants.R_ROCK)
        self._empties_per_column  = self.collect_rocks_per_column(Constants.EMPTY)

        self._points_per_column = [0] * self._number_of_rows
        self.calculate_r_rock_position()
    
    def collect_rocks_per_column(self, rock_type):
        rocks_per_column = [[]] * self._number_of_rows

        for c,r in [(c,r) for r in range(0, len(self._platform_transposed[0])) for c in range(0, self._number_of_rows)]:
            if self._platform_transposed[c][r] == rock_type:
                current_rocks = rocks_per_column[c].copy()
                current_rocks.append(Rock(rock_type, r,c))
                rocks_per_column[c] = current_rocks

        return rocks_per_column
    
    def calculate_r_rock_position(self):
        
        for c in range(0,self._number_of_rows):
            total_points = 0
            for i, s_rock in enumerate(self._s_rocks_per_column[c]):
                find_next_s_rock_row = min([next_s_rock.row for next_s_rock in self._s_rocks_per_column[c] if next_s_rock.row > s_rock.row], default=self._number_of_rows)
                find_r_rocks_in_between = [r_rock for r_rock in self._r_rocks_per_column[c] if r_rock.row > s_rock.row and r_rock.row < find_next_s_rock_row]

                points = self._number_of_rows - s_rock.row
                
                for r_rock in find_r_rocks_in_between:
                    total_points += points
                    points -= 1


            self._points_per_column[c] = total_points
        

                
        print('test')

with open("day14/input.txt") as file:
    input = []
    for line in file:
        input.append(line.replace("\n", ""))
    input.insert(0, "#" * len(line))
    input.append("#" * len(line))

platform = Platform(input)
answer_1 = sum(platform._points_per_column)
print('test')