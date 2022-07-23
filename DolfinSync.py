from PyQt5.QtWidgets import QTableWidgetItem, QMainWindow, QHeaderView, QFileDialog, QCheckBox, \
                            QWidget, QHBoxLayout, QVBoxLayout, QProgressBar, QApplication, \
                            QDialog, QLineEdit, QLabel, QPushButton, QAbstractItemView, \
                            QMessageBox, QListView, QTreeWidgetItem, QToolButton, QTreeView, QFileSystemModel, \
                            QTableView

from PyQt5 import uic
from PyQt5.QtGui import QIcon, QColor, QPainter, QPen, QPixmap, QStandardItemModel, QStandardItem,\
                        QPainterPath, QFont, QImageReader
from PyQt5.QtCore import Qt, QRect, QSortFilterProxyModel, QSettings, QEvent, QRegExp, QSize, \
                         QItemSelectionModel, QDateTime, QBuffer, QIODevice, QByteArray

import re,os,sys
from pathlib import Path
from peewee import *
import hashlib
from datetime import datetime, timezone
import requests
from PIL import Image
from PIL.ExifTags import TAGS
#import imagesize
from datetime import datetime
import time
import io

PROGRAM_NAME = "DolfinSync"
PROGRAM_VERSION = "0.0.1"

#DEFAULT_IP_ADDRESS = "222.233.253.74"
DEFAULT_IP_ADDRESS = "127.0.0.1"
DEFAULT_PORT = "8000"

RET_ALREADY_EXIST = 1
RET_UPLOAD_SUCCESS = 2
RET_UPLOAD_ERROR = 3

db = SqliteDatabase('dolfinsync.db')

class DolfinImageFile(Model):
    path = CharField()
    type = CharField()
    name = CharField()
    md5hash = CharField()
    uploaded = BooleanField()
    size = IntegerField()
    exifdatetime = DateTimeField()
    file_created = DateTimeField()
    file_modified = DateTimeField()
    parent = ForeignKeyField('self', backref='children', null=True)

    class Meta:
        database = db

class PreferencesDialog(QDialog):
    '''
    PreferencesDialog shows preferences.

    Args:
        None

    Attributes:
        well..
    '''
    def __init__(self,parent):
        super().__init__()
        self.setGeometry(QRect(100, 100, 400, 300))
        self.setWindowTitle("설정")
        #self.lbl_main_view.setMinimumSize(400, 300)

        self.parent = parent
        self.lblServerAddress = QLabel()
        self.edtServerAddress = QLineEdit()
        self.edtServerPort = QLineEdit()
        self.lblDataFolder = QLabel()
        self.edtDataFolder = QLineEdit()

        self.edtServerPort.setFixedWidth(50)

        self.btnDataFolder = QPushButton()
        self.btnDataFolder.setText("선택")
        self.btnDataFolder.clicked.connect(self.select_folder)

        self.btnOkay = QPushButton()
        self.btnOkay.setText("확인")
        self.btnOkay.clicked.connect(self.Okay)

        self.btnCancel = QPushButton()
        self.btnCancel.setText("취소")
        self.btnCancel.clicked.connect(self.Cancel)


        self.layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.lblServerAddress)
        self.layout1.addWidget(self.edtServerAddress)
        self.layout1.addWidget(self.edtServerPort)
        self.layout3 = QHBoxLayout()
        self.layout3.addWidget(self.lblDataFolder)
        self.layout3.addWidget(self.edtDataFolder)
        self.layout3.addWidget(self.btnDataFolder)
        self.layout4 = QHBoxLayout()
        self.layout4.addWidget(self.btnOkay)
        self.layout4.addWidget(self.btnCancel)
        self.layout.addLayout(self.layout1)
        #self.layout.addLayout(self.layout2)
        self.layout.addLayout(self.layout3)
        self.layout.addLayout(self.layout4)
        self.setLayout(self.layout)
        self.server_address = ''
        self.server_port = ''
        self.data_folder = ''
        #print("pref dlg data_folder:", self.data_folder)
        self.read_settings()
        #print("pref dlg data_folder:", self.data_folder)
        self.lblServerAddress.setText("서버 주소")
        #self.lblServerPort.setText("Server Port")
        self.lblDataFolder.setText("사진 위치")

        self.edtDataFolder.setText(str(self.data_folder.resolve()))
        self.edtServerAddress.setText(self.server_address)
        self.edtServerPort.setText(self.server_port)

    def write_settings(self):
        self.parent.server_address = self.edtServerAddress.text()
        self.parent.server_port = self.edtServerPort.text()
        self.parent.data_folder = Path(self.edtDataFolder.text())
        #print( self.parent.server_address,self.parent.server_port, self.parent.data_folder)

    def read_settings(self):
        self.server_address = self.parent.server_address
        self.server_port = self.parent.server_port
        self.data_folder = self.parent.data_folder.resolve()
        #print("pref dlg data folder:", self.data_folder)
        #print("pref dlg server address:", self.server_address)

    def Okay(self):
        self.write_settings()
        self.close()

    def Cancel(self):
        self.close()

    def select_folder(self):
        folder = str(QFileDialog.getExistingDirectory(self, "폴더 선택", str(self.data_folder)))
        if folder:
            self.data_folder = Path(folder).resolve()
            self.edtDataFolder.setText(folder)

