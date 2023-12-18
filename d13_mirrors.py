
# index:        |0   1   2   3   4   5   6   7   8|
# line:         |#   .   #   #   .   .   #   #   .|
# gap indexing: |# 0 . 1 # 2 # 3 . 4 . 5 # 6 # 7 .|


def list_reflections(in_list : str | list[str]) -> set[int]:
    reflections = set()
    
    for gap_no in range(len(in_list)-1):
        reflection_possible = True
        # verify refleciton around gap number gap_no
        l_layers = gap_no + 1
        r_layers = len(in_list) - (gap_no + 1)
        layers_to_check = min(l_layers, r_layers)
        for i in range(layers_to_check):
            if in_list[gap_no - i] != in_list[gap_no + 1 + i]:
                reflection_possible = False
        
        if reflection_possible:
            reflections.add(gap_no)
    
    return reflections

def list_col_discrepancies(in_list: str) -> list[int]:
    discrepancy_cts = []
    # for each gap, note the discrepancy count
    # smudges are in rows/columns with a total discrepancy count of 1
    
    for gap_no in range(len(in_list)-1):
        discrepancy_counter = 0
        # verify refleciton around gap number gap_no
        l_layers = gap_no + 1
        r_layers = len(in_list) - (gap_no + 1)
        layers_to_check = min(l_layers, r_layers)
        for i in range(layers_to_check):
            if in_list[gap_no - i] != in_list[gap_no + 1 + i]:
                discrepancy_counter += 1
        discrepancy_cts.append(discrepancy_counter)
    
    return discrepancy_cts

def list_row_discrepancies(in_diagram : list[str]) -> list[list[int]]:
    discrepancy_cts = []
    # for each gap, note the discrepancy count
    # smudges are in rows/columns with a total discrepancy count of 1
    
    for gap_no in range(len(in_diagram)-1):
        discrepancy_counter = 0
        # verify refleciton around gap number gap_no
        l_layers = gap_no + 1
        r_layers = len(in_diagram) - (gap_no + 1)
        layers_to_check = min(l_layers, r_layers)
        for i in range(layers_to_check):
            discrepancy_counter += sum(1 for a, b in zip(in_diagram[gap_no - i], in_diagram[gap_no + 1 + i]) if a != b)
        discrepancy_cts.append(discrepancy_counter)
    
    return discrepancy_cts

with open("input.txt") as input_file:
    input_ = input_file.read() 

input_lines = input_.split('\n')
if input_lines[-1] != "":
    input_lines.append("") # adjust final diagram's input

all_diagrams = []
current_diagram = []
for line in input_lines:
    if line == "":
        all_diagrams.append(current_diagram)
        current_diagram = []
        continue
    else:
        current_diagram.append(line)

reflections_score = 0
for diagram in all_diagrams:

    # row reflections sweep
    reflections = list_reflections(diagram)
    if(len(reflections) > 0):
        reflections_score += (100*reflections.pop())
        reflections_score += 100 # adjust for zero-indexed gaps
        continue

    # column reflections sweep
    # elimination method
    reflections = set(range(len(diagram[0])))
    for line in diagram:
        local_reflections = list_reflections(line)
        reflections = reflections.intersection(local_reflections)
    
    # todo reflections_score += reflections.pop()
    reflections_score += 1 # adjust for zero-indexed gaps

print(reflections_score)

smudge_reflection_score = 0
for diagram in all_diagrams:
    row_discrepancies = list_row_discrepancies(diagram)

    one_off_idex = -1
    smudge_location = "unknown"

    for index, discrepancy_ct in enumerate(row_discrepancies):
        if discrepancy_ct == 1:
            one_off_idex = index
            smudge_location = "row_gap"
            break

    if one_off_idex < 0:

        col_diffs = []
        for line in diagram:
            col_diffs.append(list_col_discrepancies(line))
        
        # flatten to col-wise sums
        col_diffs_sums = [sum(x) for x in zip(*col_diffs)]

        for index, discrepancy_ct in enumerate(col_diffs_sums):
            if discrepancy_ct == 1:
                one_off_idex = index
                smudge_location = "col_gap"
                break

    if smudge_location == "row_gap":
        smudge_reflection_score += 100 * index
        smudge_reflection_score += 100 # adjust for zero-indexed gaps
    
    elif smudge_location == "col_gap":
        smudge_reflection_score += index
        smudge_reflection_score += 1 # adjust for zero-indexed gaps
    
print(smudge_reflection_score)