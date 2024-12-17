import os
import subprocess
import sys

def create_venv(venv_dir="venv"):
    """Create a virtual environment if it doesn't exist."""
    if not os.path.exists(venv_dir):
        print(f"Creating virtual environment in {venv_dir}...")
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
    else:
        print(f"Virtual environment already exists in {venv_dir}.")


def upgrade_pip(venv_dir="venv"):
    """Upgrade pip in the virtual environment."""
    pip_executable = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "pip")
    print("Upgrading pip...")
    subprocess.run([pip_executable, "install", "--upgrade", "pip"], check=True)


def install_requirements(requirements_file="requirements.txt", venv_dir="venv"):
    """Install required packages from requirements.txt."""
    pip_executable = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "pip")
    print("Installing required packages...")
    subprocess.run([pip_executable, "install", "-r", requirements_file], check=True)


def create_dataset_folder(folder="dataset"):
    """Ensure the dataset folder exists."""
    print(f"Ensuring dataset folder exists: {folder}")
    os.makedirs(folder, exist_ok=True)


def run_python_script(script_path, venv_dir="venv"):
    """Run a Python script in the virtual environment."""
    python_executable = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "python")
    print(f"Running Python script: {script_path}")
    subprocess.run([python_executable, script_path], check=True)


if __name__ == "__main__":
    venv_dir = "venv"
    requirements_file = "requirements.txt"

    create_venv(venv_dir)
    upgrade_pip(venv_dir)
    install_requirements(requirements_file, venv_dir)
    create_dataset_folder()
    print("Setup completed!")
    print()
    run_python_script("verify_path.py")