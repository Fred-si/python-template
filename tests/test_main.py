from python_template.main import hello_world


class TestMain:
    def test_main_should_return_hello_world(self) -> None:
        assert hello_world() == "Hello, world!"
