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
            dictJugadores[j][4] += dictJugadores[j][0][dictJugadores[j][7] -1][2]

# Aqui repartimos la carta a la banca
for i in dictJugadores.keys():
    if dictJugadores[i][3] == 0:
            carta = random.choice(mazo)
            dictJugadores[i][0].append(carta)
            mazo.remove(carta)
            dictJugadores[i][7] += 1
            dictJugadores[i][4] += dictJugadores[i][0][dictJugadores[i][7] -1][2]

# Seleccionamos el jugador por el orden que tenemos en la lista, la banca se deja para el final.

for i in listaJugadores:
    if dictJugadores[i][3] != 0 and dictJugadores[i][1] == "jugando":
        print("Turno del jugador" + str(dictJugadores[i][3]))
        
        
        # Enseñamos todas las cartas y puntos de cada jugador
        for i in dictJugadores.keys():
            print("cartas de jugador", dictJugadores[i][0])
            print("puntos de jugador", dictJugadores[i][4])
        
        flagPlantarse = False
        
        # Hacemos un menú para que el jugador decida que quiere hacer enseñandole sus cartas cada vez que roba.
        
        while not flagPlantarse:
            print(dictJugadores[i])
            
            for j in dictJugadores[i][0]:
                print("Tus cartas son: " + str(j[0]) + " de " + str(j[1]))
                
            print("Que quieres hacer?\n    1.- Robar carta\n    2.- Plantarte")
            
            plantarse = int(input("Elige el número de la opción que quieras seleccionar: "))
            
            # Si decide robar le añadiremos la carta a su lista de cartas y la eliminaremos del mazo, actualizando los puntos y la cantidad de cartas en mano
            if plantarse == 1:
                carta = random.choice(mazo)
                dictJugadores[i][0].append(carta)
                mazo.remove(carta)
                dictJugadores[i][7] += 1
                dictJugadores[i][4] += dictJugadores[i][0][dictJugadores[i][7] -1][2]
                
            elif plantarse == 2:
                dictJugadores[i][1] == "plantado"
                flagPlantarse = True
                
            else:
                print("ERROR: Opción no válida.")