class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        #self.setupUi(self)
        self.lbl_text = QLabel(self)
        self.lbl_text.setGeometry(50, 50, 320, 80)
        #self.pb_progress = QProgressBar(self)
        self.pb_progress = QProgressBar(self)
        self.pb_progress.setGeometry(50, 150, 320, 40)
        self.pb_progress.setValue(0)
        self.setGeometry(200, 200, 400, 250)

    def set_progress_text(self,text_format):
        self.text_format = text_format

    def set_max_value(self,max_value):
        self.max_value = max_value

    def set_curr_value(self,curr_value):
        self.curr_value = curr_value
        self.pb_progress.setValue(int((self.curr_value/float(self.max_value))*100))
        self.lbl_text.setText(self.text_format.format(self.curr_value, self.max_value))
        #self.lbl_text.setText(label_text)
        self.update()
        QApplication.processEvents()
    


form_class = uic.loadUiType("DolfinSync.ui")[0]
class DolfinSyncWindow(QMainWindow, form_class):

    def check_db(self):
        db.connect()
        tables = db.get_tables()
        if tables:
            return
            print(tables)
        else:
            db.create_tables([DolfinImageFile])
        
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.read_settings()
        self.check_db()
        #self.treeView = QTreeView()
        '''
        self.fileSystemModel = QFileSystemModel(self.treeView)
        self.fileSystemModel.setReadOnly(False)
        self.fileSystemModel.setNameFilters(["*.jpg"])
        root = self.fileSystemModel.setRootPath(str(self.data_folder))
        self.fileSystemModel.setNameFilterDisables(False)
        self.treeView.setModel(self.fileSystemModel)
        self.treeView.setRootIndex(root)
        self.treeView.setColumnWidth(0, 300)
        self.treeView.setColumnWidth(1, 100)
        self.treeView.setColumnHidden(2,True)
        self.treeView.setColumnHidden(3,True)
        '''
        self.actionPreferences.triggered.connect(self.open_preferences)

        #self.treeView.doubleClicked.connect(self.treeViewDoubleClicked)

        self.btnTest.clicked.connect(self.btnTestClicked)
        self.btnTest.hide()
        self.btnReadTree.clicked.connect(self.btnReadTreeClicked)
        self.btnLoadTree.clicked.connect(self.btnLoadTreeClicked)
        self.btnLoadTree.hide()
        self.btnSendImage.clicked.connect(self.btnSendImageClicked)
        self.btnSendImage.hide()
        self.btnSendAll.clicked.connect(self.btnSendAllClicked)
        self.btnOpenFolder.clicked.connect(self.select_folder)
        #self.data_folder = Path('.)
        self.edtServerAddress.textChanged.connect(self.address_changed)
        self.edtPortNumber.textChanged.connect(self.portno_changed)

        self.reset_views()

        self.dir_record_tree = []
        self.file_record_hash = {}
        self.dir_list = []
        self.file_list = []
        if self.data_folder != '':
            self.load_dir()
            self.edtDataFolder.setText(str(self.data_folder))
        self.setWindowTitle("DolfinSync")

    def btnTestClicked(self):
        print("server:", self.server_address)
        print("port:", self.server_port)
        print("data folder:", self.data_folder)

    def address_changed(self):
        self.server_address = self.edtServerAddress.text()

    def portno_changed(self):
        self.server_port = self.edtPortNumber.text()

    def select_folder(self):
        folder = str(QFileDialog.getExistingDirectory(self, "폴더 선택", str(self.data_folder)))
        if folder:
            self.data_folder = Path(folder).resolve()
            self.edtDataFolder.setText(folder)
            self.reset_database()

    def reset_views(self):

        self.dir_model = QStandardItemModel()
        self.file_model = QStandardItemModel()
        self.file_model.setColumnCount(2)
        self.treeView.setModel(self.dir_model)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.file_model)
        #self.listView.setModel(self.proxy_model)
        self.tableView.setModel(self.proxy_model)
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.tableView.hideColumn(1)
        self.tableView.setColumnWidth(0,300)
        self.tableView.verticalHeader().setDefaultSectionSize(15)
        #self.tableView.hideColumn(1)

        self.treeView.setHeaderHidden( True )
        self.tableView.horizontalHeader().hide()
        self.tableView.verticalHeader().hide()

        #self.treeView.expandAll()
        #print("__init__ dir model row count:", self.dir_model.rowCount())
        self.dirSelModel = self.treeView.selectionModel()
        self.dirSelModel.selectionChanged.connect(self.dirSelectionChanged)
        #self.fileSelModel = self.listView.selectionModel()
        #self.fileSelModel.selectionChanged.connect(self.fileSelectionChanged)
        self.fileSelModel = self.tableView.selectionModel()
        self.fileSelModel.selectionChanged.connect(self.fileSelectionChanged)

    def fileSelectionChanged(self):
        #print(self.tableView.rowHeight(3))
        #print(self.tableView.setRowHeight(3,20))
        return
        index = self.fileSelModel.currentIndex()
        print(index,index.row())
        item1 = self.file_model.item(index.row(),0)
        item2 = self.file_model.item(index.row(),1)
        print(item1.text(),item2.text() )

        index_list = self.fileSelModel.selection().indexes()
        print(index_list)
        item1 = self.file_model.itemFromIndex(index_list[0])
        print(item1, item1.text())
        #item2 = self.file_model.itemFromIndex(index_list[1])
        #print(item2, item2.text())


    def dirSelectionChanged(self):
        index_list = self.dirSelModel.selection().indexes()
        #print(index_list)
        item1 = self.dir_model.itemFromIndex(index_list[0])
        #print(item1, item1.text())
        item2 = self.dir_model.itemFromIndex(index_list[1])
        #print(item2, item2.text())
        filter_text = item2.text()
        #print(filter_text)
        #filter_text.replace("\\","\\\\")
        #print("filter text:", filter_text)

        self.proxy_model.setFilterRegExp(QRegExp('^'+filter_text+'$', Qt.CaseInsensitive))
        self.proxy_model.setFilterKeyColumn(1)
        #print()

    def load_subdir (self,item,children):
        #print("load subdir", item, children)
        for rec in children:
            if rec.type == 'file':
                sub_item1 = QStandardItem(Path(rec.path).name)
                sub_item2 = QStandardItem(str(Path(rec.path).parent.as_posix()))
                #print( sub_item1.text(), sub_item2.text() )
                self.file_model.appendRow([sub_item1,sub_item2])
                if rec.path not in self.file_record_hash.keys():
                    self.file_record_hash[rec.path] = rec
                #print("column count:", self.file_model.columnCount())
                #print(self.file_model.item(0,0).text(),self.file_model.item(0,1).text())
            else:
                sub_item1 = QStandardItem(Path(rec.path).name)
                sub_item2 = QStandardItem(str(Path(rec.path).as_posix()))
                #sub_item.setData(rec)
                item.appendRow([sub_item1,sub_item2])
                if rec.children:
                    self.load_subdir(sub_item1, rec.children)
        return
    
    def load_dir(self):
        all_record = DolfinImageFile.filter(type='dir',parent=None)

        for rec in all_record:
            #print(rec.path)
            #print("readdir 1 dir model row count:", self.dir_model.rowCount())
            item1 = QStandardItem(Path(rec.path).name)
            item2 = QStandardItem(rec.path)
            self.dir_model.appendRow([item1,item2] )
            if rec.children:
                self.load_subdir(item1,rec.children)
            #print("row count:", self.dir_model.rowCount())
            #if rec.parent == None:
            #    item1.expand
        #self.treeView.expandAll()
        self.treeView.hideColumn(1)
        self.treeView.collapseAll()
        self.treeView.expandToDepth(0)
        #self.listView.hideColumn(1)
        #self.treeView.setColumnWidth( 2, 50 )
            
        '''
        model = QStandardItemModel()
        parentItem = model.invisibleRootItem()
        for i in range(4):
            item = QStandardItem("item %d" % i)
            parentItem.appendRow(item)
            parentItem = item'''

    def get_selected_file(self):
        index = self.tableView.currentIndex()
        #print(index)

        selected_index_list = self.fileSelModel.selection().indexes()
        if len(selected_index_list) == 0:
            return
        #print("selected_index",selected_index_list)

        new_index_list = []
        model = selected_index_list[0].model()
        if hasattr(model, 'mapToSource'):
            for index in selected_index_list:
                new_index = model.mapToSource(index)
                new_index_list.append(new_index)
        #print("new_index_list",new_index_list)
        item_text_list = []
        for index in new_index_list:
            item = self.file_model.itemFromIndex(index)
            #print("item_text:",item.text())
            item_text_list.append(item.text())
        filepath = item_text_list[1]
        filename = item_text_list[0]
        return filepath, filename


    def upload_file(self,record):
        fullpath = record.path
        #print(fullpath)

        dirname = ''
        path_list = Path(fullpath).parts
        for pathname in path_list:
            find_date_in_dir = re.match("(\d{8}).*",pathname)
            #print("pathname:",pathname,"find_date:", find_date_in_dir)
            if find_date_in_dir:
                dirname = find_date_in_dir.group(0)
                break
                #print("dirname:",dirname)

        hostname = self.server_address
        portnumber = self.server_port
        #hostname = '127.0.0.1'

        get_url = "http://{}:{}/dolfinrest/dolfinimage_detail_md5hash/{}/{}/".format(hostname,portnumber,record.md5hash,record.name)
        #print(get_url)
        response = requests.get(get_url)
        #print(response.status_code)
        if int( response.status_code / 100 ) == 2:
            record.uploaded = True
            record.save()
            #print('retrieve success. returning.')
            return RET_ALREADY_EXIST


        #data_hash = {'filename':record.name,'md5hash':record.md5hash,'exifdatetime':record.exifdatetime, 'dirname':dirname,'obsdate':record.exifdatetime.strftime('%Y-%m-%d')}
        data_hash = {'filename':record.name,'md5hash':record.md5hash,'exifdatetime':record.exifdatetime, 'dirname':dirname,'obsdate':record.exifdatetime.date()}

        fd = open(fullpath, 'rb')
        file_hash = {'imagefile': fd}   
        #fields = {'title':'test','filename':item_text_list[1],'md5hash':hash_val,"imagefile": fd}
        #print(data_hash)

        #post_url = "http://222.233.253.74:8000/dolfinrest/dolfinimage_list/"
        post_url = "http://{}:{}/dolfinrest/dolfinimage_list/".format(hostname,portnumber)

        #print(requests.Request('POST', post_url, files=file_hash, data=data_hash).prepare().body)
        response = requests.post(post_url, files=file_hash,data=data_hash)
        #print(response)
        
        if int( response.status_code / 100 ) == 2:
        #log = open("log.txt","w")
        #log.write(str(response.json()))
        #log.close()
        #print(response.json())
            record.uploaded = True
            record.save()
            return RET_UPLOAD_SUCCESS
        elif int( response.status_code / 100 ) == 5:
            #print(response)
            record.uploaded = False
            record.save()
            return RET_UPLOAD_ERROR
        
    def reset_database(self):
        with db.atomic() as txn:
            q = DolfinImageFile.delete()
            q.execute()
        self.reset_views()        
        self.dir_list = []
        self.file_list = []

    def build_index(self):
        print("reading tree", datetime.now())
        rootdir = self.data_folder

        if self.cbxResetIndex.isChecked():
            self.reset_database()

        self.setRootdir(rootdir)
        #fd = open("output.log","w")
        print("checking database", datetime.now())
        dir_hash = {}
        #rec_list = [ self.dir_list, ]
        total_count = len(self.temp_dir_list) + len(self.temp_file_list)
        current_count = 0

        self.progress_dialog = ProgressDialog()
        self.progress_dialog.setModal(True)
        label_text = "Indexing image files {} of {} from folder \n{}...".format(current_count,total_count,rootdir)
        self.progress_dialog.lbl_text.setText(label_text)
        self.progress_dialog.pb_progress.setValue(0)
        self.progress_dialog.show()

        with db.atomic() as txn:
            for list in [ self.temp_dir_list, self.temp_file_list ]:
                for entry_hash in list:
                    current_count += 1
                    if current_count % 100 == 0:
                        print( current_count, "out of", total_count, "loaded.")
                    #print(f)
                    self.progress_dialog.pb_progress.setValue(int((current_count/float(total_count))*100))
                    label_text = "Indexing image files {} of {} from folder \n{}..".format(current_count, total_count,rootdir)
                    self.progress_dialog.lbl_text.setText(label_text)
                    self.progress_dialog.update()
                    QApplication.processEvents()
                    
                    fullpath = Path(entry_hash['path'])
                    #stem = fullpath.stem
                    fname = fullpath.name
                    rec_image0 = DolfinImageFile.get_or_none( path=str(fullpath.as_posix()) )
                    if not rec_image0:
                        file_info = self.get_file_info(fullpath)
                        #print(file_info)
                        if str(fullpath.parent.as_posix()) in dir_hash.keys():
                            parent = dir_hash[str(fullpath.parent.as_posix())]
                            #print(fullpath.parent)
                        else:
                            parent = None

                        rec_image = DolfinImageFile()
                        #print("rec_image:",rec_image)
                        rec_image.path = str(fullpath.as_posix())
                        rec_image.type = file_info['type']
                        rec_image.name = fname
                        rec_image.file_created = file_info['ctime']
                        rec_image.file_modified = file_info['mtime']
                        if file_info['type'] == 'file':
                            rec_image.size = file_info['size']
                            rec_image.md5hash = file_info['md5hash']
                            rec_image.uploaded = False
                            rec_image.exifdatetime = file_info['exifdatetime']
                            rec_image.parent=parent
                        elif file_info['type'] == 'dir':
                            rec_image.size = entry_hash['size']
                            rec_image.exifdatetime = file_info['ctime']
                            rec_image.md5hash = ''
                            rec_image.uploaded = False
                            rec_image.parent=parent
                        #print("rec_image:",rec_image)

                        rec_image.save()
                        if file_info['type'] == 'dir':
                            dir_hash[str(fullpath.as_posix())] = rec_image
                            #print(rec_image)
                            #print(dir_hash)
                        else:
                            self.file_record_hash[str(fullpath.as_posix())] = rec_image
                    else:
                        pass

        print("database done", datetime.now())
        self.progress_dialog.close()
        #QApplication.restoreOverrideCursor()


    def btnReadTreeClicked(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)

        self.build_index()
        self.load_dir()

        QApplication.restoreOverrideCursor()


    def btnLoadTreeClicked(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.load_dir()
        #self.treeView.hideColumn(2)
        QApplication.restoreOverrideCursor()

    def btnSendImageClicked(self):

        QApplication.setOverrideCursor(Qt.WaitCursor)

        filepath, filename = self.get_selected_file()
        fullpath = Path(filepath,filename).resolve()        
        str_fullpath = str(fullpath.as_posix())
        record = DolfinImageFile.get(type='file',path=str_fullpath)
        ret = self.upload_file(record)

        QApplication.restoreOverrideCursor()

    def btnSendAllClicked(self):
        print("send all")
        #return

        QApplication.setOverrideCursor(Qt.WaitCursor)

        if self.cbxUploadReset.isChecked():
            record_list = DolfinImageFile.filter(type='file')
        else:
            record_list = DolfinImageFile.filter(type='file',uploaded=False)
        print("record count:",len(record_list))
        total_count = len(record_list)
        current_count = 0
        error_count = 0
        already_exist_count = 0
        upload_success_count = 0
        #return

        self.progress_dialog = ProgressDialog()
        self.progress_dialog.setModal(True)
        label_text = "Uploading image files {} of {}...".format(current_count,total_count)
        self.progress_dialog.lbl_text.setText(label_text)
        self.progress_dialog.pb_progress.setValue(0)
        self.progress_dialog.show()

        for index, record in enumerate(record_list):
            current_count += 1
            if current_count % 100 == 0:
                print( current_count, "out of", total_count, "uploaded.")

            self.progress_dialog.pb_progress.setValue(int((current_count/float(total_count))*100))
            label_text = "Uploading image files {} of {}...".format(current_count, total_count)
            self.progress_dialog.lbl_text.setText(label_text)
            self.progress_dialog.update()
            QApplication.processEvents()

            #fullpath = record.path
            result = self.upload_file(record)
            if result == RET_UPLOAD_ERROR:
                error_count += 1
            elif result == RET_ALREADY_EXIST:
                already_exist_count += 1
            elif result == RET_UPLOAD_SUCCESS:
                upload_success_count += 1

        print("success:", upload_success_count)
        print("error:", error_count)
        print("already exist:", already_exist_count)
        print("total:", total_count)
        self.progress_dialog.close()

        QApplication.restoreOverrideCursor()


    def treeViewDoubleClicked(self):
        index = self.treeView.currentIndex()
        print(index)
        self.treeView.setCurrentIndex(index)
        #self.stackedWidget.setCurrentIndex(CLOSEUP_VIEW)
    
    def setRootdir(self,rootdir):
        #rootdir = 
        #rootpath = Path(rootdir).resolve()
        #stat_result = os.stat(rootpath)
        self.temp_file_list = []
        self.temp_dir_list = []

        #self.fs_list.append([str(rootpath),'dir',datetime.fromtimestamp(stat_result.st_ctime), datetime.fromtimestamp(stat_result.st_mtime),0])

        for (root,dirs,files) in os.walk(rootdir, topdown=True):
            #print(root,dirs,len(files),files[:10])
            #print(dirs)
            #for dir in dirs:
            #print(files)
            jpg_count = 0
            for file in files:
                filepath = Path(root,file).resolve()
                if filepath.suffix.upper() != '.JPG':
                    #print(file_path, file_path.suffix)
                    continue
                jpg_count += 1
                #stat_result = os.stat(filepath)

                #exif_info = self.get_exif_info(filepath)
                image_record = DolfinImageFile.get_or_none( path=str(filepath.as_posix()) )
                if image_record is None:
                    self.temp_file_list.append({'path':str(filepath),'type':'file'})
                    continue

            if jpg_count + len(dirs) > 0:
                dirpath = Path(root).resolve()
                self.temp_dir_list.append({'path':str(dirpath),'type':'dir','size':jpg_count})
                
                continue               
    
    def closeEvent(self, event):
        #if self.mainview_dlg is not None:
        #    self.mainview_dlg.close()
        print("closing")
        self.write_settings()

    def write_settings(self):
        #print("write settings", str(self.data_folder))
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope,"DiploSoft", "DolfinSync")

        settings.beginGroup("Defaults")
        settings.setValue("Server Address", self.server_address)
        settings.setValue("Server Port", self.server_port)
        settings.setValue("Data Folder", str(self.data_folder))
        settings.endGroup()

    def read_settings(self):
        #print("read settings")
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope,"DiploSoft", "DolfinSync")

        settings.beginGroup("Defaults")
        self.server_address = settings.value("Server Address", DEFAULT_IP_ADDRESS)
        self.server_port = settings.value("Server Port", DEFAULT_PORT)
        self.data_folder = Path(settings.value("Data Folder", "."))
        self.working_folder = self.data_folder
        self.edtServerAddress.setText(self.server_address)
        self.edtPortNumber.setText(self.server_port)
        self.edtDataFolder.setText(str(self.data_folder))
        settings.endGroup()


    def open_preferences(self):
        #self.preferences_dialog = PreferencesDialog(self)
        #self.preferences_dialog.parent = self
        #self.preferences_dialog.show()
        pass

    def get_file_info(self, fullpath):

        file_info = {}

        ''' file stat '''
        stat_result = os.stat(fullpath)
        file_info['mtime'] = stat_result.st_mtime
        file_info['ctime'] = stat_result.st_ctime

        if os.path.isdir(fullpath):
            file_info['type'] = 'dir'
        else:
            file_info['type'] = 'file'

        if os.path.isdir( fullpath ):
            return file_info

        file_info['size'] = stat_result.st_size

        ''' md5 hash value '''
        file_info['md5hash'], image_data = self.get_md5hash_info(fullpath)

        ''' exif info '''
        exif_info = self.get_exif_info(fullpath, image_data)
        file_info['exifdatetime'] = exif_info['datetime']
        file_info['latitude'] = exif_info['latitude']
        file_info['longitude'] = exif_info['longitude']
        file_info['map_datum'] = exif_info['map_datum']

        return file_info

    def get_md5hash_info(self,filepath):
        afile = open(filepath, 'rb')
        hasher = hashlib.md5()
        image_data = afile.read()
        hasher.update(image_data)
        afile.close()
        md5hash = hasher.hexdigest()
        return md5hash, image_data

    def get_exif_info(self, fullpath, image_data=None):
        image_info = {'date':'','time':'','latitude':'','longitude':'','map_datum':''}
        img = None
        if image_data:
            #img = Image.open()
            img = Image.open(io.BytesIO(image_data))
        else:
            img = Image.open(fullpath)
        ret = {}
        #print(filename)
        try:
            info = img._getexif()
            for tag, value in info.items():
                decoded=TAGS.get(tag, tag)
                ret[decoded]= value
                #print("exif:", decoded, value)
            try:
                if ret['GPSInfo'] != None:
                    gps_info = ret['GPSInfo']
                    #print("gps info:", gps_info)
                degree_symbol = "°"
                minute_symbol = "'"
                longitude = str(int(gps_info[4][0])) + degree_symbol + str(gps_info[4][1]) + minute_symbol + gps_info[3]
                latitude = str(int(gps_info[2][0])) + degree_symbol + str(gps_info[2][1]) + minute_symbol + gps_info[1]
                map_datum = gps_info[18]
                image_info['latitude'] = latitude
                image_info['longitude'] = longitude
                image_info['map_datum'] = map_datum

            except KeyError:
                pass
                #print( "GPS Data Don't Exist for", Path(filename).name)


            try:
                if ret['DateTimeOriginal'] is not None:
                    exif_timestamp = ret['DateTimeOriginal']
                    #print("original:", exifTimestamp)
                    image_info['date'], image_info['time'] = exif_timestamp.split()
            except KeyError:
                pass
                #print( "DateTimeOriginal Don't Exist")
            try:
                if ret['DateTimeDigitized'] is not None:
                    exif_timestamp = ret['DateTimeDigitized']
                    image_info['date'], image_info['time'] = exif_timestamp.split()
            except KeyError:
                pass
                #print( "DateTimeDigitized Don't Exist")
            try:
                if ret['DateTime'] is not None:
                    exif_timestamp = ret['DateTime']
                    image_info['date'], image_info['time'] = exif_timestamp.split()
            except KeyError:
                pass
                #print( "DateTime Don't Exist")

        except Exception as e:
            pass
            #print(e)

        if image_info['date'] == '':
            str1 = time.ctime(os.path.getmtime(fullpath))
            datetime_object = datetime.strptime(str1, '%a %b %d %H:%M:%S %Y')
            image_info['date'] = datetime_object.strftime("%Y-%m-%d")
            image_info['time'] = datetime_object.strftime("%H:%M:%S")
        else:
            image_info['date'] = "-".join( image_info['date'].split(":") )
        image_info['datetime'] = image_info['date'] + ' ' + image_info['time']
        return image_info
#app = QApplication(sys.argv)
#treeView = QTreeView()
#fileSystemModel = QFileSystemModel(treeView)
#fileSystemModel.setReadOnly(False)
#root = fileSystemModel.setRootPath('.')
#treeView.setModel(fileSystemModel)
#treeView.setRootIndex(root)
#treeView.show()
#app.exec_()

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('marc_icon.png'))

    #WindowClass의 인스턴스 생성
    myWindow = DolfinSyncWindow()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
