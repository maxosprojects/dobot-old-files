import java.util.Timer;
import java.util.TimerTask;

import CPlusDll.DobotDll;
import CPlusDll.DobotDll.*;

// tip: The demo must import Jna library, inner DobotDemo folder of this project
public class Main
{
	public static void main(String[] args) {
		try { 
			
			Main app = new Main();
			app.Start();
			
			JogInstantCmd test = new JogInstantCmd();
			test.isJoint = 1;
	    	while(true)
	    	{
	    		try{
	    			test.cmd = 1;
	    			DobotDll.instance.SetJogInstantCmd(test);
		    		Thread.sleep(200);
		            test.cmd = 0;
		            DobotDll.instance.SetJogInstantCmd(test);
		    		Thread.sleep(1000);
		            test.cmd = 2;
		            DobotDll.instance.SetJogInstantCmd(test);
		    		Thread.sleep(200);
		            test.cmd = 0;
		            DobotDll.instance.SetJogInstantCmd(test);
		    		Thread.sleep(1000);
		    		
	    		} catch (Exception e) {  
	                e.printStackTrace();  
	            }
	    	}
			
			//DobotDll.instance.DisconnectDobot();
		} catch (Exception e) {  
            e.printStackTrace();  
        }
	}

	private void Start() {
		
  		StartPeriodic();

	    StartDobot();

	    StartGetStatus();
	}
	/* (non-Java-doc)
	 * @see java.lang.Object#Object()
	 */
	public Main() {
		super();
	}


	private void StartDobot() {
		
		DobotResult ret = DobotResult.values()[DobotDll.instance.ConnectDobot()];
        // ��ʼ����
        if (ret == DobotResult.DobotResult_NotFound || ret == DobotResult.DobotResult_Occupied
        		|| ret == DobotResult.DobotResult_NoDataUploaded)
        {
            Msg("Connect error, code:" + ret.name());
            return;
        }
        Msg("connect success code:" + ret.name());
        // reset and start
        //DobotDll.instance.ResetDobot();
        DobotDll.instance.SetCmdTimeout(500);
        DobotDll.instance.SetEndType(EndType.EndTypePump.ordinal());

        // Must set when sensor is not exist
        InitialPose initialPose = new InitialPose();
        initialPose.joint2Angle = 45;
        initialPose.joint3Angle = 45;
        DobotDll.instance.SetInitialPose(initialPose);
        
        JogStaticParams jsParam = new JogStaticParams();
        jsParam.jointMaxVelocity = 200;
        jsParam.jointMaxAcceleration = 200;
        jsParam.servoMaxVelocity = 200;
        jsParam.servoMaxAcceleration = 200;
        jsParam.linearMaxVelocity = 200;
        jsParam.linearMaxAcceleration = 200;
        DobotDll.instance.SetJogStaticParams(jsParam);

        JogDynamicParams jdParam = new JogDynamicParams();
        jdParam.velocityRatio = 30;
        DobotDll.instance.SetJogDynamicParams(jdParam);

        PlaybackStaticParams pbsParam = new PlaybackStaticParams();
        pbsParam.jointMaxVelocity = 200;
        pbsParam.jointMaxAcceleration = 200;
        pbsParam.servoMaxVelocity = 200;
        pbsParam.servoMaxAcceleration = 200;
        pbsParam.linearMaxVelocity = 800;
        pbsParam.linearMaxAcceleration = 1000;
        pbsParam.pauseTime = 100;
        pbsParam.jumpHeight = 20;
        DobotDll.instance.SetPlaybackStaticParams(pbsParam);

        PlaybackDynamicParams pbdParam = new PlaybackDynamicParams();
        pbdParam.velocityRatio = 30;
        pbdParam.accelerationRatio = 30;
        DobotDll.instance.SetPlaybackDynamicParams(pbdParam);
        
	}

	private void StartPeriodic() {
		
		Timer timer = new Timer();
        timer.schedule(new TimerTask() {
            public void run() {
            	// call in interval 200ms
                DobotDll.instance.PeriodicTask();
            }
        }, 10, 100);// 
	}
	
	private void StartGetStatus() {
		Timer timerPos = new Timer();
        timerPos.schedule(new TimerTask() {
            public void run() {
            	// call in interval 300ms
            	Pose pose = new Pose();
                DobotDll.instance.GetPose(pose);

                Msg("joint1Angle="+pose.jointAngle[0]+"  " 
                		+ "joint2Angle="+pose.jointAngle[1]+"  "
                		+ "joint3Angle="+pose.jointAngle[2]+"  "
                		+ "joint4Angle="+pose.jointAngle[3]+"  "
                		+ "x="+pose.x+"  "
                		+ "y="+pose.y+"  "
                		+ "z="+pose.z+"  "
                		+ "rHead="+pose.rHead+"  "
                		+ "isGripper="+pose.gripper+"  ");
            }
        }, 100, 500);//
	}
	
	private void Msg(String string) {
		System.out.println(string); 
	}
}