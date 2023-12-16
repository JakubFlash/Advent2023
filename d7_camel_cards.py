HAND_GROUPS = [
        "high_cards",
        "pairs",
        "two_pairs",
        "threes",
        "fulls",
        "quads",
        "fives"
    ]

def group_hands(hands: list[tuple[str, int]]) -> dict[str : list[tuple[str, int]]]:
    hands_grouped = {group : [] for group in HAND_GROUPS}
    group_cardinalities = { # groups which can identified with cardinality alone
        5 : "high_cards",
        4 : "pairs",
        1 : "fives"  
    }

    for hand in hands:
        cardinality = len(set(hand[0]))

        if cardinality == 2: # resolve between quads and fulls
            duplicate_counter = 0
            for i in range(1,5):
                if hand[0][0] == hand[0][i]:
                    duplicate_counter += 1
            if duplicate_counter == 0 or duplicate_counter == 3:
                group = "quads"
            else:
                group = "fulls"

        elif cardinality == 3: # resolve between threes and two_pairs
            trips_counter = 0
            # in sorted hands, a three includes middle card: AAABC, ABBBC, ABCCC
            hand_sorted = "".join(sorted(hand[0]))
            trips_candidate = hand_sorted[2] 
            for i in range(0,5):
                if hand_sorted[i] == trips_candidate:
                    trips_counter += 1
            if trips_counter == 3:
                group = "threes"
            else:
                group = "two_pairs"

        else:
            group = group_cardinalities[cardinality] # generic resolution
            
        hands_grouped[group].append(hand)
    
    return hands_grouped


def sort_group(hands: list[tuple[str, int]]) -> list:

    def _eval_card(label : str) -> int:
        match label:
            case "T":
                return 10
            case "J":
                return 11
            case "Q":
                return 12
            case "K":
                return 13
            case "A":
                return 14
            case _:
                return int(label)
    
    def _evaluate_hand_pos(hand: str) -> int:
        pos = _eval_card(hand[0]) * 100000000
        pos += _eval_card(hand[1]) * 1000000
        pos += _eval_card(hand[2]) * 10000
        pos += _eval_card(hand[3]) * 100
        pos += _eval_card(hand[4])
        return pos
    
    hands_sorted = sorted(hands, key=lambda x: _evaluate_hand_pos(x[0]))
    return hands_sorted

def calc_score(sorted_hand_groups : dict[str : list[tuple[str, int]]]) -> int:
    reverse_rank = 1
    cum_score = 0

    for group in HAND_GROUPS:
        my_group = sorted_hand_groups[group]
        for hand in my_group:
            cum_score += reverse_rank * int(hand[1])
            reverse_rank += 1

    return cum_score


with open("input.txt") as input_file:
    input_ = input_file.read() 

input_lines = input_.split('\n')

hands = [tuple(line.split()) for line in input_lines]
groups = group_hands(hands)

groups_sorted = {}
for name, group in groups.items():
    if len(group) > 1:
        sorted_group = sort_group(group)
    else:
        sorted_group = group
    groups_sorted[name] = sorted_group

score = calc_score(groups_sorted)
print(score)