#ifndef DOBOTDLL_H
#define DOBOTDLL_H

#include "dobotdll_global.h"
#include "DobotType.h"

extern "C" DOBOTDLLSHARED_EXPORT int ConnectDobot(void);
extern "C" DOBOTDLLSHARED_EXPORT void DisconnectDobot(void);
extern "C" DOBOTDLLSHARED_EXPORT void ResetDobot(void);
extern "C" DOBOTDLLSHARED_EXPORT void PeriodicTask(void);
extern "C" DOBOTDLLSHARED_EXPORT int SetCmdTimeout(uint32_t cmdTimeout);
extern "C" DOBOTDLLSHARED_EXPORT int DobotExec(void);

// Public functions
// EndType
extern "C" DOBOTDLLSHARED_EXPORT int SetEndType(EndType endType);

// InitialPose
extern "C" DOBOTDLLSHARED_EXPORT int SetInitialPose(InitialPose *initialPose);

// Pose
extern "C" DOBOTDLLSHARED_EXPORT int GetPose(Pose *pose);

// Jog functions
extern "C" DOBOTDLLSHARED_EXPORT int SetJogStaticParams(JogStaticParams *jogStaticParams);
extern "C" DOBOTDLLSHARED_EXPORT int SetJogDynamicParams(JogDynamicParams *jogDynamicParams);
extern "C" DOBOTDLLSHARED_EXPORT int SetJogInstantCmd(JogInstantCmd *jogInstantCmd);

// Playback functions
extern "C" DOBOTDLLSHARED_EXPORT int SetPlaybackStaticParams(PlaybackStaticParams *playbackStaticParams);
extern "C" DOBOTDLLSHARED_EXPORT int SetPlaybackDynamicParams(PlaybackDynamicParams *playbackDynamicParams);
extern "C" DOBOTDLLSHARED_EXPORT int SetPlaybackBufferCmd(PlaybackBufferCmd *playbackBufferCmd);
extern "C" DOBOTDLLSHARED_EXPORT int SetPlaybackAngleBufferCmd(PlaybackBufferCmd *playbackBufferCmd);

#endif // DOBOTDLL_H
