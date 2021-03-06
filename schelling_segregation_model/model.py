from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector


class SchellingAgent(Agent):
    '''
    Define the Agent
    One of the core class
    '''

    def __init__(self, pos, model, agent_type):
        '''
        Create a new Schelling agent.

        Args:
            unique_id: Unique identifier for the agent.
            x, y: Agent initial location.
            agent_type: Indicator for the agengt’s type (minority = 1, majority = 0)
        '''
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type

    def step(self):
        # Iterate to see how many similar agents at the beginning (it's 0 initially)
        similiar = 0
        # `neighbor_iter` method is defined in mesa/space.py/Grid, in order to iterate over position neighbours.
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type == self.type:  # Why this syntax works? Need to look up it.
                similiar += 1

        # If unhappy, move
        # If around similar agents are less homophily (3), then move to an empty cell.
        # model.homophily is defined in the Model class below.
        if similiar < self.model.homophily:
            # `move_to_empty` is defined in mesa/space.py/Grid
            self.model.grid.move_to_empty(self)
        # If around similar agents are not less homophily (3), then plus the similar agents.
        else:
            self.model.happy += 1


class Schelling(Model):
    '''
    Define the Model
    The other core class
    '''

    '''
    mesa/space.py/Grid has 3 properties:
        - width
        - height
        - torus
    So `minority_pc` and `homophily` are customized properties here.
    '''
    def __init__(self, height = 20, width = 20, density = 0.8,
    minority_pc = 0.2, homophily = 3):
        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily

        # Scheduler is used `RandomActivation`, which is defined in mesa/time.py/RandomActivation.
        # Specify *time* of the model.
        self.schedule = RandomActivation(self)
        # `SingleGrid` is defined in mesa/space.py/SingleGrid.
        # Grid which strictly enforces one object per cell.
        # Specify *space* of the model.
        # width, height, torus are the native properties.
        self.grid = SingleGrid(width, height, torus = True)

        # Without happy agents initially
        self.happy = 0
        # DataCollector collects 3 types of data:
        # model-level data, agent-level data, and tables
        # A DataCollector is instantiated with 2 dictionaries of reporter names and associated variable names or functions for each, one for model-level data and one for agent-level data; a third dictionary provides table names and columns. Variable names are converted into functions which retrieve attributes of that name.
        self.datacollector = DataCollector(
            {'happy': 'happy'},  # Model-level count of happy agents, only one agent-level reporter
            # For testing purposes, agent’s individual x and y
            # lambda function, it is like:
            # lambda x, y: x ** y
            {'x': lambda a: a.pos[0], 'y': lambda a: a.pos[1]},
        )

        # Set up agents
        # We use grid iterator that returns
        # the coordinates of a cell as well
        # as its contents. (coord_iter)
        # coord_iter is defined in mesa/space.py, which, which returns coordinates as well as cell contents.
        for cell in self.grid.coord_iter():
            # Grid cells are indexed by [x][y] (tuple), where [0][0] is assumed to be the bottom-left and [width-1][height-1] is the top-right. If a grid is toroidal, the top and bottom, and left and right, edges wrap to each other.
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                if self.random.random() < self.minority_pc:
                    agent_type = 1
                else:
                    agent_type = 0

                agent = SchellingAgent((x, y), self, agent_type)
                # position_agent is defined in mesa/space.py. Position an agent on the grid. This is used when first placing agents!
                self.grid.position_agent(agent, (x, y))
                # schedule.add() method is defined in mesa/time.py.
                # Add an Agent object to the schedule.
                # 
                # Aggs:
                #   agent: An Agent to be added to the schedule. Note: the agent must have a step() method. 
                self.schedule.add(agent)

        self.running = True
        # datacollector.collect() method is defined in mesa/datacollection.py. When the collect(…) method is called, it collects these attributes and executes these functions one by one and store the results.
        self.datacollector.collect(self)

    # Oh, I did’t understand step(…) method previously. Now I know as a consequential method, it executes all stages for all agents.
    def step(self):
        '''
        Run one step of the model. If all agents are happy, halt the model.
        '''
        self.happy = 0  # Reset counter of happy agents
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Method get_agent_count is defined in mesa/time.py. It returns the current number agents in the queue. 
        if self.happy == self.schedule.get_agent_count():
            self.running = False

# comments on 2021/04/26 22:36
