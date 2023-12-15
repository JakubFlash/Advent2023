
with open("input.txt") as input_file:
    input_ = input_file.read()

lines = input_.split('\n')
points_total = 0
for line in lines:
    numbers = line.split(": ")[1]
    (left_nos, right_nos) = numbers.split(" | ")
    winning_numbers = set(left_nos.split())
    present_numbers = set(right_nos.split())
    matches = set.intersection(winning_numbers, present_numbers)
    if len(matches) > 0:
        points = 2**(len(matches) - 1)
        points_total += points

print("total points: " + str(points_total))
