import tensorflow as tf

import numpy as np
import random
from collections import deque
# Defining our Deep Q-Learning Trader

class Agent():  

# -----------------------------------------------------------------------

  # CONSTRUTOR

  def __init__(self, state_size, action_space=3, model_name="AITrader"):
    
    self.state_size = state_size # Tamanho da entrada da rede neural 
    self.action_space = action_space # Espaço de ação será 3, Comprar, Vender, Sem Ação (Tamanho da saída da rede neural)
    self.memory = deque(maxlen=2000) # Memória com 2000 posições. A função Deque permite adicionar elementos ao final, enquanto remove elementos do início.
    self.inventory = [] # Terá as comprar que já fizemos
    self.model_name = model_name # Nome do modelo para o Keras
    
    self.gamma = 0.95 # Parâmetro que ajudará a maximizar a recompensa
    self.epsilon = 1.0 # Taxa de aleatoriedade para atitudes ganacioas do algorítimo.
    self.epsilon_final = 0.01 # Taxa final reduzida
    self.epsilon_decay = 0.995 # Velocidade de decaimento da taxa

    self.model = self.model_builder() # Inicializa um modelo e de rede neural e salva na classe

# -----------------------------------------------------------------------

  # DEFININDO A REDE NEURAL

  def model_builder(self):
        
    model = tf.keras.models.Sequential()     
    model.add(tf.keras.layers.Dense(units=32, activation='relu', input_dim=self.state_size))
    model.add(tf.keras.layers.Dense(units=64, activation='relu'))
    model.add(tf.keras.layers.Dense(units=128, activation='relu'))
    model.add(tf.keras.layers.Dense(units=self.action_space, activation='linear')) # De maneira geral, teremos 3 saída na rede geral (número de espaços de ação)


    model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)); # Compilamos o modelo

    return model # Retornamos o modelo pela função.

# -----------------------------------------------------------------------

  # FUNÇÃO DE TRADE
  # Usa o Epsilon e um número aleatório para definir se usará um dado aleatório ou a previsão da rede.

  def trade(self, state):
    print('TRADE FUNCTION:')

    if random.random() <= self.epsilon:
      return random.randrange(self.action_space)
    actions = self.model.predict(state)
    print('Actions = ', actions)
    print('Actions Argmax = ', np.argmax(actions[0]))

    return np.argmax(actions[0])

# -----------------------------------------------------------------------

  # LOTE DE TREINAMENTO

  # Definindo o modelo para treinamento do lote

  def batch_train(self, batch_size): # Função que tem o tamanho do lote como argumento

    batch = [] # Iremos usar a memória como lote, por isso iniciamos com uma lista vazia

    # Iteramos sobre a memória, adicionando seus elementos ao lote batch
    for i in range(len(self.memory) - batch_size + 1, len(self.memory)): 
      batch.append(self.memory[i])

    # Agora temos um lote de dados e devemos iterar sobre cada estado, recompensa,
    # proximo_estado e conclusão do lote e treinar o modelo com isso.
    for state, action, reward, next_state, done in batch:
      reward = reward

      # Se não estivermos no último agente da memória, então calculamos a
      # recompensa descontando a recompensa total da recompensa atual.
      if not done:
        reward = reward + self.gamma * np.amax(self.model.predict(next_state)[0])

      # Fazemos uma previsão e alocamos à varivel target
      target = self.model.predict(state)
      target[0][action] = reward

      # Treinamos o modelo com o estado, usando a previsão como resultado esperado.
      self.model.fit(state, target, epochs=1, verbose=0)

    # Por fim decrementamos o epsilon a fim de gradativamente diminuir tentativas ganaciosas. 
    if self.epsilon > self.epsilon_final:
      self.epsilon *= self.epsilon_decay