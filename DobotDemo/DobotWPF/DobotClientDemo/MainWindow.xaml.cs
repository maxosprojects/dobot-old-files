using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Threading;
using DobotClientDemo.CPlusDll;

namespace DobotClientDemo
{
    /// <summary>
    /// MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private byte isJoint = (byte)0;
        private bool isConnectted = false;
        private JogInstantCmd currentCmd;

        public MainWindow()
        {
            InitializeComponent();
            
            sld.Value = 30;
            sld.AddHandler(Slider.MouseLeftButtonUpEvent, new MouseButtonEventHandler(blurSlider_MouseLeftButtonUp), true);
            sld1.Value = 30;
            sld1.AddHandler(Slider.MouseLeftButtonUpEvent, new MouseButtonEventHandler(blurSlider_MouseLeftButtonUp), true);
            sldAcc.Value = 30;
            sldAcc.AddHandler(Slider.MouseLeftButtonUpEvent, new MouseButtonEventHandler(blurSlider_MouseLeftButtonUp), true);

            StartPeriodic();

            StartDobot();
        }

        /// <summary>
        /// StartDobot
        /// </summary>
        private void StartDobot()
        {
            int ret;

            // start connect
            if ((ret = DobotDll.ConnectDobot()) >= (int)DobotResult.DobotResult_Error_Min)
            {
                Msg("Connect error ,code:" + ret.ToString(), MsgInfoType.Error);
                return;
            }

            isConnectted = true;
            // reset and start
            //DobotDll.ResetDobot();
            DobotDll.SetCmdTimeout(500);
            DobotDll.SetEndType(EndType.EndTypePump);

            // Must set when sensor is not exist
            InitialPose initialPose;
            initialPose.joint2Angle = 45;
            initialPose.joint3Angle = 45;
            DobotDll.SetInitialPose(ref initialPose);


            JogStaticParams jsParam;
            jsParam.jointMaxVelocity = 15;
            jsParam.jointMaxAcceleration = 50;
            jsParam.servoMaxVelocity = 30;
            jsParam.servoMaxAcceleration = 10;
            jsParam.linearMaxVelocity = 40;
            jsParam.linearMaxAcceleration = 40;
            DobotDll.SetJogStaticParams(ref jsParam);

            JogDynamicParams jdParam;
            jdParam.velocityRatio = 30;
            DobotDll.SetJogDynamicParams(ref jdParam);

            PlaybackStaticParams pbsParam;
            pbsParam.jointMaxVelocity = 200;
            pbsParam.jointMaxAcceleration = 200;
            pbsParam.servoMaxVelocity = 200;
            pbsParam.servoMaxAcceleration = 200;
            pbsParam.linearMaxVelocity = 800;
            pbsParam.linearMaxAcceleration = 1000;
            pbsParam.pauseTime = 100;
            pbsParam.jumpHeight = 20;
            DobotDll.SetPlaybackStaticParams(ref pbsParam);

            PlaybackDynamicParams pbdParam;
            pbdParam.velocityRatio = 30;
            pbdParam.accelerationRatio = 30;
            DobotDll.SetPlaybackDynamicParams(ref pbdParam);
        }

        /// <summary>
        /// StartPeriodic
        /// </summary>
        private void StartPeriodic()
        {
            // start peridic cmd
            DispatcherTimer cmdTimer = new DispatcherTimer();
            cmdTimer.Interval = new TimeSpan(0, 0, 0, 0, 200);
            cmdTimer.Tick += CmdTimer_Tick;
            cmdTimer.Start();

            // start get pose peridic cmd
            DispatcherTimer posTimer = new DispatcherTimer();
            posTimer.Interval = new TimeSpan(0, 0, 0, 0, 600);
            posTimer.Tick += PosTimer_Tick;
            posTimer.Start();
        }

        private void PosTimer_Tick(object sender, EventArgs e)
        {
            if (!isConnectted)
                return;

            Pose pose = new Pose();
            DobotDll.GetPose(ref pose);

            tbJoint1Angle.Text = pose.jointAngle[0].ToString();
            tbJoint2Angle.Text = pose.jointAngle[1].ToString();
            tbJoint3Angle.Text = pose.jointAngle[2].ToString();
            tbJoint4Angle.Text = pose.jointAngle[3].ToString();

            if (sync.IsChecked == true)
            {
                isGrab.IsChecked = pose.isGrab == 1;
                X.Text = pose.x.ToString();
                Y.Text = pose.y.ToString();
                Z.Text = pose.z.ToString();
                rHead.Text = pose.rHead.ToString();
                pauseTime.Text = "0";
                isGripper.Text = pose.gripper.ToString();
            }

        }

        private void CmdTimer_Tick(object sender, EventArgs e)
        {
            // called in 200ms
            DobotDll.PeriodicTask();
        }

