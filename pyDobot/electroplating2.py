#! /usr/bin/env python


import time
import sys

from DobotSerialInterface import DobotSerialInterface

dobot_interface = DobotSerialInterface(sys.argv[1])

print "Opened connection"
dobot_interface.set_speed()
dobot_interface.set_playback_config()

hot_beaker = [16.5, -236, 2];

Beakers = [ [0, 0, 0], #0 dummy beaker for numbering
             hot_beaker, #1
			[-161, 137, 3], #2
			[-110, 241, 3],  #3
			[3.5, 194.3, 3], #4
			[100.6, 242.7, 3], #5
			[153.9, 138.1, 3], #6
			[260, 114.4, 3], #7
			hot_beaker, #8
			[208.7,-17.2, 3], #9
			[258.5, -118.2, 3], #10
			hot_beaker, #11
			[135.6, -151.5, 3]]; #12
            

home_xyz = [215, 0, 100];
            
time.sleep(2)

def move_xy(x,y,z,duration = 2):
    dobot_interface.send_absolute_position(x, y, z, 0);  # MOVL
    time.sleep(duration);

def move_angles(base, rear, front, duration = 2):
    dobot_interface.send_absolute_angles(base, rear, front, 0);
    time.sleep(duration);

#dobot_interface.send_absolute_position(250, 0, 120, 0)  # MOVL
#time.sleep(sleep_duration)
#dobot_interface.send_absolute_angles(30, 20.0, 20.0, 0)
    
time.sleep(3);

move_xy(home_xyz[0], home_xyz[1], home_xyz[2]);

#go to hot beaker for step 1
move_angles(-30, 20, 20);
move_angles(-60, 20, 20);
move_angles(-90, 20, 20);

move_xy(Beakers[1][0], Beakers[1][1], 100);
move_xy(Beakers[1][0], Beakers[1][1], 40);

move_angles(-60, 20, 20);
move_angles(-30, 20, 20);
move_angles(30, 20, 20);
move_angles(60, 20, 20);
move_angles(90, 20, 20);
move_angles(125, 20, 20);

print('1st Beaker done');
move_xy(Beakers[2][0], Beakers[2][1], 100);
move_xy(Beakers[2][0], Beakers[2][1], 40);

move_angles(110, 20, 20)

print('2 Beaker done');
move_xy(Beakers[3][0], Beakers[3][1], 100);
move_xy(Beakers[3][0], Beakers[3][1], 40);

print('3 Beaker done');
move_xy(Beakers[4][0], Beakers[4][1], 100);
move_xy(Beakers[4][0], Beakers[4][1], 40);

print('4 Beaker done');
move_xy(Beakers[5][0], Beakers[5][1], 100);
move_xy(Beakers[5][0], Beakers[5][1], 40);

print('5 Beaker done');

move_xy(Beakers[6][0], Beakers[6][1], 100);
move_xy(Beakers[6][0], Beakers[6][1], 40);

print('6 Beaker done');

move_xy(Beakers[7][0], Beakers[7][1], 100);
move_xy(Beakers[7][0], Beakers[7][1], 40);

print('7 Beaker done');

move_angles(0, 20, 20);
move_angles(-30, 20, 20);
move_angles(-60, 20, 20);
move_angles(-90, 20, 20);

print('turned towards 8 beaker');

move_xy(Beakers[8][0], Beakers[8][1], 100);
move_xy(Beakers[8][0], Beakers[8][1], 40);
print('8 Beaker done');

move_angles(-60, 20, 20);
move_angles(-30, 20, 20);
move_angles(0, 45, 20);
move_xy(home_xyz[0], home_xyz[1], home_xyz[2]);



# move_angles(120, 20, 20);
# move_xy(-161, 137, 100); #over 1st beaker.
# move_xy(-161, 137, -20);

# move_xy(-161, 137, 100);
# move_xy(-130, 170, 100); #over 2nd beaker.

# move_xy(-110, 241, 100); #over 2nd beaker.

# #move_angles(90, 20, 20);

# #move_xy(3.5, 194, 100); #over 3rd beaker.

# #move_xy(100.6, 242.7, 100); #over 4th beaker


# move_angles(90, 20, 20);
# move_angles(60, 20, 20);
# move_angles(30, 20, 20);
# move_angles(0, 20, 20);
    

        
        
        
        
        
        
        