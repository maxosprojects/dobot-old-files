#! /usr/bin/env python


import time

from DobotSerialInterface import DobotSerialInterface

dobot_interface = DobotSerialInterface('/dev/dobot')

print "Opened connection"
dobot_interface.set_speed()
dobot_interface.set_playback_config()


sleep_duration = 2
Beakers = [ [-180, 90, 3],
			[-130, 185, 3],
			[0, 180, 3], 
			[100, 250, 3],
			[150, 150, 3],
			[265, 120, 3],
			[210, -10, 3],
			[285, -110, 3],
			[150, -150, 3],
			[115, -265, 3],
			[25, -85, 3],
			[-90, -165, 3]];

first_round = False
time.sleep(2)
i = -2;
# print "SENDING FIRST COMMAND"
while (i < len(Beakers) - 1):
    # continue
    #set_initial_angles(45, 45)
	i = i + 1;
    if first_round:
		first_round = False
        #  88.62541198730469, -0.9358671307563782
        # dobot_interface.apply_arm_angle_offsets(1.37, 0.936)
        # self.apply_arm_angle_offsets(0, 0, dobot_interface.current_status)
        time.sleep(2)
    else:
        # continue
        dobot_interface.send_absolute_position(Beakers[i][0], Beakers[i][1], 50, 0)  # MOVL
        time.sleep(sleep_duration)
        print "send position"

        #dobot_interface.send_absolute_angles(-30, 0.0, 0.0, 30)
        # dobot_interface.send_absolute_angles(0, 20.0, 00.0)
        # dobot_interface.send_absolute_angles(0, 10.0, 00.0)
        #time.sleep(2)
        #dobot_interface.send_absolute_angles(30, 30.0, 00.0, -30)
        #time.sleep(2)
