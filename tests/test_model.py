import unittest

from utop.model import Model


class ModelTest(unittest.TestCase):

    def get_model(self):
        """ Get a clean Model object. 
        
        :return: The Model object
        :rtype: Model
        """
        Model.running = False
        model = Model()
        return model

