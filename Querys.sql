-- 1 Mostrar la Carta inicial más repetida por cada jugador(mostrar nombre jugador y carta). 
SELECT DISTINCT CASE WHEN usuario.username IS NOT NULL THEN usuario.username ELSE bot.descripcion END AS "Jugador", MODA.carta_inicial "Carta inicial más repetida"
FROM (SELECT idparticipante, carta_inicial, count(*), 
	ROW_NUMBER() OVER (PARTITION BY idparticipante ORDER BY count(*) DESC) AS "RN"
	FROM turnos
	GROUP BY carta_inicial, idparticipante) AS MODA
INNER JOIN turnos ON turnos.idparticipante = MODA.idparticipante
INNER JOIN participante ON participante.id_participante = turnos.idparticipante
INNER JOIN jugador ON jugador.idjugador = participante.id_jugador
LEFT JOIN usuario ON jugador.idusuario = usuario.idusuario
LEFT JOIN bot ON jugador.idbot = bot.idbot
WHERE RN = 1;

-- 2 Jugador que realiza la apuesta más alta por partida. (Mostrar nombre jugador)
SELECT idpartida AS Partida, Jugador
FROM (
	SELECT CASE WHEN usuario.username IS NOT NULL THEN usuario.username ELSE bot.descripcion END AS Jugador, MAX(turnos.apuesta) AS apuesta, partida.idpartida AS idpartida 
	FROM jugador
	LEFT JOIN bot ON bot.idbot = jugador.idbot
	LEFT JOIN usuario ON usuario.idusuario = jugador.idusuario
	INNER JOIN participante ON jugador.idjugador = participante.id_jugador
	INNER JOIN turnos ON participante.id_participante = turnos.idparticipante
	INNER JOIN partida ON turnos.idpartida=partida.idpartida
	WHERE turnos.apuesta IS NOT NULL
	GROUP BY partida.idpartida, usuario.username) tabla
WHERE (apuesta, idpartida) IN (
	SELECT MAX(turnos.apuesta), partida.idpartida
	FROM jugador
	LEFT JOIN bot ON bot.idbot = jugador.idbot
	LEFT JOIN usuario ON usuario.idusuario = jugador.idusuario
	INNER JOIN participante ON jugador.idjugador = participante.id_jugador
	INNER JOIN turnos ON participante.id_participante = turnos.idparticipante
	INNER JOIN partida ON turnos.idpartida = partida.idpartida
	GROUP BY partida.idpartida
	ORDER BY MAX(turnos.apuesta) DESC)
GROUP BY idpartida
ORDER BY idpartida ASC;

-- 3 Jugador que realiza apuesta más baja por partida. (Mostrar nombre jugador)
SELECT idpartida AS Partida, Jugador 
FROM (
	SELECT CASE WHEN usuario.username IS NOT NULL THEN usuario.username ELSE bot.descripcion END AS Jugador, MIN(turnos.apuesta) AS apuesta, partida.idpartida AS idpartida 
	FROM jugador
	LEFT JOIN bot ON bot.idbot = jugador.idbot
	LEFT JOIN usuario ON usuario.idusuario = jugador.idusuario
	INNER JOIN participante ON jugador.idjugador = participante.id_jugador
	INNER JOIN turnos ON participante.id_participante = turnos.idparticipante
	INNER JOIN partida ON turnos.idpartida=partida.idpartida
	WHERE turnos.apuesta IS NOT NULL
	GROUP BY partida.idpartida, usuario.username) tabla
WHERE (apuesta, idpartida) IN (
	SELECT MIN(turnos.apuesta), partida.idpartida
	FROM jugador
	LEFT JOIN bot ON bot.idbot = jugador.idbot
	LEFT JOIN usuario ON usuario.idusuario = jugador.idusuario
	INNER JOIN participante ON jugador.idjugador = participante.id_jugador
	INNER JOIN turnos ON participante.id_participante = turnos.idparticipante
	INNER JOIN partida ON turnos.idpartida = partida.idpartida
	GROUP BY partida.idpartida
	ORDER BY MIN(turnos.apuesta) DESC)
GROUP BY idpartida
ORDER BY idpartida ASC;

-- 4 Ratio de turnos ganados por jugador en cada partida (%),mostrar columna Nombre jugador, Nombre partida, nueva columna "porcentaje %"
SELECT partida.nombre_sala AS "Nombre partida", CASE WHEN usuario.username IS NOT NULL THEN usuario.username ELSE bot.descripcion END AS "Jugador", (y.Victoria/x.Total)*100 AS "Porcentaje %"
FROM (
	SELECT DISTINCT idpartida, MAX(numero_turno) AS "Total"
	FROM turnos
	GROUP BY idpartida) AS x
INNER JOIN (
	SELECT idpartida, idparticipante, count(*) AS "Victoria"
	FROM turnos
	WHERE (puntos_final - puntos_inicio) > 0
	GROUP BY idparticipante, idpartida) AS y
ON y.idpartida = x.idpartida
INNER JOIN partida ON y.idpartida = partida.idpartida
INNER JOIN participante ON participante.id_participante = y.idparticipante
INNER JOIN jugador ON jugador.idjugador = participante.id_jugador
LEFT JOIN usuario ON jugador.idusuario = usuario.idusuario
LEFT JOIN bot ON jugador.idbot = bot.idbot
GROUP BY y.idparticipante, x.idpartida;

