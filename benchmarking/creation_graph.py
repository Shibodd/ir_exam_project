import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def creazione_grafico(dcg,idcg,query):
    dcg_x = np.arange(len(dcg) + 1)
    dcg = np.concatenate((np.array([0]), dcg))

    idcg_x = np.arange(len(idcg) + 1)
    idcg = np.concatenate((np.array([0]), idcg))

    plt.figure(None,[10,10])
    plt.subplot(211)

    plt.xticks(dcg_x)
    plt.setp((plt.plot(dcg_x, dcg, 'bo', dcg_x, dcg, 'k')),'color','g')
    plt.setp((plt.plot(idcg_x, idcg, 'bo', idcg_x, idcg, 'k')),'color','r')

    plt.grid(True)
    plt.title(query)
    plt.xlabel('Rank')
    plt.ylabel('Gain')
    plt.legend(['DCG','','Lower bound for IDCG',''])
    plt.show()

