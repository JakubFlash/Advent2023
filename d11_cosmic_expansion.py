from itertools import product

def locate_galaxies(matrix : list[str]) -> list[tuple[int,int]]:
    galaxies = []
    for pos, line in enumerate(matrix):
        index = 0
        while True:
            index = line.find('#', index)
            if index == -1:
                break
            galaxies.append((pos, index))
            index += 1
    return galaxies


with open("input.txt") as input_file:
    input_ = input_file.read() 

input_lines = input_.split('\n')

# find lines and columns to expand
# -- eliminate non-empty ones from a list of all
input_columns_expanded = set(range(len(input_lines[0])))
input_lines_expanded = set(range(len(input_lines)))

galaxies = locate_galaxies(input_lines)
for galaxy in galaxies:
    input_lines_expanded.discard(galaxy[0])
    input_columns_expanded.discard(galaxy[1])

# space expansion
expanded_input = []

future_width = len(input_lines[0]) + len(input_columns_expanded)
blank_line = '*' * future_width

row_offset = 0
for line_no, line in enumerate(input_lines):

    new_line = line

    col_offset = 0
    for col_pos in input_columns_expanded:
        col_pos += col_offset
        col_offset += 1
        new_line = new_line[0:col_pos] + '*' + new_line[col_pos:]
        
    expanded_input.append(new_line)
    if line_no in input_lines_expanded:
        expanded_input.append(blank_line)

# lazy galaxy coords refresh
galaxies = locate_galaxies(expanded_input)

galaxy_pairs = set(product(galaxies, repeat=2))

total_dist = 0
total_dist_super = 0
super_crossed = 0

super_cols = []
super_rows = []
offset = 0
for line_no in input_lines_expanded:
    offset += 1
    super_rows.append(line_no + offset)

offset = 0
for col_no in input_columns_expanded:
    super_cols.append(col_no + offset)
    offset += 1

for pair in galaxy_pairs:
    galaxy_left = pair[0]
    galaxy_right = pair[1]
    total_dist += abs(galaxy_left[0]-galaxy_right[0])
    total_dist += abs(galaxy_left[1]-galaxy_right[1])

    rows_crossed = set(range(
        min(galaxy_left[0], galaxy_right[0]),
        max(galaxy_left[0], galaxy_right[0])))
    
    cols_crossed = set(range(
        min(galaxy_left[1], galaxy_right[1]),
        max(galaxy_left[1], galaxy_right[1])))
    
    super_crossed += len(set.intersection(rows_crossed, super_rows))
    super_crossed += len(set.intersection(cols_crossed, super_cols))

total_dist /= 2 # adjust for bi-directional (doubled) set of pairs
print(total_dist)

super_crossed /= 2 # adjust for bi-directional (doubled) set of pairs
super_scale = 1000000 - 2
total_dist = total_dist + super_scale*super_crossed
print(total_dist)