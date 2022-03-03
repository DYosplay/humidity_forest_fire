# Dados do aluno:
    João Pedro Felix de Almeida
    Matrícula: 19/0015292
    Modelo utilizado: FOREST_FIRE

# Explicações

## Apresentação do novo modelo
Aqui proponho e implemento uma variação do modelo de incêndio em florestas disponibilizado.

A modificação nasce da inserção da variável (manipulável) de humidade do ar e o objetivo é analisar como essa variável interfere no experimento.

## Hipótese causal: 
Quanto maior o nível de humidade do ar, mais difícil é para que um incêndio se espalhe em uma floresta. Da mesma maneira, quanto menor o nível de humidade do ar, mais fácil é para que um incêndio se espalhe em uma floresta.

## Justificativa para as mudanças realizadas nos arquivos:

server.py: 
1) Adicionado o parâmetro de modelo "humidity" do tipo slider. É isso que permite ao usuário manipular o parâmetro através da interface gráfica.

model.py: 
1) As variáveis "density" e "humidity" agora são salvas como variáveis do modelo. Isso não interfere na execução do mesmo. Foi adicionado apenas para facilitar o salvamento dos arquivos csv.

2) Foi criado um novo datacollector onde os dados são coletados após o término do último passo de execução. Esse coletor é responsável por obter informações relativas aos agentes e serve basicamente para determinar quanto tempo (em passos) foi necessário até que uma árvore começasse a pegar fogo.

3) Ao término da execução do último passo, tanto o coletor já existente (que coleta dados a nível de modelo), quanto o coletor criado por mim (que coleta dados a nível de agente) geram seus respectivos arquivos csv. O nome desses arquivos utiliza um carimbo data e hora, bem como explicitam os valores dos parâmetros "humidity" e "density" utilizados.

agent.py
1) Os agentes agora possuem a variável "count_steps", que marca quanto tempo (em passos) foi necessário até que a árvore começasse a pegar fogo. O valor padrão é -1, o que significa que se a árvore nunca pegar fogo, o valor na planilha será -1. 
Também foi adicionada uma variável auxiliar que altera aleatoriamente o nível da humidade do ar em 10 pontos percentuais para mais ou para menos na região da árvore em questão. Isso serve apenas para inserir um fator mais caótico no experimento e tornar os resultados mais evidentes (fáceis de serem analisados).

2) Agora, para determinar se o fogo se espalha de uma árvore para outra é feita a geração de um número aleatório entre 0 e 1 (inclusos). Se este número for superior a humidade naquela região (deslocada com a variável auxiliar explicada anteriormente) e, além disso, essa árvore que pode pegar fogo estiver com o estado "Fine", o fogo se espalha.
Caso contrário, isto é, ou o número gerado for menor que a humidade naquela região, ou a árvore não esteja com o estado "Fine", o incêndio não se espalha.

3) Agora, sempre que uma árvore começa a pegar fogo, o número do passo é salvo na variável do agente "count_steps"

## Como usar o simulador:
Apenas defina um valor para a densidade de árvores e para a humidade na floresta a partir dos sliders. Quanto maior a densidade, maior a quantidade de árvores e consequentemente mais próximas elas estarão. Quanto menor a humidade, mais fácil é para um incêncio se alastrar.

## Descrição das variáveis armazenadas nos arquivos .csv
Existem dois tipos de arquivos csv, um do ponto de vista dos agentes e outro do modelo.
As árvores representam os agentes e o conjunto de árvores representa o modelo.

A quantidade de passos necessários até que uma árvore comece a pegar fogo é uma informação do agente, ou seja, individual para cada árvore.

A quantidade de árvores em determinada situação (bem, pegando fogo ou queimada) em algum passo em toda a floresta, por sua vez, é uma informação da floresta (e portanto do modelo) e por isso só pode ser obtida a partir de uma análise de todos os agentes que compõem o modelo.

model_data: esse arquivo corresponde as variáveis geradas a nível de modelo. Trata-se de um .csv gerado a partir do coletor de dados que já estava pronto no modelo original.
Nesse arquivo, a primeira coluna corresponde ao passo da iteração. As colunas seguintes, nomeadas Fine, On Fire e Burned Out, respectivamente, denotam quantas árvores, naquele passo (step), se encontravam naquela situação em toda a floresta.

agent_data: esse arquivo corresponde as variáveis a nível de agente. Trata-se de um csv gerado a partir do coletor de dados que eu implementei.
Nesse arquivo, a primeira coluna, com nome "Step", corresponde ao passo da iteração. A segunda coluna corresponde ao Id do agente, que nada mais é que uma tupla com as coordenadas (x, y) da árvore. A última coluna, como nome "Steps to fire up", corresponde ao número de passos que foram necessários para que a árvore em questão começasse a pegar fogo. Caso a árvore nunca tenha pegado fogo, a variável assume o valor -1.














# Versão original do readme.md

# Forest Fire Model

## Summary

The [forest fire model](http://en.wikipedia.org/wiki/Forest-fire_model) is a simple, cellular automaton simulation of a fire spreading through a forest. The forest is a grid of cells, each of which can either be empty or contain a tree. Trees can be unburned, on fire, or burned. The fire spreads from every on-fire tree to unburned neighbors; the on-fire tree then becomes burned. This continues until the fire dies out.

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

To view and run the model analyses, use the ``Forest Fire Model`` Notebook.

## Files

### ``forest_fire/model.py``

This defines the model. There is one agent class, **TreeCell**. Each TreeCell object which has (x, y) coordinates on the grid, and its condition is *Fine* by default. Every step, if the tree's condition is *On Fire*, it spreads the fire to any *Fine* trees in its [Von Neumann neighborhood](http://en.wikipedia.org/wiki/Von_Neumann_neighborhood) before changing its own condition to *Burned Out*.

The **ForestFire** class is the model container. It is instantiated with width and height parameters which define the grid size, and density, which is the probability of any given cell having a tree in it. When a new model is instantiated, cells are randomly filled with trees with probability equal to density. All the trees in the left-hand column (x=0) are set to *On Fire*.

Each step of the model, trees are activated in random order, spreading the fire and burning out. This continues until there are no more trees on fire -- the fire has completely burned out.


### ``forest_fire/server.py``

This code defines and launches the in-browser visualization for the ForestFire model. It includes the **forest_fire_draw** method, which takes a TreeCell object as an argument and turns it into a portrayal to be drawn in the browser. Each tree is drawn as a rectangle filling the entire cell, with a color based on its condition. *Fine* trees are green, *On Fire* trees red, and *Burned Out* trees are black.

## Further Reading

Read about the Forest Fire model on Wikipedia: http://en.wikipedia.org/wiki/Forest-fire_model

This is directly based on the comparable NetLogo model:

Wilensky, U. (1997). NetLogo Fire model. http://ccl.northwestern.edu/netlogo/models/Fire. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

