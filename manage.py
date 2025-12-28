import os
import shutil
import subprocess
import sys

from anonflow import __version_str__, paths

def _check_command(cmd: str):
    return shutil.which(cmd) is not None

def _install_with_pip(package: str):
    if _check_command("pipx"):
        print(f"Trying to install {package} via pipx...")
        subprocess.run(["pipx", "install", package], check=True)
    elif _check_command("pip"):
        print(f"pipx not found. Installing {package} via pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
    else:
        raise RuntimeError(f"Failed to install {package}. Please check your pip/pipx setup.")

def _compile_translations():
    if not _check_command("pybabel"):
        print("pybabel not found!")
        user_input = input("Do you want to install it? [y/N]: ").strip().lower()
        if user_input == "y":
            _install_with_pip("babel")
        else:
            raise FileNotFoundError("pybabel not found. Please install it first or compile translations manually.")

    subprocess.run(["pybabel", "compile", "-d", paths.TRANSLATIONS_DIR], check=True)
    print("Translations compiled successfully!")

def _check_translations():
    mo_files, po_files = set(), set()
    for root, dirs, files in os.walk(paths.TRANSLATIONS_DIR):
        for file in files:
            if file.endswith(".mo"):
                mo_files.add(file[:-3])
            if file.endswith(".po"):
                po_files.add(file[:-3])

    return mo_files == po_files

def main():
    os.environ["VERSION"] = __version_str__
    args = sys.argv[1:]

    try:
        if args:
            if not _check_translations():
                _compile_translations()

            if args[0] == "run":
                subprocess.run(["python", "-m", "anonflow"], check=True)
            elif args[0] == "docker" and len(args) > 1:
                subprocess.run(["docker", "compose"] + args[1:], check=True)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
