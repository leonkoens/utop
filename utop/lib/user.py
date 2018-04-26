import subprocess

from utop.lib.dataobject import DataObject


class User:

    def __init__(self, data):
        labels = ['name', 'passwd', 'uid', 'gid', 'comment', 'home', 'shell']
        user = dict(zip(labels, data))
        self.__dict__.update(user)

    def get_data(self):
        return self.__dict__


class UserList(DataObject):

    def _read_passwd(self):
        """
        Read the user data from /etc/passwd.
        """
        with open('/etc/passwd', 'r') as handle:
            self._passwd = handle.read()

    def _parse_passwd(self):
        """
        Parse the data from /etc/passwd and create User objects.
        """

        uids = {}

        for line in self._passwd.split("\n"):
            try:
                data = line.split(":")
                user = User(data)
                uids[data[2]] = user.get_data()
            except IndexError:
                pass  # Ignore headers

        self.uids = uids

    def get_data(self):
        return self.uids
