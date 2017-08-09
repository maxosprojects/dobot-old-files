import time

import sys
from DobotSerialInterface import DobotSerialInterface

#x, y, duration
Beakers = [ #[-180, 90, 3],
			#[-130, 185, 3],
			#[0, 180, 3], 
			#[100, 250, 3],
			#[150, 150, 3],
			[265, 120, 3],
			[210, -10, 3]
			#[285, -110, 3]
			#extra
			#[215, 80, 5],
			#[215, -70, 5]
			#extra
			#[150, -150, 3],
			#[115, -265, 3],
			#[25, -85, 3],
			#[-90, -165, 3]
			];
class Electroplating:

    sleep_duration = 4.0;
    dobot_interface = None;
    
    home_location = [215, 0];
    xy_locations = [];
    durations = [];
    z_up = 100;
    z_down = 100;
    z_mid = 50;
    
    def __init__(self,comport):
    
        self.dobot_interface = DobotSerialInterface(comport);
        time.sleep(2.0);
        
        if(not self.dobot_interface):
            print "failed to open connection";
        else:
            print "Opened connection"
            self.dobot_interface.set_speed()
            self.dobot_interface.set_playback_config()
    
    def __del__(self):
        del self.dobot_interface;
   
    def gotoHome(self):
        self.dobot_interface.send_absolute_position(self.home_location[0], self.home_location[1], self.z_up, 0)  # MOVL
        time.sleep(self.sleep_duration);
        
    def move_xy(x,y,z,duration = 2):
        dobot_interface.send_absolute_position(x, y, z, 0);  # MOVL
        time.sleep(duration);

    def move_angles(base, rear, front, duration = 2):
        dobot_interface.send_absolute_angles(base, rear, front, 0);
        time.sleep(duration);

    def addXYLocation(self, x, y, duration):
        self.xy_locations.append([x,y]);
        self.durations.append(duration);

    def execute(self):
        #start at home position with z_up
        self.gotoHome();

        for i in range(len(self.xy_locations)):

            #move with z_up over recommended x_y position
            self.dobot_interface.send_absolute_position(self.xy_locations[i][0], self.xy_locations[i][1], self.z_up, 0)  # MOVL
            time.sleep(self.sleep_duration);
			
            #put it in the beaker and hold for normal time + added duration in that beaker
            self.dobot_interface.send_absolute_position(self.xy_locations[i][0], self.xy_locations[i][1], self.z_down, 0)  # MOVL
            time.sleep(self.sleep_duration);

            #shake
            #t_end = time.time() + self.durations[i];
            #while time.time() < t_end:
            #    self.dobot_interface.send_absolute_position(self.xy_locations[i][0], self.xy_locations[i][1], self.z_down + 10, 0)  # MOVL
            #    time.sleep(0.5);
            #    self.dobot_interface.send_absolute_position(self.xy_locations[i][0], self.xy_locations[i][1], self.z_down, 0)  # MOVL
            #    time.sleep(0.5);
                
            #bring up in z
            self.dobot_interface.send_absolute_position(self.xy_locations[i][0], self.xy_locations[i][1], self.z_up, 0)  # MOVL
            time.sleep(self.sleep_duration);
            

electroplating = Electroplating(sys.argv[1]);

for b in range(len(Beakers)):
	electroplating.addXYLocation(Beakers[b][0], Beakers[b][1], Beakers[b][2]);

#electroplating.addXYLocation(215, -70, 5);# x, y, duration

electroplating.execute();

electroplating.gotoHome();
