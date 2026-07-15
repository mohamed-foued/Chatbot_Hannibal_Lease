"""
Lanceur Hannibal Lease : venv, installation des dépendances, Streamlit.
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / "venv"
MAIN_APP = ROOT / "main.py"
REQUIREMENTS = ROOT / "requirements.txt"


def venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def in_venv() -> bool:
    return Path(sys.executable).resolve() == venv_python().resolve()


def ensure_venv() -> None:
    if VENV_DIR.exists():
        return
    print("Création du venv...")
    subprocess.run(
        [sys.executable, "-m", "venv", str(VENV_DIR)],
        check=True,
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def reexec_in_venv() -> None:
    python = venv_python()
    if not python.exists():
        print("Erreur : Python du venv introuvable.")
        raise SystemExit(1)
    result = subprocess.run([str(python), str(Path(__file__).resolve()), *sys.argv[1:]], cwd=ROOT)
    raise SystemExit(result.returncode)


def ask_yes_no(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} (o/n) : ").strip().lower()
        if answer in {"o", "oui", "y", "yes"}:
            return True
        if answer in {"n", "non", "no"}:
            return False


def install_requirements() -> bool:
    print("Installation en cours...")
    cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-q",
        "--disable-pip-version-check",
        "-r",
        str(REQUIREMENTS),
    ]
    return subprocess.run(cmd, cwd=ROOT, stdout=subprocess.DEVNULL).returncode == 0


def launch_app() -> int:
    if not MAIN_APP.exists():
        print("Erreur : main.py introuvable.")
        return 1

    print("Lancement → http://localhost:8501  (Ctrl+C pour arrêter)\n")
    env = os.environ.copy()
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

    return subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(MAIN_APP),
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
            "--logger.level",
            "error",
        ],
        cwd=ROOT,
        env=env,
    ).returncode


def main() -> int:
    print("Hannibal Lease\n")

    ensure_venv()
    if not in_venv():
        reexec_in_venv()

    if ask_yes_no("Installer les dépendances ?"):
        if not install_requirements():
            print("Échec de l'installation.")
            return 1
        print("OK.\n")

    return launch_app()


if __name__ == "__main__":
    raise SystemExit(main())
