import logging

from utop.model import Model
from utop.view import View


class Content(View):
    """ Draw the content of utop. This is the list of users with the
    other selected columns.
    """

    def draw(self):
        """ Draw the whole pane. """
        self.window.erase()
        self.draw_headers()
        self.draw_columns()

    def draw_columns(self):
        """ Draw the values of the sorted columns, per line. """
        i = 1  # Depends on what line the headers are.
        list_max = max(0, self.model.maxy - i)

        for user in self.model.sorted_users[:list_max]:
            j = 0

            user_data = self.model.user_data[user]

            for key in self.model.sorted_columns:
                value = Model.columns[key]['format'].format(user_data[key])
                self.addstr(i, j, value)
                j += Model.columns[key]['width']

            i += 1

    def draw_headers(self):
        """ Draw the headers of the content view. """
        i = 0

        for key in self.model.sorted_columns:
            self.addstr(0, i, self.model.columns[key]['title'][0], underline=True)
            self.addstr(0, i+1, self.model.columns[key]['title'][1:])
            i += self.model.columns[key]['width']
