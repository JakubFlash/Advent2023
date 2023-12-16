from math import ceil

race_specs = [
    (45, 295),
    (98, 1734),
    (83, 1278),
    (73, 1210)
    ]

race_specs_test = [
    (7, 9),
    (15, 40),
    (30, 200)
    ]

race_specs_p2 = [
    (45988373, 295173412781210)
    ]

race_specs_test_p2 = [
    (71530, 940200)
    ]


def calculate_distance(time_limit : int, time_pressed : int) -> int:
    time_for_movement = time_limit - time_pressed
    if time_for_movement > 0:
        return time_pressed * time_for_movement
    else:
        return 0

def bisect_lowest_lhs_win(t_limit : int, goal : int) -> int:
    # locates first winning duration

    left = 0
    right = ceil(t_limit/2) # initial search boundaries

    while(abs(left-right) > 1):
            
        inclusive_mid = ceil((left+right) / 2)
        mid_wins = calculate_distance(t_limit, inclusive_mid) > goal

        if mid_wins:
            right = inclusive_mid
        elif not mid_wins:
            left = inclusive_mid
            
    return right
    

ways_to_win_prod = 1

for spec in race_specs_p2:
    
    time = spec[0]
    distance = spec[1]

    midpoint = time/2
    shortest_winning_press_t = bisect_lowest_lhs_win(time, distance)

    wincons_lhs = midpoint - shortest_winning_press_t
    total_wincons = 1 + wincons_lhs * 2
    print(f"total wincons: {total_wincons}")
    ways_to_win_prod *= total_wincons

print(f"total ways to win: {ways_to_win_prod}")
