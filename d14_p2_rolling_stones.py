import time

def summarize_load(layout : list[str]) -> int:
    total_load = 0
    modifier = len(layout)
    for line in layout:
        local_load = line.count('O') * modifier
        
        total_load += local_load
        modifier -= 1

    return total_load
        
def tilt(layout : list[str], direction : int) -> list[str]:
    clockwise_rotations = {
        "N" : 0,
        "W" : 1,
        "S" : 2,
        "E" : 3
    }

    return_rotations = {
        "N" : 0,
        "W" : 3,
        "S" : 2,
        "E" : 1
    }
    # directions: N=0, W=1, S=2, E=3
    resulting_layout = []
    # rotate for direction to face upwards
    # transpose
    # per each line:
    # '#' as substring divisor
    # substrings sorted reverse alphabetically
    # un-transpose
    # un-rotate
    for i in range(direction):
        rotated = []
        rotated = [''.join(line) for line in zip(*reversed(layout))]
        layout = rotated

    layout_T = [''.join(line) for line in zip(*layout)]

    layout_T_tilted = []
    for line in layout_T:
        sections = line.split("#")
        sections_tilted = [''.join(sorted(section, reverse=True)) for section in sections]
        line_tilted = '#'.join(sections_tilted)
        layout_T_tilted.append(line_tilted)

    layout = [''.join(line) for line in zip(*layout_T_tilted)]
    
    for i in range(4-direction):
        rotated = []
        rotated = [''.join(line) for line in zip(*reversed(layout))]
        layout = rotated

    return layout

start_time = time.time()
with open("input.txt") as input_file:
    input_ = input_file.read() 

input_lines = input_.split('\n')
input_lines_form_zero = input_lines

permutations_encountered = set()

total_cycles = 1000000000

for cycle in range(total_cycles):
    
    for i in range(4):
        input_lines = tilt(input_lines, i)
    

    if tuple(input_lines) in permutations_encountered:
        print(f"repetition after cycle no. {cycle}")
        A_form = input_lines
        break
    permutations_encountered.add(tuple(input_lines))

# locate offset
#  zero>| offset | A_form | (cycle - offset = repetitions) | A_form
input_lines = input_lines_form_zero
for c in range(cycle+1):
    for i in range(4):
        input_lines = tilt(input_lines, i)
    if tuple(input_lines) == tuple(A_form):
        print(f"OK, offset = {c}")
        break
print("is it ok?")
# (długość cyklu to tyle ile od start form do A form)
offset = c
repetitions = cycle - offset
# tysiąc minus ofset modulo długość cyklu
final_cycles = (total_cycles - offset) % repetitions

for cycle in range(final_cycles - 1):
    for i in range(4):
        input_lines = tilt(input_lines, i)

print(*input_lines, sep='\n')
print(summarize_load(input_lines))
print(f"total time: {time.time() - start_time}")

