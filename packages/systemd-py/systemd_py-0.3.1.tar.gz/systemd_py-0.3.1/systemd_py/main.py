from typing import List

from .core.models import Section
from .utils.files import get_file
from .utils.daemon import Daemon


class Systemd:
    """
    Create systemd service file
    """

    def __init__(self, name: str, sections: List[Section]):
        """
        Create systemd service file

        :param name: Name of the systemd service
        :type name: str

        :param sections: List of sections
        :type sections: List[Section]
        """

        self._name = name
        self._sections = sections

        self._service = None

        self.daemon = Daemon(name)

    def create(self) -> str:
        """
        Build systemd service file

        :return: systemd service file
        :rtype: str
        """

        header = f'# {self._name}.service\n\n'
        sections = "\n\n".join(
            [str(s) for s in self._sections if str(s) != '' and str(s) is not None and not str(s).isspace()]
        )
        footer = f"\n\n# Via systemd_py"

        self._service = header + sections + footer

        return self._service

    def save(self, path: str) -> None:
        """
        Save systemd service file

        :param path: Path to save systemd service file
        :type path: str

        :return: None
        :rtype: None
        """

        if self._service is None:
            self.create()

        path = get_file(self._name, path)

        with open(path, 'w') as f:
            f.write(self._service)

        print(f'Saved {path}')

    def save_in_os(self) -> None:
        """
        Save systemd service file in /etc/systemd/system

        :return: None
        :rtype: None
        """

        self.save('/etc/systemd/system')

    def start_service(self):
        """
        Start service

        :return: None
        :rtype: None
        """

        self.daemon.reload()
        self.daemon.enable()
        self.daemon.start()

    def __str__(self):
        if self._service is None:
            self.create()

        return self._service

    def __repr__(self):
        return self.__str__()
