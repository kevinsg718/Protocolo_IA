import socketio
import math, random
import numpy as np

sio = socketio.Client()
userName = "k" + str(random.randint(1, 1000))
tournamentID = 12


# ¿que hacer cuando se conecta?
@sio.on('connect')
def on_connect():
    print("Usuario conectado")
    sio.emit('signin', {
        "user_name": userName,
        "tournament_id": tournamentID,
        "user_role": "player"
    })


# ¿que hacer cuando el servidor nos indica que estamos listos?
# aqui es donde se juega
@sio.on('ready')
def on_ready(data):
    movement = play(data)  # computar la mejor movida que se pueda realiaar

    # enviar movimiento a servidor
    sio.emit('play',
             {
                 "player_turn_id": data['player_turn_id'],
                 "tournament_id": tournamentID,
                 "game_id": data['game_id'],
                 "movement": movement
             })


# cuando se ha terminado una partida se debe indicar al servidor que estamos listos
@sio.on('finish')
def on_finish(data):
    print("Se ha terminado el juego")
    try:
        ganador = data["winner_turn_id"]
        if ganador == data['player_turn_id']:
            print("Se ha terminado el juego: GANE YO")
        else:
            print("Se ha terminado el juego: PERDI YO :(")

    except KeyError:
        print("CREO QUE QUEDAMOS EMPATE! ES PEOR QUE PERDER")

    sio.emit('player_ready', {
        "tournament_id": tournamentID,
        "game_id": data['game_id'],
        "player_turn_id": data['player_turn_id']
    })


# FUNCIONES IMPORTANTES
# sirve para imprimir el tablero
def to_string_board(board):
    tipo_ficha = ['_', 'X', 'O']
    result = '    A  B  C  D  E  F  G  H'
    for i in range(len(board)):
        if i % 8 == 0:
            result += '\n\n ' + str(int(math.floor(i / 8)) + 1) + ' '
        result += ' ' + tipo_ficha[board[i]] + ' '
    return result


