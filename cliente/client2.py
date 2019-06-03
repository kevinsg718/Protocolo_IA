import socketio
import math, random
import numpy as np
import minimax

sio = socketio.Client()
userName = str(input("Ingrese nombre: "))
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

    ####################################################################################################################
    # PASO 1: obtener las posiblesMovimientos movidas
    movimientos, direcciones = minimax.obtener_movimientos(board, playerID)

    # imprimir los movimientos encontrados
    posiblesMovimientos = ""
    for mov in movimientos:
        posiblesMovimientos += numero_letras(mov) + " "
    print("Los posibles movimientos son: ", posiblesMovimientos)

    ####################################################################################################################
    # PASO 2: ANALIZAR LOS POSIBLES MOVIMIENTOS Y ESCOGER EL MEJOR
    # movimiento = random.choice(movimientos)
    valor, mejorMovimiento = minimax.minimax_alphabetha(board=board, movimientos=movimientos, depth=3, a=-math.inf,
                                                        b=math.inf,
                                                        maximizador=True, data=data,
                                                        direcciones=direcciones, playerID=playerID)
    print("Mi movimiento es: ", numero_letras(mejorMovimiento), "\n\n")
    return mejorMovimiento


def numero_letras(movimiento):
    fila = int(movimiento / 8) + 1
    columna = "ABCDEFGH"[movimiento % 8]
    return str(fila) + str(columna)


sio.connect("http://localhost:4000")
sio.wait()