        // event handle
        private void ProcessEvt(object sender, EventArgs e)
        {
            if (!isConnectted)
                return;

            Button obj = (Button)sender;
            String con = obj.Content.ToString();
            switch(con)
            {
                case "SendPlaybackCmd":
                    {
                        PlaybackBufferCmd pdbCmd;
                        float x, y, z, r, gripper, pTime;

                        if (!float.TryParse(X.Text, out x) || !float.TryParse(Y.Text, out y) || !float.TryParse(Z.Text, out z) || !float.TryParse(rHead.Text, out r)
                            || !float.TryParse(isGripper.Text, out gripper) || !float.TryParse(pauseTime.Text, out pTime))
                        {
                            Msg("Please input float formate", MsgInfoType.Error);
                            return;
                        }
                        Msg("", MsgInfoType.Info);

                        pdbCmd.playbackPoint.isGrab = isGrab.IsChecked == true ? (byte)1 : (byte)0;
                        pdbCmd.playbackPoint.motionStyle = (byte)modeStyle.SelectedIndex;
                        pdbCmd.playbackPoint.x = x;
                        pdbCmd.playbackPoint.y = y;
                        pdbCmd.playbackPoint.z = z;
                        pdbCmd.playbackPoint.rHead = r;
                        pdbCmd.playbackPoint.gripper = gripper;
                        pdbCmd.playbackPoint.pauseTime = pTime;
                        DobotDll.SetPlaybackBufferCmd(ref pdbCmd);
                    }break;
                default:
                    break;
            }
        }

        // control event handle
        private void OnEvent(object sender, MouseButtonEventArgs e)
        {
            if (!isConnectted)
                return;

            Button obj = (Button)sender;
            String con = obj.Content.ToString();
            switch(con)
            {
                case "X+":
                case "Joint1+":
                    {
                        currentCmd.isJoint = isJoint;
                        currentCmd.cmd = e.ButtonState == MouseButtonState.Pressed? JogCmd.JogAPPressed : JogCmd.JogIdle;
                        DobotDll.SetJogInstantCmd(ref currentCmd);
                    }
                    break;
                case "X-":
                case "Joint1-":
                    {
                        currentCmd.isJoint = isJoint;
                        currentCmd.cmd = e.ButtonState == MouseButtonState.Pressed ? JogCmd.JogANPressed : JogCmd.JogIdle;
                        DobotDll.SetJogInstantCmd(ref currentCmd);
                    }
                    break;
                case "Y+":
                case "Joint2+":
                    {
                        currentCmd.isJoint = isJoint;
                        currentCmd.cmd = e.ButtonState == MouseButtonState.Pressed ? JogCmd.JogBPPressed : JogCmd.JogIdle;
                        DobotDll.SetJogInstantCmd(ref currentCmd);
                    }
                    break;
                case "Y-":
                case "Joint2-":
                    {
                        currentCmd.isJoint = isJoint;
                        currentCmd.cmd = e.ButtonState == MouseButtonState.Pressed ? JogCmd.JogBNPressed : JogCmd.JogIdle;
                        DobotDll.SetJogInstantCmd(ref currentCmd);
                    }
                    break;
                case "Z+":
                case "Joint3+":
                    {
                        currentCmd.isJoint = isJoint;
                        currentCmd.cmd = e.ButtonState == MouseButtonState.Pressed ? JogCmd.JogCPPressed : JogCmd.JogIdle;
                        DobotDll.SetJogInstantCmd(ref currentCmd);
                    }
                    break;
                case "Z-":
                case "Joint3-":
                    {
                        currentCmd.isJoint = isJoint;
                        currentCmd.cmd = e.ButtonState == MouseButtonState.Pressed ? JogCmd.JogCNPressed : JogCmd.JogIdle;
                        DobotDll.SetJogInstantCmd(ref currentCmd);
                    }
                    break;
                case "R+":
                case "Joint4+":
                    {
                        currentCmd.isJoint = isJoint;
                        currentCmd.cmd = e.ButtonState == MouseButtonState.Pressed ? JogCmd.JogDPPressed : JogCmd.JogIdle;
                        DobotDll.SetJogInstantCmd(ref currentCmd);
                    }
                    break;
                case "R-":
                case "Joint4-":
                    {
                        currentCmd.isJoint = isJoint;
                        currentCmd.cmd = e.ButtonState == MouseButtonState.Pressed ? JogCmd.JogDNPressed : JogCmd.JogIdle;
                        DobotDll.SetJogInstantCmd(ref currentCmd);
                    }
                    break;
                case "Gripper+":
                    {
                        currentCmd.isJoint = isJoint;
                        currentCmd.cmd = e.ButtonState == MouseButtonState.Pressed ? JogCmd.JogGPPressed : JogCmd.JogIdle;
                        DobotDll.SetJogInstantCmd(ref currentCmd);
                    }
                    break;
                case "Gripper-":
                    {
                        currentCmd.isJoint = isJoint;
                        currentCmd.cmd = e.ButtonState == MouseButtonState.Pressed ? JogCmd.JogGNPressed : JogCmd.JogIdle;
                        DobotDll.SetJogInstantCmd(ref currentCmd);
                    }
                    break;
                default: 
                    break;
            }
        }

