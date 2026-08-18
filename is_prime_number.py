#!/usr/bin/env python3
"""Simple prime number checker.

Usage:
  python is_prime_number.py 17      # non-interactive
  python is_prime_number.py         # prompts for input
"""

import sys


def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def main() -> None:
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            print("Please provide an integer as argument.")
            sys.exit(1)
    else:
        try:
            n = int(input("Enter an integer: ").strip())
        except Exception:
            print("Invalid input.")
            sys.exit(1)

    print(f"{n} is {'a prime' if is_prime(n) else 'not a prime'} number.")


if __name__ == '__main__':
    main()
