import random

# Creamos las listas y diccionarios que necesitamos, un diccionario de prioridades y un mazo donde estan todos los valores de prioridades

prioridad = {"oros": 1, "copas": 2, "bastos": 3, "espadas": 4}

mazo = [(1, "oros", 1), (2, "oros", 2), (3, "oros", 3), (4, "oros", 4), (5, "oros", 5), (6, "oros", 6), (7, "oros", 7),
        (10, "oros", 0.5), (11, "oros", 0.5), (12, "oros", 0.5), (1, "copas", 1), (2, "copas", 2), (3, "copas", 3),
        (4, "copas", 4), (5, "copas", 5), (6, "copas", 6), (7, "copas", 7), (10, "copas", 0.5), (11, "copas", 0.5),
        (12, "copas", 0.5), (1, "bastos", 1), (2, "bastos", 2), (3, "bastos", 3), (4, "bastos", 4), (5, "bastos", 5),
        (6, "bastos", 6), (7, "bastos", 7), (10, "bastos", 0.5), (11, "bastos", 0.5), (12, "bastos", 0.5),
        (1, "espadas", 1), (2, "espadas", 2), (3, "espadas", 3), (4, "espadas", 4), (5, "espadas", 5),
        (6, "espadas", 6), (7, "espadas", 7), (10, "espadas", 0.5), (11, "espadas", 0.5), (12, "espadas", 0.5), ]

# Preguntamos la cantidad de jugadores que serán y creamos una lista con todos ellos, asegurandonos que empiezan por una letra y no contienen espacios

sieteMedioTitulo = "* Siete y medio *"

for i in range(len(sieteMedioTitulo)):
    print("*", end="")
print()

print(sieteMedioTitulo)

for i in range(len(sieteMedioTitulo)):
    print("*", end="")
print()
print()

listaJugadores = []
dictJugadores = {}

flagCantidadJugadores = False

while not flagCantidadJugadores:
    cantidadJugadores = int(input("¿Cuantos jugadores va a tener la partida?  (mínimo 2, máximo 8): "))

    if cantidadJugadores > 8 or cantidadJugadores < 2:
        print("ERROR: Elige una cantidad entre 2 y 8.")
    else:
        cantidadHumanos = int(input("Cuantos seran humanos? "))
        if cantidadJugadores < cantidadHumanos:
            print("ERROR: La cantidad de humanos no puede ser superior a la de jugadores")
        elif cantidadJugadores <= 8 and cantidadJugadores >= 2:
            flagCantidadJugadores = True

print()
c = 0
cantidadBots= cantidadJugadores-cantidadHumanos

for i in range(cantidadBots):
    listaJugadores.append("maquina"+str(i+1))
    dictJugadores["maquina"+str(i+1)] = [[], "jugando", "jugando", c, 0, 0, 20, 0]
    c+=1
print(dictJugadores)

while len(listaJugadores) < cantidadJugadores:

    nombreJugador = input("    Introduce el nombre del jugador " + str(c + 1) + ": ")
    if nombreJugador[0].isalpha() == True and " " not in nombreJugador:
        listaJugadores.append(nombreJugador)
        dictJugadores[nombreJugador] = [[], "jugando", "jugando", c, 0, 0, 20,
                                        0]  # lista de cartas, estado de la mano, estado de la partida, prioridad del jugador, puntos mano, puntos apostados, puntos restantes, mano
        c += 1
    else:
        print("ERROR: Tu nombre no empieza por una letra o contiene espacios.")

# Elegimos una carta aleatoria del mazo para ver cual va a ser el orden de jugadores

listaPrioridad = []

for i in range(len(listaJugadores)):
    carta = random.choice(mazo)
    mazo.remove(carta)
    listaPrioridad.append([listaJugadores[i], carta])
# print("listaPrioridad")
# print(listaPrioridad)
# '''porque ordena esto y porque esta asi??
# listaPrioridad
# [['maquina1', (5, 'espadas', 5)], ['y', (11, 'oros', 0.5)], ['m', (6, 'oros', 6)]]
# listaPrioridad2
# [['maquina1', (5, 'espadas', 5)], ['m', (6, 'oros', 6)], ['y', (11, 'oros', 0.5)]]
# '''
for i in range(len(listaPrioridad) - 1):
    for j in range(len(listaPrioridad) - 1 - i):
        if listaPrioridad[j][1][0] >= listaPrioridad[j + 1][1][0]:
            if listaPrioridad[j][1][0] == listaPrioridad[j + 1][1][0]:
                if prioridad[listaPrioridad[j][1][1]] > prioridad[listaPrioridad[j + 1][1][1]]:
                    listaPrioridad[j], listaPrioridad[j + 1] = listaPrioridad[j + 1], listaPrioridad[j]

            else:
                listaPrioridad[j], listaPrioridad[j + 1] = listaPrioridad[j + 1], listaPrioridad[j]
# print("listaPrioridad2")
# print(listaPrioridad)
# Hacemos una lista con el orden de los jugadores y devolvemos las cartas al mazo ya que ya las tenemos en listaPrioridad

listaJugadores = []

for i in listaPrioridad:
    listaJugadores.append(i[0])
    mazo.append(i[1])

# Actualizamos el orden
for i in dictJugadores:
    dictJugadores[i][3] = listaJugadores.index(i)

# Añadimos una variable banca para poder dejarla aparte
banca = listaJugadores[0]

# Repartimos una carta a cada jugador en orden, dejando al ultimo la banca
for i in range(1, len(dictJugadores)):
    for j in dictJugadores.keys():
        if i == dictJugadores[j][3]:
            carta = random.choice(mazo)
            dictJugadores[j][0].append(carta)
            mazo.remove(carta)
            dictJugadores[j][7] += 1
            dictJugadores[j][4] += dictJugadores[j][0][dictJugadores[j][7] - 1][2]

