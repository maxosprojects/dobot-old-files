import time
import sys
import os

#x, y, duration
Beakers = [ [-180, 90, 3],
			[-130, 185, 3],
			[0, 180, 3], 
			[100, 250, 3],
			[150, 150, 3],
			[265, 120, 3],
			[210, -10, 3],
			[285, -110, 3],
			#extra
			[215, 80, 5],
			[215, -70, 5],
			#extra
			[150, -150, 3],
			[115, -265, 3],
			[25, -85, 3],
			[-90, -165, 3]
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
    f = None
        
    def __init__(self):
    
       
        self.f = open("XMLFromPoints.xml",'w');
        self.f.write("""<?xml version='1.0' encoding='UTF-8'?>\n<playback>\n""");
        #if(not self.dobot_interface):
       #     print "failed to open connection";
       # else:
        #    print "Opened connection"
        #    self.dobot_interface.set_speed()
       #     self.dobot_interface.set_playback_config()
    
    def __del__(self):
   #     del self.dobot_interface;
        self.f.write("</playback>");
        self.f.close();
   
   
    def addXYLocation(self, x, y, duration):
        self.xy_locations.append([x,y]);
        self.durations.append(duration);

    def execute(self):
        for i in range(len(self.xy_locations)):
            thisStr = """\t<point>\n\t\t<motionStyle>MOVL</motionStyle>\n\t\t<isGrab>false</isGrab>\n\t\t<x>""";
            thisStr += str(self.xy_locations[i][0]);
            thisStr += """</x>\n\t\t<y>""";
            thisStr += str(self.xy_locations[i][1]);
            thisStr += """</y>\n\t\t<z>100</z>\n\t\t<rHead>0</rHead>\n\t\t<gripper>0</gripper>\n\t\t<pauseTime>""";
            thisStr += str(self.durations[i]);
            thisStr += """</pauseTime>\n\t</point>\n""";
            self.f.write(thisStr);

electroplating = Electroplating();

for b in range(len(Beakers)):
	electroplating.addXYLocation(Beakers[b][0], Beakers[b][1], Beakers[b][2]);

#electroplating.addXYLocation(215, -70, 5);# x, y, duration

electroplating.execute();

