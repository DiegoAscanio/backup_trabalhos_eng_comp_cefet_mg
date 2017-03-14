var land;

var posX;
var posY;

var myId = 0;
var ameba;
var player;
var amebasList;

var ready = false;
var eurecaServer;


Ameba = function (index, game, player, x, y) {
	this.cursor = {
		mover: false
	};
	this.input = {
		mover: false
	};
	var x = x;
	var y = y;
	this.time = 0;
	this.mass = 100;

	this.game = game;
	this.player = player;
	this.currentSpeed = 0;
	this.alive = true;

    this.lastUpdate = 0;

	this.ameba = game.add.sprite(x, y, 'ameba');
	this.ameba.anchor.set(0.5);
	this.ameba.id = index;

	game.physics.enable(this.ameba, Phaser.Physics.ARCADE);
	this.ameba.body.immovable = false;
	this.ameba.body.collideWorldBounds = true;
}

Ameba.prototype.alimentar = function () {
}

Ameba.prototype.velocidade = function () {
	/*
		Para quando a funcionalidade de alimentar estiver pronta
	*/
	// return 600 * Math.exp(-0.001*this.mass) + 200;
	return 100*Math.sin(this.time) + 100;
}

Ameba.prototype.kill = function () {
	this.alive = false;
	this.ameba.kill();
}

Ameba.prototype.update = function () {
	/*for (i in amebasList) {
		if (this != amebasList[i]) {
			game.physics.arcade.collide(this.ameba, amebasList[i].ameba);
		}
	}*/
	/*
	basicamente realiza os movimentos para cada player
	*/
	//inputChanged = (this.cursor.mover != this.input.mover);
	if (Date.now() - this.lastUpdate > 50) {
        this.lastUpdate = Date.now();
		/* gerencia a mudança dos inputs aqui
		   enviando novos valores ao servidor */
		if (this.ameba.id == myId) { // sou Eu!
			this.input.x = this.ameba.x;
            this.input.y = this.ameba.y;
			eurecaServer.handlePlayersState(this.input);
		}
	}

	if (this.cursor.mover) {
		game.physics.arcade.moveToXY(this.ameba, this.cursor.toX, this.cursor.toY, this.velocidade());
	}
	else {
		this.ameba.body.velocity.setTo(0, 0);
	}
}

function preload() {
	game.load.image('ameba', 'assets/sprites/shinyball.png');
	game.load.image('piso', 'assets/textures/metal.png');
}

function create(position) {
	// configuracoes do ambiente
	// delimita o tamanho do mundo para um quadrado de 1000px x 1000px
	game.world.setBounds(0, 0, 1000, 1000);
	game.stage.disableVisibilityChange = true;

	land = game.add.tileSprite(0, 0, 1000, 1000, 'piso');
	//land.fixedToCamera = false;

	// configuracoes do jogador
	amebasList = {};

	player = new Ameba(myId, game, ameba, position.x, position.y);

	amebasList[myId] = player;
	ameba = player.ameba;
	ameba.x = position.x;
	ameba.y = position.y;

	game.camera.follow(ameba);
	//game.camera.deadzone = new Phaser.Rectangle(150, 150, 500, 300);
	game.camera.focusOnXY(0, 0);

}

function eurecaClientSetup() {
	// cria uma instancia do cliente eureca.io
	var eurecaClient = new Eureca.Client();

	eurecaClient.ready(function (proxy) {
		eurecaServer = proxy;
	});

	// metodos definidos sob o namespace exports tornam-se chamáveis para o servidor

	// setPlayer - exec. pelo serv. para definir o jogador (id) e sua posicao
	eurecaClient.exports.setId = function(id, position) {
		// create é executado aqui para ter-se certeza de que nada é criado antes que o id seja assinalado ao jogador
		myId = id;
        console.log(position);
		create(position);
		eurecaServer.handshake();
		ready = true;
	}

	// kill - exec. pelo serv. para matar algum jogador
	eurecaClient.exports.kill = function(id) {
		if (amebasList[id]) {
			amebasList[id].kill();
			console.log('Killing ', id, amebasList[id]);
			delete(amebasList[id]);
		}
	}

	// spawnEnemy - exec. pelo serv. para adicionar novos jogadores à partida
	eurecaClient.exports.spawnEnemy = function(id, position) {
		if (id == myId) { // sou eu
			return;
		}
		console.log('SPAWN');
        console.log(position);
		if (amebasList[id] == null) {
			var amb = new Ameba (id, game, ameba, position.x, position.y);
			amebasList[id] = amb;
		}
	}

	// updateState - exec. pelo serv para mover outros jogadores
	eurecaClient.exports.updateState = function(id, state) {
        if(myId == id){
            amebasList[id].cursor = state;
            amebasList[id].update();
        }
		else if (amebasList[id]) {
			amebasList[id].cursor = state;
			amebasList[id].ameba.x = state.x;
			amebasList[id].ameba.y = state.y;
			//amebasList[id].x = state.nextPosition.x;
			//amebasList[id].y = state.nextPosition.y;
			amebasList[id].update();
		}
	}
}

function update () {
	if (!ready) {
		return;
	}
	player.input.mover = game.input.mousePointer.isDown;
	if (player.input.mover) {
		player.input.toX = game.input.mousePointer.x + game.camera.x;
		player.input.toY = game.input.mousePointer.y + game.camera.y;
	}

	//land.tilePosition.x = -game.camera.x;
	//land.tilePosition.y = -game.camera.y;

	for (var i in amebasList) {
		if (!amebasList[i]) {
			continue;
		}
		if (amebasList[i].alive) {
			amebasList[i].update();
		}
	}
}

var game = new Phaser.Game(800, 600, Phaser.AUTO, 'ascan.io', { preload: preload, create: eurecaClientSetup, update: update});