-- 5 Porcentaje de partidas ganadas Bots en general. Nueva columna "porcentaje %"
SELECT (x.victoriaBot / y.partidasTotales) * 100 AS "Porcentaje %"
FROM (
	SELECT count(DISTINCT partida.idpartida) AS victoriaBot
	FROM partida
	INNER JOIN turnos ON turnos.idpartida = partida.idpartida
	INNER JOIN participante ON participante.id_participante = turnos.idparticipante
	INNER JOIN jugador ON jugador.idjugador = participante.id_jugador
	INNER JOIN bot ON jugador.idbot = bot.idbot) AS x, 
    (
    SELECT MAX(idpartida) AS partidasTotales 
    FROM partida) AS y;

-- 6 Mostrar los datos de los jugadores y el tiempo que han durado sus partidas ganadas cuya puntuación obtenida es mayor que la media puntos de las partidas ganadas totales.
SELECT DISTINCT partida.idpartida AS Partida, CASE WHEN usuario.username IS NOT NULL THEN usuario.username ELSE bot.descripcion END AS Jugador, usuario.email, TIMEDIFF(partida.hora_fin, partida.hora_inicio) AS "Duración de la partida"
FROM partida
INNER JOIN turnos ON partida.idpartida = turnos.idpartida
INNER JOIN participante ON turnos.idparticipante = participante.id_participante
INNER JOIN jugador ON participante.id_jugador = jugador.idjugador
LEFT JOIN bot ON jugador.idbot = bot.idbot
LEFT JOIN usuario ON jugador.idusuario = usuario.idusuario
WHERE (partida.idpartida, idparticipante) IN (SELECT idpartida, ganador_partida AS idparticipante FROM partida) AND puntos_final > 
(
	SELECT AVG(puntos_final)
	FROM(
		SELECT idpartida, numero_turno, puntos_final,
		ROW_NUMBER () OVER (PARTITION BY idpartida ORDER BY numero_turno DESC) AS RN
		FROM turnos
		WHERE (idpartida, idparticipante) IN (SELECT idpartida, ganador_partida FROM partida order by idpartida)) as x
	WHERE RN = 1);

-- 7 Cuántas rondas se ganan en cada partida según el palo. Ejemplo: Partida 1 - 5 rondas - Bastos como carta inicial.
SELECT partida.idpartida AS "Partida", count(*) "Rondas", tipo_carta.descripcion AS "Palo Inicial"
FROM partida
INNER JOIN turnos ON partida.idpartida = turnos.idpartida
INNER JOIN cartas ON turnos.carta_inicial = cartas.idcartas
INNER JOIN tipo_carta ON cartas.tipo = tipo_carta.idtipo_carta
WHERE (puntos_final - puntos_inicio) > 0
GROUP BY tipo_carta.descripcion, partida.nombre_sala
ORDER BY partida;

-- 8 Cuantas rondas gana la banca en cada partida.
SELECT idpartida AS "Partida", count(*) AS "Victorias de la banca"
FROM turnos
WHERE (puntos_final - puntos_inicio) > 0 AND es_banca = 1
GROUP BY idpartida;

-- 9 Cuántos usuarios han sido la banca en cada partida. Por ejemplo partida 1 - 3 jugadores, partida 2 - 1 jugador...
SELECT idpartida AS Partida, count(*) AS "Usuarios que han sido banca"
FROM (
	SELECT DISTINCT turnos.idpartida, turnos.idparticipante, usuario.username
	FROM turnos
	INNER JOIN participante ON turnos.idparticipante = participante.id_participante
	INNER JOIN jugador ON participante.id_jugador = jugador.idjugador
	INNER JOIN usuario ON jugador.idusuario = usuario.idusuario
	WHERE es_banca = 1  AND jugador.idusuario IS NOT NULL) AS x
GROUP BY idpartida
ORDER BY idpartida;

-- 10 Partida con la puntuación más alta final de todos los jugadores, mostrar nombre jugador, nombre partida,así como añadir una columna nueva en la que diga si ha ganado la partida o no.  
SELECT CASE WHEN usuario.username IS NOT NULL THEN usuario.username ELSE bot.descripcion END AS Jugador, nombre_sala AS "Nombre de la Partida", IF((
	SELECT idjugador
	FROM participante
	INNER JOIN jugador ON participante.id_jugador = jugador.idjugador
	WHERE id_participante = (
		SELECT partida.ganador_partida
		FROM partida
		INNER JOIN turnos ON partida.idpartida = turnos.idpartida
		WHERE turnos.puntos_final = (
			SELECT MAX(puntos_final)
			FROM turnos))) = jugador.idjugador, "Si", "No") AS "¿Ganó la partida?"
FROM turnos
INNER JOIN partida ON turnos.idpartida = partida.idpartida
INNER JOIN participante ON participante.id_participante = turnos.idparticipante
INNER JOIN jugador ON jugador.idjugador = participante.id_jugador
LEFT JOIN usuario ON jugador.idusuario = usuario.idusuario
LEFT JOIN bot ON jugador.idbot = bot.idbot
WHERE turnos.puntos_final = (
	SELECT MAX(puntos_final)
	FROM turnos);

-- 11 Calcular la apuesta media por partida.
SELECT idpartida AS Partida, AVG(apuesta) AS "Apuesta media"
FROM turnos
GROUP BY idpartida;

-- 12 Mostrar los datos de los usuarios que no son bot, así como cual ha sido su última apuesta en cada partida que ha jugado.
-- 13 Calcular el valor total de las cartas y el numero total de cartas que se han dado inicialmente en las manos en la partida. Por ejemplo, en la partida se han dado 50 cartas y el valor total de las cartas es 47,5.
-- 14 Diferencia de puntos de los participantes de las partidas entre la ronda 1 y 5. Ejemplo: Rafa tenia 20 puntos, en la ronda 5 tiene 15, tiene -5 puntos de diferencia.
