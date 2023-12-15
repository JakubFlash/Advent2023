
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



with open("input.txt") as input_file:
    possible_ID_sum = 0
    for id, line in enumerate(input_file, 1):
        if not is_game_faulty(line):
            possible_ID_sum += id
    
    print("possible ID sum: ", possible_ID_sum)
