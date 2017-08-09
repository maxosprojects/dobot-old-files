var dobotCmd = {
    CONNECTDOBOT : 0,
    DISCONNECTDOBOT : 1,
    RESETDOBOT : 2,
    PERIODICTACK : 3,
    SETCMDTIMEOUT : 4,

    SETENDTYPE : 5,
    SETINITIALPOSE : 6,
    GETPOSE : 7,

    SETJOGSTATICPARAMS : 8,
    SETJOGDYNAMICPARAMS : 9,
    SETJOGINSTANTCMD : 10,

    SETPLAYBACKSTATICPARAMS : 11,
    SETPLAYBACKDYNAMICPARAMS : 12,
    SETPLAYBACKBUFFERCMD : 13
}

var dobotApi = {
	currentPose:{
		x:0,
		y:0,
		z:0,
		rHead:0,
		jointAngle:[0.0, 0.0, 0.0, 0.0],
		isGrab:false,
		gripper:0,
		dobotConnectStatus:false
	},
    connectDobot: function () {
        var buf = new Buffer(44, 'hex');
        buf.writeInt32LE(dobotCmd.CONNECTDOBOT, 0);
        dobotClient.send(buf);
	},
	disconnectDobot:function(){
		this.periodicTask(0);
		this.getPose(0);
	    var buf = new Buffer(44, 'hex');
	    buf.writeInt32LE(dobotCmd.DISCONNECTDOBOT, 0);
	    dobotClient.send(buf);
	},
	resetDobot:function(){
	    var buf = new Buffer(44, 'hex');
	    buf.writeInt32LE(dobotCmd.RESETDOBOT, 0);
	    dobotClient.send(buf);
	},
	periodicTask:function(interval){
		// The client must call this function periodic when interval is zero. otherwise(is not zero), the server will run it periodic
	    var buf = new Buffer(44, 'hex');
	    buf.writeInt32LE(dobotCmd.PERIODICTACK, 0);
	    buf.writeInt32LE(interval, 4);
	    dobotClient.send(buf);
	},
	setCmdTimeout:function(cmdTimeout){
	    var buf = new Buffer(44, 'hex');
	    buf.writeInt32LE(dobotCmd.SETCMDTIMEOUT, 0);
	    buf.writeInt32LE(cmdTimeout, 4);
	    dobotClient.send(buf);
	},
	setEndType:function(endType){
	    var buf = new Buffer(44, 'hex');
	    buf.writeInt32LE(dobotCmd.SETENDTYPE, 0);
	    buf.writeInt32LE(endType, 4);
	    dobotClient.send(buf);
	},
	setInitialPose:function(initialPose){
	    var buf = new Buffer(44, 'hex');
	    buf.writeInt32LE(dobotCmd.SETINITIALPOSE, 0);
	    buf.writeFloatLE(initialPose.joint2Angle, 4);
	    buf.writeFloatLE(initialPose.joint3Angle, 8);
	    dobotClient.send(buf);
	},
	getPose:function(interval){ 
		// The client must call this function periodic when interval is zero. otherwise(is not zero), the server will run it periodic
	    var buf = new Buffer(44, 'hex');
	    buf.writeInt32LE(dobotCmd.GETPOSE, 0);
	    buf.writeInt32LE(interval, 4);
	    dobotClient.send(buf);
	},
	setJogStaticParams:function(jogStaticParams){
	    var buf = new Buffer(44, 'hex');
	    var i = 0;
	    buf.writeInt32LE(dobotCmd.SETJOGSTATICPARAMS, i);
	    i += 4;
	    buf.writeFloatLE(jogStaticParams.jointMaxVelocity, i);
	    i += 4;
	    buf.writeFloatLE(jogStaticParams.jointMaxAcceleration, i);
	    i += 4;
	    buf.writeFloatLE(jogStaticParams.servoMaxVelocity, i);
	    i += 4;
	    buf.writeFloatLE(jogStaticParams.servoMaxAcceleration, i);
	    i += 4;
	    buf.writeFloatLE(jogStaticParams.linearMaxVelocity, i);
	    i += 4;
	    buf.writeFloatLE(jogStaticParams.linearMaxAcceleration, i);
	    dobotClient.send(buf);
	},
	setJogDynamicParams:function(jogDynamicParams){
	    var buf = new Buffer(44, 'hex');
	    buf.writeInt32LE(dobotCmd.SETJOGDYNAMICPARAMS, 0);
	    buf.writeFloatLE(jogDynamicParams.velocityRatio, 4);
	    dobotClient.send(buf);
	},
	setJogInstantCmd :function(jogInstantCmd){
	    var buf = new Buffer(44, 'hex');
	    buf.writeInt32LE(dobotCmd.SETJOGINSTANTCMD, 0);
	    buf.writeUInt8(jogInstantCmd.isJoint, 4);
	    buf.writeInt32LE(jogInstantCmd.cmd, 5);
	    dobotClient.send(buf);
	},
	setPlaybackStaticParams:function(playbackStaticParams){
	    var buf = new Buffer(44, 'hex');
	    var i = 0;
	    buf.writeInt32LE(dobotCmd.SETPLAYBACKSTATICPARAMS, i);
	    i += 4;
	    buf.writeFloatLE(playbackStaticParams.jointMaxVelocity, i);
	    i += 4;
	    buf.writeFloatLE(playbackStaticParams.jointMaxAcceleration, i);
	    i += 4;
	    buf.writeFloatLE(playbackStaticParams.servoMaxVelocity, i);
	    i += 4;
	    buf.writeFloatLE(playbackStaticParams.servoMaxAcceleration, i);
	    i += 4;
	    buf.writeFloatLE(playbackStaticParams.linearMaxVelocity, i);
	    i += 4;
	    buf.writeFloatLE(playbackStaticParams.linearMaxAcceleration, i);
	    i += 4;
	    buf.writeFloatLE(playbackStaticParams.pauseTime, i);
	    i += 4;
	    buf.writeFloatLE(playbackStaticParams.jumpHeight, i);
	    dobotClient.send(buf);
	},
	setPlaybackDynamicParams:function(playbackDynamicParams){
	    var buf = new Buffer(44, 'hex');
	    buf.writeInt32LE(dobotCmd.SETPLAYBACKDYNAMICPARAMS, 0);
	    buf.writeFloatLE(playbackDynamicParams.velocityRatio, 4);
	    buf.writeFloatLE(playbackDynamicParams.accelerationRatio, 8);
	    dobotClient.send(buf);
	},
	setPlaybackBufferCmd:function(playbackBufferCmd){
	    var buf = new Buffer(44, 'hex');
	    buf.writeInt32LE(dobotCmd.SETPLAYBACKBUFFERCMD, 0);
	    buf.writeUInt8(playbackBufferCmd.playbackPoint.motionStyle, 4);
	    buf.writeUInt8(playbackBufferCmd.playbackPoint.isGrab, 5);
	    buf.writeFloatLE(playbackBufferCmd.playbackPoint.x, 6);
	    buf.writeFloatLE(playbackBufferCmd.playbackPoint.y, 10);
	    buf.writeFloatLE(playbackBufferCmd.playbackPoint.z, 14);
	    buf.writeFloatLE(playbackBufferCmd.playbackPoint.rHead, 18);
	    buf.writeFloatLE(playbackBufferCmd.playbackPoint.gripper, 22);
	    buf.writeFloatLE(playbackBufferCmd.playbackPoint.pauseTime, 26);
	    dobotClient.send(buf);
	},
	processCmd: function (buf) {
	    var cmd = buf.readInt32LE();
	    switch(cmd){
	        case dobotCmd.CONNECTDOBOT:
	            dobotClient.dobotConnectStatus = buf.readInt32LE(4);
	            console.log('CONNECTDOBOT: ' + dobotClient.dobotConnectStatus);
	            break;
	        case dobotCmd.GETPOSE:
	        	this.currentPose.x = buf.readFloatLE(4);
	        	this.currentPose.y = buf.readFloatLE(8);
	        	this.currentPose.z = buf.readFloatLE(12);
	        	this.currentPose.rHead = buf.readFloatLE(16);
	        	this.currentPose.jointAngle[0] = buf.readFloatLE(20);
	        	this.currentPose.jointAngle[1] = buf.readFloatLE(24);
	        	this.currentPose.jointAngle[2] = buf.readFloatLE(28);
	        	this.currentPose.jointAngle[3] = buf.readFloatLE(32);
	        	this.currentPose.isGrab = buf.readUInt8(36);
	        	this.currentPose.gripper = buf.readFloatLE(37);
	        	this.currentPose.dobotConnectStatus = dobotClient.dobotConnectStatus;
	            break;
	        default:
	            break;
	    }
	}
}

