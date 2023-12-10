from pathlib import Path
from shutil import rmtree
from typing import NamedTuple

CURRENT_FILE = Path(__file__)
PROJECT_ROOT = CURRENT_FILE.parent

MAKEFILE_TEMPLATE = Path(PROJECT_ROOT, "Makefile.template")
MAKEFILE = Path(PROJECT_ROOT, "Makefile")

PYPROJECT_TEMPLATE = Path(PROJECT_ROOT, "pyproject.template.toml")
PYPROJECT = Path(PROJECT_ROOT, "pyproject.toml")

README_TEMPLATE = Path(PROJECT_ROOT, "README.template.md")
README = Path(PROJECT_ROOT, "README.md")

GIT_DIRECTORY = Path(PROJECT_ROOT, ".git")


class ProjectInfo(NamedTuple):
    name: str
    description: str


def main() -> None:
    project_infos = ask_project_infos()

    format_file(PYPROJECT_TEMPLATE, PYPROJECT, project_infos)
    format_file(README_TEMPLATE, README, project_infos)

    MAKEFILE_TEMPLATE.rename(MAKEFILE)
    rmtree(GIT_DIRECTORY)
    CURRENT_FILE.unlink()


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


def format_file(template: Path, target: Path, project_infos: ProjectInfo) -> None:
    with template.open() as file:
        file_content = file.read()

    file_content = format_template(file_content, project_infos)

    with target.open("w") as file:
        file.write(file_content)

    template.unlink()


def format_template(template: str, project_infos: ProjectInfo) -> str:
    """Format pyproject template with project infos.

    >>> format_template('', ProjectInfo('', ''))
    Traceback (most recent call last):
        ...
    ValueError: pyproject template not contain "{{ project_name }}" placeholder.

    >>> format_template('{{ project_name }}', ProjectInfo('', ''))
    Traceback (most recent call last):
        ...
    ValueError: pyproject template not contain "{{ project_description }}" placeholder.

    >>> format_template(
    ...     '{{ project_name }} {{ project_description }}',
    ...     ProjectInfo('',''),
    ... )
    ' '

    >>> format_template(
    ...     '{{ project_name }} {{ project_description }}',
    ...     ProjectInfo('foo',''),
    ... )
    'foo '

    >>> format_template(
    ...     '{{ project_name }} {{ project_description }}',
    ...     ProjectInfo('','foo'),
    ... )
    ' foo'

    >>> format_template(
    ...     '{{ project_name }} {{ project_description }}',
    ...     ProjectInfo('foo','bar'),
    ... )
    'foo bar'
    """
    name_placeholder = "{{ project_name }}"
    description_placeholder = "{{ project_description }}"
    error_template = 'Template not contain "{placeholder}" placeholder.'

    if name_placeholder not in template:
        error_message = error_template.format(placeholder=name_placeholder)
        raise ValueError(error_message)

    if description_placeholder not in template:
        error_message = error_template.format(placeholder=description_placeholder)
        raise ValueError(error_message)

    return template.replace(
        name_placeholder,
        project_infos.name,
    ).replace(
        description_placeholder,
        project_infos.description,
    )


if __name__ == "__main__":
    main()
