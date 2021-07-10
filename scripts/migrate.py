import subprocess


def main():
    cmd = ["python", "manage.py", "migrate"]
    subprocess.run(cmd)
