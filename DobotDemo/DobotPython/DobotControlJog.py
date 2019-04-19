import sys
from ctypes import *
import threading
import time

def PeriodicTask():
    dll.PeriodicTask()
    threading.Timer(0.1, PeriodicTask).start()

def GetPoseTask():
    pose = Pose()
    dll.GetPose(byref(pose))
    print 'Pose:', pose.x, pose.y, pose.z, pose.rHead, pose.joint1Angle, pose.joint2Angle, pose.joint3Angle, pose.joint4Angle
    threading.Timer(0.5, GetPoseTask).start()

# For initial pose
class InitialPose(Structure):
    _fields_ = [("joint2Angle", c_float), ("joint3Angle", c_float)]

# For pose
class Pose(Structure):
    _fields_ = [
        ("x", c_float),
        ("y", c_float),
        ("z", c_float),
        ("rHead", c_float),
        ("joint1Angle", c_float),
        ("joint2Angle", c_float),
        ("joint3Angle", c_float),
        ("joint4Angle", c_float),
        ("isGrab", c_byte),
        ("gripper", c_float)
        ]

# For jog
class JogStaticParams(Structure):
    _fields_ = [
        ("jointMaxVelocity", c_float), ("jointMaxAcceleration", c_float),
        ("servoMaxVelocity", c_float), ("servoMaxAcceleration", c_float),
        ("linearMaxVelocity", c_float), ("linearMaxAcceleration", c_float)
        ]

class JogDynamicParams(Structure):
    _fields_ = [("velocityRatio", c_float)]

class JogInstantCmd(Structure):
    _fields_ = [("isJoint", c_byte), ("cmd", c_int)]

sys.path.append(sys.path[0])
dll = cdll.LoadLibrary(sys.path[0] + '//DobotDll.dll');
PeriodicTask()
GetPoseTask()

errorString = [
    'Success',
    'Warning:Long arm angle not good!',
    'Warning:Short arm angle not good!',
    'Both long & short arm angle not good!',
    'Error:Dobot not found!',
    "Error:COM port occupied!",
    "Error:No data uploaded!"
    ]

result = dll.ConnectDobot()
print errorString[result]

if (result < 4):
    # Set command timeout
    dll.SetCmdTimeout(3000)
    # Set initial pose
    initialPose = InitialPose()
    initialPose.joint2Angle = 45
    initialPose.joint3Angle = 45
    dll.SetInitialPose.argtypes = [POINTER(InitialPose)]
    dll.SetInitialPose(byref(initialPose))

    # Set static & dynamic param
    jogStaticParams = JogStaticParams()
    jogStaticParams.jointMaxVelocity = 200;
    jogStaticParams.jointMaxAcceleration = 200;
    jogStaticParams.servoMaxVelocity = 200;
    jogStaticParams.servoMaxAcceleration = 200;
    jogStaticParams.linearMaxVelocity = 200;
    jogStaticParams.linearMaxAcceleration = 200;

    jogDynamicParams = JogDynamicParams();
    jogDynamicParams.velocityRatio = 30;

    dll.SetJogStaticParams(byref(jogStaticParams))
    dll.SetJogDynamicParams(byref(jogDynamicParams))

    dll.SetJogInstantCmd.argtypes = [POINTER(JogInstantCmd)]
    test = JogInstantCmd()
    test.isJoint = 1
    while 1:
        test.cmd = 1;
        dll.SetJogInstantCmd(byref(test))
        time.sleep(0.2)
        test.cmd = 0;
        dll.SetJogInstantCmd(byref(test))
        time.sleep(1)
        test.cmd = 2;
        dll.SetJogInstantCmd(byref(test))
        time.sleep(0.2)
        test.cmd = 0;
        dll.SetJogInstantCmd(byref(test))
        time.sleep(1)
dll.DisconnectDobot()
