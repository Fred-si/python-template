from .hello import hello_world


def test_hello() -> None:
    assert hello_world() == 'Hello, world!'
