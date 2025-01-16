from string import ascii_lowercase, digits

CHARACTERS = digits + ascii_lowercase


def get_remainder(input: str, factor: int, code_points: str) -> int:
    if not all(c in code_points for c in input):
        raise ValueError

    sum = 0
    n = len(code_points)
    char_map = {c: i for i, c in enumerate(code_points)}

    for character in reversed(input):
        code_point = char_map[character]
        increment = factor * code_point
        sum += (increment // n) + (increment % n)

        factor = 1 if factor == 2 else 2

    return sum % n


def generate_check_character(input: str) -> str:
    n = len(CHARACTERS)
    remainder = get_remainder(input, 2, CHARACTERS)
    return CHARACTERS[(n - remainder) % n]


def validate_string(input: str) -> bool:
    remainder = get_remainder(input, 1, CHARACTERS)
    return remainder == 0


if __name__ == "__main__":
    print(generate_check_character("92hello1worl9ds"))
    print(validate_string("92hello1worlx6zd"))
