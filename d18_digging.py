
import sys

def mark_cube(field : list[str], location : tuple[int,int]) -> list[str]:
    before = list(field[location[0]])
    before[location[1]] = '#'
    after = ''.join(before)
    field[location[0]] = after

    return field

with open("input.txt") as input_file:
    input_ = input_file.read() 

input_lines = input_.split('\n')

commands = []
for line in input_lines:
    (direction, distance, _) = line.split()
    commands.append((direction, int(distance)))

# prepare field
total_up = 0
total_down = 0
total_left = 0
total_right = 0

for command in commands:
    match command[0]:
        case 'R':
            total_right += command[1]
        case 'L':
            total_left += command[1]
        case 'U':
            total_up += command[1]
        case 'D':
            total_down += command[1]

field_w = total_left + total_right + 3
field_h = total_up + total_down + 3
starting_pos = (total_up + 1, total_left + 1)

field = ['.' * field_w] * field_h

mark_cube(field, starting_pos)

cur_pos = starting_pos

for command in commands:
    locations_digged = []
    match command[0]:
        case 'R':
            for i in range(command[1]):
                cur_pos = (cur_pos[0], cur_pos[1] + 1)
                mark_cube(field, cur_pos)
        case 'L':
            for i in range(command[1]):
                cur_pos = (cur_pos[0], cur_pos[1] - 1)
                mark_cube(field, cur_pos)
        case 'U':
            for i in range(command[1]):
                cur_pos = (cur_pos[0] - 1, cur_pos[1])
                mark_cube(field, cur_pos)
        case 'D':
            for i in range(command[1]):
                cur_pos = (cur_pos[0] + 1, cur_pos[1])
                mark_cube(field, cur_pos)

starting_point = (0,0)


def flood(field: list[str], location : tuple[int,int]):
    negative = location[0] < 0 or location[1] < 0
    if negative or location[0] >= len(field) or location[1] >= len(field[0]):
        return
    if field[location[0]][location[1]] != '.':
        return
    

    before = list(field[location[0]])
    before[location[1]] = '/'
    after = ''.join(before)
    field[location[0]] = after

    flood(field, (location[0], location[1] - 1))
    flood(field, (location[0] + 1, location[1]))
    flood(field, (location[0], location[1] + 1))
    flood(field, (location[0] - 1, location[1]))


reduced_field = []
for line in field:
    if line.count('#') != 0:
        reduced_field.append(line)

reduced_field.append("." * len(reduced_field[0]))


field=reduced_field
print(f"total fields: {len(reduced_field[0]) * len(reduced_field)}")

sys.setrecursionlimit(1500000)
flood(field, starting_point)
#print(*field, sep='\n')
total_area = 0

for line in field:
    total_area += line.count('#')
    total_area += line.count('.')

print(f"total area: {total_area}")

"""
out_f = open("output.txt", "w")

for line in field:
    out_f.write(line)
    out_f.write('\n')
out_f.close()
"""