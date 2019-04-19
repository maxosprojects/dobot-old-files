var dobotClient = require('./DobotJsClient');

var dobotAjax = {
  connect:function(req){
      dobotClient.init(req.body.addr, req.body.port);
      dobotClient.start();
      console.log("connect");
  },
  disconnect:function(){
      dobotClient.api.disconnectDobot();
      console.log("disconnect");
  },
  reset:function(){
      dobotClient.api.resetDobot();
      console.log("reset");
  },
  setCmdTimeout:function(){
  	  dobotClient.api.setCmdTimeout(3000);
      console.log("setCmdTimeout");
  },
  setEndType:function(req){
  	  dobotClient.api.setEndType(req.body.value);
      console.log("setEndType");
  },
  setInitialPose:function(req){
  	  var initialPose = {
  	  	joint2Angle:req.body.joint2Angle,
  	  	joint3Angle:req.body.joint3Angle
  	  };
  	  dobotClient.api.setInitialPose(initialPose);
      console.log("initialPose");
  },
  setJogStaticParams:function(req){
  	  var jogStaticParams = {
  	  	jointMaxVelocity:200,
  	  	jointMaxAcceleration:200,
  	  	servoMaxVelocity:200,
  	  	servoMaxAcceleration:200,
  	  	linearMaxVelocity:200,
  	  	linearMaxAcceleration:200
  	  };
  	  dobotClient.api.setJogStaticParams(jogStaticParams);
      console.log("setJogStaticParams");
  },
  setJogDynamicParams:function(req){
  	  var jogDynamicParams = {
  	  	velocityRatio:req.body.velocityRatio
  	  };
  	  dobotClient.api.setJogDynamicParams(jogDynamicParams);
      console.log("setJogDynamicParams");
  },
  setJogInstantCmd:function(req){
  	  var jogInstantCmd = {
  	  	isJoint:req.body.isJoint,
  	  	cmd:req.body.cmd
  	  };
  	  dobotClient.api.setJogInstantCmd(jogInstantCmd);
      console.log("setJogInstantCmd");
  },
  setPlaybackStaticParams:function(req){
  	  var playbackStaticParams = {
  	  	jointMaxVelocity:200,
  	  	jointMaxAcceleration:200,
  	  	servoMaxVelocity:200,
  	  	servoMaxAcceleration:200,
  	  	linearMaxVelocity:200,
  	  	linearMaxAcceleration:200,
  	  	pauseTime:1,
  	  	jumpHeight:40
  	  };
  	  dobotClient.api.setPlaybackStaticParams(playbackStaticParams);
      console.log("setPlaybackStaticParams");
  },
  setPlaybackDynamicParams:function(req){
  	  var playbackDynamicParams = {
  	  	velocityRatio:req.body.velocityRatio,
  	  	accelerationRatio:req.body.accelerationRatio
  	  };
  	  dobotClient.api.setPlaybackDynamicParams(playbackDynamicParams);
      console.log("setPlaybackDynamicParams");
  },
  setPlaybackBufferCmd:function(req){
  	  var playbackBufferCmd = {
  		  playbackPoint:{
  			motionStyle:req.body.motionStyle,
  			isGrab:req.body.isGrab,
  			x:req.body.x,
  			y:req.body.y,
  			z:req.body.z,
  			rHead:req.body.rHead,
  			gripper:req.body.gripper,
  			pauseTime:req.body.pauseTime
  		}
  	  };
  	  dobotClient.api.setPlaybackBufferCmd(playbackBufferCmd);
      console.log("setPlaybackBufferCmd");
  },
  getPose:function(req, res){
  	var pose = dobotClient.api.currentPose;
  	res.json(pose);
  },
  processCmd:function(req, res){
      switch(req.body.type)
      {
        case 'connect':
          this.connect(req);
          break;
        case 'disconnect':
          this.disconnect();
        break;
        case 'reset':
          this.reset();
        break;
        case 'setCmdTimeout':
          this.setCmdTimeout();
        break;
        case 'setEndType':
          this.setEndType(req);
        break;
        case 'setInitialPose':
          this.setInitialPose(req);
        break;
        case 'setJogStaticParams':
          this.setJogStaticParams(req);
        break;
        case 'setJogDynamicParams':
          this.setJogDynamicParams(req);
        break;
        case 'setJogInstantCmd':
        	this.setJogInstantCmd(req);
        	break;
        case 'setPlaybackStaticParams':
          this.setPlaybackStaticParams(req);
        break;
        case 'setPlaybackDynamicParams':
          this.setPlaybackDynamicParams(req);
        break;
        case 'setPlaybackBufferCmd':
          this.setPlaybackBufferCmd(req);
        break;
        case 'getPose':
          this.getPose(req, res);
        break;
        default:
        break;
    }
    if(req.body.type != 'getPose'){
     	res.send('Control Success!'); 
 	}
  }
}

module.exports = dobotAjax;