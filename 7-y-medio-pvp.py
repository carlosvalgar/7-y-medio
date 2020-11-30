import random

# Creamos las listas y diccionarios que necesitamos, un diccionario de prioridades y un mazo donde estan todos los valores de prioridades

prioridad = {"oros": 1, "copas": 2, "bastos": 3, "espadas": 4}

mazo = [(1, "oros", 1), (2, "oros", 2), (3, "oros", 3), (4, "oros", 4), (5, "oros", 5), (6, "oros", 6), (7, "oros", 7), (10, "oros", 0.5), (11, "oros", 0.5), (12, "oros", 0.5),(1, "copas", 1), (2, "copas", 2), (3, "copas", 3), (4, "copas", 4), (5, "copas", 5), (6, "copas", 6), (7, "copas", 7), (10, "copas", 0.5), (11, "copas", 0.5), (12, "copas", 0.5), (1, "bastos", 1), (2, "bastos", 2), (3, "bastos", 3), (4, "bastos", 4), (5, "bastos", 5), (6, "bastos", 6), (7, "bastos", 7), (10, "bastos", 0.5), (11, "bastos", 0.5), (12, "bastos", 0.5), (1, "espadas", 1), (2, "espadas", 2), (3, "espadas", 3), (4, "espadas", 4), (5, "espadas", 5), (6, "espadas", 6), (7, "espadas", 7), (10, "espadas", 0.5), (11, "espadas", 0.5), (12, "espadas", 0.5),]

# Preguntamos la cantidad de jugadores que serán y creamos una lista con todos ellos, asegurandonos que empiezan por una letra y no contienen espacios

listaJugadores = []
dictJugadores = {}

flagCantidadJugadores = False

while not flagCantidadJugadores:
    cantidadJugadores = int(input("¿Cuantos jugadores váis a jugar? (mínimo 2, máximo 8): "))
    
    if cantidadJugadores > 8 or cantidadJugadores < 2:
        print("ERROR: Elige una cantidad entre 2 y 8.")
    
    elif cantidadJugadores <= 8 and cantidadJugadores >= 2:
        flagCantidadJugadores = True

c = 0

while len(listaJugadores) < cantidadJugadores: 
    
    nombreJugador = input("Introduce el nombre del jugador " + str(c + 1) + ": ")
    
    if nombreJugador[0:1].isalpha() == True and " " not in nombreJugador:
        listaJugadores.append(nombreJugador)
        dictJugadores[nombreJugador] = [[], "jugando", "jugando", c, 0, 0, 20, 0] #lista de cartas, estado de la mano, estado de la partida, prioridad del jugador, puntos mano, puntos apostados, puntos restantes, mano
        c += 1
    else:
        print("ERROR: Tu nombre no empieza por una letra o contiene espacios.")

# Elegimos una carta aleatoria del mazo para ver cual va a ser el orden de jugadores

listaPrioridad = []

for i in range(len(listaJugadores)):
    carta = random.choice(mazo)
    mazo.remove(carta)
    listaPrioridad.append([listaJugadores[i], carta])
    

for i in range(len(listaPrioridad) -1):
    for j in range(len(listaPrioridad) -1 -i):
        if listaPrioridad[j][1][0] >= listaPrioridad[j + 1][1][0]:
            if listaPrioridad[j][1][0] == listaPrioridad[j + 1][1][0]:
                if prioridad[listaPrioridad[j][1][1]] > prioridad[listaPrioridad[j + 1][1][1]]:
                    listaPrioridad[j], listaPrioridad[j + 1] = listaPrioridad[j + 1], listaPrioridad[j]
                
            else:
                listaPrioridad[j], listaPrioridad[j + 1] = listaPrioridad[j + 1], listaPrioridad[j]
    
# Hacemos una lista con el orden de los jugadores y devolvemos las cartas al mazo

listaJugadores = []

for i in listaPrioridad:
    listaJugadores.append(i[0])
    mazo.append(i[1])

# Actualizamos el orden 
for i in dictJugadores:
    dictJugadores[i][3] = listaJugadores.index(i)


# Repartimos una carta a cada jugador en orden, dejando al ultimo la banca
for i in range(1, len(dictJugadores)):
    for j in dictJugadores.keys():
        if i == dictJugadores[j][3]:
            carta = random.choice(mazo)
            dictJugadores[j][0].append(carta)
            mazo.remove(carta)
            dictJugadores[j][7] += 1

#falta la banca
print(dictJugadores)
