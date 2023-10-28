def verifica():
    print("inserire un punteggio da 0 a 2 (non rilevante, poco rilevante, rilevante)")
    new_s=input("enter a number")
    try:
        new_s=int(new_s)
        return new_s
    except:
        print("errore")
        return verifica()