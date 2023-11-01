import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t*t)

def creazione_grafico(dcg,idcg):
    dcg_line=dcg
    idcg_line=idcg
    plt.figure(None,[10,10])
    plt.subplot(211)
    plt.setp((plt.plot(dcg, f(dcg), 'bo', dcg_line, f(dcg_line), 'k')),'color','g')
    plt.setp((plt.plot(idcg, f(idcg), 'bo', idcg_line, f(idcg_line), 'k')),'color','r')

    plt.title('Evaluation Comments')
    plt.xlabel('Comment Numbers')
    plt.ylabel('Comments Rating')
    plt.legend(['DCG','','IDCG Ideal',''])
    plt.show()

