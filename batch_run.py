from forest_fire import model
import itertools
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
from datetime import datetime
import os

'''
Variáveis de controle: 
# height = altura do grid e width = largura do grid
'''
fixed_params = dict(height=100, width=100)  # Height and width are constant

'''
Variáveis independentes:
# density (densidade) que diz respeito a quantidade de árvores presentes na floresta
# humidity (humidade) que diz respeito a humidade média do ar na floresta
'''

# Se for uma execução de batch normal (em que ambas variáveis independentes variam), descomentar as duas linhas abaixo e comentar as duas linhas seguintes.
# Ambas variam de 0.1 até 1 em passos de 0.1
# variable_params = dict(density=np.linspace(0, 1, 11)[1:], humidity=np.linspace(0.1, 1, 11)[1:])

# Se for uma execução da mesma simulação várias vezes (para identificar se os resultados seguem uma distribuição aproximadamente normal)
n_simulations = 300
density_list = [0.55] * n_simulations
humidity_list = [0.32]
variable_params = dict(density= density_list, humidity=humidity_list)

'''
Variáveis dependentes:
# Fine: que corresponde ao número de árvores não queimadas ao término da execução
# BurnedOut: que corresponde ao número de árvores queimadas ao término da execução 
# NumberFineClusteres: que corresponde ao número de clusteres de árvores não queimadas ao término da execução
# AvFineClusteresSize: que corresponde ao tamanho médio dos clusteres de árvores não queimadas ao término da execução
# NumberBurnedOutClusteres: que corresponde ao número de clusteres de árvores queimadas ao término da execução
# AvBurnedOutClusteresSize: que corresponde ao tamanho médio dos clusteres de árvores queimadas ao término da execução
# Além disso, existe a variável dependente 'On Fire' (comentada nessa model reporter) que corresponde ao número de árvores queimando. Porém, como a simulação só acaba quando não existem mais árvores queimando, ao término da execução (que é quando ocorre a medição desse model reporter) esse número é necessariamente 0, visto que a condição de parada do modelo é justamente não haver mais árvores queimando e o número de árvores ser finito.
'''

model_reporter = {
    "Fine":  lambda m: model.ForestFire.count_type(m, "Fine"),
    # "On Fire":  lambda m: model.ForestFire.count_type(m, "On Fire"),
    "BurnedOut":  lambda m: model.ForestFire.count_type(m, "Burned Out"),
    "NumberFineClusteres": lambda m:  model.ForestFire.count_clusteres(m, "Fine")[0],
    "AvFineClusteresSize": lambda m:  model.ForestFire.count_clusteres(m, "Fine")[1],
    "NumberBurnedOutClusteres": lambda m:  model.ForestFire.count_clusteres(m, "Burned Out")[0],
    "AvBurnedOutClusteresSize": lambda m:  model.ForestFire.count_clusteres(m, "Burned Out")[1]
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
now = str(datetime.now()).replace(":", "-")
#df.columns.values[0] = "Step"

if not os.path.exists('batch_spreadsheet'):
    os.mkdir('batch_spreadsheet')

if not os.path.exists('images'):
    os.mkdir('images')

#df.to_pickle("batch_spreadsheet" + os.sep + "model_data humi=" + str(humidity_list[0]) + " dens=" + str(density_list[0]) + " " + now + ".csv")

df.to_csv("batch_spreadsheet" + os.sep + "model_data humi=" + str(humidity_list[0]) + " dens=" + str(density_list[0]) + " " + now + ".csv")



# #plt.hist(df.Fine, edgecolor='black', bins=20)
# #plt.xticks(range(1,3)) # para plotagem de 1 até 3, pode ser util pra plotar ate 10000

plt.clf()
plt.hist(df.Fine, edgecolor='black', bins=40)
plt.savefig("images" + os.sep + "Fine.png")

plt.clf()
plt.hist(df.BurnedOut, edgecolor='black', bins=40)
plt.savefig("images" + os.sep + "BurnedOut.png")

plt.clf()
plt.hist(df.NumberFineClusteres, edgecolor='black', bins=40)
plt.savefig("images" + os.sep + "NumberFineClusteres.png")

plt.clf()
df['AvFineClusteresSize'] = df['AvFineClusteresSize'].astype(float)
plt.hist(df.AvFineClusteresSize, edgecolor='black', bins=60)
plt.savefig("images" + os.sep + "AvFineClusteresSize.png")

plt.clf()
plt.hist(df.NumberBurnedOutClusteres, edgecolor='black', bins=40)
plt.savefig("images" + os.sep + "NumberBurnedOutClusteres.png")

plt.clf()
#plt.xticks(range(0,10000))
df['AvBurnedOutClusteresSize'] = df['AvBurnedOutClusteresSize'].astype(float)
plt.hist(df.AvBurnedOutClusteresSize, edgecolor='black', bins=60)
plt.savefig("images" + os.sep + "AvBurnedOutClusteresSize.png")

text = ""
text += "AvFineClusteresSize: Mean:" + str(df['AvFineClusteresSize'].mean()) + ", Std: " + str(df['AvFineClusteresSize'].std()) + '\n'
text += "Fine: Mean:" + str(df['Fine'].mean()) + ", Std: " + str(df['Fine'].std()) + '\n'
text += "BurnedOut: Mean:" + str(df['BurnedOut'].mean()) + ", Std: " + str(df['BurnedOut'].std()) + '\n'
text += "NumberFineClusteres: Mean:" + str(df['NumberFineClusteres'].mean()) + ", Std: " + str(df['NumberFineClusteres'].std()) + '\n'
text += "NumberBurnedOutClusteres: Mean:" + str(df['NumberBurnedOutClusteres'].mean()) + ", Std: " + str(df['NumberBurnedOutClusteres'].std()) + '\n'
text += "AvBurnedOutClusteresSize: Mean:" + str(df['AvBurnedOutClusteresSize'].mean()) + ", Std: " + str(df['AvBurnedOutClusteresSize'].std()) + '\n'

txt_file = open("Metrics model_data humi=" + str(humidity_list[0]) + " dens=" + str(density_list[0]) + " " + now + ".txt", 'w')
txt_file.write(text)

# # plt.savefig("plot.png")
# # plt.show()
