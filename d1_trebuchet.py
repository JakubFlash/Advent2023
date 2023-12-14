
def extract_numbers(cal_code: str) -> int:
    digits_only = filter(str.isdigit, cal_code)
    digits_only = "".join(digits_only)
    ldigit = int(digits_only[0])
    rdigit = int(digits_only[-1])
    return 10*ldigit + rdigit


total = 0

with open("input.txt") as input_file:
    for line in input_file:
        total += extract_numbers(line)

print("total: ", total)



