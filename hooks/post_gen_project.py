import subprocess
from pathlib import Path


def run(command: list[str], *, raise_error: bool = True) -> str:
    completed = subprocess.run(command, capture_output=True, check=False)  # noqa: S603

    if raise_error and completed.returncode != 0:
        print(run(['ls', 'src']))
        print(f"Erreur lors de l’execution de la commande {command}")
        print(completed.stderr.decode())

        raise subprocess.CalledProcessError(
            completed.returncode,
            command,
        )

    return completed.stdout.decode()


python_version = "{{ cookiecutter.python_version }}"

print("Create venv...")
run([f"python{python_version}", "-m", "venv", "venv"])
run(["./venv/bin/pip", "install", "--upgrade", "pip"])

print("Install requirements...")
run(["./venv/bin/pip", "install", "-e", ".[dev]"])

print("Setup Git...")
run(["git", "init"])

# Autoupdate modify .pre-commit-config.yaml, we need to run it before add files
run(["./venv/bin/pre-commit", "autoupdate"])

run(["./venv/bin/pre-commit", "install", "--install-hooks"])

# Some pre-commit hooks return non-zero code even if modify files.
# We need to run pre-commit before for prevent git commit fail.
# First, pre-commit need index files
run(["git", "add", "."])
run(["./venv/bin/pre-commit"], raise_error=False)
# Re-index files modified by hooks
run(["git", "add", "."])

run(["git", "commit", "-m", "Setup project"])

print("\nAll done, run:")
print(f"    cd {Path.cwd()} && source venv/bin/activate")
print("    gh repo create --public -s .")
print("    git push --set-upstream origin main")