var dobotClient = {
	net : null,
	host : "127.0.0.1",
	port : 8888,
	client: null,
	socketConnectStatus:false,
    dobotConnectStatus: 0,
    api:dobotApi,
	init:function(host, port){
		this.host = host;
		this.port = port;
		this.net = require('net');
		this.client = new this.net.Socket();

		this.onEvent();
	},
	connect:function(){
		var $this = this;
		this.client.connect(this.port, this.host, function() {
		    $this.socketConnectStatus = true;
	        console.log("CONNECTED TO: " + $this.host + ":" + $this.port);
	        // Set interval > 0 and Server will run periodic task.
	        $this.api.periodicTask(400);
	        $this.api.getPose(500);
	        $this.api.connectDobot();
		});
	},
	onEvent:function(){
		var $this = this;
		this.client.on('data', function(data) {
	    	$this.api.processCmd(data);
		});
		this.client.on('close', function() {
			$this .dobotConnectStatus  = false;
	    	console.log('Connection closed');
		});
		this.client.on('error', function (e) {
			$this .dobotConnectStatus  = false;
		    console.log('Error happend '+ e);
		});

	},
	send:function(data){
	    this.client.write(data);
	},
	start:function(){// Start connection
		var $this = this;
		/* Had move to connect function;
	    setInterval(function () {
	        $this.api.periodicTask(0);
	    }, 400);

	    setInterval(function () {
	        $this.api.getPose(0);
	    }, 600);
		*/
	    this.connect();
	}
}
module.exports = dobotClient;

//dobotClient.init("127.0.0.1", 8881);
//dobotClient.start();