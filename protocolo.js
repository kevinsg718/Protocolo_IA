
//sign in 
var socket = require('socket.io-client')(URL);  // for example: http://127.0.0.1:3000
socket.on('connect', function(){});



// registro de jugador
//params
//user_name: string, fully qualified javascript id for your username (ie. no spaces, starting with letter, etc.)
//tournament_id: int, positive integer to the League you are connecting with.
//user_role: string, send "player".

socket.on('connect', function(){
  socket.emit('signin', {
    user_name: "Kevinsg",
    tournament_id: 15803,
    user_role: 'player'
  });
});

//ok de sign in es enviada si el sign in esta bien
socket.on('ok_signin', function(){
  console.log("Successfully signed in!");
});

//ok ready esta es enviada cuando el coordinador da el ok de realizar la jugada
//params
//game_id: int, integer representing the id of the game playing.
//player_turn_id: int, 1 for player 1, 2 for player 2.
//board: [int], 1D array of integers, containing the board representation.
socket.on('ready', function(data){
  var gameID = data.game_id;
  var playerTurnID = data.player_turn_id;
  var board = data.board;
});

//ok de finish es enviada cuando el coordinador indica que termino el juego

socket.on('finish', function(data){
  var gameID = data.game_id;
  var playerTurnID = data.player_turn_id;
  var winnerTurnID = data.winner_turn_id;
  var board = data.board;
});


//resetear Emitir dos senales

//senal de play
//params
//tournament_id: int, positive integer to the League you are connecting with.
//player_turn_id: int, 1 for player 1, 2 for player 2, but you can simply echo what you received from the ready signal.
//game_id: int, integer representing the id of the game playing.
//movement: ?, any type representing the movement of the specific game you are playing. For instance, othello only needs an integer representing the tile clicked.
//senal de ready para jugar el turno
socket.on('ready', function(data){
  var gameID = data.game_id;
  var playerTurnID = data.player_turn_id;
  var board = data.board;
  
  // TODO: Your logic / user input here
  
  socket.emit('play', {
    tournament_id: tournamentID,
    player_turn_id: playerTurnID,
    game_id: gameID,
    movement: ?
  });
});

//senal jugador listo
//despues de haber terminado se debe resetear la disponibilidad del jugador permite a tu coordinador 
//hacer match con otro jugador

socket.on('finish', function(data){
  var gameID = data.game_id;
  var playerTurnID = data.player_turn_id;
  var winnerTurnID = data.winner_turn_id;
  var board = data.board;
  
  // TODO: Your cleaning board logic here
  
  socket.emit('player_ready', {
    tournament_id: tournamentID,
    player_turn_id: playerTurnID,
    game_id: gameID
  });
});


