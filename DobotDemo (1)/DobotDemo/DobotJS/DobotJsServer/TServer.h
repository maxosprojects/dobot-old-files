#ifndef TSERVER_H
#define TSERVER_H

#include <QObject>
#include <QTcpServer>
#include <QTcpSocket>

class TServer:public QObject
{
    Q_OBJECT

public:
    TServer();
    void Start(void);

signals:
    void processIO(void);

private slots:
    void  OnProcessConnection(void);
    void  OnProcessText(void);
    void  OnProcessIO(void);

private:
    char Checksum(char *buf, int len);
    void timerEvent(QTimerEvent *event);

private:
    QTcpServer  m_listenSocket;  // 侦听套接字
    QTcpSocket  *m_readWriteSocket;//读写套接字
    QByteArray  m_buffer;

    int m_periodicTimer;
    int m_poseTimer;
};

#endif // TSERVER_H
