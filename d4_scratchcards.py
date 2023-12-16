
with open("input.txt") as input_file:
    input_ = input_file.read()

lines = input_.split('\n')

points_total = 0
card_match_counts = {}

for pos, line in enumerate(lines):
    numbers = line.split(": ")[1]

    (left_nos, right_nos) = numbers.split(" | ")
    winning_numbers = set(left_nos.split())
    present_numbers = set(right_nos.split())
    matches = set.intersection(winning_numbers, present_numbers)

    card_match_counts[pos] = len(matches)

    if len(matches) > 0:
        points = 2**(len(matches) - 1)
        points_total += points

print("total points: " + str(points_total))

cards_handled = len(card_match_counts)

# initiate queue of card copies
card_queue = {}
for pos, card_score in card_match_counts.items():

    if card_score < 1:
        continue

    for i in range(card_score):
        added_card_no = pos + i + 1
        card_queue[added_card_no] = card_queue.get(added_card_no, 0) + 1

# loop over queue and determine next iteration's content
while len(card_queue):
    new_queue = {} # walk through original queue, populate new and swap
    for card_copy_pos, card_copy_count in card_queue.items():

        my_card_score = card_match_counts[card_copy_pos]
        if my_card_score < 1:
            continue

        for i in range(my_card_score):
            added_card_no = card_copy_pos + i + 1
            new_queue[added_card_no] = new_queue.get(added_card_no, 0) + card_copy_count

    cards_handled += sum(card_queue.values())
    card_queue = new_queue

print(cards_handled)