# -*- coding: utf-8 -*-
"""Atividade com ChatGPT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16yz_CrfOkNf95Y-7dA48MLtTs6wnDSsx

# Utilizando o CrossValidation

O objetivo da `CrossValidation` é avaliar o desempenho do modelo através de uma divisão do conjunto de dados em vários subconjuntos para que o modelo possa ser treinado e avaliado várias vezes em diferentes partições do conjunto de dados. Sendo o objetivo principal obter uma estimativa mais precisa do desempenho do modelo em dados não vistos.

---

Importando as bibliotecas necessárias:
"""

import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix

"""Carregando a base de dados:"""

url = 'https://gist.githubusercontent.com/tonicprism/95bc1a6de11c9ede0530d250828d24b5/raw/8ae4d8cae2b6a957933956b1e17c9424f641e771/mobile_price_classification.csv'
data = pd.read_csv(url)

"""Mostrando as colunas da base de dados:"""

#analisando as primeiras entradas do df
data.head()

"""Mostrando informações sobre a base de dados (número total de linhas, o tipo de cada atributo e o número de valores não nulos):"""

data.info()

"""Plotando um histograma para cada atributo numérico presente na base de dados."""

data.hist(bins=50, figsize=(20,15))
plt.show()

"""Definindo as variáveis independentes (X) e a variável dependente (y):"""

X = data.drop('price_range', axis=1)
y = data['price_range']

"""Criando o modelo de classificação (por exemplo, DecisionTreeClassifier) e defina seus hiperparâmetros, se necessário:"""

clf = DecisionTreeClassifier(max_depth=3)

"""Executando a validação cruzada usando o cross_val_score:"""

scores = cross_val_score(clf, X, y, cv=10)

"""> Onde o parâmetro cv=10 define o número de folds (divisões) que serão utilizados na validação cruzada.

Exibindo a média e o desvio padrão das métricas de avaliação:
"""

print("Acurácia: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

"""> O resultado *mostra* a acurácia média e o desvio padrão das acurácias calculadas em cada um dos folds.

# Utilizando o GridSearch

O objetivo da técnica `GridSearch` é otimizar os **hiperparâmetros** (parâmetros do modelo utilizado) através de uma busca exaustiva em uma grade de possíveis valores de hiperparâmetros (no exemplo a baixo será utilizado os hiperparâmetros do modelo `DecisionTreeClassifier`) para encontrar a combinação que produz o melhor desempenho do modelo.

---

Importando o `sklearn.model_selection`, `train_test_split` e `GridSearchCV`
"""

from sklearn.model_selection import train_test_split, GridSearchCV

# Dividindo em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Definindo a grade de parâmetros a ser testada
param_grid = {'criterion': ['gini', 'entropy'], 
              'max_depth': [2, 4, 6, 8, 10], 
              'min_samples_split': [2, 5, 10, 15, 20],
              'min_samples_leaf': [1, 2, 4, 6, 8]}

# Instanciando o GridSearchCV
grid_search = GridSearchCV(clf, param_grid, cv=5)

# Treinando o modelo
grid_search.fit(X_train, y_train)

# Imprimindo os melhores parâmetros encontrados
print("Melhores parâmetros: ", grid_search.best_params_)

# Fazendo previsões no conjunto de teste
y_pred = grid_search.predict(X_test)

# Imprimindo a acurácia do modelo
print("Acurácia: ", grid_search.score(X_test, y_test))

"""# Os resultados do uso das técnicas Cross `Validation` e `GridSearch` (Em gráfico)"""

# Criando uma tabela com os resultados
results = pd.DataFrame(grid_search.cv_results_)

# Mostrando a tabela
print(results[['params', 'mean_test_score', 'std_test_score', 'rank_test_score']])

"""Gerando um gráfico com a correlação dos atributos da minha base de dado, indicando o grau de relação entre elas (quanto menor a porcentagem, menor o grau de relação entre o elemento da linha vertical e linha horizontal)."""

correlation = data.corr()

print(correlation)

plot = sns.heatmap(correlation, annot = True, fmt=".1%", lineWidths=0.6)

"""Gerando um historiograma com o resultado do uso das técnicas."""

# Gerando o gráfico de distribuição dos resultados
sns.histplot(data=scores, kde=True)