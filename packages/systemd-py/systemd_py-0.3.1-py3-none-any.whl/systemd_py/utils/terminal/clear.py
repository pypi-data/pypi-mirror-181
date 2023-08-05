import os
import subprocess


def clear() -> int:
    """
    Clear the terminal
    :return: The return code of the command
    :rtype: int
    """

    if os.name == 'posix':
        return subprocess.call('clear', shell=True)
    if os.name == 'nt':
        return subprocess.call('cls', shell=True)

    raise Exception(f'Unknown OS: {os.name}')
