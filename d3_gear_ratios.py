class PartNo:
    def __init__(self, literal, lpos, line_no) -> None:
        self.literal = literal
        self.val = int(literal)
        self.lpos = lpos
        self.rpos = lpos + len(literal) - 1
        self.line_no = line_no


with open("input.txt") as input_file:
    input_ = input_file.read()

lines = input_.split('\n')

xmax = len(lines[0])

# add padding for uniform handling in case of edges
v_padding = '.' * xmax
lines_vertically_padded = [v_padding, *lines, v_padding]

lines_padded : list[str] = []
for line in lines_vertically_padded:
    lines_padded.append('.' + line + '.')

xmax += 2

# determine a set of all symbols
symbols_l = filter(lambda x: x!='.' and not x.isdigit(), input_)
symbols = set(symbols_l)

# find each number (literal, lpos, line_no)
symbol_clearing = {symbol : '.' for symbol in symbols}
symbol_clearing_t = str.maketrans(symbol_clearing)
lines_cleared = [line.translate(symbol_clearing_t) for line in lines_padded]

part_numbers : list[PartNo] = []

for line_no, line in enumerate(lines_cleared):
    splitted = line.split('.')
    offset = 0
    for pos, literal in enumerate(splitted):
        if literal != '':
            part_number_found = PartNo(literal, offset + pos, line_no)
            part_numbers.append(part_number_found)
            # print(f"\tnew part: {new_part.val} at position {new_part.lpos} on line {new_part.line_no}")
            offset = offset + len(literal)

# determine valid part numbers:
# any symbols in <line_no - 1, lpos - 1> to (line_no + 1, rpos + 1) rectangle?

def verify_part(my_part : PartNo) -> bool:
    lines_to_check = [my_part.line_no - 1, my_part.line_no + 1, my_part.line_no]
    pos_to_check = range(my_part.lpos - 1, my_part.rpos + 2)
    for line in lines_to_check:
        for pos in pos_to_check:
            if lines_padded[line][pos] in symbols:
                return True

    return False


valid_part_numbers = [part_no for part_no in part_numbers if verify_part(part_no)]

total = 0
for part_no in valid_part_numbers:
    total += part_no.val

print("total: " + str(total))

def find_adjacent_parts(parts : list[PartNo], adj_line_no : int, adj_pos : int):
    for my_part in parts:
        if (my_part.lpos - 1 <= adj_pos             # to the right of the left edge
            and my_part.rpos + 1 >= adj_pos         # to the left of the right edge
            and my_part.line_no - 1 <= adj_line_no  # below top edge
            and my_part.line_no + 1 >= adj_line_no  # above bottom edge
            ): yield my_part


total_gear_ratio = 0

# for each star literal, find each adjacent part_no
stars = []
for line_no, line in enumerate(lines_padded):
    for pos in range(xmax):
        if line[pos] == '*':
            stars.append((line_no, pos))
            star = (line_no, pos)

gear_sets : list[PartNo] = []
for star in stars:
    line_no = star[0]
    pos = star[1]
    gear = list(find_adjacent_parts(valid_part_numbers, line_no, pos))
    if len(gear) == 2:
        gear_sets.append(gear)

ratios_sum = 0
for gear in gear_sets:
    ratio = 1
    for part_no in gear:
        ratio *= part_no.val
    ratios_sum += ratio

print(ratios_sum)
