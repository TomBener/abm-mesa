from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation

from .agent import TreeCell

class ForestFire(Model):
    '''
    Simple Forest Fire Model.
    '''

    def __init__(self, height = 100, width = 100, density = 0.65):
        self.schedule = RandomActivation(self)