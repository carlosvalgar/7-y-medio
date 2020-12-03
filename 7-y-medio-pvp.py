import random

rondas = 1

# Creamos las listas y diccionarios que necesitamos, un diccionario de prioridades y un mazo donde estan todos los valores de prioridades

prioridad = {"oros": 1, "copas": 2, "espadas": 3, "bastos": 4}

mazo = [(1, "oros", 1), (2, "oros", 2), (3, "oros", 3), (4, "oros", 4), (5, "oros", 5), (6, "oros", 6), (7, "oros", 7), (10, "oros", 0.5), (11, "oros", 0.5), (12, "oros", 0.5),(1, "copas", 1), (2, "copas", 2), (3, "copas", 3), (4, "copas", 4), (5, "copas", 5), (6, "copas", 6), (7, "copas", 7), (10, "copas", 0.5), (11, "copas", 0.5), (12, "copas", 0.5), (1, "bastos", 1), (2, "bastos", 2), (3, "bastos", 3), (4, "bastos", 4), (5, "bastos", 5), (6, "bastos", 6), (7, "bastos", 7), (10, "bastos", 0.5), (11, "bastos", 0.5), (12, "bastos", 0.5), (1, "espadas", 1), (2, "espadas", 2), (3, "espadas", 3), (4, "espadas", 4), (5, "espadas", 5), (6, "espadas", 6), (7, "espadas", 7), (10, "espadas", 0.5), (11, "espadas", 0.5), (12, "espadas", 0.5),]

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
    cantidadJugadores = int(input("¿Cuantos jugadores váis a jugar? (mínimo 2, máximo 8): "))
    
    if cantidadJugadores == 1:
        print("\nERROR: ¿Que quieres jugar al solitario?\n")
        
    elif cantidadJugadores > 8 or cantidadJugadores < 2:
        print("\nERROR: Elige una cantidad entre 2 y 8.\n")
    
    elif cantidadJugadores <= 8 and cantidadJugadores >= 2:
        flagCantidadJugadores = True

print("\nLos nombres de los jugadores deben empezar por una letra y no contener espacios.\n")
c = 0

while len(listaJugadores) < cantidadJugadores: 
    
    nombreJugador = input("    Introduce el nombre del jugador " + str(c + 1) + ": ")
    
    if nombreJugador in listaJugadores:
        print("ERROR: Ese nombre de jugador ya esta escogido.")
    
    elif nombreJugador[0:1].isalpha() == True and " " not in nombreJugador:
        listaJugadores.append(nombreJugador)
        dictJugadores[nombreJugador] = [[], "jugando", "jugando", c, 0, 0, 20, 0] #lista de cartas, estado de la mano, estado de la partida, prioridad del jugador, puntos mano, puntos apostados, puntos restantes, cartas en mano
        c += 1
    else:
        print("\nERROR: Tu nombre no empieza por una letra o contiene espacios.\n")

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

# Añadimos una variable banca para poder dejarla aparte

banca = listaJugadores[0]

# Aqui es donde haremos el bucle de partidas

flagFinPartida = False
ronda = 1

