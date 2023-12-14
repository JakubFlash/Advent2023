DIGIT_NAMES = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine"
]

DIGIT_NAMES_INVERTED = [name[::-1] for name in DIGIT_NAMES]


def insert_earliest_digit_literal(cal_code: str, digit_list: [str]) -> str:

    # list of (digit, position) for digits in <1, 9> (as "zero" is out of scope)
    digit_positions = [(a, -1) for a in range(1,10)]
    for i in range(9):
        digit_positions[i] = (
            i+1, # compensate for lack of "zero" keyword
            cal_code.find(digit_list[i])
            )

    digit_positions.sort(key=lambda x: x[1])

    earliest_pos = (-1,-1)
    for i in range(9):
        if digit_positions[i][1] >= 0:
            earliest_pos = digit_positions[i]
            break
    
    if earliest_pos == (-1,-1):
        return cal_code
    
    (dig, pos) = earliest_pos
    cal_code = cal_code[:pos] + str(dig) + cal_code[pos:]
    return cal_code



def extract_numbers(cal_code: str) -> int:
    digits_only = filter(str.isdigit, cal_code)
    digits_only = "".join(digits_only)
    ldigit = int(digits_only[0])
    rdigit = int(digits_only[-1])
    return 10*ldigit + rdigit


total = 0

with open("input.txt") as input_file:
    for line in input_file:

        # first digit literal insertion
        line_augmented = insert_earliest_digit_literal(line, DIGIT_NAMES)

        # last digit literal insertion
        line_augmented = line_augmented[::-1]
        line_augmented = insert_earliest_digit_literal(line_augmented, DIGIT_NAMES_INVERTED)
        line_augmented = line_augmented[::-1]

        total += extract_numbers(line_augmented)

print("total: ", total)