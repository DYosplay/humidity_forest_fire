from hashlib import new
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation
from datetime import datetime
from .agent import TreeCell
from os import sep
import sys

class ForestFire(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65, humidity=0.6):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)
        
        self.density = density
        self.humidity = humidity
        
        # acontece a cada passo
        self.datacollector = DataCollector(
            model_reporters={
                "Width": lambda x: width,
                "Height": lambda x: height,
                "Density": lambda x: self.density,
                "Humidity ": lambda x: self.humidity,    
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "# Fine Clusteres": lambda m: self.count_clusteres(m, "Fine")[0],
                "Av. Fine Clusteres Size": lambda m: self.count_clusteres(m, "Fine")[1],
                "# Burned Out Clusteres": lambda m: self.count_clusteres(m, "Burned Out")[0],
                "Av. Burned Out Clusteres Size": lambda m: self.count_clusteres(m, "Burned Out")[1]
            }
        )

        # acontece ao termino do ultimo passo
        self.datacollector_agent = DataCollector(
            agent_reporters={
                "Width": lambda x: width,
                "Height": lambda x: height,
                "Density": lambda x: self.density,
                "Humidity ": lambda x: self.humidity,
                "Steps to fire up": lambda x: x.count_steps
            }
        )

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
                    new_tree.count_steps = 0
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False
            

            ###### DESCOMENTAR SE NÃO FOR BATCH RUN
            # now = str(datetime.now()).replace(":", "-")
            # df = self.datacollector.get_model_vars_dataframe()
            # #df.columns.values[0] = "Step"
            # df.to_csv("spreadsheet" + sep + "model_data humi=" + str(self.humidity) + " dens=" + str(self.density) + " " + now + ".csv")

            # self.datacollector_agent.collect(self)
            # df2 = self.datacollector_agent.get_agent_vars_dataframe()
            # df2.to_csv("spreadsheet" + sep + "agent_data humi=" + str(self.humidity) + " dens=" + str(self.density) + " " + now + ".csv")
        
        

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
    
    @staticmethod
    def count_clusteres(model, tree_condition):
        # número de clusteres
        n_clusteres = 0 

        # dicionario com os tamanhos
        dictionary = {}

        # itera por cada uma das árvores
        for tree in model.schedule.agents:
            # se a arvore nao tiver sido visitada e estiver bem
            if tree.visited == 0 and tree.condition == tree_condition:
                # faz a DFS
                count = ForestFire.depth_first_search(model, n_clusteres, tree, tree_condition)
                
                # contabiliza o tamanho dos clusteres
                if count in dictionary:
                    dictionary[count] += 1
                else:
                    dictionary[count] = 1
                
                # incrementa o número de clusters
                n_clusteres += 1
        
        # marca todas as arvores como não visitadas
        for tree in model.schedule.agents:
            tree.visited = 0
        
        # tamanho medio dos clusteres
        if(len(dictionary) > 0):
            numerator = [i*dictionary [i] for i in dictionary]
            mean_clusteres = "{:.1f}".format(sum(numerator) / sum(list(dictionary.values())))
        else:
            mean_clusteres = 0
        # retorna o número de clusteres e o tamanho medio deles
        return (n_clusteres, mean_clusteres)

    @staticmethod
    def depth_first_search(model, n_clusteres, tree, tree_condition):
        # define uma pilha
        tree_stack = []
        count = 0
        # coloca a arvore na pilha
        tree_stack.append(tree)

        # enquanto a pilha não estiver vazia
        while tree_stack != []:
            v = tree_stack.pop()

            # se essa arvore nao tiver sido visitada e estiver na condição solicitada
            if v.visited == 0 and v.condition == tree_condition:
                count+=1
                # marca essa arvore como visitada
                v.visited = n_clusteres + 1
                
                # para cada vizinha dessa arvore
                for neighbor in v.model.grid.neighbor_iter(v.pos):
                    tree_stack.append(neighbor)

        return count
            

    # def depth_first_search(model, n_clusteres, tree, tree_condition):
    #     tree.visited = n_clusteres + 1
    #     # para cada vizinha dessa arvore
    #     for neighbor in tree.model.grid.neighbor_iter(tree.pos):
    #         # se essa arvore vizinha nao tiver sido visitada e estiver bem
    #         if neighbor.visited == 0 and neighbor.condition == tree_condition:
    #             ForestFire.depth_first_search(model, n_clusteres, neighbor, tree_condition)


