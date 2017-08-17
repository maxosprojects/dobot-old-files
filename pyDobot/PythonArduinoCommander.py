#! /usr/bin/env python
import time
import sys
import serial

from Arduino import Arduino
from Arduino import Servos

class ArduinoBoard:
    
    arduinoPort = 'COM6';
    arduinoBaudRate = 9600;    
    board = None;
    gripperServo = None;
    
    ECRelay = 2;
    PDRelay = 3;
    RHRelay = 4;
    
    voltageSensorPin = 0;
    currentSensorPin = 2;
    gripperServoPin = 9;
    gripperServoClose = 80;
    gripperServoOpen = 160;
    
    
    def __init__(self, baud=arduinoBaudRate, port=arduinoPort):
        self.board = Arduino(baud, port);
        if(self.board is None):
            print "Error Initializing Arduino Board"
        else:
            print "Initialized Arduino Board";
        time.sleep(1);
        self.setPinModes();
        
        self.gripperServo = Servos(self.board);
        if(self.gripperServo is None):
            print "Error Initializing Gripper Servo"
        else:
            print "Initialized Gripper Servo";
        
        time.sleep(1);
        print "Attaching Servo..";
        self.gripperServo.attach(self.gripperServoPin, self.gripperServoClose, self.gripperServoOpen);
        print "Servo Attached..";
        
        self.stopCurrent();
    
    def __del__(self):
        self.gripperServo.detach(self.gripperServoPin);
        self.board.close();
        self.stopCurrent();
        print "Destroyed Class";

    def setPinModes(self):
        self.board.pinMode(self.ECRelay, "OUTPUT");
        self.board.pinMode(self.PDRelay, "OUTPUT");
        self.board.pinMode(self.RHRelay, "OUTPUT");
        print "Pin Modes Set";
        
    def setVoltage(self):
        #do something
        i = 0;
    
    def readVoltage(self):
        vout = 0.0;
        vin = 0.0;
        voltageSensorR1 = 30000.0;   
        voltageSensorR2 = 7500.0; 
        voltageValue = 0;
        for i in range(0,64):
            voltageValue = voltageValue + self.board.analogRead(self.voltageSensorPin);
        voltageValue = voltageValue / 64;
        vout = (voltageValue * 5.0) / 1024.0; #offsetting the analogRead value
        vin = vout / (voltageSensorR2/(voltageSensorR1+voltageSensorR2)); 
        return vin;
    
    def gripperOpen(self):
        self.gripperServo.write(self.gripperServoPin, self.gripperServoOpen);
    
    def gripperClose(self):
        self.gripperServo.write(self.gripperServoPin, self.gripperServoClose);
    
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
        
# thisBoard = ArduinoBoard(9600,'COM6');
        
# grip = raw_input("Press Enter to Open Gripper..");
# thisBoard.gripperOpen();
# grip = raw_input("Press Enter to Close Gripper..");
# print "Closing Gripper in 2 seconds..";
# time.sleep(2);
# thisBoard.gripperClose();
# grip = raw_input("Press Enter to Start Process..");
# #1
# print "Starting Process in 2 seconds";


# #interactive_run();
# print("Voltage is ", thisBoard.readVoltage());
# time.sleep(2);
# thisBoard.startCurrentEC();
# time.sleep(2);
# thisBoard.stopCurrent();
    

    # #2print("Voltage is ", thisBoard.readVoltage());
# thisBoard.startCurrentPD();
# time.sleep(2);
# thisBoard.stopCurrent();

    # #3
# print("Voltage is ", thisBoard.readVoltage());

# del thisBoard;