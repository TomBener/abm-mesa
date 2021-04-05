# Code: https://mesa.readthedocs.io/en/master/tutorials/intro_tutorial.html
# Model: http://arxiv.org/abs/cond-mat/0211175


from mesa import Agent, Model, model
from mesa.time import RandomActivation
import matplotlib.pyplot as plt

class MoneyAgent(Agent):
    '''An agent with fixed initial wealth.'''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):
        if self.wealth == 0:
            return
        other_agent = self.random.choice(self.model.schedule.agents)
        other_agent.wealth += 1
        self.wealth -= 1
        
        print(f'Hi, I am agent {self.unique_id}, and I have {self.wealth} unit of money.')

class MoneyModel(Model):
    '''A model with some number of agents.'''
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()

empety_model = MoneyModel(10)
empety_model.step()
