def is_vowel(char: str) -> bool:
    if len(char) != 1:
        raise ValueError(f"Expected a single character, got {char}")

    return char.lower() in "aeiou"


if __name__ == "__main__":
    print(is_vowel("a"))
    print(is_vowel("b"))
