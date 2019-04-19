function grabClick() {
	if(document.getElementById("Grab").checked)
	{
		dobotUI.setJogInstantCmd(9, 1);
	}
	else
	{
		dobotUI.setJogInstantCmd(10, 1);
	}
}

function laserClick() {
	if(document.getElementById("Laser").checked)
	{
		dobotUI.setJogInstantCmd(13, 1);
	}
	else
	{
		dobotUI.setJogInstantCmd(14, 1);
	}
}
function endTypeSelectFun(){
	var V = $("#endTypeSelect").val();
	if(V == 0)
	{
		$("#Grab").attr("disabled", false);
		$("#Laser").attr("disabled", true);
		$("button[name='btnGrp']").attr("disabled", true);
	}
	else if(V == 1)
	{
		$("#Grab").attr("disabled", true);
		$("#Laser").attr("disabled", false);
		$("button[name='btnGrp']").attr("disabled", true);
	}
	else if(V == 2)
	{
		$("#Grab").attr("disabled", true);
		$("#Laser").attr("disabled", true);
		$("button[name='btnGrp']").attr("disabled", false);
	}
	dobotUI.setEndType();
}

var dobotUI = {
	index:0,
	url:"http://" + location.host + "/ps_post",
	connect:function(){
		var addr = $("#addr").val(), port = $("#port").val();
		var param = {type:"connect", addr: addr,  port, port};
		$.post(this.url, param, function(data){
 			$("#tip").html(data);
		}, "text");
	},
	disconnect:function(){
		var param = {type:"disconnect"};
		$.post(this.url, param, function(data){
 			$("#tip").html(data);
		}, "text");
	},
	reset:function(){
		var param = {type:"reset"};
		$.post(this.url, param, function(data){
 			$("#tip").html(data);
		}, "text");
	},
	setCmdTimeout:function(){
		var param = {type:"setCmdTimeout"};
		$.post(this.url, param, function(data){
 			$("#tip").html(data);
		}, "text");
	},
	setEndType:function(){
		var endType = $("#endTypeSelect").val();
		var param = {type:"setEndType", value:endType};
		$.post(this.url, param, function(data){
 			$("#tip").html(data);
		}, "text");
	},
	setInitialPose:function(){
		var param = {type:"setInitialPose", joint2Angle:45, joint3Angle:45};
		$.post(this.url, param, function(data){
 			$("#tip").html(data);
		}, "text");
	},
	setJogStaticParams:function(){
		var param = {type:"setJogStaticParams"};
		$.post(this.url, param, function(data){
 			$("#tip").html(data);
		}, "text");
	},
	setJogDynamicParams:function(va){
		var param = {type:"setJogDynamicParams", velocityRatio: va};
		$.post(this.url, param, function(data){
 			$("#tip").html(data);
		}, "text");
	},
	setJogInstantCmd:function(ty, status){
		var joint = $("#jointTypeSelect").val();
		ty = status == 1 ? ty : 0;
		var param = {type:"setJogInstantCmd", isJoint:joint, cmd: ty};
		$.post(this.url, param, function(data){
 			$("#tip").html(data);
		}, "text");
	},
	setPlaybackStaticParams:function(){
		var param = {type:"setPlaybackStaticParams"};
		$.post(this.url, param, function(data){
 			$("#tip").html(data);
		}, "text");
	},
	setPlaybackDynamicParams:function(vr, ar){
		var param = {type:"setPlaybackDynamicParams", velocityRatio:vr, accelerationRatio:ar};
		$.post(this.url, param, function(data){
 			$("#tip").html(data);
		}, "text");
	},
	setPlaybackBufferCmd:function(vr, ar){
		var param = {
			type:"setPlaybackBufferCmd",
			motionStyle:$("#modeStyleSelect").val(),
  			isGrab:document.getElementById("Laser").checked ? 1 : 0,
  			x:$("#X").val(),
  			y:$("#Y").val(),
  			z:$("#Z").val(),
  			rHead:$("#rHead").val(),
  			gripper:$("#Gripper").val(),
  			pauseTime:$("#PauseTime").val()
		};
		$.post(this.url, param, function(data){
 			$("#tip").html(data);
		}, "text");
	},
	init:function(){
		var $this = this;
		setInterval(function () {
	        var param = {type:"getPose"};
			$.post($this.url, param, function(data){
				// 是否实时显示机械臂数据
				if(document.getElementById("isRealDisStatus").checked && data.dobotConnectStatus  <= 3)
				{
		 			$("#joint1Angle").val(data.jointAngle[0].toFixed(4));
		 			$("#joint2Angle").val(data.jointAngle[1].toFixed(4));
		 			$("#joint3Angle").val(data.jointAngle[2].toFixed(4));
		 			$("#joint4Angle").val(data.jointAngle[3].toFixed(4));


		 			$("#X").val(data.x.toFixed(4));
		 			$("#Y").val(data.y.toFixed(4));
		 			$("#Z").val(data.z.toFixed(4));
		 			$("#rHead").val(data.rHead.toFixed(4));
		 			$("#Gripper").val(data.gripper.toFixed(4));
		 			$("#PauseTime").val(0);

		 			document.getElementById("isGrab").checked = data.isGrab;
		 		}
			}, "json");
	    }, 1000);

	}
}
function jointTypeSelectFun(){
	if($("#jointTypeSelect").val() == 0){
		$("#btnGroup1").show();
		$("#btnGroup2").hide();
	}else{
		$("#btnGroup1").hide();
		$("#btnGroup2").show();
	}
}
function refreshSwatch() {
	var slider = $( "#slider" ).slider( "value" ),
	psliderv = $( "#psliderv" ).slider( "value" ),
	pslidera = $( "#pslidera" ).slider( "value" );
	$("#sliderVal").val(slider);
	$("#pslidervVal").val(psliderv);
	$("#pslideraVal").val(pslidera);
}
$(function() {
	$( "#slider, #psliderv, #pslidera" ).slider({
	  orientation: "horizontal",
	  range: "min",
	  max: 100,
	  value: 50,
	  slide: refreshSwatch,
	  change: refreshSwatch
	});
	$( "#slider").slider({
		stop:function(event, ui){
			dobotUI.setJogDynamicParams($( "#slider" ).slider( "value" ));
		}
	});
	$( "#psliderv, #pslidera").slider({
		stop:function(event, ui){
			dobotUI.setPlaybackDynamicParams($( "#psliderv" ).slider( "value" ), $( "#pslidera" ).slider( "value" ));
		}
	});
	$( "#slider" ).slider( "value", 50 );
	$( "#psliderv" ).slider( "value", 50 );
	$( "#pslidera" ).slider( "value", 50 );
});