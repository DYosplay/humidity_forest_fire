from mesa import Agent
from mesa.datacollection import DataCollector
import random

class TreeCell(Agent):
    """
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """

    def __init__(self, pos, humidity, model):
        """
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"
        self.fire_force = random.uniform(0, 1)
        self.three_humidity = humidity + random.uniform(-0.1, 0.1)

        

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        if self.condition == "On Fire":
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                # se a arvore vizinha estiver bem e a "forca do fogo" for maior que a humidade da arvore, pega fogo.
                if neighbor.condition == "Fine" and self.fire_force > neighbor.three_humidity:
                    neighbor.condition = "On Fire"
                    
            self.condition = "Burned Out"

        
