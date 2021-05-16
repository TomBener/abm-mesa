# Defines the behaviours of an individual cell, which can be in two states: DEAD or ALIVE

from mesa import Agent


class Cell(Agent):

    # Represent a simple ALIVE or DEAD cell in the simulation.
    DEAD = 0
    ALIVE = 1

    def __init__(self, pos, model, init_state=DEAD):
        # Create a cell, in the given state, at the given x, y position.
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = init_state
        # Single Pre Underscore is used for internal use. Most of us don't use it because of that reason.
        # single pre underscore doesn't stop you from accessing the single pre underscore variable.
        # SO, Single Pre Underscore is only meant to use for the internal use.
        self._nextstate = None

        # Single Post Underscore: To avoid conflicts with the Python Keywords
        # Double Pre Underscore: Tells the Python interpreter to rewrite the attribute name of subclasses to avoid naming conflicts.
        # Double Pre And Post Underscores: magic methods or dunder methods

    @property
    def isAlive(self):
        return self.state == self.ALIVE

    @property
    def neighbors(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def step(self):
        '''
        Compute if the cell will be dead or alive at the next click. This is based on the number of alive or dead neighbors. The state is not changed here, but is just computed and stored in self._nextState, because our current state may still be necesssary for our neighbors to calculate their nest state.
        '''

        # Get the neighbors and apply the rules on whether to be alive or dead at the next tick.
        live_neighbors = sum(neighbor.isAlive for neighbor in self.neighbors)

        # Assume nextState is unchanged, unless changed below.
        self._nextState = self.state
        if self.isAlive:
            if live_neighbors < 2 or live_neighbors > 3:
                self._nextState == self.DEAD
            else:
                if live_neighbors == 3:
                    self._nextState = self.ALIVE

    def advance(self):
        '''
        Set the state to the new computed state -- computed in step().
        '''
        self.state = self._ALIVE