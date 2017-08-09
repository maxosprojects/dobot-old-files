#! /usr/bin/env python
import time
import sys
import serial

from DobotSerialInterface import DobotSerialInterface

port = 'COM4'
displayPort = 'COM9'

displaySerial = serial.Serial(displayPort, 9600, timeout=5);

if len(sys.argv) >= 2:
    port = sys.argv[1];

print "Setting Port to %s" % (port);
    
dobot_interface = DobotSerialInterface(port)

print "Opened connection"
dobot_interface.set_speed()
dobot_interface.set_playback_config()

hot_x = 16.5
hot_y = -232;
z_up = 50;
z_down = -55;

          # X, Y, Shake_Duration
Beakers = [ [0, 0, 0], #0 dummy beaker for numbering
            [hot_x, hot_y, 5], #1
			[-225+15, 140-10, 7], #2
			[-120, 241, 7],  #3
			[3.5, 235-5, 7], #4
			[115, 275-5, 10], #5
			[142+5, 157.8, 7], #6
			[260+10, 114.3, 7], #7
			[hot_x, hot_y, 40], #8
			[220.7,0, 7], #9
			[262+10, -100-10, 7], #10
			[hot_x, hot_y, 70], #11
			[135.6+15, -151.5+4, 7]]; #12
            

home_xyz = [215, 0, 100];
            
time.sleep(2)


def move_xy(x,y,z,duration = 2):
    dobot_interface.send_absolute_position(x, y, z, 0);  # MOVL
    time.sleep(duration);
    

def move_angles(base, rear, front, duration = 2):
    dobot_interface.send_absolute_angles(base, rear, front, 0);
    time.sleep(duration);

def interactive_run():
    a = raw_input('Enter 0 for angles, 1 for xyz, 2 to exit: ');
    while int(a) < 2: 
        print 'Current Position: ',
        print dobot_interface.current_status.position
        print 'Current angles: ',
        print dobot_interface.current_status.angles
        s = raw_input("Please enter comma separated 3 numbers: ")
        mynums = [float(i) for i in s.split(',')]
        if(len(mynums) != 3):
            print('Need exactly 3 numbers');
        else:
            print('Moving now..');
            if(int(a) == 1): # xyz
                move_xy(mynums[0], mynums[1], mynums[2]);
                print dobot_interface.current_status.position
            else: #a == 0 - angles
                move_angles(mynums[0], mynums[1], mynums[2]);
                print dobot_interface.current_status.angles
                
        a = raw_input('Enter 0 for angles, 1 for xyz, 2 to exit: ');   
        
    return;
  
def shake(x, y, z, shakeDuration):
    t_end = time.time() + shakeDuration;
    while time.time() < t_end:
        move_xy(x, y, z + 10, 0.3);
        move_xy(x, y, z - 10, 0.3);
    
    time.sleep(1);
    move_xy(x, y, z + 10, 1);
    
def up_down_beaker(id):

    print "Doing beaker %d now" % (id);
    displaySerial.write("Beaker no. %d" % (id));
    move_xy(Beakers[id][0], Beakers[id][1], z_up);
    move_xy(Beakers[id][0], Beakers[id][1], z_down);
    
    if(id == 1 or id == 11):
        shake(Beakers[id][0], Beakers[id][1], z_down - 10, Beakers[id][2]); #x, y, z and shake_duration
    elif(id == 8):
        shake(Beakers[id][0], Beakers[id][1], z_down - 15, Beakers[id][2]); #x, y, z and shake_duration
    else:
        shake(Beakers[id][0], Beakers[id][1], z_down, Beakers[id][2]); #x, y, z and shake_duration
    
    #hold the position so the drops can drip - 5 second pause
    move_xy(Beakers[id][0], Beakers[id][1], z_up, 5);
 
time.sleep(3);

move_xy(home_xyz[0], home_xyz[1], home_xyz[2]);

a = raw_input("Enter 0 for automatic movement, and 1 for interactive: ");

if(int(a) == 0):
    num = raw_input("Enter number of loops: ");
    num_loops = int(num);
    while(num_loops):
        num_loops = num_loops - 1;
        #1
        #move_angles(-40, 30, 10);
        #move_angles(-90, 30, 10);
        #up_down_beaker(1);

        #2
        move_angles(-40, 30, 10);
        move_angles(0, 30, 10);
        move_angles(40, 30, 10);
        move_angles(80, 30, 10);
        move_angles(125, 30, 10);
        move_angles(150, 30, 10);   
        up_down_beaker(2);

        #3
        move_angles(120, 30, 10)
        up_down_beaker(3);

        #4
        move_angles(116, 30, 10);
        up_down_beaker(4);
        #interactive_run();
        
        #5
        move_angles(75, 30, 10);
        up_down_beaker(5);

        #6
        move_angles(45, 30, 10);
        move_angles(48, 8, 10);    
        up_down_beaker(6);
        
        #7
        move_angles(25, 30, 10);
        up_down_beaker(7);

        #8
        move_angles(0, 30, 10);
        move_angles(-40, 20, 10);
        move_angles(-90, 20, 10);
        up_down_beaker(8);

        #9
        move_angles(-60, 20, 10);
        move_angles(-30, 20, 10);
        move_angles(0, 30, 10);
        move_xy(home_xyz[0], home_xyz[1], home_xyz[2]);
        up_down_beaker(9);
        
        #10
        move_angles(-23, 43, 10);
        up_down_beaker(10);
        
        # Need to do activation again:
        #5
        move_angles(0, 30, 10);
        move_angles(25, 30, 10);
        move_angles(45, 30, 10);
        move_angles(75, 30, 10);
        up_down_beaker(5);
        
        #6 (second activation drag out)
        move_angles(45, 30, 10);
        move_angles(48, 8, 10);    
        up_down_beaker(6);
        
        #7 (second activation wash)
        move_angles(25, 30, 10);
        up_down_beaker(7);
        move_angles(0, 30, 10);
        
        #11
        move_angles(-40, 20, 10);
        move_angles(-90, 20, 10);
        up_down_beaker(11);

        #12
        move_angles(-40, 30, 10);
        up_down_beaker(12);
        
        #13 (redip in 10)
        ### Adding steps to compensate for missing 13th beaker with DI water. Redipping in 10.
        move_angles(-30, 20, 10);
        move_angles(-23, 43, 10);
        up_down_beaker(10);
        ###
        
        #Home
        move_angles(-30, 20, 10);
        move_angles(0, 20, 10);
        move_xy(home_xyz[0], home_xyz[1], home_xyz[2]);
        displaySerial.write('End');
        
        time.sleep(5);
        
        print "%d loops remaining" % (num_loops);
        displaySerial.write('End');
        displaySerial.close();
        cc = raw_input("Press Enter to Continue...");
else:
    interactive_run();