from utop import model
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
                width = Model.columns[key]['width']

                color = model.COLOR_DEFAULT

                if i - 1 == self.model.selected_row:
                    color = model.COLOR_CYAN
                elif i - 1 in self.model.tagged_rows:
                    color = model.COLOR_YELLOW

                self.addstr(i, j, value[:width-2], color=color)
                j += width

            i += 1

    def draw_headers(self):
        """ Draw the headers of the content view. """
        i = 0

        for key in self.model.sorted_columns:
            color = model.COLOR_DEFAULT

            if self.model.sort_by == key:
                color = model.COLOR_CYAN

            self.addstr(0, i, self.model.columns[key]['title'][0], underline=True, color=color)
            self.addstr(0, i+1, self.model.columns[key]['title'][1:], color=color)

            i += self.model.columns[key]['width']
