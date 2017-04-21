

class Controller(object):

    def __init__(self, model):
        self.model = model

    def handle_key(self, key):
        if key == ord('q'):
            self.model.running = False
        elif key == ord('p'):
            self.model.sort_by = 'procs'
        elif key == ord('m'):
            self.model.sort_by = 'mem'
        elif key == ord('c'):
            self.model.sort_by = 'cpu'
        elif key == ord('u'):
            self.model.sort_by = 'user'
        elif key == ord('h') or key == ord('H'):
            self.model.mode = 'help'