# Aqui repartimos la carta a la banca

carta = random.choice(mazo)
dictJugadores[banca][0].append(carta)
mazo.remove(carta)
dictJugadores[banca][7] += 1
dictJugadores[banca][4] += dictJugadores[banca][0][dictJugadores[banca][7] - 1][2]

# Seleccionamos el jugador por el orden que tenemos en la lista, la banca se deja para el final.

print()

empezarPartida = "* ¡Empieza la partida! *"

for i in range(len(empezarPartida)):
    print("*", end="")
print()

print(empezarPartida)

for i in range(len(empezarPartida)):
    print("*", end="")
print()

for i in listaJugadores:
    print (i)
    if dictJugadores[i][3] != 0 and dictJugadores[i][1] == "jugando":
        print("\nTurno del jugador " + str(i) + ":\n")

        # Enseñamos todas las cartas y puntos de cada jugador
        for j in dictJugadores.keys():
            print("".ljust(4) + "Información del jugador " + str(j), end="")

            if dictJugadores[j][3] == 0:
                print(" (Banca):")

            else:
                print(" (" + str(dictJugadores[j][1]) + "):")

            if dictJugadores[j][1] != "eliminado":

                print("".ljust(8) + "Cartas en mano: ", end="")

                for k in dictJugadores[j][0]:
                    print(str(k[0]) + " de " + str(k[1]) + ", ", end="")

                print()
                print("".ljust(8) + "Puntos de la mano: ", dictJugadores[j][4])
                print()

            elif dictJugadores[j][1] == "eliminado":
                print()

        flagPlantarse = False

        # Hacemos un menú para que el jugador decida que quiere hacer enseñandole sus cartas cada vez que roba.

        while not flagPlantarse:
            print("Tus cartas son: ", end="")

            for j in dictJugadores[i][0]:
                print(str(j[0]) + " de " + str(j[1]), end=", ")
            print()

            print("Tienes " + str(dictJugadores[i][4]) + " puntos en mano")

            print("\n"+i.title()+", Que quieres hacer?\n    1.- Robar carta\n    2.- Plantarte\n")

            plantarse = int(input("Elige el número de la opción que quieras seleccionar: "))

            # Si decide robar le añadiremos la carta a su lista de cartas y la eliminaremos del mazo, actualizando los puntos y la cantidad de cartas en mano

            if plantarse == 1:
                carta = random.choice(mazo)
                dictJugadores[i][0].append(carta)
                mazo.remove(carta)
                dictJugadores[i][7] += 1
                dictJugadores[i][4] += dictJugadores[i][0][dictJugadores[i][7] - 1][2]

            elif plantarse == 2:
                dictJugadores[i][1] = "plantado"
                flagPlantarse = True

            else:
                print("ERROR: Opción no válida.")

            # Si se pasa de 7.5 lo eliminaremos directamente

            if dictJugadores[i][4] > 7.5:
                dictJugadores[i][1] = "eliminado"
                flagPlantarse = True

# Ahora hacemos el turno de la banca

print("\nTurno del jugador " + str(banca) + ":\n")

# Enseñamos todas las cartas y puntos de cada jugador
for j in dictJugadores.keys():
    print("".ljust(4) + "Información del jugador " + str(j), end="")

    if dictJugadores[j][3] == 0:
        print(" (Banca):")

    else:
        print(" (" + str(dictJugadores[j][1]) + "):")

    if dictJugadores[j][1] != "eliminado":

        print("".ljust(8) + "Cartas en mano: ", end="")

        for k in dictJugadores[j][0]:
            print(str(k[0]) + " de " + str(k[1]) + ", ", end="")

        print()
        print("".ljust(8) + "Puntos de la mano: ", dictJugadores[j][4])
        print()

    elif dictJugadores[j][1] == "eliminado":
        print()

flagPlantarse = False

# Hacemos un menú para que el jugador decida que quiere hacer enseñandole sus cartas cada vez que roba.

while not flagPlantarse:
    print("Tus cartas son: ", end="")

    for j in dictJugadores[banca][0]:
        print(str(j[0]) + " de " + str(j[1]), end=", ")
    print()

    print("Tienes " + str(dictJugadores[banca][4]) + " puntos en mano")

    print("\n"+banca.title()+" Que quieres hacer?\n    1.- Robar carta\n    2.- Plantarte\n")

    plantarse = int(input("Elige el número de la opción que quieras seleccionar: "))

    # Si decide robar le añadiremos la carta a su lista de cartas y la eliminaremos del mazo, actualizando los puntos y la cantidad de cartas en mano

    if plantarse == 1:
        carta = random.choice(mazo)
        dictJugadores[banca][0].append(carta)
        mazo.remove(carta)
        dictJugadores[banca][7] += 1
        dictJugadores[banca][4] += dictJugadores[banca][0][dictJugadores[banca][7] - 1][2]

    elif plantarse == 2:
        dictJugadores[banca][1] = "plantado"
        flagPlantarse = True

    else:
        print("ERROR: Opción no válida.")

    # Si la banca se pasa de 7.5 o lo iguala salimos del bucle porque ya se ha acabado la ronda

    if dictJugadores[banca][4] >= 7.5:
        flagPlantarse = True

# Una vez acabada la ronda procedemos al reparto de puntos

if dictJugadores[banca][4] == 7.5:
    print("Todos los jugadores a pagar")

elif dictJugadores[banca][4] > 7.5:
    print("La banca paga a todos")

elif dictJugadores[banca][4] < 7.5:
    print("Se procede a contar los puntos")