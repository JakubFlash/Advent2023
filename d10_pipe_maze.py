with open("input.txt") as input_file:
    input_ = input_file.read() 

input_lines = input_.split('\n')
x_max = len(input_lines[0])
y_max = len(input_lines)

s_index = -1
s_line_no = -1

for line_no, line in enumerate(input_lines):
    checked = line.find('S')
    if checked >= 0:
        s_index = checked
        s_line_no = line_no
        break

print(s_index)
print(s_line_no)

previous_tile = (s_index, s_line_no)
current_tile = (s_index + 1, s_line_no)

CONNECTIONS = { # (x (column), y (line))
    '-' : ((-1,  0), ( 1,  0)),
    '|' : (( 0, -1), ( 0,  1)),
    'L' : (( 1,  0), ( 0, -1)),
    'J' : ((-1,  0), ( 0, -1)),
    '7' : ((-1,  0), ( 0,  1)),
    'F' : (( 1,  0), ( 0,  1)),
}

def read_tile_face(coords : tuple[int, int]) -> str:
    return input_lines[coords[1]][coords[0]]

def travel(start_tile : tuple[int, int], direciton : tuple[int,int]) -> tuple[int, int]:
    return tuple(map(lambda i, j: i+j, start_tile, direciton))

done = False
total_hops = 0
while(not done):
    directions = CONNECTIONS[read_tile_face(current_tile)]
    neighbour_a = travel(current_tile, directions[0])
    neighbour_b = travel(current_tile, directions[1])

    if neighbour_a == previous_tile:
        if neighbour_b == previous_tile:
            print("\n\n\t\t ERROR -- both n are previous tile")
        #traveling to neighbour B
        previous_tile = current_tile
        current_tile = neighbour_b

    elif neighbour_b == previous_tile:
        #travelling to neighbour A
        previous_tile = current_tile
        current_tile = neighbour_a
    else:
        print("\n\n\t\tError -- neither neighbour is previous tile")
    total_hops += 1
    if read_tile_face(current_tile) == 'S':
        done = True
    print(f"travelled from {read_tile_face(previous_tile)} to {read_tile_face(current_tile)}")

print(total_hops)