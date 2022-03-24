from forest_fire import model
import itertools
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import matplotlib.pyplot as plt
import numpy as np

fixed_params = dict(height=50, width=50)  # Height and width are constant
# Vary density from 0.01 to 1, in 0.01 increments:
variable_params = dict(density=np.linspace(0, 1, 11)[1:], humidity=np.linspace(0.1, 1, 11)[1:])

# At the end of each model run, calculate the fraction of trees which are Burned Out
model_reporter = {
    "BurnedOut": lambda m: (
        model.ForestFire.count_type(m, "Burned Out") / m.schedule.get_agent_count()
    )
}

# Create the batch runner
param_run = BatchRunner(
    model.ForestFire,
    variable_parameters=variable_params,
    fixed_parameters=fixed_params,
    model_reporters=model_reporter,
)

param_run.run_all()
df = param_run.get_model_vars_dataframe()
plt.scatter(df.density, df.BurnedOut)
plt.xlim(0, 1)
plt.show()