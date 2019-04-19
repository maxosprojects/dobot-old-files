#include "TServer.h"
#include <QDebug>
#include "tservertype.h"
#include "DobotDll.h"
#include <QTimerEvent>

TServer::TServer()
{
    m_buffer.clear();
    m_periodicTimer = 0;
    m_poseTimer = 0;
    connect(this, SIGNAL(processIO()), this, SLOT(OnProcessIO()));
}

void TServer::Start(void)
{
    qDebug() << "TServer: Start listen prot 8881";
    m_listenSocket.listen(QHostAddress::Any, 8881);
    m_listenSocket.setMaxPendingConnections(10); // 只允许一个连接
    QObject::connect(&m_listenSocket,SIGNAL(newConnection()),this,SLOT(OnProcessConnection()));
}

// mcuisp校验和计算
char TServer::Checksum(char *buf, int len)
{
    char sum = buf[0];
    for(int i = 1; i < len; i++)
    {
        sum ^= buf[i];
    }
    return sum;
}

void TServer::timerEvent(QTimerEvent *event)
{
    if(event->timerId() == m_periodicTimer)
    {
        PeriodicTask();
    }
    else if(event->timerId() == m_poseTimer)
    {
        Pose pose;
        GetPose(&pose);

        struct package pkg;
        pkg.cmd = GETPOSE;
        memcpy(pkg.buf, &pose, sizeof(Pose));
        m_readWriteSocket->write((char *)&pkg, sizeof(struct package));
    }
}

void TServer::OnProcessConnection()
{
    qDebug() << "TServer: New connnection established";
    m_readWriteSocket = m_listenSocket.nextPendingConnection();
    m_buffer.clear();
    QObject::connect(m_readWriteSocket,SIGNAL(readyRead()),this,SLOT(OnProcessText()));
}

void TServer::OnProcessText()
{
    m_buffer.append(m_readWriteSocket->readAll());
    emit processIO(); // 有数据收到，开始处理IO命令
    //qDebug() << "TServer: Get Data";
}

void TServer::OnProcessIO(void)
{
    int pkgLen = sizeof(struct package);
    while(true)
    {
        if(m_buffer.size() < pkgLen)
            return;

        struct package pkg;
        memcpy(&pkg, m_buffer.data(), pkgLen);
        m_buffer.remove(0, pkgLen);

        switch (pkg.cmd) {
        case CONNECTDOBOT:
        {
            DobotResult ret = (DobotResult)ConnectDobot();

            struct package pkg;
            pkg.cmd = CONNECTDOBOT;
            memcpy(pkg.buf, &ret, 4);
            m_readWriteSocket->write((char *)&pkg, pkgLen);
            qDebug() << "TServer: Connect result " << ret;
        }break;
        case DISCONNECTDOBOT:
            DisconnectDobot();
            qDebug() << "TServer: DisconnectDobot";
            break;
        case RESETDOBOT:
            ResetDobot();
            qDebug() << "TServer: ResetDobot";
            break;
        case PERIODICTACK:
        {
            qint32 ptime = 0;
            memcpy(&ptime, pkg.buf, 4);
            if(ptime == 0 )
            {
                if(m_periodicTimer != 0)
                {
                    killTimer(m_periodicTimer);
                    m_periodicTimer = 0;
                }
                PeriodicTask();
                qDebug() << "TServer: PeriodicTask";
            }
            else
            {
                if(m_periodicTimer != 0)
                {
                    killTimer(m_periodicTimer);
                    m_periodicTimer = 0;
                }
                m_periodicTimer = startTimer(ptime);
                qDebug() << "TServer: PeriodicTask interval " << ptime;
            }
        }break;
        case SETCMDTIMEOUT:
        {
            qint32 time = 0;
            memcpy(&time, pkg.buf, 4);
            SetCmdTimeout(time);
            qDebug() << "TServer: SetCmdTimeout time[" << time << "]";
        }break;
        case SETENDTYPE:
            qint32 endType;
            memcpy(&endType, pkg.buf, 4);
            SetEndType((EndType)endType);
            qDebug() << "TServer: SetEndType endType[" << endType << "]";
            break;
        case SETINITIALPOSE:
            InitialPose initPose;
            memcpy(&initPose, pkg.buf, sizeof(InitialPose));
            SetInitialPose(&initPose);
            qDebug() << "TServer: SetInitialPose joint2Angle:" << initPose.joint2Angle << ",joint3Angle:" << initPose.joint3Angle;
            break;
        case GETPOSE:
        {
            qint32 otime = 0;
            memcpy(&otime, pkg.buf, 4);
            if(otime == 0 )
            {
                if(m_poseTimer != 0)
                {
                    killTimer(m_poseTimer);
                    m_poseTimer = 0;
                }
                Pose pose;
                GetPose(&pose);

                struct package pkg;
                pkg.cmd = GETPOSE;
                memcpy(pkg.buf, &pose, sizeof(Pose));
                m_readWriteSocket->write((char *)&pkg, pkgLen);
                qDebug() << "TServer: GetPose";
            }
            else
            {
                if(m_poseTimer != 0)
                {
                    killTimer(m_poseTimer);
                    m_poseTimer = 0;
                }
                m_poseTimer = startTimer(otime);
                qDebug() << "TServer: GetPose interval " << otime;
            }
        }break;
        case SETJOGSTATICPARAMS:
            JogStaticParams jsParam;
            memcpy(&jsParam, pkg.buf, sizeof(JogStaticParams));
            SetJogStaticParams(&jsParam);
            qDebug() << "TServer: SetJogStaticParams";
            break;
        case SETJOGDYNAMICPARAMS:
            JogDynamicParams jdParam;
            memcpy(&jdParam, pkg.buf, sizeof(JogDynamicParams));
            SetJogDynamicParams(&jdParam);
            qDebug() << "TServer: SetJogDynamicParams velocityRatio:" << jdParam.velocityRatio;
            break;
        case SETJOGINSTANTCMD:
            JogInstantCmd cmdParam;
            cmdParam.isJoint = pkg.buf[0];
            memcpy(&cmdParam.cmd, &pkg.buf[1], 4);
            SetJogInstantCmd(&cmdParam);
            qDebug() << "TServer: SetJogInstantCmd isJoint" << cmdParam.isJoint << ",cmd：" << cmdParam.cmd;
            break;
        case SETPLAYBACKSTATICPARAMS:
            PlaybackStaticParams pbsParam;
            memcpy(&pbsParam, pkg.buf, sizeof(PlaybackStaticParams));
            SetPlaybackStaticParams(&pbsParam);
            qDebug() << "TServer: PlaybackStaticParams";
            break;
        case SETPLAYBACKDYNAMICPARAMS:
            PlaybackDynamicParams pbdParam;
            memcpy(&pbdParam, pkg.buf, sizeof(PlaybackDynamicParams));
            SetPlaybackDynamicParams(&pbdParam);
            qDebug() << "TServer: PlaybackDynamicParams velocityRatio:" << pbdParam.velocityRatio << ",accelerationRatio:" << pbdParam.accelerationRatio;
            break;
        case SETPLAYBACKBUFFERCMD:
            PlaybackBufferCmd pbdbParam;
            pbdbParam.playbackPoint.motionStyle = pkg.buf[0];
            pbdbParam.playbackPoint.isGrab = pkg.buf[1];
            memcpy(&pbdbParam.playbackPoint.x, &pkg.buf[2], sizeof(PlaybackBufferCmd) - 2);
            SetPlaybackBufferCmd(&pbdbParam);
            qDebug() << "TServer: SetPlaybackBufferCmd";
            break;
        default:
            break;
        }
    }
}
