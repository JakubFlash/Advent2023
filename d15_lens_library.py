
def hash_char(hash_before : int, char_i : str) -> int:
    hash_before += ord(char_i)
    hash_before *= 17
    hash_before = hash_before % 256
    return hash_before

with open("input.txt") as input_file:
    input_ = input_file.read()
    input_sequence = input_.split(',')

    total_hash = 0
    for sequence in input_sequence:
        hash = 0
        for ch in sequence:
            hash = hash_char(hash, ch)
        total_hash += hash
    


print(total_hash)