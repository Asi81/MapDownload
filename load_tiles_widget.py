from PySide import QtGui, QtCore
from load_tiles_mainwin_pyside import Ui_LoadTilesWindow

import sys
import os
import download_handler





class LoadTilesWindow(QtGui.QMainWindow, Ui_LoadTilesWindow   ):


    def __init__(self):
        super(LoadTilesWindow,self).__init__()

        self.setupUi(self)
        self.load_kml_act.triggered.connect(self.onLoadKmlClicked)
        self.load_settings_act.triggered.connect(self.onLoadSettingsClicked)
        self.save_settings_act.triggered.connect(self.onSaveSettingsClicked)

        self.download_btn.clicked.connect(self.onDownloadBtnClicked)
        self.min_zoom_sl.valueChanged.connect(self.onMinZoomChanged)
        self.min_zoom_sb.valueChanged.connect(self.onMinZoomChanged)
        self.max_zoom_sl.valueChanged.connect(self.onMaxZoomChanged)
        self.max_zoom_sb.valueChanged.connect(self.onMaxZoomChanged)
        self.calc_tile_cnt_btn.clicked.connect(self.onCalcBtnClicked)
        self.select_folder_btn.clicked.connect(self.onSelectFolderClicked)

        self.folder_le.setText(os.path.join("C:\\Temp\\topomaps") )
        self.printf = self.printFunc()
        self.h = download_handler.DownloadHandler(self.printf)
        self.h.load()
        self.write_pars_to_widget()


    def write_pars_to_widget(self):
        self.project_le.setText(self.h.proj_name)
        self.west_sb.setValue(self.h.west)
        self.north_sb.setValue(self.h.north)
        self.east_sb.setValue(self.h.east)
        self.south_sb.setValue(self.h.south)
        self.min_zoom_sb.setValue(self.h.zoom1)
        self.min_zoom_sl.setValue(self.h.zoom1)
        self.max_zoom_sb.setValue(self.h.zoom2)
        self.max_zoom_sl.setValue(self.h.zoom2)
        self.folder_le.setText(os.path.join(self.h.proj_folder))


    def read_widget_pars(self):
        self.h.proj_name = self.project_le.text()
        self.h.north = self.north_sb.value()
        self.h.south = self.south_sb.value()
        self.h.west = self.west_sb.value()
        self.h.east = self.east_sb.value()
        self.h.zoom1 = self.min_zoom_sb.value()
        self.h.zoom2 = self.max_zoom_sb.value()
        self.h.proj_folder = self.folder_le.text()


    def onLoadKmlClicked(self):
        fname = QtGui.QFileDialog.getOpenFileName(self,"Open kml file","","Kml file (*.kml)")
        if fname:
            self.h.load_koordinates_from_kml(fname[0])
            self.write_pars_to_widget()

    def onLoadSettingsClicked(self):
        fname = QtGui.QFileDialog.getOpenFileName(self,"Open json file with settings","","Json file (*.json)")
        if fname:
            self.h.load(fname[0])
            self.write_pars_to_widget()
            self.printf("Settings loaded from %s" % fname[0])

    def onSaveSettingsClicked(self):
        fname = QtGui.QFileDialog.getSaveFileName (self,"Save json file with settings","","Json file (*.json)")
        if fname:
            self.read_widget_pars()
            self.h.save(fname[0])
            self.printf("Settings saved to %s" % fname[0])

    def onDownloadBtnClicked(self):
        self.read_widget_pars()
        self.h.save()
        if len(self.h.proj_name) == 0:
            QtGui.QMessageBox.critical(self,"Error","Project name is not defined")
            return
        self.h.download_tiles_and_make_kml()
        pass

    def onMinZoomChanged(self, val):
        if val > self.max_zoom_sl.value():
            self.max_zoom_sl.setValue(val)
            self.max_zoom_sb.setValue(val)

    def onMaxZoomChanged(self, val):
        if val < self.min_zoom_sl.value():
            self.min_zoom_sl.setValue(val)
            self.min_zoom_sb.setValue(val)

    def onCalcBtnClicked(self):
        self.read_widget_pars()
        self.h.print_tilecount()

    def onSelectFolderClicked(self):
        fld = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory","", QtGui.QFileDialog.ShowDirsOnly
                                                     | QtGui.QFileDialog.DontResolveSymlinks)
        if fld:
            self.folder_le.setText(fld)


    def printFunc(self):
        win = self
        def printf(arg:str,end = "\n"):
            while "\r" in arg:
                arg = arg[arg.index("\r")+1:]
                win.log_te.moveCursor(QtGui.QTextCursor.StartOfLine)
                while not win.log_te.textCursor().atEnd():
                    win.log_te.textCursor().deleteChar()
            win.log_te.insertPlainText(arg + end)

            QtCore.QCoreApplication.processEvents()
        return printf





app = QtGui.QApplication(sys.argv)
window = LoadTilesWindow()
printf = window.printFunc()
window.show()
error_code = app.exec_()
window.read_widget_pars()
window.h.save()
sys.exit(error_code)
