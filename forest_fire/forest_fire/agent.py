from xml.etree.ElementTree import tostring
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
        self.count_steps = -1
        # self.datacollector = DataCollector(
        #     agent_reporters={
        #         "Position": self.get_pos,
        #         "Fire Force": self.get_fire_force,
        #         "Three Humidity": self.get_three_humidity,
        #     }
        # )
        

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        if self.condition == "On Fire":
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                # se a arvore vizinha estiver bem e a "forca do fogo" for maior que a humidade da arvore, pega fogo.
                if neighbor.condition == "Fine" and self.fire_force > neighbor.three_humidity:
                    neighbor.condition = "On Fire"
                    neighbor.count_steps = self.model.schedule.steps
                        #print("Oi\nsteps:", self.model.schedule.steps)
            self.condition = "Burned Out"

            #self.datacollector.collect(self)

            #print(self.datacollector.get_agent_vars_dataframe())


    # def get_pos(self):
    #     return self.pos 
    
    # def get_fire_force(self):
    #     return self.fire_force 

    # def get_three_humidity(self):
    #     return self.three_humidity 

