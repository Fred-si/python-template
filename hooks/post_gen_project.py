import os
import subprocess


def run(command: list[str]) -> None:
    subprocess.run(command, capture_output=True, check=True)


python_version = '{{ cookiecutter.python_version }}'

print("Create venv...")
run([f"python{python_version}", "-m", "venv", "venv"])

print("Upgrade pip...")
run(["./venv/bin/pip", "install", "--upgrade", "pip"])

print("Install requirements...")
run(["./venv/bin/pip", "install", "-r", "requirements-dev.txt"])

print("Install types...")
run(["./venv/bin/mypy", "--install-types", "--non-interactive", "."])

print("Setup Git...")
run(["git", "init"])
# autoupdate modify .pre-commit-config.yaml, we need to run it before add files
run(["./venv/bin/pre-commit", "autoupdate"])
run(["git", "add", "."])

run(["./venv/bin/pre-commit", "install", "--install-hooks"])
run(["git", "commit", "-m", "Setup project"])

print("\nAll done, run:")
print(f"    cd {os.getcwd()} && source venv/bin/activate")
print("    gh repo create --public -s .")
