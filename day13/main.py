pattern = []
class Pattern():
    def __init__(self, pattern):
        self.pattern = pattern
        self.value = self.find_pattern()
        print(self.value)

    def find_pattern(self):

        found_in_row = self.compare_rows(self.pattern)
        found_in_row_smutch = self.compare_rows_smutch(self.pattern)
        found_in_column = 0
        found_in_column_smutch = 0

        if not found_in_row:
            found_in_column = self.compare_rows(list(zip(*self.pattern)))
        if not found_in_row_smutch:
            found_in_column_smutch = self.compare_rows_smutch(list(zip(*self.pattern)))


        return (found_in_row*100 + found_in_column,(found_in_row_smutch*100 + found_in_column_smutch))

    def compare_rows(self, matrix):

        serie_a_sub, serie_b_sub = [],[1]
        r=0
        while not serie_a_sub == serie_b_sub and r < len(matrix):
            r += 1
            serie_a = matrix[:r]
            serie_b = matrix[r:]
            smallest_serie_count = min(len(serie_a), len(serie_b))
            serie_a.reverse()
            serie_a_sub = serie_a[:smallest_serie_count]
            serie_b_sub = serie_b[:smallest_serie_count]
            if serie_a_sub == serie_b_sub:
                print("found pattern")
                print(serie_a_sub)
                print(serie_b_sub)

        return 0 if r == len(matrix) else r
    
    def compare_rows_smutch(self, matrix):


        r=0
        smutch = False
        while not smutch and r < len(matrix):
            r += 1
            serie_a = matrix[:r]
            serie_b = matrix[r:]
            smallest_serie_count = min(len(serie_a), len(serie_b))
            serie_a.reverse()
            smutch = self.find_one_smutch(serie_a[:smallest_serie_count], serie_b[:smallest_serie_count])
            if smutch:
                print("found pattern")
                print(serie_a)
                print(serie_b)

        return 0 if r == len(matrix) else r
    
    def find_one_smutch(self, serie_a, serie_b):
        count = 0
    
        for r in range(0, len(serie_a)):
            for c in range(0, len(serie_a[r])):
                if serie_a[r][c] != serie_b[r][c]:
                    count += 1
                if count > 1:
                    break
            if count > 1:
                break

        if count == 1:
            return True
        return False
            


        # self.compare_prev_and_next(self.pattern[0], self.pattern[2:])

    def compare_prev_and_next(self, serie_a, serie_b):

        
        print(serie_a)

    @classmethod
    def from_string(cls, pattern):
        return cls(pattern)
    
patterns = []
pattern = []
with open("day13/input.txt") as file:
    for line in file:
        if line == "\n":
            patterns.append(Pattern.from_string(pattern))
            pattern = []
        else:
            pattern.append([*line.replace("\n", "")])
    patterns.append(Pattern.from_string(pattern))

answer_1 = sum([p.value[0] for p in patterns])
answer_2 = sum([p.value[1] for p in patterns])
print("test")
