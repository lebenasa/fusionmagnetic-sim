#############################################################################
# Makefile for building: bin/magnetic
# Generated by qmake (3.0) (Qt 5.4.1)
# Project:  MAGNETIC.pro
# Template: app
# Command: /home/leben/Qt5.4.1/5.4/gcc_64/bin/qmake -spec linux-g++ -o Makefile MAGNETIC.pro
#############################################################################

MAKEFILE      = Makefile

####### Compiler, tools and options

CC            = gcc
CXX           = g++
DEFINES       = -DQT_NO_DEBUG
CFLAGS        = -pipe -O2 -Wall -W -D_REENTRANT -fPIE $(DEFINES)
CXXFLAGS      = -pipe -O2 -std=c++0x -Wall -W -D_REENTRANT -fPIE $(DEFINES)
INCPATH       = -I. -Isrc/core -I../../Qt5.4.1/5.4/gcc_64/mkspecs/linux-g++
QMAKE         = /home/leben/Qt5.4.1/5.4/gcc_64/bin/qmake
DEL_FILE      = rm -f
CHK_DIR_EXISTS= test -d
MKDIR         = mkdir -p
COPY          = cp -f
COPY_FILE     = cp -f
COPY_DIR      = cp -f -R
INSTALL_FILE  = install -m 644 -p
INSTALL_PROGRAM = install -m 755 -p
INSTALL_DIR   = $(COPY_DIR)
DEL_FILE      = rm -f
SYMLINK       = ln -f -s
DEL_DIR       = rmdir
MOVE          = mv -f
TAR           = tar -cf
COMPRESS      = gzip -9f
DISTNAME      = magnetic1.0.0
DISTDIR = /home/leben/Labs/magnetic/.tmp/magnetic1.0.0
LINK          = g++
LFLAGS        = -Wl,-O1 -Wl,-rpath,/home/leben/Qt5.4.1/5.4/gcc_64
LIBS          = $(SUBLIBS) -lpthread 
AR            = ar cqs
RANLIB        = 
SED           = sed
STRIP         = strip

####### Output directory

OBJECTS_DIR   = ./

####### Files

SOURCES       = src/main.cpp \
		src/application.cpp \
		src/fields.cpp \
		src/simulator.cpp 
OBJECTS       = main.o \
		application.o \
		fields.o \
		simulator.o
DIST          = ../../Qt5.4.1/5.4/gcc_64/mkspecs/features/spec_pre.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/common/shell-unix.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/common/unix.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/common/linux.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/common/gcc-base.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/common/gcc-base-unix.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/common/g++-base.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/common/g++-unix.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/qconfig.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_bluetooth.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_bluetooth_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_bootstrap_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_clucene_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_concurrent.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_concurrent_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_core.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_core_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_dbus.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_dbus_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_declarative.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_declarative_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_designer.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_designer_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_designercomponents_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_enginio.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_enginio_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_gui.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_gui_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_help.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_help_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_location.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_location_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_multimedia.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_multimedia_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_multimediawidgets.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_multimediawidgets_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_network.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_network_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_nfc.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_nfc_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_opengl.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_opengl_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_openglextensions.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_openglextensions_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_platformsupport_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_positioning.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_positioning_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_printsupport.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_printsupport_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qml.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qml_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qmldevtools_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qmltest.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qmltest_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qtmultimediaquicktools_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quick.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quick_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quickparticles_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quickwidgets.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quickwidgets_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_script.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_script_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_scripttools.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_scripttools_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_sensors.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_sensors_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_serialport.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_serialport_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_sql.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_sql_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_svg.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_svg_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_testlib.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_testlib_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_uitools.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_uitools_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webchannel.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webchannel_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webengine.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webengine_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webenginecore.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webenginecore_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webenginewidgets.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webenginewidgets_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webkit.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webkit_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webkitwidgets.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webkitwidgets_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_websockets.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_websockets_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webview.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webview_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_widgets.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_widgets_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_x11extras.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_x11extras_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_xml.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_xml_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_xmlpatterns.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_xmlpatterns_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/qt_functions.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/qt_config.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/linux-g++/qmake.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/spec_post.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/exclusive_builds.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/default_pre.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/resolve_config.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/default_post.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/precompile_header.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/c++11.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/c++14.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/warn_on.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/qt.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/unix/thread.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/testcase_targets.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/exceptions.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/yacc.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/lex.prf \
		MAGNETIC.pro src/application.h \
		src/fields.h \
		src/simulator.h \
		src/rk54.h src/main.cpp \
		src/application.cpp \
		src/fields.cpp \
		src/simulator.cpp
