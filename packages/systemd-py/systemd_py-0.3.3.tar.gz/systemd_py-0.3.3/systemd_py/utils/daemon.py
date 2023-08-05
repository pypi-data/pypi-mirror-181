import subprocess


class Daemon:
    """
    Systemd daemon
    """

    def __init__(self, name: str):
        """
        Systemd daemon

        :param name: Name of the systemd daemon
        :type name: str
        """

        self._name = name

    @staticmethod
    def reload() -> None:
        """
        Reload systemd daemon
        """

        subprocess.run(['systemctl', 'daemon-reload'], check=True)
        print('Reloaded systemd daemon')

    def enable(self) -> None:
        """
        Enable systemd service
        """

        subprocess.run(['systemctl', 'enable', self._name], check=True)
        print(f'Enabled {self._name}')

    def disable(self) -> None:
        """
        Disable systemd service
        """

        subprocess.run(['systemctl', 'disable', self._name], check=True)
        print(f'Disabled {self._name}')

    def start(self) -> None:
        """
        Start systemd service
        """

        subprocess.run(['systemctl', 'start', self._name], check=True)
        print(f'Started {self._name}')

    def stop(self) -> None:
        """
        Stop systemd service
        """

        subprocess.run(['systemctl', 'stop', self._name], check=True)
        print(f'Stopped {self._name}')

    def restart(self) -> None:
        """
        Restart systemd service
        """

        subprocess.run(['systemctl', 'restart', self._name], check=True)
        print(f'Restarted {self._name}')

    def status(self) -> None:
        """
        Status systemd service
        """

        subprocess.run(['systemctl', 'status', self._name], check=True)
        print(f'Status {self._name}')

    def logs(self) -> None:
        """
        Logs systemd service
        """

        subprocess.run(['journalctl', '-u', self._name], check=True)
        print(f'Logs {self._name}')

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return self.__str__()
