var express = require('express'),
    app = express(app),
    server = require('http').createServer(app);

app.use(express.static(__dirname));

var Eureca = require('eureca.io');
var eurecaServer = new Eureca.Server({allow: ['setId', 'spawnEnemy', 'kill', 'updateState']});
var clients = {};

var coord = 100;

eurecaServer.attach(server); // acopla eureca.io no servidor http

// detecta conexao do cliente
eurecaServer.onConnect(function (conn) {
	console.log('New Client id=%s ', conn.id, conn.remoteAddress);

	// o metodo getClient disponibiliza um proxy que nos permite chamar procedimentos remotos nos clientes
	var remote = eurecaServer.getClient(conn.id);

	// posicao do cliente
	currentPosition = {x: coord, y: coord};
	coord += 100;

	// registra o cliente
	clients[conn.id] = {id:conn.id, remote:remote};

	console.log(clients);


	// aqui chamamos o metodo setId do cliente
	remote.setId(conn.id, currentPosition);
});

// detecta disconexao do cliente
eurecaServer.onDisconnect(function (conn) {
    console.log('Client disconnected', conn.id);

	var removeId = clients[conn.id].id;

	delete clients[conn.id];

	for (var c in clients) {
		var remote = clients[c].remote;
		// aqui chamamos o metodo kill definido nos clientes para matar o cliente recem desconectado
		remote.kill(conn.id);
	}
    coord -= 100;
});

// metodo handshake para spawnar os jogadores
eurecaServer.exports.handshake = function() {
	//var conn = this.connection;
	for (var c in clients) {
		var remote = clients[c].remote;
		for (var cc in clients) {
			// envia a ultima posicao conhecida
			var position = clients[cc].laststate ? {x:clients[cc].laststate.x, y:clients[cc].laststate.y} : {x:0, y:0};
			remote.spawnEnemy(clients[cc].id, position);
		}
	}
}

// metodo para processar as inputs dos jogadores
eurecaServer.exports.handlePlayersState = function(state) {
	var conn = this.connection;
	var updateClient = clients[conn.id];

	for (var c in clients) {
		var remote = clients[c].remote;
		remote.updateState(updateClient.id, state);

		// mantem ultimo estado conhecido para enviarmos aos novos clientes conectados
		clients[c].laststate = state;
	}
}

server.listen(8000);