while not flagFinPartida and ronda <= rondas:

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

    carta = random.choice(mazo)
    dictJugadores[banca][0].append(carta)
    mazo.remove(carta)
    dictJugadores[banca][7] += 1
    dictJugadores[banca][4] += dictJugadores[banca][0][dictJugadores[banca][7] -1][2]

    # Seleccionamos el jugador por el orden que tenemos en la lista, la banca se deja para el final.

    print()

    if ronda == 1:
        empezarPartida = "* ¡Empieza la partida! *"

        for i in range(len(empezarPartida)):
            print("*", end="")
        print()

        print(empezarPartida)

        for i in range(len(empezarPartida)):
            print("*", end="")
        print()
    
    empezarRonda = "* Ronda " + str(ronda) + " *"

    for i in range(len(empezarRonda)):
        print("*", end="")
    print()

    print(empezarRonda)

    for i in range(len(empezarRonda)):
        print("*", end="")
    print()

    for i in listaJugadores:
        if dictJugadores[i][3] != 0 and dictJugadores[i][1] == "jugando" and dictJugadores[i][2] != "eliminado":
            print("\nTurno del jugador " + str(i) + ":\n")
            
            
            # Enseñamos todas las cartas y puntos de cada jugador
            for j in listaJugadores:
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
                    print("".ljust(8) + "Puntos apostados: ", dictJugadores[j][5])
                    print()
                
                elif dictJugadores[j][1] == "eliminado":
                    print()
            
            # Una vez enseñadas las cartas le pedimos cuantos puntos quiere apostar
            
            flagPuntosApostados = False
            
            while not flagPuntosApostados:        
                dictJugadores[i][5] = int(input("¿Cuántos puntos quieres apostar jugador " + str(i) + " (tienes " + str(dictJugadores[i][6]) + " puntos restantes)? "))
                
                if dictJugadores[i][5] <= dictJugadores[i][6] and dictJugadores[i][5] > 0:
                    flagPuntosApostados = True
                
                elif dictJugadores[i][5] > dictJugadores[i][6]:
                    print("\nERROR: Has intentado apostar más puntos de los que tienes.\n")
                    
                else:
                    print("\nERROR: Has introducido una apuesta no válida.\n")
            print()
            
            flagPlantarse = False
            
            # Hacemos un menú para que el jugador decida que quiere hacer enseñandole sus cartas cada vez que roba.
            
            while not flagPlantarse:          
                print("Tus cartas son: ", end="")
                
                for j in dictJugadores[i][0]:
                    print(str(j[0]) + " de " + str(j[1]), end=", ")
                print()
                
                print("Tienes " + str(dictJugadores[i][4]) + " puntos en mano")
                    
                print("\nQue quieres hacer?\n    1.- Robar carta\n    2.- Plantarte\n")
                
                plantarse = int(input("Elige el número de la opción que quieras seleccionar: "))
                
                # Si decide robar le añadiremos la carta a su lista de cartas y la eliminaremos del mazo, actualizando los puntos y la cantidad de cartas en mano
                
                if plantarse == 1:
                    carta = random.choice(mazo)
                    dictJugadores[i][0].append(carta)
                    mazo.remove(carta)
                    dictJugadores[i][7] += 1
                    dictJugadores[i][4] += dictJugadores[i][0][dictJugadores[i][7] -1][2]
                    print()
                    print("".ljust(8) + "¡Jugador " + str(i) + " roba carta!\n")
                    
                elif plantarse == 2:
                    dictJugadores[i][1] = "plantado"
                    flagPlantarse = True
                    print()
                    print("".ljust(8) + "¡Jugador " + str(i) + " se planta!\n")
                    
                else:
                    print("ERROR: Opción no válida.")
                
                # Si se pasa de 7.5 lo eliminaremos directamente
                
                if dictJugadores[i][4]> 7.5:
                    dictJugadores[i][1] = "eliminado"
                    dictJugadores[banca][6] += dictJugadores[i][5]
                    dictJugadores[i][6] -= dictJugadores[i][5]
                    flagPlantarse = True
                    print("".ljust(8) + "¡Jugador " + str(i) + " es eliminado porque tiene " + str(dictJugadores[i][4]) + " puntos!\n")
                    print("".ljust(8) + "¡El jugador " + str(banca) + " (banca) gana " + str(dictJugadores[i][5]) + " puntos!\n")
                    dictJugadores[i][5] = 0

    # Miramos si los jugadores han sido eliminados, si han sido todos eliminados, la banca gana automáticamente
    
    cJugadorEliminado = 0
    
    for i in listaJugadores:
        if dictJugadores[i][3] != 0:
            if dictJugadores[i][1] == "eliminado":
                cJugadorEliminado += 1
    
    if cJugadorEliminado == len(listaJugadores) -1:
        print("¡Todos los jugadores han sido eliminados en esta ronda, gana la banca!")    
    
    elif cJugadorEliminado != len(listaJugadores) -1:
        
        # Ahora hacemos el turno de la banca

        print("\nTurno del jugador " + str(banca) + " (banca):\n")
                
                
        # Enseñamos todas las cartas y puntos de cada jugador
        for j in listaJugadores:
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
                print("".ljust(8) + "Puntos apostados: ", dictJugadores[j][5])
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
                        
            print("\nQue quieres hacer?\n    1.- Robar carta\n    2.- Plantarte\n")
                    
            plantarse = int(input("Elige el número de la opción que quieras seleccionar: "))
                    
            # Si decide robar le añadiremos la carta a su lista de cartas y la eliminaremos del mazo, actualizando los puntos y la cantidad de cartas en mano
                    
            if plantarse == 1:
                carta = random.choice(mazo)
                dictJugadores[banca][0].append(carta)
                mazo.remove(carta)
                dictJugadores[banca][7] += 1
                dictJugadores[banca][4] += dictJugadores[banca][0][dictJugadores[banca][7] -1][2]
                print()
                print("".ljust(8) + "¡La banca (Jugador " + str(banca) + ") roba carta!\n")
                        
            elif plantarse == 2:
                dictJugadores[banca][1] = "plantado"
                flagPlantarse = True
                print()
                print("".ljust(8) + "¡La banca (Jugador " + str(banca) + ") se planta!\n")
                        
            else:
                print("ERROR: Opción no válida.")
                    
            # Si la banca se pasa de 7.5 o lo iguala salimos del bucle porque ya se ha acabado la ronda
                    
            if dictJugadores[banca][4] >= 7.5:
                flagPlantarse = True

    # Una vez acabada la ronda procedemos al reparto de puntos
    cJugador = 0
    
    # Si la banca tiene 7.5 puntos gana automaticamente
    if dictJugadores[banca][4] == 7.5:
        mensajeFinRonda = "* ¡La banca ha sacado un 7.5 y gana esta ronda! *"
        for i in range(len(mensajeFinRonda)):
            print("*", end="")
        print()

        print(mensajeFinRonda)

        for i in range(len(mensajeFinRonda)):
            print("*", end="")
        print()
        
        # Se le suma los puntos que apostó el jugador a la banca y se le resta de su total, se devuelve la apuesta a 0 obviando a los eliminados
        
        for i in listaJugadores:
            if i != banca and dictJugadores[i][1] != "eliminado":
                dictJugadores[banca][6] += dictJugadores[i][5]
                dictJugadores[i][6] -= dictJugadores[i][5]
                dictJugadores[i][5]= 0        

    # Si la banca se pasa de 7.5 los jugadores que no han sido eliminados ganan automaticamente

    elif dictJugadores[banca][4] > 7.5:
        mensajeFinRonda = "* ¡La banca se ha pasado de 7.5 (Tiene " + str(dictJugadores[banca][4]) +" puntos), los jugadores que no están eliminados ganan! *"
        for i in range(len(mensajeFinRonda)):
            print("*", end="")
        print()

        print(mensajeFinRonda)

        for i in range(len(mensajeFinRonda)):
            print("*", end="")
        print()
        
        # Se le suman los puntos a cada jugador, si la banca no tiene suficientes puntos pagara lo que le quede y ya no pagará más
        
        for i in listaJugadores:
            if i != banca and dictJugadores[i][1] != "eliminado":
                
                # Paga el doble si el jugador tiene 7.5
                
                if dictJugadores[banca][6] > dictJugadores[i][5] * 2 and dictJugadores[i][4] == 7.5:
                    dictJugadores[i][6] += dictJugadores[i][5] * 2
                    dictJugadores[banca][6] -= dictJugadores[i][5] * 2
                    dictJugadores[i][5]= 0
                    
                    mensajeFinRonda = "* ¡Además el jugador " + str(i) + " tiene 7.5! *"
                    for j in range(len(mensajeFinRonda)):
                        print("*", end="")
                    print()

                    print(mensajeFinRonda)

                    for j in range(len(mensajeFinRonda)):
                        print("*", end="")
                    print()
                    
                    # Añadimos la rotacion de banca
                    
                    if cJugador == 0:
                        dictJugadores[i][3] = 0
                        dictJugadores[banca][3] = len(listaJugadores)
                        nuevaBanca = i
                        cJugador += 1
                    
                # Tiene que mirar si es el doble para acabar de pagar todos los puntos
                    
                elif dictJugadores[banca][6] <= dictJugadores[i][5] * 2 and dictJugadores[banca][6] != 0 and dictJugadores[i][4] == 7.5:
                    dictJugadores[i][6] += dictJugadores[banca][6]
                    dictJugadores[banca][6] = 0
                    dictJugadores[i][5]= 0

                    mensajeFinRonda = "* ¡Además el jugador " + str(i) + " tiene 7.5! *"
                    for j in range(len(mensajeFinRonda)):
                        print("*", end="")
                    print()

                    print(mensajeFinRonda)

                    for j in range(len(mensajeFinRonda)):
                        print("*", end="")
                    print()
                    
                    # Añadimos rotacion de banca
                    
                    if cJugador == 0:
                        dictJugadores[i][3] = 0
                        dictJugadores[banca][3] = len(listaJugadores)
                        nuevaBanca = i
                        cJugador += 1
                        
                # Le paga a los jugadores que no tienen 7.5
                
                elif dictJugadores[banca][6] > dictJugadores[i][5] and dictJugadores[i][4] != 7.5:
                    dictJugadores[i][6] += dictJugadores[i][5]
                    dictJugadores[banca][6] -= dictJugadores[i][5]
                    dictJugadores[i][5]= 0
                
                # Paga lo que le queda
                
                elif dictJugadores[banca][6] <= dictJugadores[i][5] and dictJugadores[banca][6] != 0 and dictJugadores[i][4] != 7.5:
                    dictJugadores[i][6] += dictJugadores[banca][6]
                    dictJugadores[banca][6] = 0
                    dictJugadores[i][5]= 0
                
                else:
                    dictJugadores[i][5]= 0

    # Ahora si la banca no gana o pierde automáticamente se comparan los resultados

    elif dictJugadores[banca][4] < 7.5 and cJugadorEliminado != len(listaJugadores) -1:
        for i in listaJugadores:        
            
            # Comparamos todos los jugadores que no estan eliminados
            
            if i != banca and dictJugadores[i][1] != "eliminado" and dictJugadores[banca][6] != 0:
                
                # Si el jugador gana con un 7 y medio se le dara el doble de puntos apostados y la banca perdera el doble, en caso de no poder pagar, dara todos los que le queden
                
                if dictJugadores[i][4] == 7.5:
                    if dictJugadores[banca][6] >= dictJugadores[i][5] * 2:
                        dictJugadores[i][6] += dictJugadores[i][5] * 2
                        dictJugadores[banca][6] -= dictJugadores[i][5] * 2
                        dictJugadores[i][5] = 0
                        
                    else:
                        dictJugadores[i][6] += dictJugadores[banca][6]
                        dictJugadores[banca][6] = 0
                        dictJugadores[i][5] = 0
                    
                    mensajeFinRonda = "* ¡El jugador " + str(i) + " gana a la banca con un 7.5, ahora será la banca! *"
                    for i in range(len(mensajeFinRonda)):
                        print("*", end="")
                    print()

                    print(mensajeFinRonda)

                    for i in range(len(mensajeFinRonda)):
                        print("*", end="")
                    print()
                    
                    # Le añadimos un contador para que el primer jugador que cumpla esta condicion en esta ronda se convierta en la banca
                    
                    if cJugador == 0:
                        dictJugadores[i][3] = 0
                        dictJugadores[banca][3] = len(listaJugadores)
                        nuevaBanca = i
                        cJugador += 1
                
                # Si la banca tiene mas puntos o los mismos que el jugador la banca gana
                    
                elif dictJugadores[banca][4] >= dictJugadores[i][4]:
                    dictJugadores[banca][6] += dictJugadores[i][5]
                    dictJugadores[i][6] -= dictJugadores[i][5]
                    dictJugadores[i][5] = 0
                    
                    mensajeFinRonda = "* ¡La banca gana al jugador " + str(i) + "! *"
                    for i in range(len(mensajeFinRonda)):
                        print("*", end="")
                    print()

                    print(mensajeFinRonda)

                    for i in range(len(mensajeFinRonda)):
                        print("*", end="")
                    print()
                    
                # Si la banca tiene menos puntos que el jugador, la banca le dara los puntos apostados al jugador
                    
                elif dictJugadores[banca][4] < dictJugadores[i][4]:
                    if dictJugadores[banca][6] >= dictJugadores[i][5]:
                        dictJugadores[i][6] += dictJugadores[i][5]
                        dictJugadores[banca][6] -= dictJugadores[i][5]
                        dictJugadores[i][5] = 0
                        
                    else:
                        dictJugadores[i][6] += dictJugadores[banca][6]
                        dictJugadores[banca][6] = 0
                        dictJugadores[i][5] = 0
                    
                    mensajeFinRonda = "* ¡El jugador " + str(i) + " gana a la banca! *"
                    for i in range(len(mensajeFinRonda)):
                        print("*", end="")
                    print()

                    print(mensajeFinRonda)

                    for i in range(len(mensajeFinRonda)):
                        print("*", end="")
                    print()

    # Vamos a reiniciar las estadisticas de todos los jugadores y el mazo

    mazo = [(1, "oros", 1), (2, "oros", 2), (3, "oros", 3), (4, "oros", 4), (5, "oros", 5), (6, "oros", 6), (7, "oros", 7), (10, "oros", 0.5), (11, "oros", 0.5), (12, "oros", 0.5),(1, "copas", 1), (2, "copas", 2), (3, "copas", 3), (4, "copas", 4), (5, "copas", 5), (6, "copas", 6), (7, "copas", 7), (10, "copas", 0.5), (11, "copas", 0.5), (12, "copas", 0.5), (1, "bastos", 1), (2, "bastos", 2), (3, "bastos", 3), (4, "bastos", 4), (5, "bastos", 5), (6, "bastos", 6), (7, "bastos", 7), (10, "bastos", 0.5), (11, "bastos", 0.5), (12, "bastos", 0.5), (1, "espadas", 1), (2, "espadas", 2), (3, "espadas", 3), (4, "espadas", 4), (5, "espadas", 5), (6, "espadas", 6), (7, "espadas", 7), (10, "espadas", 0.5), (11, "espadas", 0.5), (12, "espadas", 0.5),]

    # Se reinician todos los jugadores y se revisa su estado, si queda un jugador o menos que no esten eliminados se acaba la partida

    print()
    
    listaJugadoresEliminados = []

    for i in listaJugadores:
        dictJugadores[i][0] = []
        
        if dictJugadores[i][6] != 0:
            dictJugadores[i][1] = "jugando"
        
        elif dictJugadores[i][6] == 0:
            dictJugadores[i][1] = "eliminado"
            dictJugadores[i][2] = "eliminado"
            dictJugadores[i][3] = -1
            listaJugadoresEliminados.append(i)
            print("".ljust(8) + ">>> El jugador " + str(i) + " ha sido eliminado de la partida")
            
        
        dictJugadores[i][4] = 0
        dictJugadores[i][7] = 0

    # Sacamos los jugadores eliminados de la lista de prioridad

    for i in listaJugadoresEliminados:
        listaJugadores.remove(i)

    # Si solo queda 1 jugador se acaba la partida
    
    if len(listaJugadores) <= 1:
        flagFinPartida = True

    # Cambiamos el orden de prioridad de jugadores si han habido cambios de banca

    if dictJugadores[banca][3] != 0:
        
        # Si no se ha eliminado la banca significa que un jugador ha destronado la banca con un 7.5, por lo que cambiamos de sitio esos dos jugadores
        
        if dictJugadores[banca][2] != "eliminado":    
            listaJugadores.remove(banca)
            listaJugadores.remove(nuevaBanca)
            
            # Lo separo porque si se queda la lista vacia no puedo asignarle un valor de 0  
            
            if len(listaJugadores) == 0:
                listaJugadores.append(nuevaBanca)
                
            else:
                listaJugadores.insert(0, nuevaBanca)
                
            listaJugadores.append(banca)
            banca = nuevaBanca
        
        # Volvemos a organizar la lista de Jugadores y modificamos las prioridades, si se ha eliminado la banca ya la habremos quitado de la lista por lo que ya estará ordenada
        
        for i in dictJugadores:
            if dictJugadores[i][2] != "eliminado":
                dictJugadores[i][3] = listaJugadores.index(i)
        
    ronda += 1
    
