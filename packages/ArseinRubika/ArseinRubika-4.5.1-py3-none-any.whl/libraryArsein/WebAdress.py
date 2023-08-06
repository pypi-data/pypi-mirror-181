import random
from random import choice

class server_bot:
    listservers = []
    myservers = []
    matnadress = []
    filesadress = []
    for addadadress in range(1,201):
        listservers.append(addadadress)
    for addserver in range(1,201):
        ser = 'https://messengerg2cADDAD.iranlms.ir'
        S = ser.replace("ADDAD",f"{choice(listservers)}")
        myservers.append(S)
    matnadress.extend(myservers)
    filesadress.extend(myservers)
