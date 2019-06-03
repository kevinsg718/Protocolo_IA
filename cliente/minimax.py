import numpy as np


def minimax_alphabetha(board, movimientos, depth, a, b, maximizador, data, playerID, direcciones):
    # verificar si ya llegue a la profundidad deseada o ya es un estado final (no movimientos)
    if depth == 0 or movimientos == 0:
        return valor_board(board, data['player_turn_id']), 0  # se analiza el valor con el id del jugador original

    # se va invirtiendo el player ID al del padre, para poder computar los movimientos
    if playerID == 1:
        nuevoPlayerID = 2
    else:
        nuevoPlayerID = 1

    if maximizador:
        mejorMovimiento = ""
        for movimiento, direccion in zip(movimientos, direcciones):
            nuevoBoard = mover(np.array(board), movimiento, playerID, direccion)
            nuevosMovimientos, nuevasDirecciones = obtener_movimientos(nuevoBoard, nuevoPlayerID)
            valor, movimiento_anterior = minimax_alphabetha(nuevoBoard, nuevosMovimientos, depth - 1, a, b, False, data,
                                                            nuevoPlayerID,
                                                            nuevasDirecciones)
            a = max(a, valor)

            mejorMovimiento = movimiento
            if a >= b:
                break

        return a, mejorMovimiento

    else:
        mejorMovimiento = ""
        for movimiento, direccion in zip(movimientos, direcciones):
            nuevoBoard = mover(board, movimiento, playerID, direccion)
            nuevosMovimientos, nuevasDirecciones = obtener_movimientos(nuevoBoard, nuevoPlayerID)
            valor, movimiento_anterior = minimax_alphabetha(nuevoBoard, nuevosMovimientos, depth - 1, a, b, True, data,
                                                            nuevoPlayerID,
                                                            nuevasDirecciones)
            b = min(b, valor)

            mejorMovimiento = movimiento
            if a >= b:
                break

        return b, mejorMovimiento


# aplica una heuristica para evaluar si es una buena movida
def valor_board(board, playerID):
    fichasJugador = 0
    fichasContrario = 0
    for fila in board:
        for posicion in fila:
            if posicion != 0:
                if posicion == playerID:
                    fichasJugador += 1
                else:
                    fichasContrario += 1

    return fichasJugador + fichasContrario


def mover(board, movimiento, playerID, direcciones):
    # aplicar el movimiento seleccionado al board anterior
    columna = movimiento % 8
    fila = int(movimiento / 8)
    board[fila][columna] = playerID

    # por cada direccion en la que se tienen que realizr cambios
    for direccion in direcciones:
        try:
            # 1- DERECHA
            if direccion == 1:
                cambio = columna + 1
                valor = board[fila][cambio]
                while valor != playerID:
                    board[fila][cambio] = playerID
                    cambio += 1
                    valor = board[fila][cambio]

            # 2- IZQUIERDA
            if direccion == 2:
                cambio = columna - 1
                valor = board[fila][cambio]
                while valor != playerID:
                    board[fila][cambio] = playerID
                    cambio -= 1
                    valor = board[fila][cambio]

            # 3- ABAJO
            if direccion == 3:
                cambio = fila + 1
                valor = board[cambio][columna]
                while valor != playerID:
                    board[cambio][columna] = playerID
                    cambio += 1
                    valor = board[cambio][columna]

            # 4- ARRIBA
            if direccion == 4:
                cambio = fila - 1
                valor = board[cambio][columna]
                while valor != playerID:
                    board[cambio][columna] = playerID
                    cambio += 1
                    valor = board[cambio][columna]

            # 5- DIAGONAL 1
            if direccion == 5:
                cambio_fila = fila + 1
                cambio_columna = columna + 1
                valor = board[cambio_fila][cambio_columna]
                while valor != playerID:
                    board[cambio_fila][cambio_columna] = playerID
                    cambio_fila += 1
                    cambio_columna += 1
                    valor = board[cambio_fila][cambio_columna]

            # 6- DIAGONAL 2
            if direccion == 6:
                cambio_fila = fila - 1
                cambio_columna = columna + 1
                valor = board[cambio_fila][cambio_columna]
                while valor != playerID:
                    board[cambio_fila][cambio_columna] = playerID
                    cambio_fila -= 1
                    cambio_columna += 1
                    valor = board[cambio_fila][cambio_columna]

            # 7- DIAGONAL 3
            if direccion == 7:
                cambio_fila = fila + 1
                cambio_columna = columna - 1
                valor = board[cambio_fila][cambio_columna]
                while valor != playerID:
                    board[cambio_fila][cambio_columna] = playerID
                    cambio_fila += 1
                    cambio_columna -= 1
                    valor = board[cambio_fila][cambio_columna]

            # 8- DIAGONAL 4
            if direccion == 7:
                cambio_fila = fila - 1
                cambio_columna = columna - 1
                valor = board[cambio_fila][cambio_columna]
                while valor != playerID:
                    board[cambio_fila][cambio_columna] = playerID
                    cambio_fila -= 1
                    cambio_columna -= 1
                    valor = board[cambio_fila][cambio_columna]

        except IndexError:
            print("Ha ocurrido algo mal.")

    return board


