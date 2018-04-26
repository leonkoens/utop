

class DataObject:

    def __init__(self, read_data=True):
        if read_data:
            self._run_methods('read')
            self._run_methods('parse')

    def _run_methods(self, method_type):
        for method in [m for m in dir(self) if m.startswith('_{}_'.format(method_type))]:
            getattr(self, method)()

    def get_data(self):
        raise NotImplementedError
