import curses.textpad
import logging
import curses


class Controller(object):

    def __init__(self, model):
        self.model = model

    def handle_key(self, key):
        if key == -1:
            return

        if key == ord('q'):
            self.model.running = False
        elif key == ord('p'):
            self.model.sort_by = 'procs'
        elif key == ord('m'):
            self.model.sort_by = 'mem_percentage'
        elif key == ord('c'):
            self.model.sort_by = 'cpu_percentage'
        elif key == ord('u'):
            self.model.sort_by = 'user'
        elif key == ord('h') or key == ord('H'):
            self.model.mode = 'help'
        elif chr(key) in ['t', 'T']:

            self.model.paneset.footer.window.clear()
            self.model.paneset.footer.window.refresh()

            def check_return(x):
                if x == ord("\n"):
                    # Return the Ctrl-G command, which terminates the window, returning its
                    # contents.
                    return curses.ascii.BEL

                if chr(x).isdigit():
                    return x

            box = curses.textpad.Textbox(self.model.paneset.footer.window, insert_mode=True)
            box.edit(check_return)
            self.model.set_ticks_max(int(box.gather()))
