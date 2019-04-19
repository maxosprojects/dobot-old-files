#ifndef DOBOTTYPE_H
#define DOBOTTYPE_H

#include <stdint.h>

/*********************************************************************************************************
** Types
*********************************************************************************************************/

/*
 * End type
 */
enum EndType {
    EndTypePump,
    EndTypeGripper,
    EndTypeLaser
};

/*
 * Initial pose
 */
typedef struct tagInitialPose {
    float joint2Angle;
    float joint3Angle;
}InitialPose;

/*
 * Pose
 */
typedef struct tagPose {
    float x;
    float y;
    float z;
    float rHead;
    float jointAngle[4];
    float isGrab;
    float gripper;
}Pose;

/*
 * Jog
 */
typedef struct tagJogStaticParams {
    float jointMaxVelocity;
    float jointMaxAcceleration;
    float servoMaxVelocity;
    float servoMaxAcceleration;
    float linearMaxVelocity;
    float linearMaxAcceleration;
}JogStaticParams;

typedef struct tagJogDynamicParams {
    float velocityRatio;
}JogDynamicParams;

/*
 * Jog Cmd
 */
enum JogCmd {
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

/*
 * Jog instant cmd
 */
typedef struct tagJogInstantCmd {
    uint8_t isJoint;
    enum JogCmd cmd;
}JogInstantCmd;

/*
 * Playback
 */
typedef struct tagPlaybackStaticParams {
    float jointMaxVelocity;
    float jointMaxAcceleration;
    float servoMaxVelocity;
    float servoMaxAcceleration;
    float linearMaxVelocity;
    float linearMaxAcceleration;
    float pauseTime;
    float jumpHeight;
}PlaybackStaticParams;

typedef struct tagPlaybackDynamicParams {
    float velocityRatio;
    float accelerationRatio;
}PlaybackDynamicParams;

enum PlaybackInstantCmd {
    PlaybackStart,
    PlaybackPause,
    PlaybackStop
};

// For play back
enum MotionStyle {
    JUMP,
    MOVJ,
    MOVL
};

typedef struct tagPlaybackPoint {
    uint8_t motionStyle;
    uint8_t isGrab;
    float x;
    float y;
    float z;
    float rHead;
    float gripper;
    float pauseTime;
}PlaybackPoint;

typedef struct tagPlaybackPointAngle {
    uint8_t motionStyle;
    uint8_t isGrab;
    float joint1;
    float joint2;
    float joint3;
    float joint4;
    float gripper;
    float pauseTime;
}PlaybackPointAngle;

typedef struct tagPlaybackBufferCmd {
    union {
        PlaybackPoint playbackPoint;
        PlaybackPointAngle playbackPointAngle;
    };
}PlaybackBufferCmd;

/*********************************************************************************************************
** API result
*********************************************************************************************************/

enum DobotResult {
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
    DobotResult_BufferFull,
    DobotResult_Timeout,
    DobotResult_Error_Max = DobotResult_Timeout
};

#endif
