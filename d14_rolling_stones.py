"""def summarize_load(layout : list[str]) -> int:
    total_load = 0
    modifier = len(layout)
    for line in layout:
        local_load = line.count('O') * modifier
        
        total_load += local_load
        modifier -= 1

    return total_load
        
def tilt_north(layout : list[str]) -> list[str]:
    resulting_layout = []
    # start the count at the beginning or at #
    # count Os column-wise
    # stop the count at #"""

def tilt_n_summarize_load(layout : list[str]) -> int:
    
    def _load() -> int:
        res_load = 0
        group_modifier = max_modifier - group_start_pos

        for i in range(group_size):
            res_load += group_modifier - i

        return res_load

    # transpose for simpler row-wise sums
    layout_T = [''.join(line) for line in zip(*layout)]

    max_modifier = len(layout_T[0])
    t_load = 0
    for line in layout_T:

        #initialize group count
        group_size = 0
        group_start_pos = 0

        for ch_pos, ch in enumerate(line):
            match ch:
                case '.':
                    continue
                case 'O':
                    group_size += 1
                case '#':
                    t_load += _load()

                    # reset group count
                    group_size = 0
                    group_start_pos = ch_pos + 1
        # end of line -> end of its final group
        t_load += _load()

    return t_load


with open("input.txt") as input_file:
    input_ = input_file.read() 

input_lines = input_.split('\n')

print(tilt_n_summarize_load(input_lines))