# aqui se realizara el procesamiento de lo que se puede realizar
def play(data):
    # mostrar informacion
    board = data['board']
    print(to_string_board(board))

    # transformar el tablero para poder utilizar columnas y filas1
    board = np.array(board).reshape((8, 8))
    playerID = data['player_turn_id']

    # PASO 1: obtener las posibles movidas
    movimientos = []
    valido = False
    for fila in range(8):
        for columna in range(8):
            valido = False
            # TIENE QUE ESTAR VACIA LA POSICION
            if board[fila][columna] != 0:
                continue  # analizar la siguiente posicion

            # PARA DERECHA
            if columna < 7:
                if board[fila][columna + 1] not in [0, playerID]:
                    siguiente_columna = columna + 2
                    while siguiente_columna <= 7:
                        if board[fila][siguiente_columna] == playerID:
                            movimientos.append(fila * 8 + columna)
                            valido = True
                            break

                        elif board[fila][siguiente_columna] == 0:
                            break

                        siguiente_columna += 1

            if valido:
                continue  # detener si ya se verifico que es valido

            # PARA IZQUIERDA
            if columna > 0:
                if board[fila][columna - 1] not in [0, playerID]:
                    siguiente_columna = columna - 2
                    while siguiente_columna >= 0:
                        if board[fila][siguiente_columna] == playerID:
                            movimientos.append(fila * 8 + columna)
                            valido = True
                            break

                        elif board[fila][siguiente_columna] == 0:
                            break

                        siguiente_columna -= 1
            if valido:
                continue  # detener si ya se verifico que es valido

            # ABAJO
            if fila < 7:
                if board[fila + 1][columna] not in [0, playerID]:
                    siguiente_fila = fila + 2
                    while siguiente_fila <= 7:
                        if board[siguiente_fila][columna] == playerID:
                            movimientos.append(fila * 8 + columna)
                            valido = True
                            break

                        elif board[siguiente_fila][columna] == 0:
                            break

                        siguiente_fila += 1
            if valido:
                continue  # detener si ya se verifico que es valido

            # ARRIBA
            if fila > 0:
                if board[fila - 1][columna] not in [0, playerID]:
                    siguiente_fila = fila - 2
                    while siguiente_fila >= 0:
                        if board[siguiente_fila][columna] == playerID:
                            movimientos.append(fila * 8 + columna)
                            valido = True
                            break

                        elif board[siguiente_fila][columna] == 0:
                            break

                        siguiente_fila -= 1
            if valido:
                continue  # detener si ya se verifico que es valido

            # DIAGONAL DERECHA ABAJO
            if fila < 7 and columna < 7:
                if board[fila + 1][columna + 1] not in [0, playerID]:
                    siguiente_fila = fila + 2
                    siguiente_columna = columna + 2
                    while siguiente_fila <= 7 and siguiente_columna <= 7:
                        if board[siguiente_fila][siguiente_columna] == playerID:
                            movimientos.append(fila * 8 + columna)
                            valido = True
                            break

                        elif board[siguiente_fila][siguiente_columna] == 0:
                            break

                        siguiente_fila += 1
                        siguiente_columna += 1
            if valido:
                continue  # detener si ya se verifico que es valido

            # 3.2) DIAGONAL DERECHA ARRIBA
            if fila > 0 and columna < 7:
                if board[fila - 1][columna + 1] not in [0, playerID]:
                    siguiente_fila = fila - 2
                    siguiente_columna = columna + 2
                    while siguiente_fila >= 0 and siguiente_columna <= 7:
                        if board[siguiente_fila][siguiente_columna] == playerID:
                            movimientos.append(fila * 8 + columna)
                            valido = True
                            break

                        elif board[siguiente_fila][siguiente_columna] == 0:
                            break

                        siguiente_fila -= 1
                        siguiente_columna += 1
            if valido:
                continue  # detener si ya se verifico que es valido

            # DIAGONAL IZQUIERDA ABAJO
            if fila < 7 and columna > 0:
                if board[fila + 1][columna - 1] not in [0, playerID]:
                    siguiente_fila = fila + 2
                    siguiente_columna = columna - 2
                    while siguiente_fila <= 7 and siguiente_columna >= 0:
                        if board[siguiente_fila][siguiente_columna] == playerID:
                            movimientos.append(fila * 8 + columna)
                            valido = True
                            break

                        elif board[siguiente_fila][siguiente_columna] == 0:
                            break

                        siguiente_fila += 1
                        siguiente_columna -= 1
            if valido:
                continue  # detener si ya se verifico que es valido

            # DIAGONAL IZQUIERDA ARRIBA
            if fila > 0 and columna > 0:
                if board[fila - 1][columna - 1] not in [0, playerID]:
                    siguiente_fila = fila - 2
                    siguiente_columna = columna - 2
                    while siguiente_fila >= 0 and siguiente_columna >= 0:
                        if board[siguiente_fila][siguiente_columna] == playerID:
                            movimientos.append(fila * 8 + columna)
                            valido = True
                            break

                        elif board[siguiente_fila][siguiente_columna] == 0:
                            break

                        siguiente_fila -= 1
                        siguiente_columna -= 1

    # PASO 2: ANALIZAR LOS POSIBLES MOVIMIENTOS Y ESCOGER EL MEJOR
    movimiento = random.choice(movimientos)
    # imprimir los movimientos
    posibles = ""
    for mov in movimientos:
        posibles += numero_letras(mov) + " "

    print("Los posibles movimientos son: ", posibles)

    print("Mi movimiento es: ", numero_letras(movimiento), "\n\n")
    return movimiento


def numero_letras(movimiento):
    fila = int(movimiento / 8) + 1
    columna = "ABCDEFGH"[movimiento % 8]
    return str(fila) + str(columna)


sio.connect("http://localhost:4000")
sio.wait()
