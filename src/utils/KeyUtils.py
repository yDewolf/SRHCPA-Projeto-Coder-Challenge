import utils.fileUtils.CsvUtils as CsvUtils

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# lowered_alphabet = []
# for char in alphabet:
#     lowered_alphabet.append(char.lower())
# 
# print(str(lowered_alphabet))


# Really bad and simple encryption system
# Made just for fun
def encrypt_key(key: str):
    offset = len(key)

    offsetted_key = ""
    for char in key:
        char = char.lower()
        new_char = char

        if alphabet.__contains__(char):
            new_char = offset_char(char, offset)

        elif char.isnumeric():
            new_char = int(char) % offset

        offsetted_key += str(new_char)
    
    chars_list = []
    swapped_list = []
    for char in offsetted_key:
        chars_list.append(char)
        swapped_list.append(char)

    for idx, char in enumerate(chars_list):
        if char.isnumeric():
            if int(char) < len(offsetted_key):
                swap_idx = int(char)

                store = chars_list[swap_idx]

                swapped_list[swap_idx] = offset_char(store, swap_idx)
                swapped_list[idx] = store
        
        elif idx != 0:
            if offset % idx == 0:
                swapped_list[idx] = char.swapcase()
        
    final_key = ""
    for char in swapped_list:
        final_key += str(char)
    
    return final_key

def offset_char(char: str, offset: int):
    char_idx = alphabet.index(char) + offset
    while char_idx >= len(alphabet):
        char_idx -= len(alphabet)
    
    return alphabet[char_idx]


def check_registered_key(key: str, keys_path: str) -> int:
    perm_level: int = 0

    keys = CsvUtils.get_csv_values_with_key(keys_path, ["key", "perm_level"], "key")
    encrypted_key = encrypt_key(key)

    if keys.__contains__(encrypted_key):
        perm_level = keys[encrypted_key]["perm_level"]
        print(f"Valid key with perm level: {perm_level}")
    else:
        # Push Warning:
        print("WARNING: Invalid Key!")

    return perm_level