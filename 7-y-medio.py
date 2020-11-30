import random

mazo = [(1, "oros", 1), (2, "oros", 2), (3, "oros", 3), (4, "oros", 4), (5, "oros", 5), (6, "oros", 6), (7, "oros", 7), (10, "oros", 0.5), (11, "oros", 0.5), (12, "oros", 0.5),(1, "copas", 1), (2, "copas", 2), (3, "copas", 3), (4, "copas", 4), (5, "copas", 5), (6, "copas", 6), (7, "copas", 7), (10, "copas", 0.5), (11, "copas", 0.5), (12, "copas", 0.5), (1, "bastos", 1), (2, "bastos", 2), (3, "bastos", 3), (4, "bastos", 4), (5, "bastos", 5), (6, "bastos", 6), (7, "bastos", 7), (10, "bastos", 0.5), (11, "bastos", 0.5), (12, "bastos", 0.5), (1, "espadas", 1), (2, "espadas", 2), (3, "espadas", 3), (4, "espadas", 4), (5, "espadas", 5), (6, "espadas", 6), (7, "espadas", 7), (10, "espadas", 0.5), (11, "espadas", 0.5), (12, "espadas", 0.5),]

listaJugadores = []

flagCantidadJugadores = False

while not flagCantidadJugadores:
    cantidadJugadores = int(input("¿Cuantos jugadores váis a jugar? (mínimo 2, máximo 8): "))
    
    if cantidadJugadores > 8 or cantidadJugadores < 2:
        print("ERROR: Elige una cantidad entre 2 y 8.")
    
    elif cantidadJugadores <= 8 and cantidadJugadores >= 2:
        flagCantidadJugadores = True

c = 1

while len(listaJugadores) < cantidadJugadores: 
    
    nombreJugador = input("Introduce el nombre del jugador " + str(c) + ": ")
    
    if nombreJugador[0:1].isalpha() == True and " " not in nombreJugador:
        listaJugadores.append(nombreJugador)
        c += 1
    else:
        print("ERROR: Tu nombre no empieza por una letra o contiene espacios.")

listaPrioridad = []

for i in range(len(listaJugadores)):
    carta = random.choice(mazo)
    mazo.remove(carta)
    listaPrioridad.append([listaJugadores[i], carta])
    
print(mazo)
print(listaPrioridad)
    
