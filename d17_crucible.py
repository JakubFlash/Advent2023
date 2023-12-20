from collections import deque


with open("input.txt") as input_file:
    input_ = input_file.read() 

input_lines = input_.split('\n')




"""
nodes   : city squares
edges   : 2-4 directly neighbouring squares
weights : cost of entering given block
"""
directions = {
    "right" : 0,
    "down" : 1,
    "left" : 2,
    "up" : 3
}

class CityBlock():

    def __init__(self, cost, col_no, row_no) -> None:
        self.visited = False
        self.distance = -1 # infinity
        self.parent = None
        self.track_record = deque([-1,-1,-1], 3) # anti 3 consecutive steps in one dir
        self.cost_of_entry = cost

        self.u_neighbour = None
        self.d_neighbour = None
        self.l_neighbour = None
        self.r_neighbour = None

        self.pos_x = col_no
        self.pos_y = row_no # for heuristic if switching from Dijkstra to A*

def connect_nodes_updown(bottom : CityBlock, top : CityBlock) -> None:
    bottom.u_neighbour = top
    top.d_neighbour = bottom

def connect_nodes_leftright(left : CityBlock, right : CityBlock) -> None:
    left.r_neighbour = right
    right.l_neighbour = left

def interconnect_lines(bottom : list[CityBlock], top : list[CityBlock]) -> None:
    for i in range(len(bottom)):
        connect_nodes_updown(bottom[i], top[i])



unvisited_nodes = set()

start_pos = (0,0)

finish_pos = (len(input_lines) - 1, len(input_lines[0]) - 1)

def construct_graph(input_ : list[str]) -> set[CityBlock]:
    nodes_out = set()
    line_final_pos = len(input_lines[0]) - 1

    block_prev_line = []
    block_cur_line = []

    for line_no, line in enumerate(input_lines):

        prev_block = None
        for block_no, block in enumerate(list(line)):

            cur_block = CityBlock(int(block), block_no, line_no)
            block_cur_line.append(cur_block)
            if block_no == 0:
                prev_block = cur_block
                continue
            
            # not the first block of the line
            connect_nodes_leftright(prev_block, cur_block)
            prev_block = cur_block

            if block_no < line_final_pos:
                continue # line not finished yet

            # handle end of line
            if line_no == 0:
                block_prev_line = block_cur_line.copy()
                block_cur_line = []
                continue
            
            # this was not the first line -- interconnect nodes
            interconnect_lines(block_cur_line, block_prev_line)
            nodes_out = nodes_out.union(set(block_prev_line))

            block_prev_line = block_cur_line.copy()
            block_cur_line = []

    nodes_out = nodes_out.union(set(block_prev_line))
    return nodes_out

def locate_node_pos(pos : tuple[int,int], all_nodes : set[CityBlock]) -> CityBlock:
    for node in all_nodes:
        if (node.pos_y, node.pos_x) == pos:
            return node
    
    print(f"Node {pos[0], pos[1]} not found!")
    return None

def print_line(initial_node : CityBlock) -> None:
    while(True):
        print(initial_node.cost_of_entry, end="")
        if initial_node.r_neighbour == None:
            print("")
            return
        initial_node = initial_node.r_neighbour


def print_graph(initial_node : CityBlock) -> None:
    while(True):
        print_line(initial_node)
        initial_node = initial_node.d_neighbour

        if initial_node.d_neighbour == None:
            #final line reached
            print_line(initial_node)
            return


def find_lowest_dist_node(graph : set[CityBlock]) -> CityBlock | None:
    
    lowest_distance = -1
    lowest_distance_block = None
    for block in graph:
        if block.distance > 0: # distance not infinite
    
            if lowest_distance < 0: # first iteration?

                lowest_distance = block.distance
                lowest_distance_block = block

            elif block.distance < lowest_distance:

                lowest_distance = block.distance
                lowest_distance_block = block

    if lowest_distance_block == None:
        print("err")
    return lowest_distance_block

def Dijkstra(current_node : CityBlock, neighbour : CityBlock, direction : str) -> None:
    if not neighbour.visited:
        old_dist = neighbour.distance
        new_dist = neighbour.cost_of_entry + current_node.distance
        if old_dist < 0: #infinity
            neighbour.distance = new_dist
            neighbour.parent = current_node
            neighbour.track_record = current_node.track_record.copy()
            neighbour.track_record.appendleft(directions[direction])

        elif old_dist > new_dist:
            neighbour.distance = new_dist
            neighbour.parent = current_node
            neighbour.track_record = current_node.track_record.copy()
            neighbour.track_record.appendleft(directions[direction])
            
def is_dir_compliant(node : CityBlock, direction : str) -> bool:
    dir_no = directions[direction]
    track_copy = node.track_record.copy()
    if abs(dir_no - track_copy.popleft()) == 2:
        return False
    for track in node.track_record:
        if track != dir_no:
            return True
    return False



graph = construct_graph(input_lines)
first_block = locate_node_pos(start_pos, graph)
last_block = locate_node_pos(finish_pos, graph)
print_graph(first_block)

current_node = first_block
first_block.distance = 0

while not last_block.visited:
    # going through the neighbours
    if current_node.l_neighbour != None and is_dir_compliant(current_node, "left"):
        Dijkstra(current_node, current_node.l_neighbour, "left")
            
    if current_node.r_neighbour != None and is_dir_compliant(current_node, "right"):
        Dijkstra(current_node, current_node.r_neighbour, "right")

    if current_node.u_neighbour != None and is_dir_compliant(current_node, "up"):
        Dijkstra(current_node, current_node.u_neighbour, "up")
            
    if current_node.d_neighbour != None and is_dir_compliant(current_node, "down"):
        Dijkstra(current_node, current_node.d_neighbour, "down")

    current_node.visited = True
    graph.discard(current_node)
    current_node = find_lowest_dist_node(graph)


# reconstruct the path
current_node = last_block
while(current_node != first_block):
    print(current_node.cost_of_entry)
    current_node.cost_of_entry = "."
    current_node = current_node.parent

print(current_node.cost_of_entry)
print(last_block.distance)

print_graph(first_block)
