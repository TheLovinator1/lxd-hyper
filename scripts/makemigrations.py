import subprocess


def main():
    cmd = ["python", "manage.py", "makemigrations"]
    subprocess.run(cmd)
