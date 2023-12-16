
from math import lcm

with open("input.txt") as input_file:
    input_ = input_file.read() 

input_lines = input_.split('\n')
instruction = input_lines[0]
maps = {}
for line in input_lines[2:]:
    (location, directions) = line.split(" = ")
    (left, right) = directions.replace('(','').replace(')','').split(', ')
    maps[location] = (left, right)

i_len = len(instruction)
"""
pos = "AAA"
command_ctr = 0
i = 0
while (True):
    command = instruction[command_ctr % i_len]
    command_ctr += 1

    if command == "L":
        pos = maps[pos][0]
    elif command == "R":
        pos = maps[pos][1]

    if pos == "ZZZ":
        break
    
print(command_ctr)
"""
all_pos = maps.keys()
group_pos = list(filter(lambda x: x[2] == 'A', all_pos))

def verify_group_completion(positions : list[str]) -> bool:
    for pos in positions:
        if pos[2] != 'Z':
            return False
        
    return True

lengths = []
for pos in group_pos:
    command_ctr = 0
    while(True):
        command = instruction[command_ctr % i_len]
        command_ctr += 1

        if command == 'L':
            pos = maps[pos][0]
        elif command == 'R':
            pos = maps[pos][1]

        if pos[2] == 'Z':
            break
        
    print(command_ctr)
    lengths.append(command_ctr)

print(f"lengths: {lengths}; lcm: {lcm(*lengths)}")
