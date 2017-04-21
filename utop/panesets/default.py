from utop.pane import PaneSet, Pane
from utop.views.footer import Footer as FooterView
from utop.views.header import Header as HeaderView
from utop.views.content import Content as ContentView


class DefaultPaneSet(PaneSet):

    def set_panes(self):

        stdscr = self.model.stdscr
        maxx = self.model.maxx
        maxy = self.model.maxy

        header = Pane(stdscr, maxx, 10)
        header.set_view(HeaderView(self.model))

        content = Pane(stdscr, maxx, maxy - 12, 0, 10)
        content.set_view(ContentView(self.model))

        footer = Pane(stdscr, maxx, 2, 0, maxy - 2)
        footer.set_view(FooterView(self.model))

        self.panes.append(header)
        self.panes.append(content)
        self.panes.append(footer)
