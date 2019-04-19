using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;

namespace DobotClientDemo.CPlusDll
{
    public class DobotDll
    {
        [DllImport("DobotDll.dll", EntryPoint = "ConnectDobot", CallingConvention = CallingConvention.Winapi)]
        public static extern int ConnectDobot();


        [DllImport("DobotDll.dll", EntryPoint = "DisconnectDobot", CallingConvention = CallingConvention.Cdecl)]
        public static extern void DisconnectDobot();


        [DllImport("DobotDll.dll", EntryPoint = "ResetDobot", CallingConvention = CallingConvention.Cdecl)]
        public static extern void ResetDobot();


        [DllImport("DobotDll.dll", EntryPoint = "PeriodicTask", CallingConvention = CallingConvention.Cdecl)]
        public static extern void PeriodicTask();


        [DllImport("DobotDll.dll", EntryPoint = "SetCmdTimeout", CallingConvention = CallingConvention.Cdecl)]
        public static extern int SetCmdTimeout(uint ms);


        // public static extern functions
        [DllImport("DobotDll.dll", EntryPoint = "SetEndType", CallingConvention = CallingConvention.Cdecl)]
        public static extern int SetEndType(EndType type);


        // InitialPose
        [DllImport("DobotDll.dll", EntryPoint = "SetInitialPose", CallingConvention = CallingConvention.Cdecl)]
        public static extern int SetInitialPose(ref InitialPose initialPose);


        [DllImport("DobotDll.dll", EntryPoint = "GetPose", CallingConvention = CallingConvention.Cdecl)]
        public static extern int GetPose(ref Pose pose);


        [DllImport("DobotDll.dll", EntryPoint = "SetJogStaticParams", CallingConvention = CallingConvention.Cdecl)]
        public static extern int SetJogStaticParams(ref JogStaticParams jogStaticParams);


        [DllImport("DobotDll.dll", EntryPoint = "SetJogDynamicParams", CallingConvention = CallingConvention.Cdecl)]
        public static extern int SetJogDynamicParams(ref JogDynamicParams jogDynamicParams);


        [DllImport("DobotDll.dll", EntryPoint = "SetJogInstantCmd", CallingConvention = CallingConvention.Cdecl)]
        public static extern int SetJogInstantCmd(ref JogInstantCmd jogInstantCmd);


        [DllImport("DobotDll.dll", EntryPoint = "SetPlaybackStaticParams", CallingConvention = CallingConvention.Cdecl)]
        public static extern int SetPlaybackStaticParams(ref PlaybackStaticParams playbackStaticParams);

        [DllImport("DobotDll.dll", EntryPoint = "SetPlaybackDynamicParams", CallingConvention = CallingConvention.Cdecl)]
        public static extern int SetPlaybackDynamicParams(ref PlaybackDynamicParams playbackDynamicParams);


        [DllImport("DobotDll.dll", EntryPoint = "SetPlaybackBufferCmd", CallingConvention = CallingConvention.Cdecl)]
        public static extern int SetPlaybackBufferCmd(ref PlaybackBufferCmd playbackBufferCmd);
    }
}