if len(listaJugadores) == 1:
    
    for i in listaJugadores:
        jugadorGanador = "* ¡Ha ganado el jugador " + str(i) + " por ser el único jugador con puntos restantes! *"
        for j in range(len(jugadorGanador)):
            print("*", end="")
        print()
        print(jugadorGanador)
        for j in range(len(jugadorGanador)):
            print("*", end="")
        print()

elif ronda > rondas:
    puntosGanador = 0
    jugadorGanador = ""
    listaEmpates = []    
    
    for i in listaJugadores:
        if dictJugadores[i][6] > puntosGanador:
            puntosGanador = dictJugadores[i][6]
            jugadorGanador = i
            listaEmpates = []
            listaEmpates.append(i)
        
        elif dictJugadores [i][6] == puntosGanador:
            listaEmpates.append(i)
    
    if len(listaEmpates) == 1:
        ganador = "* El jugador con más puntos es " + str(jugadorGanador) + " por lo tanto gana la partida! *"
        
        for i in range(len(ganador)):
            print("*", end="")
        print()
        
        print(ganador)
        
        for i in range(len(ganador)):
            print("*", end="")
        print()
    
    elif len(listaEmpates) > 1:
        ganador = "* ¡Ha habido un empate! Los jugadores ganadores son: *"
        
        for i in range(len(ganador)):
            print("*", end="")
        print()
        
        print(ganador)
        
        for j in listaEmpates:
            empate = "*" + "".ljust(4) + " >>> Jugador: " + str(j)
            c = len(ganador) - len(empate)
            print(str(empate) + "*".rjust(c))
        
        for i in range(len(ganador)):
            print("*", end="")
        print()
    
input("Introduzca cualquier tecla para cerrar el programa ") 