def obtener_movimientos(board, playerID):
    movimientos = []
    direcciones_final = []
    for fila in range(8):
        for columna in range(8):
            direcciones = []
            valido = False
            # TIENE QUE ESTAR VACIA LA POSICION
            if board[fila][columna] != 0:
                continue  # analizar la siguiente posicion

            # 1- PARA DERECHA
            if columna < 7:
                if board[fila][columna + 1] not in [0, playerID]:
                    siguiente_columna = columna + 2
                    while siguiente_columna <= 7:
                        if board[fila][siguiente_columna] == playerID:
                            if not valido:
                                valido = True
                                movimientos.append(fila * 8 + columna)
                            direcciones.append(1)
                            break

                        elif board[fila][siguiente_columna] == 0:
                            break

                        siguiente_columna += 1

            # 2- PARA IZQUIERDA
            if columna > 0:
                if board[fila][columna - 1] not in [0, playerID]:
                    siguiente_columna = columna - 2
                    while siguiente_columna >= 0:
                        if board[fila][siguiente_columna] == playerID:
                            if not valido:
                                valido = True
                                movimientos.append(fila * 8 + columna)
                            direcciones.append(2)
                            break

                        elif board[fila][siguiente_columna] == 0:
                            break

                        siguiente_columna -= 1

            # 3- ABAJO
            if fila < 7:
                if board[fila + 1][columna] not in [0, playerID]:
                    siguiente_fila = fila + 2
                    while siguiente_fila <= 7:
                        if board[siguiente_fila][columna] == playerID:
                            if not valido:
                                valido = True
                                movimientos.append(fila * 8 + columna)
                            direcciones.append(3)
                            break

                        elif board[siguiente_fila][columna] == 0:
                            break

                        siguiente_fila += 1

            # 4- ARRIBA
            if fila > 0:
                if board[fila - 1][columna] not in [0, playerID]:
                    siguiente_fila = fila - 2
                    while siguiente_fila >= 0:
                        if board[siguiente_fila][columna] == playerID:
                            if not valido:
                                valido = True
                                movimientos.append(fila * 8 + columna)
                            direcciones.append(4)
                            break

                        elif board[siguiente_fila][columna] == 0:
                            break

                        siguiente_fila -= 1

            # 5- DIAGONAL DERECHA ABAJO
            if fila < 7 and columna < 7:
                if board[fila + 1][columna + 1] not in [0, playerID]:
                    siguiente_fila = fila + 2
                    siguiente_columna = columna + 2
                    while siguiente_fila <= 7 and siguiente_columna <= 7:
                        if board[siguiente_fila][siguiente_columna] == playerID:
                            if not valido:
                                valido = True
                                movimientos.append(fila * 8 + columna)
                            direcciones.append(5)
                            break

                        elif board[siguiente_fila][siguiente_columna] == 0:
                            break

                        siguiente_fila += 1
                        siguiente_columna += 1

            # 6- DIAGONAL DERECHA ARRIBA
            if fila > 0 and columna < 7:
                if board[fila - 1][columna + 1] not in [0, playerID]:
                    siguiente_fila = fila - 2
                    siguiente_columna = columna + 2
                    while siguiente_fila >= 0 and siguiente_columna <= 7:
                        if board[siguiente_fila][siguiente_columna] == playerID:
                            if not valido:
                                valido = True
                                movimientos.append(fila * 8 + columna)
                            direcciones.append(6)
                            break

                        elif board[siguiente_fila][siguiente_columna] == 0:
                            break

                        siguiente_fila -= 1
                        siguiente_columna += 1

            # 7- DIAGONAL IZQUIERDA ABAJO
            if fila < 7 and columna > 0:
                if board[fila + 1][columna - 1] not in [0, playerID]:
                    siguiente_fila = fila + 2
                    siguiente_columna = columna - 2
                    while siguiente_fila <= 7 and siguiente_columna >= 0:
                        if board[siguiente_fila][siguiente_columna] == playerID:
                            if not valido:
                                valido = True
                                movimientos.append(fila * 8 + columna)
                            direcciones.append(7)
                            break

                        elif board[siguiente_fila][siguiente_columna] == 0:
                            break

                        siguiente_fila += 1
                        siguiente_columna -= 1

            # 8- DIAGONAL IZQUIERDA ARRIBA
            if fila > 0 and columna > 0:
                if board[fila - 1][columna - 1] not in [0, playerID]:
                    siguiente_fila = fila - 2
                    siguiente_columna = columna - 2
                    while siguiente_fila >= 0 and siguiente_columna >= 0:
                        if board[siguiente_fila][siguiente_columna] == playerID:
                            if not valido:
                                valido = True
                                movimientos.append(fila * 8 + columna)
                            direcciones.append(8)
                            break

                        elif board[siguiente_fila][siguiente_columna] == 0:
                            break

                        siguiente_fila -= 1
                        siguiente_columna -= 1
            # guardar las direcciones de los movimientos correctos
            if valido:
                direcciones_final.append(direcciones)

    return movimientos, direcciones_final
