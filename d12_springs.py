
import time

_UNFOLD_INPUT = False

def count_groups(fully_known_line_in : str) -> list[int]:
    groups = []
    group_counting = False
    cur_size = 0
    for symbol in fully_known_line_in:
        if (symbol == '.' or symbol == '0') and group_counting:
            groups.append(cur_size)
            group_counting = False
            cur_size = 0
            
        elif symbol == '#' or symbol == '1':
            group_counting = True
            cur_size += 1

    #finishing off the line with a group?
    if group_counting:
        groups.append(cur_size)
    return groups

def generate_node(node_no : int) -> str:
    pass

def input_unfolding(input_t_before : tuple[str, str]) -> tuple[str, str]:
    super_layout = "?".join([input_t_before[0]] * 5)
    super_grouping = ",".join([input_t_before[1]] * 5)
    return(super_layout, super_grouping)

start_time = time.time()
with open("input.txt") as input_file:
    input_ = input_file.read() 

input_lines = input_.split('\n')

total_compliant_permutations = 0

for line in input_lines:
    (layout, grouping_goal_raw) = line.split()
    if _UNFOLD_INPUT:
        (layout, grouping_goal_raw) = input_unfolding((layout, grouping_goal_raw))

    grouping_goal_list = list(grouping_goal_raw.split(','))
    grouping_goal = [int(x) for x in grouping_goal_list]
    max_no = 2**(len(layout))
    diagram = ""
    wildcard = ""
    unknown_positions_count = 0
    for ch in layout:
        if ch == '#':
            diagram = "".join((diagram, '1'))
            wildcard = "".join((wildcard,'1'))
        elif ch == '.':
            diagram = "".join((diagram,'0'))
            wildcard = "".join((wildcard,'1'))
        elif ch == '?':
            diagram = "".join((diagram,'0'))
            wildcard = "".join((wildcard, '0'))
            unknown_positions_count += 1
    
    diagram_stencil = int(diagram, base=2)
    wildcard_stencil = int(wildcard, base=2)

    initial_candidates = []

    # filter for diagram compliance
    for candidate in range(max_no):
        if (candidate ^ diagram_stencil) == 0:
            initial_candidates.append(candidate)
            continue
        elif (candidate ^ diagram_stencil) & wildcard_stencil == 0:
            initial_candidates.append(candidate)
            continue    
    #print(f"before filtering: {max_no}, after filtering: {len(initial_candidates)}")

    # filter for spring count target compliance
    # (almost halves ttr in large input)
    total_springs_target = sum(int(x) for x in grouping_goal)
    refined_candidates = [c for c in initial_candidates if c.bit_count() == total_springs_target]

    compliant_permutations = 0
    # non-trivial checks: populate & assert compliance with grouping goal
    for candidate in refined_candidates:
        candidate_formatted = 0 # adjust for trailing zeros
        if count_groups(format(candidate, 'b')) == grouping_goal:
            compliant_permutations += 1

    total_compliant_permutations += compliant_permutations

print(f"total: {total_compliant_permutations}")
print(f"time to execute [s]: {time.time() - start_time}")
