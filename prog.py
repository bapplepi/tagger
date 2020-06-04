import io
import logging
import os
import time
import typing

import eyed3
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QDir, QSortFilterProxyModel, QModelIndex, QRegExp
from PyQt5.QtGui import QPalette, QStandardItemModel
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMenu, QAction, QFileDialog, QListView, \
    QFileSystemModel, QHBoxLayout, QTreeView, QHeaderView, QAbstractItemView


class mp3fileSystem(QFileSystemModel):

    # https://stackoverflow.com/questions/19690998/pyqt-adding-a-custom-column-to-qfilesystemmodel
    def columnCount(self, parent=QtCore.QModelIndex()):
        return super(mp3fileSystem, self).columnCount() + 2

    def data(self, index, role=Qt.DisplayRole):

        if 6 > index.column() > 0:
            if role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignCenter

            if role == QtCore.Qt.DisplayRole:
                info = self.fileInfo(index)
                if info.completeSuffix() == 'mp3':
                    song = eyed3.load(info.filePath())
                    if index.column() == 1:
                        return song.tag.title
                    if index.column() == 2:
                        artists = song.tag.artist.replace(';', '\n')
                        return artists
                    if index.column() == 3:
                        return song.tag.album
                    if index.column() == 4:
                        return song.tag.album_artist
                    if index.column() == 5:
                        return song.tag.track_num

                return ''

        elif index.column() > 1:
            return super(mp3fileSystem, self).data(self.createIndex(index.row(), index.column() - 5, index.internalId()), role)

        else:
            return super(mp3fileSystem, self).data(self.createIndex(index.row(), index.column(), index.internalId()), role)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        if section == 0 and role == 0:
            return 'File'
        if section == 1 and role == 0:
            return 'Name'
        if section == 2 and role == 0:
            return 'Contributing Artists'
        if section == 3 and role == 0:
            return 'Album'
        if section == 4 and role == 0:
            return 'Album Artist'
        if section == 5 and role == 0:
            return 'Track No.'

        return super(mp3fileSystem, self).headerData(section, orientation, role)


class window(QMainWindow):

    def editItem(self, point):
        print('f')
        index = self.songsView.indexAt(point)
        if index.column() == 0:
            self.songsView.edit(index)

    def mouseReleaseEvent(self, event):
        print('hey')
        self.editItem(event.localPos())

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            pos = event.pos()
            print('hey')
            self.editItem(event.localPos())
            return True
        return super(window, self).eventFilter(obj, event)


    def initUI(self):
        self.setGeometry(200, 200, 1400, 800)
        self.setWindowTitle('ヤバすぎる痛みを与えてやる')

        self.fileModel = mp3fileSystem()
        self.fileModel.setRootPath(QDir.rootPath())

        self.filteredFiles = QSortFilterProxyModel()
        self.filteredFiles.setSourceModel(self.fileModel)
        self.filteredFiles.setFilterRegExp('Folder|mp3')
        self.filteredFiles.setFilterKeyColumn(7)

        self.songsView = QTreeView()
        self.layout().addWidget(self.songsView)

        self.songsView.setSortingEnabled(True)
        self.songsView.setGeometry(0, 40, 1400, 760)

        self.songsView.setModel(self.filteredFiles)

        self.songsView.setRootIndex(self.filteredFiles.mapFromSource(self.fileModel.index('C:/Users/Prime/Music')))

        self.songsView.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.songsView.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.songsView.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.songsView.header().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.songsView.header().setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.songsView.header().setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.setCentralWidget(self.songsView)

        self.songsView.setEditTriggers(QTreeView.NoEditTriggers)
        self.fileModel.setReadOnly(False)

        #self.songsView.installEventFilter(self)

        self.statusBar()

        self.show()

    '''def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        selected = self.songsView.selectedIndexes()
        tag = self.songsView.columnAt(event.x())
        print(tag)'''

    def __init__(self):
        super().__init__()

        self.initUI()


def main():
    app = QApplication([])

    log_stream = io.StringIO()
    logging.basicConfig(stream=log_stream, level=logging.INFO)

    w = window()
    w.show()
    app.exec_()


main()
