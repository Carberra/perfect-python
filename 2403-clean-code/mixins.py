class ReprMixin:
    def __repr__(self) -> str:
        attrs = " | ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{type(self).__name__}({attrs})"


class Profile(ReprMixin):
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __str__(self) -> str:
        return f"{self.name} is {self.age} years old."


class Cube(ReprMixin):
    def __init__(self, width: float, height: float, depth: float) -> None:
        self.width = width
        self.height = height
        self.depth = depth

    def __str__(self) -> str:
        return f"{self.width}x{self.height}x{self.depth}"


if __name__ == "__main__":
    p = Profile("Ethan", 25)
    c = Cube(3, 4, 5)
    print(f"{p!r}")
    print(f"{c!r}")
