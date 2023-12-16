_HANDLE_RANGES = False

def execute_hop(ID_in : int, mappings : list[tuple[int, int, int]]) -> int:
    # if ID is contained within any <source, source + reach) mapping,
    # calculate offset as (ID - source); 
    # next_ID is corresponding destination + offset
    for mapping in mappings:
        dest   = int(mapping[0])
        source = int(mapping[1])
        reach  = int(mapping[2])
        if source <= ID_in and source + reach >= ID_in:
                offset = ID_in - source
                return dest + offset
        
    return ID_in


with open("input.txt") as input_file:
    input_ = input_file.read() 
    # could also be done without storage
    # (all input is handled in one swipe)

input_lines = input_.split('\n')
input_lines.append('') # adapt last mapping's input format to that of others 

total_hops = 7

IDs_raw = input_lines[0].split(": ")[1].split()
IDs = [int(id) for id in IDs_raw]
if _HANDLE_RANGES:
    sparse_IDs = []

    ID_bases = IDs[0::2] #ID bases
    ID_ranges = IDs[1::2] # ID ranges
    ID_pairs = zip(ID_bases, ID_ranges)

    for ID_pair in ID_pairs:
        my_range = range(ID_pair[0], ID_pair[0] + ID_pair[1])
        sparse_IDs += [*my_range]
    
    IDs = sparse_IDs


# doing each mapping jump with full group (bfs-like approach) - no revisits
cur_input_line = 1

for cur_hop in range(total_hops):
    
    cur_input_line += 2 # skip current mapping's header title
    mappings_to_handle : list[tuple[int, int, int]] = [] # (dest, src, reach)
    while(True):
        if input_lines[cur_input_line] == '':
            break
        mappings_to_handle.append(input_lines[cur_input_line].split())
        cur_input_line += 1
    
    next_IDs = []

    for my_id in IDs:
        next_IDs.append(execute_hop(my_id, mappings_to_handle))
    
    IDs = next_IDs
    print("hop done")

print(f"lowest location ID: {min(IDs)}")
