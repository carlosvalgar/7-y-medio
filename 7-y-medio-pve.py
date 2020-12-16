import random
import pymysql

############### CONFIGURAR ESTO ###################
# Conexión de base de datos.
conexion="127.0.0.1" #aquí pondremos nuestra dirección de la base de datos de Amazon web services
usuario="root" # usuario de la conexión
password="t32i6zcf9893715" #contraseña
BBDD="proyecto" #base de datos a la cual nos vamos a conectar
db = pymysql.connect(conexion, usuario, password, BBDD)
##################################################

# Este cursor lo usamos para ejecutar la query y almacenar sus datos

cursor = db.cursor()

# Printamos el título con formato

sieteMedioTitulo = "* Siete y medio *"

for i in range(len(sieteMedioTitulo)):
    print("*", end="")
print()

print(sieteMedioTitulo)

for i in range(len(sieteMedioTitulo)):
    print("*", end="")
print()

flagMenuPrincipal = False

while not flagMenuPrincipal:
    flagElegirOpcion = False
    
    while not flagElegirOpcion:
        try:
            print("Bienvenidos a Siete y medio. Elige una opción:\n    1.- Jugar\n    2.- Estadísticas\n    3.- Salir\n")

            menuJugarEstadisticas = int(input("> "))
            print()
            
            if menuJugarEstadisticas >= 1 and menuJugarEstadisticas <= 3:
                flagElegirOpcion = True
            
            else:
                print("ERROR: Opción no válida.\n")
            
        except ValueError:
            print("\nERROR: Introduce un número entero.\n")
                
    while menuJugarEstadisticas == 1:
        # Añadimos las opciones de la partida

        listaJugadores = []
        dictJugadores = {}
        
        rondas = 6
        ronda = 1
        minApuesta = 2
        maxApuesta = 5

        # Creamos las listas y diccionarios que necesitamos, un diccionario de prioridades y un mazo donde estan todos los valores de prioridades

        prioridad = {"oros": 1, "copas": 2, "bastos": 3, "espadas": 4}

        mazo = [(1, "oros", 1), (2, "oros", 2), (3, "oros", 3), (4, "oros", 4), (5, "oros", 5), (6, "oros", 6), (7, "oros", 7),
                (10, "oros", 0.5), (11, "oros", 0.5), (12, "oros", 0.5), (1, "copas", 1), (2, "copas", 2), (3, "copas", 3),
                (4, "copas", 4), (5, "copas", 5), (6, "copas", 6), (7, "copas", 7), (10, "copas", 0.5), (11, "copas", 0.5),
                (12, "copas", 0.5), (1, "bastos", 1), (2, "bastos", 2), (3, "bastos", 3), (4, "bastos", 4), (5, "bastos", 5),
                (6, "bastos", 6), (7, "bastos", 7), (10, "bastos", 0.5), (11, "bastos", 0.5), (12, "bastos", 0.5),
                (1, "espadas", 1), (2, "espadas", 2), (3, "espadas", 3), (4, "espadas", 4), (5, "espadas", 5),
                (6, "espadas", 6), (7, "espadas", 7), (10, "espadas", 0.5), (11, "espadas", 0.5), (12, "espadas", 0.5), ]

        # Preguntamos por la cantidad de jugadores (bots y humanos) que habrá en la partida

        flagCantidadJugadores = False

        while not flagCantidadJugadores:
            try:
                print("¿Cuántos jugadores (bots y humanos) va a tener la partida? (mínimo 2, máximo 8):\n")
                cantidadJugadores = int(input("> "))
                print()
                
                if cantidadJugadores > 8 or cantidadJugadores < 2:
                    print("ERROR: Elige una cantidad entre 2 y 8.\n")
                else:
                    while not flagCantidadJugadores:
                        try:
                            print("¿Cuántos de estos jugadores serán humanos?\n    >>>> Elige 0 para una partida de bots contra bots.\n    >>>> Elige el mismo número de jugadores que humanos para una partida sin bots.\n")
                            cantidadHumanos = int(input("> "))
                            print()
                            
                            if cantidadJugadores < cantidadHumanos:
                                print("ERROR: La cantidad de humanos no puede ser superior a la de jugadores.\n")
                                
                            elif cantidadJugadores <= 8 and cantidadJugadores >= 2:
                                flagCantidadJugadores = True
                                
                        except ValueError:
                            print("\nERROR: Introduce un número entero.\n")
                        
            except ValueError:
                print("\nERROR: Introduce un número entero.\n")

        cantidadBots = cantidadJugadores - cantidadHumanos

        # Añadimos todos los bots

        for i in range(cantidadBots):
            listaJugadores.append("Bot " + str(i + 1))
            dictJugadores["Bot " + str(i + 1)] = [[], "jugando", "jugando", 0, 0, 0, 20, 0, "bot"]

        # Añadimos los jugadores asegurandonos que su nombre empieza por una letra y no tiene espacios

        c = 0

        while len(listaJugadores) < cantidadJugadores:
            print("Introduce el nombre del jugador (humano) " + str(c + 1) + ":\n")
            nombreJugador = input("> ")
            print()
            
            try:
                if nombreJugador[0].isalpha() == True and " " not in nombreJugador and nombreJugador.isalnum() == True:
                    listaJugadores.append(nombreJugador)
                        
                    # Este dicconario contiene: lista de cartas, estado de la mano, estado de la partida, prioridad del jugador, puntos mano, puntos apostados, puntos restantes, mano, tipo de jugador
                        
                    dictJugadores[nombreJugador] = [[], "jugando", "jugando", 0, 0, 0, 20, 0, "humano"]  
                    c += 1
                        
                else:
                    print("ERROR: Tu nombre no empieza por una letra, contiene espacios o contiene símbolos especiales.\n")
                    
            except IndexError:
                print("\nERROR: El campo no puede quedar vacio.\n")

        # Repartimos una carta a cada jugador

        listaPrioridad = []

        for i in range(len(listaJugadores)):
            carta = random.choice(mazo)
            mazo.remove(carta)
            listaPrioridad.append([listaJugadores[i], carta])

        # Ordenamos los jugadores segun la carta que ha robado cada uno con el método burbuja, si llega a haber un empate lo arreglamos según el palo del que sea la carta

        for i in range(len(listaPrioridad) - 1):
            for j in range(len(listaPrioridad) - 1 - i):
                if listaPrioridad[j][1][0] >= listaPrioridad[j + 1][1][0]:
                    if listaPrioridad[j][1][0] == listaPrioridad[j + 1][1][0]:
                        if prioridad[listaPrioridad[j][1][1]] > prioridad[listaPrioridad[j + 1][1][1]]:
                            listaPrioridad[j], listaPrioridad[j + 1] = listaPrioridad[j + 1], listaPrioridad[j]

                    else:
                        listaPrioridad[j], listaPrioridad[j + 1] = listaPrioridad[j + 1], listaPrioridad[j]

        # Hacemos una lista sólo con el orden de los jugadores y devolvemos las cartas al mazo ya que ya las tenemos en listaPrioridad

        listaJugadores = []

        for i in listaPrioridad:
            listaJugadores.append(i[0])
            mazo.append(i[1])

        # Actualizamos el orden en el diccionario

        for i in dictJugadores:
            dictJugadores[i][3] = listaJugadores.index(i)

        # Añadimos una variable banca para poder dejarla aparte y le asignamos el valor nuevaBanca para hacer comparaciones despues cuando vaya a haber un cambio de banca por 7 y medio

        banca = listaJugadores[0]
        nuevaBanca = banca

        # Aqui es donde haremos el bucle de las partidas

        flagFinPartida = False

        while not flagFinPartida and ronda <= rondas:
            
            # Añadimos que dependiendo de la ronda aumenten las apuestas de los bots, habiendo un incremento al acabar el primer tercio de la partida y al acabar el segundo tercio

            if ronda >= (rondas * 2) // 3:
                minApuesta = 6
                maxApuesta = 12
                
            elif ronda >= rondas // 3:
                minApuesta = 4
                maxApuesta = 8
            
            # Repartimos una carta a cada jugador en orden, dejando al ultimo la banca
            for i in range(1, len(dictJugadores)):
                for j in dictJugadores.keys():
                    if i == dictJugadores[j][3] and dictJugadores[j][2] != "eliminado":
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
                
                # Separamos jugadores humanos y bots
                
                if dictJugadores[i][8] == "humano":
                    if dictJugadores[i][3] != 0 and dictJugadores[i][1] == "jugando" and dictJugadores[i][2] != "eliminado":
                        turnoJugador = "| Turno del jugador " + str(i) + " |"
                        
                        for x in range(len(turnoJugador)):
                            print("-", end="")
                        print()

                        print(turnoJugador)

                        for x in range(len(turnoJugador)):
                            print("-", end="")
                        print()
                        print()
                        
                        # Enseñamos todas las cartas y puntos de cada jugador
                        
                        for x in range(2):
                            for y in range(40):
                                print("*", end="")
                            print()
                        print()
                        
                        for j in listaJugadores:
                            if dictJugadores[j] != dictJugadores[i]:
                                print("Información del jugador " + str(j), end="")
                                
                                if dictJugadores[j][3] == 0:
                                    print(" (Banca):")
                                        
                                else:
                                    print(" (" + str(dictJugadores[j][1]) + "):")
                                
                                if dictJugadores[j][1] != "eliminado":
                                
                                    print("".ljust(4) + "Cartas en mano: ", end="")
                                    
                                    for k in dictJugadores[j][0]:
                                        print(str(k[0]) + " de " + str(k[1]) + ", ", end="")
                                    
                                    print()
                                    print("".ljust(4) + "Puntos de la mano: ", dictJugadores[j][4])
                                    print("".ljust(4) + "Puntos apostados: ", dictJugadores[j][5])
                                    print()
                                
                                elif dictJugadores[j][1] == "eliminado":
                                    print()
                        
                        for x in range(2):
                            for y in range(40):
                                print("*", end="")
                            print()
                        print()
                        
                        print( "Información sobre tu mano (Jugador " + str(i) + "):")
                        print("".ljust(4) + "Cartas en mano: ", end="")
                                
                        for k in dictJugadores[i][0]:
                            print(str(k[0]) + " de " + str(k[1]) + ", ", end="")
                                
                        print()
                        print("".ljust(4) + "Puntos de la mano: ", dictJugadores[i][4])
                        print()
                        
                        for x in range(2):
                            for y in range(40):
                                print("*", end="")
                            print()
                        print()
                        
                        # Una vez enseñadas las cartas le pedimos cuantos puntos quiere apostar
                        
                        flagPuntosApostados = False
                        
                        while not flagPuntosApostados:
                            try:
                                print("¿Cuántos puntos quieres apostar jugador " + str(i) + " (tienes " + str(dictJugadores[i][6]) + " puntos restantes)?\n")
                                dictJugadores[i][5] = int(input("> "))
                                print()
                                
                                if dictJugadores[i][5] <= dictJugadores[i][6] and dictJugadores[i][5] > 0:
                                    flagPuntosApostados = True
                                
                                elif dictJugadores[i][5] > dictJugadores[i][6]:
                                    print("ERROR: Has intentado apostar más puntos de los que tienes.\n")
                                    
                                else:
                                    print("ERROR: Has introducido una apuesta no válida.\n")
                                
                            except ValueError:
                                print("\nERROR: Introduce un número entero.\n")
                        
                        flagPlantarse = False
                        
                        # Hacemos un menú para que el jugador decida que quiere hacer enseñandole sus cartas cada vez que roba.
                        
                        while not flagPlantarse:
                            for x in range(2):
                                for y in range(40):
                                    print("*", end="")
                                print()
                            print()
                            
                            print("Tus cartas son: ", end="")
                            
                            for j in dictJugadores[i][0]:
                                print(str(j[0]) + " de " + str(j[1]), end=", ")
                            print()
                            
                            print("Tienes " + str(dictJugadores[i][4]) + " puntos en mano.")
                            print("Has apostado " + str(dictJugadores[i][5]) + " puntos.")
                            print()
                            
                            for x in range(2):
                                for y in range(40):
                                    print("*", end="")
                                print()
                            print()
                            
                            flagAccion = False
                            
                            while not flagAccion:
                                try:
                                    print("¿Que quieres hacer?\n    1.- Robar carta\n    2.- Plantarte\n")
                                    print("Elige el número de la opción que quieras seleccionar:\n")
                                    plantarse = int(input("> "))
                                    print()
                                    if plantarse == 1 or plantarse == 2:
                                        flagAccion = True
                                        
                                    else:
                                        print("ERROR: Opción no válida.\n")
                                        
                                except ValueError:
                                    print("\nERROR: Introduce un número entero.\n")
                            
                            # Si decide robar le añadiremos la carta a su lista de cartas y la eliminaremos del mazo, actualizando los puntos y la cantidad de cartas en mano
                            
                            if plantarse == 1:
                                carta = random.choice(mazo)
                                dictJugadores[i][0].append(carta)
                                mazo.remove(carta)
                                dictJugadores[i][7] += 1
                                dictJugadores[i][4] += dictJugadores[i][0][dictJugadores[i][7] -1][2]
                                print("¡Jugador " + str(i) + " roba carta!\n")
                                print("".ljust(4) + ">>>> ¡Ha robado el " + str(carta[0]) + " de " + str(carta[1]) + "!\n")
                                
                            elif plantarse == 2:
                                dictJugadores[i][1] = "plantado"
                                flagPlantarse = True
                                print("¡Jugador " + str(i) + " se planta!\n")
                                
                            # Si se pasa de 7.5 lo eliminaremos directamente
                            
                            if dictJugadores[i][4]> 7.5:
                                dictJugadores[i][1] = "eliminado"
                                dictJugadores[banca][6] += dictJugadores[i][5]
                                dictJugadores[i][6] -= dictJugadores[i][5]
                                flagPlantarse = True
                                print("¡Jugador " + str(i) + " es eliminado de esta ronda porque tiene " + str(dictJugadores[i][4]) + " puntos!\n")
                                print("¡El jugador " + str(banca) + " (banca) gana " + str(dictJugadores[i][5]) + " puntos!\n")
                                dictJugadores[i][5] = 0

                # Aqui haremos la logica de los bots
                
                elif dictJugadores[i][8] == "bot":
                    if dictJugadores[i][3] != 0 and dictJugadores[i][1] == "jugando" and dictJugadores[i][2] != "eliminado":
                        turnoBot = "| Turno del " + str(i) + " |"
                        
                        for x in range(len(turnoBot)):
                            print("-", end="")
                        print()

                        print(turnoBot)

                        for x in range(len(turnoBot)):
                            print("-", end="")
                        print()
                        print()
                        
                        # Enseñamos la primera carta que robó el bot
                        
                        print("El " + str(i) + " empieza con el " + str(dictJugadores[i][0][0][0]) + " de " + str(dictJugadores[i][0][0][1]) + ".\n")
                        
                        # Añadimos el codigo de lo que va a apostar el bot, empieza cumpliendo que apuesta el 20% de sus puntos dentro de un rango de 2 a 5, dependiendo de el porcentaje apostará mas cerca de un limite o del otro.
                        
                        apuestaBot = round(dictJugadores[i][6] * 0.2)
                        
                        # Miramos si el 20% es mas elevado que la apuesta maxima
                        
                        if apuestaBot > maxApuesta:
                            dictJugadores[i][5] = maxApuesta
                            print("El " + str(i) + " apuesta " + str(dictJugadores[i][5]) + " puntos.\n")
                        
                        # Miramos si el 20% es el mismo que la apuesta maxima
                        
                        elif apuestaBot == maxApuesta:
                            aleatoriedad = random.randint(-1, 0)
                            dictJugadores[i][5] = apuestaBot + aleatoriedad
                            print("El " + str(i) + " apuesta " + str(dictJugadores[i][5]) + " puntos.\n")
                        
                        # Miramos si el 20% es inferior a la apuesta maxima
                        
                        elif apuestaBot < maxApuesta:
                            
                            # Miramos si ademas es superior al minimo
                            
                            if apuestaBot > minApuesta:
                                aleatoriedad = random.randint(-1, 1)
                                dictJugadores[i][5] = apuestaBot + aleatoriedad
                                print("El " + str(i) + " apuesta " + str(dictJugadores[i][5]) + " puntos.\n")
                                
                            # Si es igual al mínimo
                            
                            elif apuestaBot == minApuesta:
                                aleatoriedad = random.randint(0, 1)
                                dictJugadores[i][5] = apuestaBot + aleatoriedad
                                print("El " + str(i) + " apuesta " + str(dictJugadores[i][5]) + " puntos.\n")
                                
                            # Si es inferior, aqui tendremos que comprobar los puntos que le quedan al bot para que no apueste mas de los que tiene
                            
                            elif apuestaBot < minApuesta:
                                
                                if dictJugadores[i][6] > minApuesta:
                                    dictJugadores[i][5] = minApuesta
                                    print("El " + str(i) + " apuesta " + str(dictJugadores[i][5]) + " puntos.\n")
                                    
                                elif dictJugadores[i][6] <= minApuesta:
                                    dictJugadores[i][5] = dictJugadores[i][6]
                                    print("El " + str(i) + " apuesta " + str(dictJugadores[i][5]) + " puntos.\n")
                        
                        while dictJugadores[i][1] == "jugando":
                        
                            # Aqui miraremos si coje carta el bot, Si tiene menos puntos en mano que la banca la cojerá siempre
                            
                            if dictJugadores[i][4] <= dictJugadores[banca][4]:
                                carta = random.choice(mazo)
                                dictJugadores[i][0].append(carta)
                                mazo.remove(carta)
                                dictJugadores[i][7] += 1
                                dictJugadores[i][4] += dictJugadores[i][0][dictJugadores[i][7] -1][2]
                                print("¡El " + str(i) + " roba carta!\n")
                                print("".ljust(4) + ">>>> ¡Ha robado el " + str(carta[0]) + " de " + str(carta[1]) + "!\n")
                                
                            # Si tiene mas puntos que la banca se calcula la posibilidad de jugar carta
                            
                            elif dictJugadores[i][4] > dictJugadores[banca][4]:
                                
                                puntosParaPasarse = 7.5 - dictJugadores[i][4]
                                
                                contadorPorcentajeRobar = 0
                                
                                for j in mazo:
                                    if j[2] <= puntosParaPasarse:
                                        contadorPorcentajeRobar += 1
                                
                                porcentajeRobarCarta = ( contadorPorcentajeRobar / len(mazo)) * 100
                                
                                # Si el porcentaje es mayor que 65 roba carta seguro
                                
                                if porcentajeRobarCarta > 65:
                                    carta = random.choice(mazo)
                                    dictJugadores[i][0].append(carta)
                                    mazo.remove(carta)
                                    dictJugadores[i][7] += 1
                                    dictJugadores[i][4] += dictJugadores[i][0][dictJugadores[i][7] -1][2]
                                    print("¡El " + str(i) + " roba carta!\n")
                                    print("".ljust(4) + ">>>> ¡Ha robado el " + str(carta[0]) + " de " + str(carta[1]) + "!\n")
                                
                                # Si esta entre 50 y 65 esas son las probabilidades de robar, por lo que generamos un numero aleatorio para ver si roba
                                
                                elif porcentajeRobarCarta >= 50 and porcentajeRobarCarta <= 65:
                                    probabilidadRobarCarta = random.random() * 100
                                    
                                    if probabilidadRobarCarta <= porcentajeRobarCarta:
                                        carta = random.choice(mazo)
                                        dictJugadores[i][0].append(carta)
                                        mazo.remove(carta)
                                        dictJugadores[i][7] += 1
                                        dictJugadores[i][4] += dictJugadores[i][0][dictJugadores[i][7] -1][2]
                                        print("¡El " + str(i) + " roba carta!\n")
                                        print("".ljust(4) + ">>>> ¡Ha robado el " + str(carta[0]) + " de " + str(carta[1]) + "!\n")
                                    
                                    else:
                                        dictJugadores[i][1] = "plantado"
                                        print("¡El " + str(i) + " se planta!\n")
                                
                                # En caso que sea menor a 50, se divide entre 3 y ese sera la probabilidad de robar carta del bot
                                
                                elif porcentajeRobarCarta < 50:
                                    probabilidadRobarCarta = random.random() * 100
                                    
                                    if probabilidadRobarCarta <= porcentajeRobarCarta / 3:
                                        carta = random.choice(mazo)
                                        dictJugadores[i][0].append(carta)
                                        mazo.remove(carta)
                                        dictJugadores[i][7] += 1
                                        dictJugadores[i][4] += dictJugadores[i][0][dictJugadores[i][7] -1][2]
                                        print("¡El " + str(i) + " roba carta!\n")
                                        print("".ljust(4) + ">>>> ¡Ha robado el " + str(carta[0]) + " de " + str(carta[1]) + "!\n")
                                    
                                    else:
                                        print("¡El " + str(i) + " se planta!\n")
                                        dictJugadores[i][1] = "plantado"
                                                    
                            # Si se pasa de 7.5 lo eliminaremos directamente
                            
                            if dictJugadores[i][4]> 7.5:
                                dictJugadores[i][1] = "eliminado"
                                dictJugadores[banca][6] += dictJugadores[i][5]
                                dictJugadores[i][6] -= dictJugadores[i][5]
                                flagPlantarse = True
                                print("¡El " + str(i) + " es eliminado de esta ronda porque tiene " + str(dictJugadores[i][4]) + " puntos!\n")
                                print("¡El jugador " + str(banca) + " (banca) gana " + str(dictJugadores[i][5]) + " puntos!\n")
                                dictJugadores[i][5] = 0
                                
            # Miramos si los jugadores han sido eliminados, si han sido todos eliminados, la banca gana automáticamente
            
            cJugadorEliminado = 0
            
            for i in listaJugadores:
                if dictJugadores[i][3] != 0:
                    if dictJugadores[i][1] == "eliminado":
                        cJugadorEliminado += 1
            
            if cJugadorEliminado == len(listaJugadores) -1:
                mensajeFinRonda = "¡Todos los jugadores han sido eliminados en esta ronda, gana la banca (" + str(banca) + ")!"
                
                for x in range(len(mensajeFinRonda)):
                    print("-", end="")
                print()

                print(mensajeFinRonda)

                for x in range(len(mensajeFinRonda)):
                    print("-", end="")
                print()
            
            elif cJugadorEliminado != len(listaJugadores) -1:
                
                # Ahora hacemos el turno de la banca, separamos jugadores de bots

                turnoBanca = "| Turno de la Banca (" + str(banca) + ") |"
                
                for x in range(len(turnoBanca)):
                    print("-", end="")
                print()

                print(turnoBanca)

                for x in range(len(turnoBanca)):
                    print("-", end="")
                print()
                print()
                
                if dictJugadores[banca][8] == "humano":

                    # Enseñamos todas las cartas y puntos de cada jugador
                    
                    for x in range(2):
                        for y in range(40):
                            print("*", end="")
                        print()
                    print()
                    
                    for j in listaJugadores:
                        if j != banca:
                            print("Información del jugador " + str(j), end="")
                                    
                            if dictJugadores[j][3] == 0:
                                print(" (Banca):")
                                            
                            else:
                                print(" (" + str(dictJugadores[j][1]) + "):")
                                    
                            if dictJugadores[j][1] != "eliminado":
                                    
                                print("".ljust(4) + "Cartas en mano: ", end="")
                                        
                                for k in dictJugadores[j][0]:
                                    print(str(k[0]) + " de " + str(k[1]) + ", ", end="")
                                        
                                print()
                                print("".ljust(8) + "Puntos de la mano: ", dictJugadores[j][4])
                                print("".ljust(8) + "Puntos apostados: ", dictJugadores[j][5])
                                print()
                                    
                            elif dictJugadores[j][1] == "eliminado":
                                print()
                                
                    for x in range(2):
                        for y in range(40):
                            print("*", end="")
                        print()
                    
                    flagPlantarse = False
                            
                    # Hacemos un menú para que el jugador decida que quiere hacer enseñandole sus cartas cada vez que roba.
                            
                    while not flagPlantarse:
                        
                        for x in range(2):
                            for y in range(40):
                                print("*", end="")
                            print()
                        print()
                        
                        print("Tus cartas son: ", end="")
                                
                        for j in dictJugadores[banca][0]:
                            print(str(j[0]) + " de " + str(j[1]), end=", ")
                        print()
                                
                        print("Tienes " + str(dictJugadores[banca][4]) + " puntos en mano.\n")
                        
                        for x in range(2):
                            for y in range(40):
                                print("*", end="")
                            print()
                        print()
                                        
                        flagAccion = False
                            
                        while not flagAccion:
                            try:
                                print("¿Que quieres hacer?\n    1.- Robar carta\n    2.- Plantarte\n")
                                print("Elige el número de la opción que quieras seleccionar:\n")
                                plantarse = int(input("> "))
                                print()
                                if plantarse == 1 or plantarse == 2:
                                    flagAccion = True
                                        
                                else:
                                    print("ERROR: Opción no válida.\n")
                                        
                            except ValueError:
                                print("\nERROR: Introduce un número entero.\n")
                                
                        # Si decide robar le añadiremos la carta a su lista de cartas y la eliminaremos del mazo, actualizando los puntos y la cantidad de cartas en mano
                                
                        if plantarse == 1:
                            carta = random.choice(mazo)
                            dictJugadores[banca][0].append(carta)
                            mazo.remove(carta)
                            dictJugadores[banca][7] += 1
                            dictJugadores[banca][4] += dictJugadores[banca][0][dictJugadores[banca][7] -1][2]
                            print("¡La banca (Jugador " + str(banca) + ") roba carta!\n")
                            print("".ljust(4) + ">>>> ¡Ha robado el " + str(carta[0]) + " de " + str(carta[1]) + "!\n")
                                    
                        elif plantarse == 2:
                            dictJugadores[banca][1] = "plantado"
                            flagPlantarse = True
                            print("¡La banca (Jugador " + str(banca) + ") se planta!\n")
                                
                        # Si la banca se pasa de 7.5 o lo iguala salimos del bucle porque ya se ha acabado la ronda
                                
                        if dictJugadores[banca][4] >= 7.5:
                            flagPlantarse = True

                # Añadimos la logica bot de la banca, siempre que haya un jugador con mas puntos que la banca va a robar carta
                
                elif dictJugadores[banca][8] == "bot":
                    flagPlantarse = False
                    
                    print("La banca (" + str(banca) + ") empieza con el " + str(dictJugadores[banca][0][0][0]) + " de " + str(dictJugadores[banca][0][0][1]) + ".\n")
                    
                    # Hacemos un bucle que se repite siempre que la banca haya robado carta, y si roba carta se repite desde el principio
                    
                    while not flagPlantarse:
                        
                        # Si tiene 7 y medio o mas se acaba el turno
                        
                        if dictJugadores[banca][4] >= 7.5:
                            flagPlantarse = True
                            
                        else:
                            botBancaRobaCarta = False
                            
                            # Miramos toda la lista de jugadores y comparamos sus puntos con los de la banca, si hay alguien que le supere roba carta y vuelve a empezar el bucle
                            
                            for i in listaJugadores:
                                if dictJugadores[i][4] > dictJugadores[banca][4]:
                                    carta = random.choice(mazo)
                                    dictJugadores[banca][0].append(carta)
                                    mazo.remove(carta)
                                    dictJugadores[banca][7] += 1
                                    dictJugadores[banca][4] += dictJugadores[banca][0][dictJugadores[banca][7] -1][2]
                                    print("¡La banca (" + str(banca) + ") roba carta!\n")
                                    print("".ljust(4) + ">>>> ¡Ha robado el " + str(carta[0]) + " de " + str(carta[1]) + "!\n")
                                    botBancaRobaCarta = True
                                    break
                            
                            # Si no ha robado carta se planta
                            
                            if botBancaRobaCarta == False:
                                dictJugadores[banca][1] = "plantado"
                                flagPlantarse = True
                                print("¡La banca (" + str(banca) + ") se planta!\n")
                        
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
                            
                            # Añadimos la rotacion de banca
                            
                            if cJugador == 0:
                                
                                mensajeFinRonda = "* ¡Además el jugador " + str(i) + " gana a la banca con un 7.5, ahora será la banca! *"
                                for j in range(len(mensajeFinRonda)):
                                    print("*", end="")
                                print()

                                print(mensajeFinRonda)

                                for j in range(len(mensajeFinRonda)):
                                    print("*", end="")
                                print()
                                
                                dictJugadores[i][3] = 0
                                dictJugadores[banca][3] = len(listaJugadores)
                                nuevaBanca = i
                                cJugador += 1

                            else:
                                mensajeFinRonda = "* ¡Además El jugador " + str(i) + " gana a la banca con un 7.5! *"
                                for j in range(len(mensajeFinRonda)):
                                    print("*", end="")
                                print()

                                print(mensajeFinRonda)

                                for j in range(len(mensajeFinRonda)):
                                    print("*", end="")
                                print()
                            
                        # Tiene que mirar si es el doble para acabar de pagar todos los puntos
                            
                        elif dictJugadores[banca][6] <= dictJugadores[i][5] * 2 and dictJugadores[banca][6] != 0 and dictJugadores[i][4] == 7.5:
                            dictJugadores[i][6] += dictJugadores[banca][6]
                            dictJugadores[banca][6] = 0
                            dictJugadores[i][5]= 0
                            
                            # Añadimos rotacion de banca
                            
                            if cJugador == 0:
                                
                                mensajeFinRonda = "* ¡Además el jugador " + str(i) + " gana a la banca con un 7.5, ahora será la banca! *"
                                for j in range(len(mensajeFinRonda)):
                                    print("*", end="")
                                print()

                                print(mensajeFinRonda)

                                for j in range(len(mensajeFinRonda)):
                                    print("*", end="")
                                print()
                                
                                dictJugadores[i][3] = 0
                                dictJugadores[banca][3] = len(listaJugadores)
                                nuevaBanca = i
                                cJugador += 1

                            else:
                                mensajeFinRonda = "* ¡Además el jugador " + str(i) + " gana a la banca con un 7.5! *"
                                for j in range(len(mensajeFinRonda)):
                                    print("*", end="")
                                print()

                                print(mensajeFinRonda)

                                for j in range(len(mensajeFinRonda)):
                                    print("*", end="")
                                print()
                                
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
                            
                            # Le añadimos un contador para que el primer jugador que cumpla esta condicion en esta ronda se convierta en la banca
                            
                            if cJugador == 0:
                                
                                mensajeFinRonda = "* ¡El jugador " + str(i) + " gana a la banca con un 7.5, ahora será la banca! *"
                                for j in range(len(mensajeFinRonda)):
                                    print("*", end="")
                                print()

                                print(mensajeFinRonda)

                                for j in range(len(mensajeFinRonda)):
                                    print("*", end="")
                                print()
                                
                                dictJugadores[i][3] = 0
                                dictJugadores[banca][3] = len(listaJugadores)
                                nuevaBanca = i
                                cJugador += 1

                            else:
                                mensajeFinRonda = "* ¡El jugador " + str(i) + " gana a la banca con un 7.5! *"
                                for j in range(len(mensajeFinRonda)):
                                    print("*", end="")
                                print()

                                print(mensajeFinRonda)

                                for j in range(len(mensajeFinRonda)):
                                    print("*", end="")
                                print()
                        
                        # Si la banca tiene mas puntos o los mismos que el jugador la banca gana
                            
                        elif dictJugadores[banca][4] >= dictJugadores[i][4]:
                            dictJugadores[banca][6] += dictJugadores[i][5]
                            dictJugadores[i][6] -= dictJugadores[i][5]
                            dictJugadores[i][5] = 0
                            
                            mensajeFinRonda = "* ¡La banca gana al jugador " + str(i) + "! *"
                            for j in range(len(mensajeFinRonda)):
                                print("*", end="")
                            print()

                            print(mensajeFinRonda)

                            for j in range(len(mensajeFinRonda)):
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
            
            listaJugadoresEliminados = []

            for i in listaJugadores:
                dictJugadores[i][0] = []
                dictJugadores[i][4] = 0
                dictJugadores[i][7] = 0
                dictJugadores[i][5] = 0
                
                if dictJugadores[i][6] != 0:
                    dictJugadores[i][1] = "jugando"
                
                elif dictJugadores[i][6] == 0:
                    dictJugadores[i][1] = "eliminado"
                    dictJugadores[i][2] = "eliminado"
                    dictJugadores[i][3] = -1
                    listaJugadoresEliminados.append(i)
                    print("".ljust(8) + ">>> El jugador " + str(i) + " ha sido eliminado de la partida.\n")
                    
            # Sacamos los jugadores eliminados de la lista de prioridad

            for i in listaJugadoresEliminados:
                listaJugadores.remove(i)

            # Si solo queda 1 jugador se acaba la partida
            
            if len(listaJugadores) <= 1:
                flagFinPartida = True

            # Cambiamos el orden de prioridad de jugadores si han habido cambios de banca por 7.5

            if banca != nuevaBanca:
                
                # Si la banca no ha sido eliminada cambiaremos de sitio al jugador con la banca
                
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
                
                # Si ha sido eliminado entonces solo añadimos la nueva banca que es quien tiene el 7.5
                
                elif dictJugadores[banca][2] == "eliminado":
                    listaJugadores.remove(nuevaBanca)
                    
                    if len(listaJugadores) == 0:
                        listaJugadores.append(nuevaBanca)
                        
                    else:
                        listaJugadores.insert(0, nuevaBanca)
                        
                    banca = nuevaBanca
                
                # Volvemos a organizar la lista de Jugadores y modificamos las prioridades, si se ha eliminado la banca ya la habremos quitado de la lista por lo que ya estará ordenada colocamos la nuevaBanca como la misma banca para las comprobaciones en la siguiente ronda
                
            for i in listaJugadores:
                dictJugadores[i][3] = listaJugadores.index(i)
                if dictJugadores[i][3] == 0:
                    banca = i
                    nuevaBanca = i
                
            ronda += 1
            
        if len(listaJugadores) == 1:
            
            for i in listaJugadores:
                jugadorGanador = "~ ¡Ha ganado el jugador " + str(i) + " por ser el único jugador con puntos restantes! ~"
                for j in range(len(jugadorGanador)):
                    print("~", end="")
                print()
                print(jugadorGanador)
                for j in range(len(jugadorGanador)):
                    print("~", end="")
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
                ganador = "~ El jugador con más puntos es " + str(jugadorGanador) + " por lo tanto gana la partida! ~"
                
                for i in range(len(ganador)):
                    print("~", end="")
                print()
                
                print(ganador)
                
                for i in range(len(ganador)):
                    print("~", end="")
                print()
            
            elif len(listaEmpates) > 1:
                ganador = "~ ¡Ha habido un empate! Los jugadores ganadores son: ~"
                
                for i in range(len(ganador)):
                    print("~", end="")
                print()
                
                print(ganador)
                
                for j in listaEmpates:
                    empate = "~" + "".ljust(4) + " >>> Jugador: " + str(j)
                    c = len(ganador) - len(empate)
                    print(str(empate) + "~".rjust(c))
                
                for i in range(len(ganador)):
                    print("~", end="")
                print()
        print()
        
        flagJugarOtraPartida = False
        
        while not flagJugarOtraPartida:
            try:
                print("¿Quieres jugar otra partida?\n    1.- Sí\n    2.- No\n")
                otraPartida = int(input("> "))
                print()
                
                if otraPartida == 1:
                    flagJugarOtraPartida = True
                
                elif otraPartida == 2:
                    flagJugarOtraPartida = True
                    menuJugarEstadisticas = 0
                
                else:
                    print("ERROR: Opción no válida.\n")
                    
            except ValueError:
                print("\nERROR: Introduce un número entero.\n")
        
    while menuJugarEstadisticas == 2:
        estadisticas = "* Estadísticas *"

        for i in range(len(estadisticas)):
            print("*", end="")
        print()

        print(estadisticas)

        for i in range(len(estadisticas)):
            print("*", end="")
        print()
        
        flagMenuEstadisticas = False
        
        while not flagMenuEstadisticas:
            try:
                print("Elige la query que deseas comprobar:\n    1.- Carta inicial más repetida por cada jugador\n    2.- Jugador que realiza la apuesta más alta por partida\n    3.- Jugador que realiza la apuesta más baja por partida\n    4.- Ratio de turnos ganados por jugador en cada partida\n    5.- Porcentaje de partidas ganadas por Bots\n    6.- Datos de los jugadores y el tiempo que han durado sus partidas ganadas cuya puntuación obtenida es mayor que la media puntos de las partidas ganadas totales\n    7.- Cuántas rondas se ganan en cada partida según el palo de la carta inicial\n    8.- Cuantas rondas gana la banca en cada partida\n    9.- Cuántos usuarios han sido la banca en cada partida\n    10.- Partida con la puntuación más alta final de todos los jugadores\n    11.- Apuesta media por partida\n    12.- Volver al Menú Principal\n")
                menuEstadisticas = int(input("> "))
                print()
                
                if menuEstadisticas >= 1 and menuEstadisticas <= 12:
                    flagMenuEstadisticas = True
                else:
                    print("ERROR: Opción no válida.\n")
                    
            except ValueError:
                print("\nERROR: Introduce un número entero.\n")
                
        if menuEstadisticas == 1:
            def exportarquery1(outfileName):
                print("Carta inicial más repetida por cada jugador:\n")
                with open(outfileName, "w") as outfile:
                    db = pymysql.connect(conexion, usuario, password, BBDD)
                    cursor = db.cursor()
                    sql = "SELECT DISTINCT CASE WHEN usuario.username IS NOT NULL THEN usuario.username ELSE bot.descripcion END AS 'Jugador', MODA.carta_inicial 'Carta inicial más repetida' FROM (SELECT idparticipante, carta_inicial, count(*), ROW_NUMBER() OVER (PARTITION BY idparticipante ORDER BY count(*) DESC) AS 'RN' FROM turnos	GROUP BY carta_inicial, idparticipante) AS MODA INNER JOIN turnos ON turnos.idparticipante = MODA.idparticipante INNER JOIN participante ON participante.id_participante = turnos.idparticipante INNER JOIN jugador ON jugador.idjugador = participante.id_jugador LEFT JOIN usuario ON jugador.idusuario = usuario.idusuario LEFT JOIN bot ON jugador.idbot = bot.idbot WHERE RN = 1;".format(0)
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    outfile.write('<?xml version="1.0" ?>\n')
                    outfile.write('<mydata>\n')
                    encabezadoQuery = "|" + "Jugador".center(10) + "|" + "Carta Inicial".center(15) + "|"
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    print(encabezadoQuery)
                    
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    for row in rows:
                        jugador = row[0]
                        cartaInicial = row[1]
                        # Now print fetched result
                        print("|" + str(jugador).center(10) + "|" + str(cartaInicial).center(15) + "|")
                        
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    print()
                    
            exportarquery1("Resultadoquery.xml")

        elif menuEstadisticas == 2:
            def exportarquery1(outfileName):
                print("Jugador que realiza la apuesta más alta por partida:\n")
                with open(outfileName, "w") as outfile:
                    db = pymysql.connect(conexion, usuario, password, BBDD)
                    cursor = db.cursor()
                    sql = "SELECT idpartida AS Partida, Jugador FROM (SELECT CASE WHEN usuario.username IS NOT NULL THEN usuario.username ELSE bot.descripcion END AS Jugador, MAX(turnos.apuesta) AS apuesta, partida.idpartida AS idpartida FROM jugador LEFT JOIN bot ON bot.idbot = jugador.idbot LEFT JOIN usuario ON usuario.idusuario = jugador.idusuario INNER JOIN participante ON jugador.idjugador = participante.id_jugador INNER JOIN turnos ON participante.id_participante = turnos.idparticipante INNER JOIN partida ON turnos.idpartida=partida.idpartida WHERE turnos.apuesta IS NOT NULL GROUP BY partida.idpartida, usuario.username) tabla WHERE (apuesta, idpartida) IN (SELECT MAX(turnos.apuesta), partida.idpartida FROM jugador LEFT JOIN bot ON bot.idbot = jugador.idbot LEFT JOIN usuario ON usuario.idusuario = jugador.idusuario INNER JOIN participante ON jugador.idjugador = participante.id_jugador INNER JOIN turnos ON participante.id_participante = turnos.idparticipante INNER JOIN partida ON turnos.idpartida = partida.idpartida GROUP BY partida.idpartida ORDER BY MAX(turnos.apuesta) DESC) GROUP BY idpartida ORDER BY idpartida ASC;".format(0)
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    outfile.write('<?xml version="1.0" ?>\n')
                    outfile.write('<mydata>\n')
                    encabezadoQuery = "|" + "Partida".center(10) + "|" + "Jugador".center(10) + "|"
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    print(encabezadoQuery)
                    
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    for row in rows:
                        partida = row[0]
                        jugador = row[1]
                        # Now print fetched result
                        print("|" + str(partida).center(10) + "|" + str(jugador).center(10) + "|")
                        
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    print()
            
            exportarquery1("Resultadoquery.xml")
        
        elif menuEstadisticas == 3:
            def exportarquery1(outfileName):
                print("Jugador que realiza la apuesta más baja por partida:\n")
                with open(outfileName, "w") as outfile:
                    db = pymysql.connect(conexion, usuario, password, BBDD)
                    cursor = db.cursor()
                    sql = "SELECT idpartida AS Partida, Jugador FROM (SELECT CASE WHEN usuario.username IS NOT NULL THEN usuario.username ELSE bot.descripcion END AS Jugador, MIN(turnos.apuesta) AS apuesta, partida.idpartida AS idpartida FROM jugador LEFT JOIN bot ON bot.idbot = jugador.idbot LEFT JOIN usuario ON usuario.idusuario = jugador.idusuario INNER JOIN participante ON jugador.idjugador = participante.id_jugador INNER JOIN turnos ON participante.id_participante = turnos.idparticipante INNER JOIN partida ON turnos.idpartida=partida.idpartida WHERE turnos.apuesta IS NOT NULL GROUP BY partida.idpartida, usuario.username) tabla WHERE (apuesta, idpartida) IN (SELECT MIN(turnos.apuesta), partida.idpartida FROM jugador LEFT JOIN bot ON bot.idbot = jugador.idbot LEFT JOIN usuario ON usuario.idusuario = jugador.idusuario INNER JOIN participante ON jugador.idjugador = participante.id_jugador INNER JOIN turnos ON participante.id_participante = turnos.idparticipante INNER JOIN partida ON turnos.idpartida = partida.idpartida GROUP BY partida.idpartida ORDER BY MIN(turnos.apuesta) DESC) GROUP BY idpartida ORDER BY idpartida ASC;".format(0)
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    outfile.write('<?xml version="1.0" ?>\n')
                    outfile.write('<mydata>\n')
                    encabezadoQuery = "|" + "Partida".center(10) + "|" + "Jugador".center(10) + "|"
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    print(encabezadoQuery)
                    
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    for row in rows:
                        partida = row[0]
                        jugador = row[1]
                        # Now print fetched result
                        print("|" + str(partida).center(10) + "|" + str(jugador).center(10) + "|")
                        
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    print()
            
            exportarquery1("Resultadoquery.xml")

        elif menuEstadisticas == 4:
            def exportarquery1(outfileName):
                print("Ratio de turnos ganados por jugador en cada partida:\n")
                with open(outfileName, "w") as outfile:
                    db = pymysql.connect(conexion, usuario, password, BBDD)
                    cursor = db.cursor()
                    sql = "SELECT partida.nombre_sala AS 'Nombre partida', CASE WHEN usuario.username IS NOT NULL THEN usuario.username ELSE bot.descripcion END AS 'Jugador', (y.Victoria/x.Total)*100 AS 'Porcentaje %' FROM (SELECT DISTINCT idpartida, MAX(numero_turno) AS 'Total' FROM turnos	GROUP BY idpartida) AS x INNER JOIN (SELECT idpartida, idparticipante, count(*) AS 'Victoria' FROM turnos WHERE (puntos_final - puntos_inicio) > 0	GROUP BY idparticipante, idpartida) AS y ON y.idpartida = x.idpartida INNER JOIN partida ON y.idpartida = partida.idpartida INNER JOIN participante ON participante.id_participante = y.idparticipante INNER JOIN jugador ON jugador.idjugador = participante.id_jugador LEFT JOIN usuario ON jugador.idusuario = usuario.idusuario LEFT JOIN bot ON jugador.idbot = bot.idbot GROUP BY y.idparticipante, x.idpartida;".format(0)
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    outfile.write('<?xml version="1.0" ?>\n')
                    outfile.write('<mydata>\n')
                    encabezadoQuery = "|" + "Nombre de la Partida".center(30) + "|" + "Jugador".center(10) + "|"  + "Porcentaje %".center(15) + "|"
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    print(encabezadoQuery)
                    
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    for row in rows:
                        nombrePartida = row[0]
                        jugador = row[1]
                        porcentaje = row[2]
                        # Now print fetched result
                        print("|" + str(nombrePartida).center(30) + "|" + str(jugador).center(10) + "|" + str(porcentaje).center(15) + "|")
                        
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    print()
            
            exportarquery1("Resultadoquery.xml")
        
        elif menuEstadisticas == 5:
            def exportarquery1(outfileName):
                print("Porcentaje de partidas ganadas por Bots:\n")
                with open(outfileName, "w") as outfile:
                    db = pymysql.connect(conexion, usuario, password, BBDD)
                    cursor = db.cursor()
                    sql = "SELECT (x.victoriaBot / y.partidasTotales) * 100 AS 'Porcentaje %' FROM (SELECT count(DISTINCT partida.idpartida) AS victoriaBot	FROM partida INNER JOIN turnos ON turnos.idpartida = partida.idpartida INNER JOIN participante ON participante.id_participante = turnos.idparticipante INNER JOIN jugador ON jugador.idjugador = participante.id_jugador INNER JOIN bot ON jugador.idbot = bot.idbot) AS x, (SELECT MAX(idpartida) AS partidasTotales FROM partida) AS y;".format(0)
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    outfile.write('<?xml version="1.0" ?>\n')
                    outfile.write('<mydata>\n')
                    encabezadoQuery = "|" + "Porcentaje %".center(15) + "|"
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    print(encabezadoQuery)
                    
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    for row in rows:
                        porcentaje = row[0]
                        # Now print fetched result
                        print("|" + str(porcentaje).center(15) + "|")
                        
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    print()
            
            exportarquery1("Resultadoquery.xml")
            
        elif menuEstadisticas == 6:
            def exportarquery1(outfileName):
                print("Datos de los jugadores y el tiempo que han durado sus partidas ganadas cuya puntuación obtenida es mayor que la media puntos de las partidas ganadas totales:\n")
                with open(outfileName, "w") as outfile:
                    db = pymysql.connect(conexion, usuario, password, BBDD)
                    cursor = db.cursor()
                    sql = "SELECT DISTINCT partida.idpartida AS Partida, CASE WHEN usuario.username IS NOT NULL THEN usuario.username ELSE bot.descripcion END AS Jugador, usuario.email, TIMEDIFF(partida.hora_fin, partida.hora_inicio) AS 'Duración de la partida' FROM partida INNER JOIN turnos ON partida.idpartida = turnos.idpartida INNER JOIN participante ON turnos.idparticipante = participante.id_participante INNER JOIN jugador ON participante.id_jugador = jugador.idjugador LEFT JOIN bot ON jugador.idbot = bot.idbot LEFT JOIN usuario ON jugador.idusuario = usuario.idusuario WHERE (partida.idpartida, idparticipante) IN (SELECT idpartida, ganador_partida AS idparticipante FROM partida) AND puntos_final > (SELECT AVG(puntos_final) FROM(SELECT idpartida, numero_turno, puntos_final, ROW_NUMBER () OVER (PARTITION BY idpartida ORDER BY numero_turno DESC) AS RN FROM turnos WHERE (idpartida, idparticipante) IN (SELECT idpartida, ganador_partida FROM partida order by idpartida)) as x WHERE RN = 1);".format(0)
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    outfile.write('<?xml version="1.0" ?>\n')
                    outfile.write('<mydata>\n')
                    encabezadoQuery = "|" + "Partida".center(15) + "|" + "Jugador".center(15) + "|" + "email".center(15) + "|" + "Duración".center(15) + "|"
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    print(encabezadoQuery)
                    
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    for row in rows:
                        partida = row[0]
                        jugador = row[1]
                        email = row[2]
                        duracion = row[3]
                        # Now print fetched result
                        print("|" + str(partida).center(15) + "|" + str(jugador).center(15) + "|" + str(email).center(15) + "|" + str(duracion).center(15) + "|")
                        
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    print()
            
            exportarquery1("Resultadoquery.xml")

        elif menuEstadisticas == 7:
            def exportarquery1(outfileName):
                print("Cuántas rondas se ganan en cada partida según el palo de la carta inicial:\n")
                with open(outfileName, "w") as outfile:
                    db = pymysql.connect(conexion, usuario, password, BBDD)
                    cursor = db.cursor()
                    sql = "SELECT partida.idpartida AS 'Partida', count(*) 'Rondas', tipo_carta.descripcion AS 'Palo Inicial' FROM partida INNER JOIN turnos ON partida.idpartida = turnos.idpartida INNER JOIN cartas ON turnos.carta_inicial = cartas.idcartas INNER JOIN tipo_carta ON cartas.tipo = tipo_carta.idtipo_carta WHERE (puntos_final - puntos_inicio) > 0 GROUP BY tipo_carta.descripcion, partida.nombre_sala ORDER BY partida;".format(0)
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    outfile.write('<?xml version="1.0" ?>\n')
                    outfile.write('<mydata>\n')
                    encabezadoQuery = "|" + "Partida".center(15) + "|" + "Rondas".center(15) + "|" + "Palo inicial".center(15) + "|"
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    print(encabezadoQuery)
                    
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    for row in rows:
                        partida = row[0]
                        rondas = row[1]
                        paloInicial = row[2]
                        # Now print fetched result
                        print("|" + str(partida).center(15) + "|" + str(rondas).center(15) + "|" + str(paloInicial).center(15) + "|")
                        
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    print()
            
            exportarquery1("Resultadoquery.xml")

        elif menuEstadisticas == 8:
            def exportarquery1(outfileName):
                print("Cuantas rondas gana la banca en cada partida:\n")
                with open(outfileName, "w") as outfile:
                    db = pymysql.connect(conexion, usuario, password, BBDD)
                    cursor = db.cursor()
                    sql = "SELECT idpartida AS 'Partida', count(*) AS 'Victorias de la banca' FROM turnos WHERE (puntos_final - puntos_inicio) > 0 AND es_banca = 1 GROUP BY idpartida;".format(0)
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    outfile.write('<?xml version="1.0" ?>\n')
                    outfile.write('<mydata>\n')
                    encabezadoQuery = "|" + "Partida".center(15) + "|" + "Victorias de la Banca".center(25) + "|"
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    print(encabezadoQuery)
                    
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    for row in rows:
                        partida = row[0]
                        victoriasBanca = row[1]
                        # Now print fetched result
                        print("|" + str(partida).center(15) + "|" + str(victoriasBanca).center(25) + "|")
                        
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    print()
            
            exportarquery1("Resultadoquery.xml")

        elif menuEstadisticas == 9:
            def exportarquery1(outfileName):
                print("Cuántos usuarios han sido la banca en cada partida:\n")
                with open(outfileName, "w") as outfile:
                    db = pymysql.connect(conexion, usuario, password, BBDD)
                    cursor = db.cursor()
                    sql = "SELECT idpartida AS Partida, count(*) AS 'Usuarios que han sido banca' FROM (SELECT DISTINCT turnos.idpartida, turnos.idparticipante, usuario.username FROM turnos INNER JOIN participante ON turnos.idparticipante = participante.id_participante INNER JOIN jugador ON participante.id_jugador = jugador.idjugador	INNER JOIN usuario ON jugador.idusuario = usuario.idusuario WHERE es_banca = 1  AND jugador.idusuario IS NOT NULL) AS x GROUP BY idpartida ORDER BY idpartida;".format(0)
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    outfile.write('<?xml version="1.0" ?>\n')
                    outfile.write('<mydata>\n')
                    encabezadoQuery = "|" + "Partida".center(15) + "|" + "Cantidad de Usuarios que han sido la Banca".center(45) + "|"
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    print(encabezadoQuery)
                    
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    for row in rows:
                        partida = row[0]
                        usuariosBanca = row[1]
                        # Now print fetched result
                        print("|" + str(partida).center(15) + "|" + str(usuariosBanca).center(45) + "|")
                        
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    print()
            
            exportarquery1("Resultadoquery.xml")

        elif menuEstadisticas == 10:
            def exportarquery1(outfileName):
                print("Partida con la puntuación más alta final de todos los jugadores:\n")
                with open(outfileName, "w") as outfile:
                    db = pymysql.connect(conexion, usuario, password, BBDD)
                    cursor = db.cursor()
                    sql = "SELECT CASE WHEN usuario.username IS NOT NULL THEN usuario.username ELSE bot.descripcion END AS Jugador, nombre_sala AS 'Nombre de la Partida', IF((SELECT idjugador	FROM participante INNER JOIN jugador ON participante.id_jugador = jugador.idjugador	WHERE id_participante = (SELECT partida.ganador_partida FROM partida INNER JOIN turnos ON partida.idpartida = turnos.idpartida	WHERE turnos.puntos_final = (SELECT MAX(puntos_final) FROM turnos))) = jugador.idjugador, 'Si', 'No') AS '¿Ganó la partida?' FROM turnos INNER JOIN partida ON turnos.idpartida = partida.idpartida INNER JOIN participante ON participante.id_participante = turnos.idparticipante INNER JOIN jugador ON jugador.idjugador = participante.id_jugador LEFT JOIN usuario ON jugador.idusuario = usuario.idusuario LEFT JOIN bot ON jugador.idbot = bot.idbot WHERE turnos.puntos_final = (SELECT MAX(puntos_final) FROM turnos);".format(0)
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    outfile.write('<?xml version="1.0" ?>\n')
                    outfile.write('<mydata>\n')
                    encabezadoQuery = "|" + "Jugador".center(15) + "|" + "Nombre de la Partida".center(25) + "|" + "¿Ganó la partida?".center(20) + "|"
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    print(encabezadoQuery)
                    
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    for row in rows:
                        jugador = row[0]
                        nombrePartida = row[1]
                        ganarPartida = row[2]
                        # Now print fetched result
                        print("|" + str(jugador).center(15) + "|" + str(nombrePartida).center(25) + "|" + str(ganarPartida).center(20) + "|")
                        
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    print()
            
            exportarquery1("Resultadoquery.xml")

        elif menuEstadisticas == 11:
            def exportarquery1(outfileName):
                print("Apuesta media por partida:\n")
                with open(outfileName, "w") as outfile:
                    db = pymysql.connect(conexion, usuario, password, BBDD)
                    cursor = db.cursor()
                    sql = "SELECT idpartida AS Partida, AVG(apuesta) AS 'Apuesta media' FROM turnos GROUP BY idpartida;".format(0)
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    outfile.write('<?xml version="1.0" ?>\n')
                    outfile.write('<mydata>\n')
                    encabezadoQuery = "|" + "Partida".center(10) + "|" + "Apuesta media".center(20) + "|"
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    print(encabezadoQuery)
                    
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    
                    for row in rows:
                        partida = row[0]
                        apuestaMedia = row[1]
                        # Now print fetched result
                        print("|" + str(partida).center(10) + "|" + str(apuestaMedia).center(20) + "|")
                        
                    for i in range(len(encabezadoQuery)):
                        print("-", end = "")
                    print()
                    print()
            
            exportarquery1("Resultadoquery.xml")

        elif menuEstadisticas == 12:
            menuJugarEstadisticas = 0
        
    if menuJugarEstadisticas == 3:
        flagMenuPrincipal = True

input("Pulse enter para cerrar el programa. ") 