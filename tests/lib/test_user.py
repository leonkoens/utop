import unittest

from utop.lib.user import UserList


class UserListTest(unittest.TestCase):

    def test_init(self):
        userlist = UserList()
        self.assertEqual(userlist.get_data()['0']['name'], 'root')
