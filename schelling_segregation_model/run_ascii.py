'''
Class TextVisualization is defined in mesa/visualization

TextVisualization: Class meant to wrap around a Model object and render it in some way using Elements, in turn, renders a particular piece of information as text.

TextData: Uses getattr to get the value of a particular property of a model and prints it, along with its name.

TextGrid: Prints a grid, assuming that the value of each cell maps to exactly one ASCII character via a converter method. This (as opposed to a dictionary) is used so as to allow the method to access Agent internals, as well to potentially render a cell based on several values (e.g. an Agent grid and a Patch value grid).
'''

from mesa.visualization.TextVisualization import TextData, TextGrid, TextVisualization

from model import Schelling


class SchellingTextVisualization(TextVisualization):
    '''
    ASCII visualization for schelling model
    '''

    def __init__(self, model):
        '''
        Create new Schelling ASCII visualization
        '''
        super().__init__(model)

        grid_viz = TextGrid(self.model.grid, self.print_ascii_agent)
        happy_viz = TextData(self.model, 'happy')
        self.elements = [grid_viz, happy_viz]

    @staticmethod
    def print_ascii_agent(a):
        '''
        Minority agents are X, Majority are 0.
        '''
        if a.type == 0:
            return '0'
        if a.type == 1:
            return 'X'


if __name__ == '__main__':
    model_params ={
        'height': 20,
        'width': 20,
        # Agent density, from 0.8 to 1.0
        'density': 0.8,
        # Fraction minority, from 0.2 to 1.0
        'minority_pc': 0.2,
        # homophily: 3
        'homophily': 3,
    }

model = Schelling(**model_params)
viz = SchellingTextVisualization(model)
for i in range(10):
    print('Step', i)
    viz.step()
    print('---')
