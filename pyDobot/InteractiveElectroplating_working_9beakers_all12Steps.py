#! /usr/bin/env python
import time
import sys
import serial

from DobotSerialInterface import DobotSerialInterface
from Arduino import Arduino

#DobotPort = '/dev/ttyACM0'
DobotPort = 'COM4'

class ArduinoBoard:
    
    arduinoPort = 'COM9';
    arduinoBaudRate = 9600;    
    board = None;
    
    ECRelay = 2;
    PDRelay = 3;
    RHRelay = 4;
    
    voltageSensorPin = 0;
    currentSensorPin = 2;
    
    
    
    
    def __init__(self, baud=arduinoBaudRate, port=arduinoPort):
        self.board = Arduino(baud, port);
        if(self.board is None):
            print "Error Initializing Arduino Board"
        else:
            print "Initialized Arduino Board";
        board.pinMode(ECRelay, "OUTPUT");
        board.pinMode(PDRelay, "OUTPUT");
        board.pinMode(RHRelay, "OUTPUT");
        
        self.stopCurrent();
    
    def setVoltage(self):
        #do something
        i = 0;
    
    def readVoltage(self):
        vout = 0.0;
        vin = 0.0;
        voltageSensorR1 = 30000.0;   
        voltageSensorR2 = 7500.0; 
        voltageValue = self.board.analogRead(self.voltageSensorPin);
        vout = (voltageValue * 5.0) / 1024.0; #offsetting the analogRead value
        vin = vout / (R2/(R1+R2)); 
        return vin;
    
    def readCurrent(self):
        mVperAmp = 100; # use 100 for 20A Module and 66 for 30A Module
        rawValue = self.board.analogRead(currentSensorPin); #can hold upto 64 10-bit A/D readings
        ACSoffset = 2500;
        voltage = 0;
        amps = 0;
        voltage = (rawValue / 1023.0) * 5000; # Gets you mV
        amps = ((voltage - ACSoffset) / mVperAmp);
        return amps;
        
    def startCurrentEC(self):
        self.board.digitalWrite(self.ECRelay, "LOW");
        self.board.digitalWrite(self.PDRelay, "HIGH");
        self.board.digitalWrite(self.RHRelay, "HIGH");
    
    def startCurrentPD(self):
        self.board.digitalWrite(self.ECRelay, "HIGH");
        self.board.digitalWrite(self.PDRelay, "LOW");
        self.board.digitalWrite(self.RHRelay, "HIGH");
    
    def startCurrentRH(self):   
        self.board.digitalWrite(self.ECRelay, "HIGH");
        self.board.digitalWrite(self.PDRelay, "HIGH");
        self.board.digitalWrite(self.RHRelay, "LOW");    

    def stopCurrent(self):
        self.board.digitalWrite(self.ECRelay, "HIGH");
        self.board.digitalWrite(self.PDRelay, "HIGH");
        self.board.digitalWrite(self.RHRelay, "HIGH");
        
        

if len(sys.argv) >= 2:
    DobotPort = sys.argv[1];

print "Setting Port to %s" % (DobotPort);
    
dobot_interface = DobotSerialInterface(DobotPort)

print "Opened connection"
dobot_interface.set_speed()
dobot_interface.set_playback_config()

z_up = 30;
z_down = 20;

          # X, Y, Shake_Duration
# Beakers = [ [0, 0, 0], #0 dummy beaker for numbering
            # [-77, -255, 5], #1
	    # [46, -262, 7], #2
	    # [65, -190,  5],
        # #[55, -137, 5],  #3
	    # [159, -210, 5], #4
	    # [239, -117, 5], #5
	    # [152, -30, 5], #6
	    # [267, 0, 5], #7
	    # [237, 122, 5], #8
	    # [154,216, 5], #9
	    # [56,144, 5], #10
	    # [-198, 214, 5], #11
	    # [42, 263, 5]]; #12
            
Beakers = [ [0, 0, 0],      #0 dummy beaker for numbering
            [-140, -165, 5], #1 # -135deg
            [-112, -271, 5],  #2 #  -112.6deg
            [0, -211, 5], #3 # -90deg
            [112, -271, 5], #4 # -67.6deg
            [149, -149, 5], #5 # -45deg
            [270, -122, 5],  #6 # -22.6deg
            [210, 0, 5],    #7 # 0deg
            [271, 113, 5],  #8 # 22.4deg
            [149, 149, 5],   #9 # 45deg
            [112, 270, 5],    #10 # 67.4deg
            [-189, 223, 5], #11 # 130deg
            [-25, 209, 5]]; #12 #97deg

            
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
            if(int(a) == 1): # xyz-
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
    
    move_xy(Beakers[id][0], Beakers[id][1], z_up);
    move_xy(Beakers[id][0], Beakers[id][1], z_down);
    
    shake(Beakers[id][0], Beakers[id][1], z_down, Beakers[id][2]); #x, y, z and shake_duration
    
    #hold the position so the drops can drip - 5 second pause
    move_xy(Beakers[id][0], Beakers[id][1], z_up, 5);
 
#time.sleep(3);

move_xy(home_xyz[0], home_xyz[1], home_xyz[2]);

a = raw_input("Enter 0 for automatic movement, and 1 for interactive: ");

if(int(a) == 0):
    num = raw_input("Enter number of loops: ");
    num_loops = int(num);
    while(num_loops):
        num_loops = num_loops - 1;
        # #1
        # move_angles(-40, 30, 10);
        # move_angles(-60, 30, 10);
        # move_angles(-90, 30, 10);
        # move_angles(-106, 30, 10);
        # move_angles(-132, 30, 10);
        # #interactive_run();
        # up_down_beaker(1);

        # #2
        # move_angles(-112, 30, 10);
        # up_down_beaker(2);

        # #3
        # move_angles(-90, 30, 10);
        # up_down_beaker(3);

        # #4
        # move_angles(-67, 30, 10);
        # up_down_beaker(4);
        # #interactive_run();
        
        # #5
        # move_angles(-45, 30, 20);
        # up_down_beaker(5);

        #6
        move_angles(-20, 8, 20);    
        up_down_beaker(6);
        
        #7
        move_angles(0, 30, 20);
        up_down_beaker(7);

        #8
        move_angles(20, 30, 20);
        up_down_beaker(8);

        #9
        move_angles(45, 20, 20);
        up_down_beaker(9);
        
        #10
        move_angles(67, 20, 20);
        up_down_beaker(10);
        
        #11
        move_angles(89, 20, 20);
        move_angles(100, 20, 20);
        move_angles(120, 20, 20);
        move_angles(130, 20, 20);
        up_down_beaker(11);

        #12
        move_angles(120, 30, 10);
        move_angles(97, 30, 10);
        up_down_beaker(12);
        
        #Home
        move_angles(60, 20, 10);
        move_angles(30, 20, 10);
        move_angles(0, 20, 10);
        move_xy(home_xyz[0], home_xyz[1], home_xyz[2]);
        
        print "%d loops remaining" % (num_loops);
            
        cc  = raw_input("Press Enter to Continue...");
else:
    interactive_run();