        private void ComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (!isConnectted)
                return;

            ComboBox obj = (ComboBox)sender;
            String tag = obj.Tag.ToString();
            if(tag == "mode")
            {
                bool isJ = ((ComboBoxItem)obj.SelectedItem).Content.ToString() == "Axis";
                isJoint = isJ ? (byte)1 : (byte)0;
                if(isJ)
                {
                    XI.Content = "Joint1+";
                    YI.Content = "Joint2+";
                    ZI.Content = "Joint3+";
                    RI.Content = "Joint4+";

                    XN.Content = "Joint1-";
                    YN.Content = "Joint2-";
                    ZN.Content = "Joint3-";
                    RN.Content = "Joint4-";
                }
                else
                {
                    XI.Content = "X+";
                    YI.Content = "Y+";
                    ZI.Content = "Z+";
                    RI.Content = "R+";

                    XN.Content = "X-";
                    YN.Content = "Y-";
                    ZN.Content = "Z-";
                    RN.Content = "R-";
                }
            }
            else if(tag == "headType")
            {
                string str = ((ComboBoxItem)obj.SelectedItem).Content.ToString();
                if (str == "Pump")
                {
                    DobotDll.SetEndType(EndType.EndTypePump);
                    cbGrab.IsEnabled = true;
                    cbLaser.IsEnabled = false;
                    btnGrpOn.IsEnabled = false;
                    btnGrpOff.IsEnabled = false;
                }
                else if (str == "Gripper")
                {
                    cbGrab.IsEnabled = false;
                    cbLaser.IsEnabled = false;
                    btnGrpOn.IsEnabled = true;
                    btnGrpOff.IsEnabled = true;
                    DobotDll.SetEndType(EndType.EndTypeGripper);
                }
                else if (str == "Laser")
                {
                    cbGrab.IsEnabled = false;
                    cbLaser.IsEnabled = true;
                    btnGrpOn.IsEnabled = false;
                    btnGrpOff.IsEnabled = false;
                    DobotDll.SetEndType(EndType.EndTypeLaser);
                }
                
            }
        }

        private void Window_Closed(object sender, EventArgs e)
        {
            DobotDll.DisconnectDobot();
        }

        private void Msg(string str, MsgInfoType infoType)
        {
            lbTip.Content = str;
            switch(infoType)
            {
                case MsgInfoType.Error:
                    lbTip.Foreground = new SolidColorBrush(Colors.Red);
                    break;
                case MsgInfoType.Info:
                    lbTip.Foreground = new SolidColorBrush(Colors.Black);
                    break;
                default: 
                    break;
            }
        }

        private void CheckBox_Checked(object sender, RoutedEventArgs e)
        {
            if (!isConnectted)
                return;

            CheckBox obj = (CheckBox)sender;
            String con = obj.Content.ToString();

            if (con == "Grab") // grab
            {
                currentCmd.isJoint = isJoint;
                currentCmd.cmd = JogCmd.JogGrab;
                DobotDll.SetJogInstantCmd(ref currentCmd);
            }
            else if (con == "Laser") // Shutting
            {
                currentCmd.isJoint = isJoint;
                currentCmd.cmd = JogCmd.JogLaserOn;
                DobotDll.SetJogInstantCmd(ref currentCmd);
            }
        }

        private void CheckBox_Unchecked(object sender, RoutedEventArgs e)
        {
            if (!isConnectted)
                return;

            CheckBox obj = (CheckBox)sender;
            String con = obj.Content.ToString();

            if (con == "Grab") // cancel grab
            {
                currentCmd.isJoint = isJoint;
                currentCmd.cmd = JogCmd.JogRelease;
                DobotDll.SetJogInstantCmd(ref currentCmd);
            }
            else if (con == "Laser") // release laser
            {
                currentCmd.isJoint = isJoint;
                currentCmd.cmd = JogCmd.JogLaserOff;
                DobotDll.SetJogInstantCmd(ref currentCmd);
            }
        }

        private void blurSlider_MouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            if (!isConnectted)
                return;

            Slider obj = (Slider)sender;
            if (obj.Name == "sld")
            {
                JogDynamicParams jdParam;
                jdParam.velocityRatio = (float)sld.Value;
                DobotDll.SetJogDynamicParams(ref jdParam);
            }
            else if (obj.Name == "sld1" || obj.Name == "sldAcc") // playback
            {
                PlaybackDynamicParams pbdParam;
                pbdParam.velocityRatio = (float)obj.Value;
                pbdParam.accelerationRatio = (float)obj.Value;
                DobotDll.SetPlaybackDynamicParams(ref pbdParam);
            }
        }
    }
}
