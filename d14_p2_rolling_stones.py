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
    """
        directions: N=0, W=1, S=2, E=3

        flow:
        rotate for (direction) to face upwards
            transpose
            per each line:
                split into substring using '#' as separator
                    substrings sorted reverse alphabetically (OOO....)
                substrings connected with # as separator
            un-transpose
        un-rotate
    """

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

total_cycles = 1000000000
permutations_encountered = set()

for start_to_form_A in range(total_cycles):
    
    for i in range(4):
        input_lines = tilt(input_lines, i)
    
    if tuple(input_lines) in permutations_encountered:
        print(f"repetition after cycle no. {start_to_form_A}")
        A_form = input_lines
        break
    permutations_encountered.add(tuple(input_lines))

"""
A_form = form of layout found to repeat, i.e. one which starts an infinite loop
zero = starting form of layout
|n| = n cycles

form: zero
    | start_to_form_A |
A_form 
    | repetition |   ^
A_form               |
    | repetition |   |
        | ... |      | X
        | ... |      |
        | ... |      |
    | repetition |   V
A_form 
    | final_cycles |
final_form

total_cycles = start_to_form_A + X * repetitions + final_cycles

final_cycles = (total_cycles - start_to_form_A) % repetitions

"""
for repetition in range(start_to_form_A):
    for i in range(4):
        input_lines = tilt(input_lines, i)
    if tuple(input_lines) == tuple(A_form):
        break
start_to_form_A += 1 # adjust for cycle count starting with 0
final_cycles = (total_cycles - start_to_form_A) % repetition

for cycle in range(final_cycles):
    for i in range(4):
        input_lines = tilt(input_lines, i)

print(*input_lines, sep='\n')
print(summarize_load(input_lines))
print(f"total time: {time.time() - start_time}")
