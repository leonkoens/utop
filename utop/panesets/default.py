from utop.pane import PaneSet, Pane
from utop.views.footer import Footer as FooterView
from utop.views.header import Header as HeaderView
from utop.views.content import Content as ContentView


class DefaultPaneSet(PaneSet):

    def set_panes(self):

        stdscr = self.model.stdscr
        maxx = self.model.maxx
        maxy = self.model.maxy

        header_size = 7
        footer_size = 2

        header = Pane(stdscr, maxx, header_size)
        header.set_view(HeaderView(self.model))

        content = Pane(stdscr, maxx, maxy - (header_size + footer_size), 0, header_size)
        content.set_view(ContentView(self.model))

        footer = Pane(stdscr, maxx, footer_size, 0, maxy - footer_size)
        footer.set_view(FooterView(self.model))

        self.panes.append(header)
        self.panes.append(content)
        self.panes.append(footer)
