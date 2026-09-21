##
## EPITECH PROJECT, 2026
## my_pgp
## File description:
## maths
##

def sub_bytes(state: list[list[int]], s_box: list[int]) -> list[list[int]]:
    """Apply the SubBytes transformation to the state using the S-box."""
    return [[s_box[byte] for byte in row] for row in state]

def inv_sub_bytes(state: list[list[int]], inv_s_box: list[int]) -> list[list[int]]:
    """Apply the InvSubBytes transformation to the state using the inverse S-box."""
    return [[inv_s_box[byte] for byte in row] for row in state]

def shift_rows(state: list[list[int]]) -> list[list[int]]:
    """Apply the ShiftRows transformation to the state."""
    return [row[i:] + row[:i] for i, row in enumerate(state)]

def inv_shift_rows(state: list[list[int]]) -> list[list[int]]:
    """Apply the InvShiftRows transformation to the state."""
    return [row[-i:] + row[:-i] for i, row in enumerate(state)]

def add_round_key(state: list[list[int]], round_key: list[list[int]]) -> list[list[int]]:
    """Apply the AddRoundKey transformation to the state."""
    return [[s_byte ^ k_byte for s_byte, k_byte in zip(s_row, k_row)] for s_row, k_row in zip(state, round_key)]
