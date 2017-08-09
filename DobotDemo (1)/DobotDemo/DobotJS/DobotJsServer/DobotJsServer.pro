QT += core network
QT -= gui

CONFIG += c++11

TARGET = DobotJsServer
CONFIG += console
CONFIG -= app_bundle

TEMPLATE = app

SOURCES += main.cpp \
    TServer.cpp

HEADERS += \
    TServer.h \
    tservertype.h \
    DobotDll.h \
    DobotType.h


LIBS += debug/DobotDll.dll