QMAKE_TARGET  = magnetic
DESTDIR       = bin/#avoid trailing-slash linebreak
TARGET        = bin/magnetic


first: all
####### Implicit rules

.SUFFIXES: .o .c .cpp .cc .cxx .C

.cpp.o:
	$(CXX) -c -include magnetic $(CXXFLAGS) $(INCPATH) -o "$@" "$<"

.cc.o:
	$(CXX) -c -include magnetic $(CXXFLAGS) $(INCPATH) -o "$@" "$<"

.cxx.o:
	$(CXX) -c -include magnetic $(CXXFLAGS) $(INCPATH) -o "$@" "$<"

.C.o:
	$(CXX) -c -include magnetic $(CXXFLAGS) $(INCPATH) -o "$@" "$<"

.c.o:
	$(CC) -c -include magnetic $(CFLAGS) $(INCPATH) -o "$@" "$<"

####### Build rules

$(TARGET):  $(OBJECTS)  
	@test -d bin/ || mkdir -p bin/
	$(LINK) $(LFLAGS) -o $(TARGET) $(OBJECTS) $(OBJCOMP) $(LIBS)

Makefile: MAGNETIC.pro ../../Qt5.4.1/5.4/gcc_64/mkspecs/linux-g++/qmake.conf ../../Qt5.4.1/5.4/gcc_64/mkspecs/features/spec_pre.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/common/shell-unix.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/common/unix.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/common/linux.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/common/gcc-base.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/common/gcc-base-unix.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/common/g++-base.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/common/g++-unix.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/qconfig.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_bluetooth.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_bluetooth_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_bootstrap_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_clucene_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_concurrent.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_concurrent_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_core.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_core_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_dbus.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_dbus_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_declarative.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_declarative_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_designer.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_designer_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_designercomponents_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_enginio.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_enginio_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_gui.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_gui_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_help.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_help_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_location.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_location_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_multimedia.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_multimedia_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_multimediawidgets.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_multimediawidgets_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_network.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_network_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_nfc.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_nfc_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_opengl.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_opengl_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_openglextensions.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_openglextensions_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_platformsupport_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_positioning.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_positioning_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_printsupport.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_printsupport_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qml.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qml_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qmldevtools_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qmltest.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qmltest_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qtmultimediaquicktools_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quick.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quick_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quickparticles_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quickwidgets.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quickwidgets_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_script.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_script_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_scripttools.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_scripttools_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_sensors.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_sensors_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_serialport.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_serialport_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_sql.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_sql_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_svg.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_svg_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_testlib.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_testlib_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_uitools.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_uitools_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webchannel.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webchannel_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webengine.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webengine_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webenginecore.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webenginecore_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webenginewidgets.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webenginewidgets_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webkit.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webkit_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webkitwidgets.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webkitwidgets_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_websockets.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_websockets_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webview.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webview_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_widgets.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_widgets_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_x11extras.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_x11extras_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_xml.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_xml_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_xmlpatterns.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_xmlpatterns_private.pri \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/qt_functions.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/qt_config.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/linux-g++/qmake.conf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/spec_post.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/exclusive_builds.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/default_pre.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/resolve_config.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/default_post.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/precompile_header.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/c++11.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/c++14.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/warn_on.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/qt.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/unix/thread.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/testcase_targets.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/exceptions.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/yacc.prf \
		../../Qt5.4.1/5.4/gcc_64/mkspecs/features/lex.prf \
		MAGNETIC.pro
	$(QMAKE) -spec linux-g++ -o Makefile MAGNETIC.pro
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/spec_pre.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/common/shell-unix.conf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/common/unix.conf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/common/linux.conf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/common/gcc-base.conf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/common/gcc-base-unix.conf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/common/g++-base.conf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/common/g++-unix.conf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/qconfig.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_bluetooth.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_bluetooth_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_bootstrap_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_clucene_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_concurrent.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_concurrent_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_core.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_core_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_dbus.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_dbus_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_declarative.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_declarative_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_designer.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_designer_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_designercomponents_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_enginio.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_enginio_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_gui.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_gui_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_help.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_help_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_location.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_location_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_multimedia.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_multimedia_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_multimediawidgets.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_multimediawidgets_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_network.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_network_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_nfc.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_nfc_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_opengl.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_opengl_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_openglextensions.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_openglextensions_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_platformsupport_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_positioning.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_positioning_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_printsupport.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_printsupport_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qml.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qml_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qmldevtools_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qmltest.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qmltest_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_qtmultimediaquicktools_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quick.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quick_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quickparticles_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quickwidgets.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_quickwidgets_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_script.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_script_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_scripttools.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_scripttools_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_sensors.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_sensors_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_serialport.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_serialport_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_sql.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_sql_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_svg.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_svg_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_testlib.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_testlib_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_uitools.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_uitools_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webchannel.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webchannel_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webengine.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webengine_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webenginecore.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webenginecore_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webenginewidgets.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webenginewidgets_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webkit.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webkit_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webkitwidgets.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webkitwidgets_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_websockets.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_websockets_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webview.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_webview_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_widgets.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_widgets_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_x11extras.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_x11extras_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_xml.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_xml_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_xmlpatterns.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/modules/qt_lib_xmlpatterns_private.pri:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/qt_functions.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/qt_config.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/linux-g++/qmake.conf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/spec_post.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/exclusive_builds.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/default_pre.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/resolve_config.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/default_post.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/precompile_header.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/c++11.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/c++14.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/warn_on.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/qt.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/unix/thread.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/testcase_targets.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/exceptions.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/yacc.prf:
../../Qt5.4.1/5.4/gcc_64/mkspecs/features/lex.prf:
MAGNETIC.pro:
qmake: FORCE
	@$(QMAKE) -spec linux-g++ -o Makefile MAGNETIC.pro

