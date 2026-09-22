#!/usr/bin/env python3

##
## EPITECH PROJECT, 2026
## my_pgp
## File description:
## main
##

import sys

from src.parsing.parsing import parse_input
from src.utils.endianness import hex_to_bytes, bytes_to_hex
from src.utils.blocks import split_into_blocks, pad_block
from src.algorithms.aes.keys import keys_expansion
from src.algorithms.aes.core import aes_encrypt_block, aes_decrypt_block
from src.algorithms.xor import xor


def process_aes(message: bytes, key: bytes, mode: str, single_block: bool) -> bytes:
    key_schedule = keys_expansion(key)
    block_size = 16

    if single_block:
        if len(message) != block_size:
            raise ValueError(f"In block mode (-b), message must be {block_size} bytes (got {len(message)}).")
        blocks = [message]
    else:
        blocks = split_into_blocks(message, block_size)
        if mode == "c" and blocks and len(blocks[-1]) < block_size:
            blocks[-1] = pad_block(blocks[-1], block_size)

    output = []
    for b in blocks:
        if mode == "c":
            output.append(aes_encrypt_block(b, key_schedule))
        else:
            output.append(aes_decrypt_block(b, key_schedule))
    return b"".join(output)


def process_xor(message: bytes, key: bytes, mode: str, single_block: bool) -> bytes:
    block_size = len(key)
    if block_size == 0:
        raise ValueError("Key cannot be empty.")

    if single_block:
        if len(message) != block_size:
            raise ValueError(f"In block mode (-b), message and key must have the same size ({block_size} bytes).")
        blocks = [message]
    else:
        blocks = split_into_blocks(message, block_size)
        if mode == "c" and blocks and len(blocks[-1]) < block_size:
            blocks[-1] = pad_block(blocks[-1], block_size)

    output = [xor(b, key[:len(b)]) if mode == "d" and len(b) < block_size else xor(b, key) for b in blocks]
    return b"".join(output)


def main():
    try:
        args = parse_input()

        if args.mode == "g":
            raise NotImplementedError("RSA key generation (-g) is not implemented yet.")

        raw_data = sys.stdin.buffer.read()
        if args.single_block and raw_data.endswith(b"\n"):
            raw_data = raw_data[:-1]

        key_bytes = hex_to_bytes(args.key)
        if args.mode == "c":
            message_bytes = raw_data
        else:
            message_bytes = hex_to_bytes(raw_data.decode("ascii").strip())

        if args.crypto_system == "aes":
            result = process_aes(message_bytes, key_bytes, args.mode, args.single_block)
        elif args.crypto_system == "xor":
            result = process_xor(message_bytes, key_bytes, args.mode, args.single_block)
        else:
            raise NotImplementedError(f"Crypto system '{args.crypto_system}' is not implemented yet.")

        if args.mode == "c":
            print(bytes_to_hex(result), end="")
        else:
            sys.stdout.buffer.write(result)

    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(84)


if __name__ == "__main__":
    main()
