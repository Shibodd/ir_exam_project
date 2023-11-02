import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def creazione_grafico(dcg,idcg,query):
    n1=len(dcg)
    n2=len(idcg)
    dcg_line=dcg
    idcg_line=idcg
    colonna_x=np.arange(0.0,n1)
    col_line_x=np.arange(0.0,n1)
    colonna_x2=np.arange(0.0,n2)
    col_line_x2=np.arange(0.0,n2)
    plt.figure(None,[10,10])
    plt.subplot(211)
    plt.xticks(colonna_x)
    plt.setp((plt.plot(colonna_x, dcg, 'bo', col_line_x, dcg_line, 'k')),'color','g')
    plt.setp((plt.plot(colonna_x2, idcg, 'bo', col_line_x2, idcg_line, 'k')),'color','r')

    plt.grid(True)
    plt.title(query)
    plt.xlabel('Rank')
    plt.ylabel('Gain')
    plt.legend(['DCG','','IDCG',''])
    plt.show()

