from pathlib import Path
from typing import NamedTuple


class ProjectInfo(NamedTuple):
    name: str
    description: str


def main() -> None:
    project_infos = ask_project_infos()
    setup_pyproject(project_infos)


def ask_project_infos() -> ProjectInfo:
    while True:
        name = ask_name()
        if ask_confirmation(f'Project name: "{name}"'):
            break

    while True:
        description = ask_description()
        if ask_confirmation(f'Project description: "{description}"'):
            break

    return ProjectInfo(name, description)


def ask_name() -> str:
    return clean_name(ask("Enter the project name: "))


def clean_name(name: str) -> str:
    """Replace underscore and spaces by dash in the given name.

    >>> clean_name('a')
    'a'
    >>> clean_name('a_a')
    'a-a'
    >>> clean_name('a a')
    'a-a'
    """
    return name.replace("_", "-").replace(" ", "-")


def ask_description() -> str:
    return clean_description(ask("Enter the project description: "))


def clean_description(description: str) -> str:
    """Capitalize the given string.

    >>> clean_description('a')
    'A'
    >>> clean_description('aa')
    'Aa'
    >>> clean_description('aa a')
    'Aa a'
    """
    return description.capitalize()


def ask_confirmation(prompt: str) -> bool:
    return (get_input(f"{prompt}? [O/n] ").lower() or "o") in "oy"


def ask(prompt: str) -> str:
    while not (answer := get_input(prompt)):
        pass

    return answer


def get_input(prompt: str) -> str:
    return input(prompt).strip()


def format_pyproject(pyproject: str, project_infos: ProjectInfo) -> str:
    """Format pyproject template with project infos.

    >>> format_pyproject('', ProjectInfo('', ''))
    Traceback (most recent call last):
        ...
    ValueError: pyproject template not contain "{{ project_name }}" placeholder.

    >>> format_pyproject('{{ project_name }}', ProjectInfo('', ''))
    Traceback (most recent call last):
        ...
    ValueError: pyproject template not contain "{{ project_description }}" placeholder.

    >>> format_pyproject(
    ...     '{{ project_name }} {{ project_description }}',
    ...     ProjectInfo('',''),
    ... )
    ' '

    >>> format_pyproject(
    ...     '{{ project_name }} {{ project_description }}',
    ...     ProjectInfo('foo',''),
    ... )
    'foo '

    >>> format_pyproject(
    ...     '{{ project_name }} {{ project_description }}',
    ...     ProjectInfo('','foo'),
    ... )
    ' foo'

    >>> format_pyproject(
    ...     '{{ project_name }} {{ project_description }}',
    ...     ProjectInfo('foo','bar'),
    ... )
    'foo bar'
    """
    name_placeholder = "{{ project_name }}"
    description_placeholder = "{{ project_description }}"
    error_template = 'pyproject template not contain "{placeholder}" placeholder.'

    if name_placeholder not in pyproject:
        error_message = error_template.format(placeholder=name_placeholder)
        raise ValueError(error_message)

    if description_placeholder not in pyproject:
        error_message = error_template.format(placeholder=description_placeholder)
        raise ValueError(error_message)

    return pyproject.replace(
        name_placeholder,
        project_infos.name,
    ).replace(
        description_placeholder,
        project_infos.description,
    )


def setup_pyproject(project_infos: ProjectInfo) -> None:
    file_dir = Path(__file__).parent

    with Path(file_dir, "pyproject.template.toml").open() as file:
        pyproject = file.read()

    pyproject = format_pyproject(pyproject, project_infos)

    with Path(file_dir, "pyproject.toml").open("w") as file:
        file.write(pyproject)


if __name__ == "__main__":
    main()
