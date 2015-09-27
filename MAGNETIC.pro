TEMPLATE = app
QT -= core gui
TARGET = magnetic
CONFIG += c++11 precompile_header

INCLUDEPATH += src/core/

PRECOMPILED_HEADER = src/precompiled.h
HEADERS = src/application.h src/fields.h src/simulator.h \
    src/rk54.h
SOURCES = src/main.cpp src/application.cpp src/fields.cpp \
          src/simulator.cpp

DESTDIR = bin/
