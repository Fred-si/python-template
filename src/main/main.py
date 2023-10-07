def main() -> str:
    return hello_world()


def hello_world() -> str:
    return f"{hello()}, {world()}!".capitalize()


def hello() -> str:
    """Say hello.

    >>> hello()
    'hello'
    """
    return "hello"


def world() -> str:
    """Say world.

    >>> world()
    'world'
    """
    return "world"
