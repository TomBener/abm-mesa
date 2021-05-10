from mesa import Agent

class TreeCell(Agent):
    '''
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition:
            - Fine
            - On Fire
            - Burned Out
        unique_id: (x, y) tuple.

    unique_id isn’t strictly necessary here,
    but it’s good practice to give one to each agent anyway.
    '''

    def __init__(self, pos, model):
        '''
        Create a new tree.
        Args:
            pos: The tree’s coordinates on the grid.
            model: standard model reference for agent
        '''
        super().__init__(pos, model)
        self.pos = pos
        # Initial condition is 'Fine'. That’s fine.
        self.condition = 'Fine'
        # self.status = 'good'  self.placeholder can be defined here

        def step(self):
            '''
            If the tree is on fire, spread it to fine tree nearby.
            '''
            if self.condition == 'On Fire':
                '''
                Please note that mesa/agent.py has imported the Model class, that is:
                from mesa.model import Model

                Python uses a dot (.) instead of a slash (/) to refer to the file path when importing packages or modules.
                
                PEP 8 explicitly recommends absolute imports.

                Be same as the Unix-like operating system. Relative imports make use of dot notation to specify location:

                # A single dot means that the module or package referenced is in the same directory as the current location.
                from .some_module import some_class

                # Two dots mean that it is in the parent directory of the current location
                from ..some_package import some_function

                # A bare dot means the current directory
                from . import some_clas

                self.model.grid.neighbor_iter is a method,
                which is defined in mesa/space.py.
                neighbor_iter: Iterates over position neighbors.
                '''
                for neighbor in self.model.grid.neighbor_iter(self.pos):
                    if neighbor.condition == 'Fine':
                        neighbor.condition = 'On Fire'
                self.condition = 'Burned Out'