qmake_all: FORCE


all: Makefile $(TARGET)

dist: distdir FORCE
	(cd `dirname $(DISTDIR)` && $(TAR) $(DISTNAME).tar $(DISTNAME) && $(COMPRESS) $(DISTNAME).tar) && $(MOVE) `dirname $(DISTDIR)`/$(DISTNAME).tar.gz . && $(DEL_FILE) -r $(DISTDIR)

distdir: FORCE
	@test -d $(DISTDIR) || mkdir -p $(DISTDIR)
	$(COPY_FILE) --parents $(DIST) $(DISTDIR)/


clean:compiler_clean 
	-$(DEL_FILE) $(OBJECTS)
	-$(DEL_FILE) magnetic.gch/c magnetic.gch/c++
	-$(DEL_FILE) *~ core *.core


distclean: clean 
	-$(DEL_FILE) $(TARGET) 
	-$(DEL_FILE) Makefile


####### Sub-libraries

###### Precompiled headers
magnetic.gch/c: src/precompiled.h src/core/simulatorlib.hpp \
		src/core/simulation.hpp
	@test -d magnetic.gch/ || mkdir -p magnetic.gch/
	$(CC) $(CFLAGS) $(INCPATH) -x c-header -c src/precompiled.h -o magnetic.gch/c

magnetic.gch/c++: src/precompiled.h src/core/simulatorlib.hpp \
		src/core/simulation.hpp
	@test -d magnetic.gch/ || mkdir -p magnetic.gch/
	$(CXX) $(CXXFLAGS) $(INCPATH) -x c++-header -c src/precompiled.h -o magnetic.gch/c++

check: first

compiler_no_pch_compiler_make_all:
compiler_no_pch_compiler_clean:
compiler_yacc_decl_make_all:
compiler_yacc_decl_clean:
compiler_yacc_impl_make_all:
compiler_yacc_impl_clean:
compiler_lex_make_all:
compiler_lex_clean:
compiler_clean: 

####### Compile

main.o: src/main.cpp src/application.h \
		src/precompiled.h \
		src/core/simulatorlib.hpp \
		src/core/simulation.hpp \
		src/simulator.h \
		src/fields.h \
		src/rk54.h \
		magnetic.gch/c++
	$(CXX) -c -include magnetic $(CXXFLAGS) $(INCPATH) -o main.o src/main.cpp

application.o: src/application.cpp src/application.h \
		src/precompiled.h \
		src/core/simulatorlib.hpp \
		src/core/simulation.hpp \
		src/simulator.h \
		src/fields.h \
		src/rk54.h \
		magnetic.gch/c++
	$(CXX) -c -include magnetic $(CXXFLAGS) $(INCPATH) -o application.o src/application.cpp

fields.o: src/fields.cpp src/fields.h \
		src/core/simulation.hpp \
		src/core/simulatorlib.hpp \
		magnetic.gch/c++
	$(CXX) -c -include magnetic $(CXXFLAGS) $(INCPATH) -o fields.o src/fields.cpp

simulator.o: src/simulator.cpp src/simulator.h \
		src/precompiled.h \
		src/core/simulatorlib.hpp \
		src/core/simulation.hpp \
		src/fields.h \
		src/rk54.h \
		magnetic.gch/c++
	$(CXX) -c -include magnetic $(CXXFLAGS) $(INCPATH) -o simulator.o src/simulator.cpp

####### Install

install:   FORCE

uninstall:   FORCE

FORCE:

