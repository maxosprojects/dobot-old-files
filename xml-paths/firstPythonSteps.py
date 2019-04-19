import serial
import struct
import time
import os
import binascii

cmd_str_10 = [ 0 for i in range(10) ]
cmd_str_42 = [ '\x00' for i in range(42) ]

ser = serial.Serial(#serial connection
    port='COM4',
    baudrate=9600,
    parity=serial.PARITY_NONE,#serial.PARITY_ODD,
    stopbits=serial.STOPBITS_ONE,#serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS#serial.SEVENBITS
)

ser.isOpen()

# Open Serial port will reset dobot, wait seconds
print "Wait 3 seconds..."
time.sleep(3) 

def dobot_cmd_send( cmd_str_10 ):
    global cmd_str_42
    cmd_str_42 = [ '\x00' for i in range(42) ]
    cmd_str_42[0]  = '\xA5'
    cmd_str_42[41] = '\x5A'
    for i in range(10):
        str4 = struct.pack( '<f', float(cmd_str_10[i]) )
        cmd_str_42[4*i+1] = str4[0]
        cmd_str_42[4*i+2] = str4[1]
        cmd_str_42[4*i+3] = str4[2]
        cmd_str_42[4*i+4] = str4[3]
    cmd_str = ''.join( cmd_str_42 )
    print binascii.b2a_hex( cmd_str )
    
    ser.write( cmd_str )

#state 3
def dobot_cmd_send_3( x = 265, y = 0, z = -30 ):
    global cmd_str_10
    cmd_str_10 = [ 0 for i in range(10) ]
    cmd_str_10[0] = 3
    cmd_str_10[2] = x
    cmd_str_10[3] = y
    cmd_str_10[4] = z
    cmd_str_10[7] = 2 # MOVL
    dobot_cmd_send( cmd_str_10 )

def dobot_cmd_send_9():
    global cmd_str_10
    cmd_str_10 = [ 0 for i in range(10) ]
    cmd_str_10[0] = 9
    cmd_str_10[1] = 1
    cmd_str_10[2] = 150#200 #JointVel
    cmd_str_10[3] = 150#200 #JointAcc
    cmd_str_10[4] = 150#200 #ServoVel
    cmd_str_10[5] = 150#200 #ServoAcc
    cmd_str_10[6] = 500#800 #LinearVel
    cmd_str_10[7] = 500#1000 #LinearAcc
    dobot_cmd_send( cmd_str_10 )

def dobot_cmd_send_10( VelRat = 100, AccRat = 100 ):
    global cmd_str_10
    cmd_str_10 = [ 0 for i in range(10) ]
    cmd_str_10[0] = 10
    cmd_str_10[2] = VelRat
    cmd_str_10[3] = AccRat
    dobot_cmd_send( cmd_str_10 )


print "Dobot Test Begin"
dobot_cmd_send_9() #config
time.sleep( 0.1 )
dobot_cmd_send_10() #config
time.sleep( 0.1 )
dobot_cmd_send_3( 260, 0, 30 ) #MOVL
time.sleep( 3 )
dobot_cmd_send_3( 260, 0, 0 ) #MOVL
time.sleep( 0.1 )
print "Dobot Test End"