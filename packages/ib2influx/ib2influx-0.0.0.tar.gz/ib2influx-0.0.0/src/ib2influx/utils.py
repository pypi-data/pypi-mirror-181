import subprocess


def cmd(command):
    """
    Run a command, checking that the return code == 0
    """
    p = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
    )
    return p.stdout.decode()
