import socketio
import math

# main socket
sio = socketio.Client()
userName = input("add username:  ")
tournamentId = int(input("tournament id:  "))


# sirve para imprimir el tablero
def human_board(board):
    tileRep = ['_', 'X', 'O']
    N = 8
    result = '    A  B  C  D  E  F  G  H'
    for i in range(len(board)):
        if i % N == 0:
            result += '\n\n ' + str(int(math.floor(i / N)) + 1) + ' '
        result += ' ' + tileRep[board[i]] + ' '
    return result


# sirve para verificar que la posicion seleccionada sea valida
def validateHumanPosition(position):
    if len(position) == 2:
        print("validated")
        row = int(position[0])
        col = str(position[1].lower())
        alph = 'abcdefgh'
        return (1 <= row <= 8) and (col in alph)
    else:
        print("unvalidated")
        return


# sirve para convertir una tupla 'letra, numero' a solo numero
def ix(row, col):
    index = 'abcdefgh'.index(col)
    val = (int(row) - 1) * 8 + index
    return val


# funcion para seleccionar el movimiento a utilizar
def play():
    move = input("Ingrese su movimiento")
    return move


# ¿que hacer cuando se conecta?
@sio.on('connect')
def on_connect():
    print("Usuario conectado")
    sio.emit('signin', {
        "user_name": userName,
        "tournament_id": tournamentId,
        "user_role": "player"
    })


# ¿que hacer cuando el servidor nos indica que estamos listos?
# aqui es donde se juega
@sio.on('ready')
def on_ready(data):
    movement = "z1"

    # repetir ciclo hasta que se tenga un movimiento valido
    while not validateHumanPosition(movement):
        movement = play()

    # enviar movimiento a servidor
    sio.emit('play',
             {
                 "player_turn_id": data['player_turn_id'],
                 "tournament_id": tournamentId,
                 "game_id": data['game_id'],
                 "movement": ix(movement[0], movement[1])
             })


# cuando se ha terminado una partida se debe indicar al servidor que estamos listos
@sio.on('finish')
def on_finish(data):
    print("Se ha terminado el juego")
    sio.emit('player_ready', {
        "tournament_id": tournamentId,
        "game_id": data['game_id'],
        "player_turn_id": data['player_turn_id']
    })


sio.connect("http://localhost:4000")
