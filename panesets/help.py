from pane import PaneSet, Pane
from views.help import Help


class HelpPaneSet(PaneSet):

    def set_panes(self):

        stdscr = self.model.stdscr
        maxx = self.model.maxx
        maxy = self.model.maxy

        complete = Pane(stdscr, maxx, maxy)
        complete.set_view(Help(self.model))
        self.panes.append(complete)
