
def is_game_faulty(game: str) -> bool:
    rounds_raw = game.split(': ')[1] # drop game index

    rounds = rounds_raw.split('; ') # round = a group of selections

    for round in rounds:
        # transform each round into a (color : number) dict
        # query the dict for rules conformance
        selections = round.split(', ')
        color_counts = {}
        
        for selection in selections:
            c_count, color = selection.split()
            color_counts[color] = color_counts.get(color, 0) + int(c_count)

        if color_counts.get("red", 0) > 12:
            return True
        
        elif color_counts.get("green", 0) > 13:
            return True
        
        elif color_counts.get("blue", 0) > 14:
            return True

    return False

def calculate_power(game: str) -> int:
    rounds_raw = game.split(': ')[1] # drop game index

    rounds = rounds_raw.split('; ') # round = a group of selections

    max_color_counts = {}
    for round in rounds:
        # transform each round into a (color : number) dict
        # query the dict for rules conformance
        selections = round.split(', ')
        color_counts = {}
        
        for selection in selections:
            c_count, color = selection.split()
            color_counts[color] = color_counts.get(color, 0) + int(c_count)

        for (color, c_count) in color_counts.items():
            if max_color_counts.get(color, 0) < c_count:
                max_color_counts[color] = c_count
    
    power = 1
    for c_count in max_color_counts.values():
        power *= c_count

    return power

with open("input.txt") as input_file:
    possible_ID_sum = 0
    power_sum = 0
    for id, line in enumerate(input_file, 1):

        power_sum += calculate_power(line)

        if not is_game_faulty(line):
            possible_ID_sum += id

    print("possible ID sum: ", possible_ID_sum)
    print("sum of all powers: ", power_sum)

