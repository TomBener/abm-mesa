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
        '''
        Create a new forest fire model.

        Args:
            - height: the grid's height
            - width: the grid's width
            - density: what fraction of grid cells have a tree in them (initially)
        '''

        '''
        Set up model ojects
        
        RandomActivation is a schedular which actives each agent once per step,
        in random order, with the order reshuffled every step.
        This is equivalent to the NetLogo 'ask agent…' and is generally the
        default behavior for an ABM
        self.schedule = RandomActivation(self)
        self.grid = Grid(height, width, torus=False)
        '''
        self.datacollector = DataCollector(
            {
                # lambda function, it is like: lambda x, y: x ** y
                'Fine': lambda m: self.count_type(m, 'Fine'),
                'On Fire': lambda m: self.count_type(m, 'On Fire'),
                'Burned Out': lambda m: self.count_type(m, 'Burned Out'),
            }
        )

        # Place a tree in each cell with Prob = density (here is 0.65)
        # coord_iter: returns coordinates as well as cell contents.
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = 'On Fire'
                # place_agent: positions an agent on the grid, and set its pos variable.
                self.grid._place_agent((x, y), new_tree)
                # Add an agent object to the schedule.
                self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        '''
        Advance the model by one step.
        '''
        self.schedule.step()
        # Collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, 'On Fire') == 0:
            self.running = False

    @staticmethod  # I don’t know this method
    def count_type(model, tree_condition):
        '''
        Helper method to count trees in a given condition in a given model.
        '''
        # Bear in mind this kind method
        # initial score is 0, which is very helpful.
        count = 0
        '''
        The default DataCollector has sevaral assumptions:
            - The model has a schedule object called 'schedule'
            - The schedule has an agent list called 'agents'
            - For collecting agent-level variables, agents must have a unique_id
        '''
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
