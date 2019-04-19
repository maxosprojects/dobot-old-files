using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;

namespace DobotClientDemo.CPlusDll
{
    public enum EndType
    {
        EndTypePump,
        EndTypeGripper,
        EndTypeLaser
    };

    public struct InitialPose
    {
        public float joint2Angle;
        public float joint3Angle;
    };

    public struct Pose
    {
        public float x;
        public float y;
        public float z;
        public float rHead;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 4)]
        public float[] jointAngle;
        public float isGrab;
        public float gripper;
    };

    public struct JogStaticParams
    {
        public float jointMaxVelocity;
        public float jointMaxAcceleration;
        public float servoMaxVelocity;
        public float servoMaxAcceleration;
        public float linearMaxVelocity;
        public float linearMaxAcceleration;
    };

    public struct JogDynamicParams
    {
        public float velocityRatio;
    };

    public enum JogCmd
    {
        JogIdle,
        JogAPPressed,
        JogANPressed,
        JogBPPressed,
        JogBNPressed,
        JogCPPressed,
        JogCNPressed,
        JogDPPressed,
        JogDNPressed,
        JogGrab,
        JogRelease,
        JogGPPressed,
        JogGNPressed,
        JogLaserOn,
        JogLaserOff
    };

    public struct JogInstantCmd
    {
        public byte isJoint;
        public JogCmd cmd;
    };

    public struct PlaybackStaticParams
    {
        public float jointMaxVelocity;
        public float jointMaxAcceleration;
        public float servoMaxVelocity;
        public float servoMaxAcceleration;
        public float linearMaxVelocity;
        public float linearMaxAcceleration;
        public float pauseTime;
        public float jumpHeight;
    };

    public struct PlaybackDynamicParams
    {
        public float velocityRatio;
        public float accelerationRatio;
    };

    public enum PlaybackInstantCmd
    {
        PlaybackStart,
        PlaybackPause,
        PlaybackStop
    };

    public struct PlaybackPoint
    {
        public byte motionStyle;
        public byte isGrab;
        public float x;
        public float y;
        public float z;
        public float rHead;
        public float gripper;
        public float pauseTime;
    };

    public struct PlaybackBufferCmd
    {
        public PlaybackPoint playbackPoint;
    };

    public enum DobotResult
    {
        DobotResult_NoError,
        DobotResult_Warning_Min,
        DobotResult_Sensor1Warning = DobotResult_Warning_Min,
        DobotResult_Sensor2Warning,
        DobotResult_Sensor12Warning,
        DobotResult_Warning_Max = DobotResult_Sensor12Warning,

        DobotResult_Error_Min,
        DobotResult_NotFound = DobotResult_Error_Min,
        DobotResult_Occupied,
        DobotResult_NoDataUploaded,
        DobotResult_Timeout,
        DobotResult_Error_Max = DobotResult_Timeout
    };
}
