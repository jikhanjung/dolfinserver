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

import os,sys
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

PROGRAM_NAME = "DolfinID"
PROGRAM_VERSION = "0.0.1"

db = SqliteDatabase('dolfinid.db')

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
        self.setWindowTitle("Preferences")
        #self.lbl_main_view.setMinimumSize(400, 300)

        self.parent = parent
        self.lblServerAddress = QLabel()
        self.edtServerAddress = QLineEdit()
        self.lblDataFolder = QLabel()
        self.edtDataFolder = QLineEdit()

        self.btnDataFolder = QPushButton()
        self.btnDataFolder.setText("Select Folder")
        self.btnDataFolder.clicked.connect(self.select_folder)

        self.btnOkay = QPushButton()
        self.btnOkay.setText("OK")
        self.btnOkay.clicked.connect(self.Okay)

        self.btnCancel = QPushButton()
        self.btnCancel.setText("Cancel")
        self.btnCancel.clicked.connect(self.Cancel)


        self.layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.lblServerAddress)
        self.layout1.addWidget(self.edtServerAddress)
        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.lblDataFolder)
        self.layout2.addWidget(self.edtDataFolder)
        self.layout2.addWidget(self.btnDataFolder)
        self.layout3 = QHBoxLayout()
        self.layout3.addWidget(self.btnOkay)
        self.layout3.addWidget(self.btnCancel)
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)
        self.layout.addLayout(self.layout3)
        self.setLayout(self.layout)
        self.server_address = ''
        self.data_folder = ''
        #print("pref dlg data_folder:", self.data_folder)
        self.read_settings()
        #print("pref dlg data_folder:", self.data_folder)
        self.lblServerAddress.setText("Dolfin ID Prefix")
        self.lblDataFolder.setText("Data Folder")
        self.edtServerAddress.setText("")
        self.edtDataFolder.setText(str(self.data_folder.resolve()))

    def write_settings(self):
        self.parent.server_address = self.edtServerAddress.text()
        self.parent.data_folder = Path(self.edtDataFolder.text())
        #print( self.parent.dolfinid_prefix, self.parent.data_folder)

    def read_settings(self):
        self.server_address = self.parent.server_address
        self.data_folder = self.parent.data_folder.resolve()
        print("pref dlg data folder:", self.data_folder)
        print("pref dlg server address:", self.server_address)

    def Okay(self):
        self.write_settings()
        self.close()

    def Cancel(self):
        self.close()

    def select_folder(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Folder", str(self.data_folder)))
        if folder:
            self.data_folder = Path(folder).resolve()
            self.edtDataFolder.setText(folder)

class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        #self.setupUi(self)
        self.lbl_text = QLabel(self)
        self.lbl_text.setGeometry(100, 50, 300, 20)
        #self.pb_progress = QProgressBar(self)
        self.pb_progress = QProgressBar(self)
        self.pb_progress.setGeometry(50, 120, 320, 40)
        self.pb_progress.setValue(0)
        self.setGeometry(600, 400, 400, 210)

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
    


form_class = uic.loadUiType("DolfinID.ui")[0]
class DolfinIDWindow(QMainWindow, form_class):

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

        self.btnReadTree.clicked.connect(self.btnReadTreeClicked)
        self.btnLoadTree.clicked.connect(self.btnLoadTreeClicked)
        self.btnSendImage.clicked.connect(self.btnSendImageClicked)
        self.btnSendAll.clicked.connect(self.btnSendAllClicked)
        #self.data_folder = Path('.')
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

        self.dir_record_tree = []
        self.file_record_hash = {}
        self.dir_list = []
        self.file_list = []

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
        print(index)

        selected_index_list = self.fileSelModel.selection().indexes()
        if len(selected_index_list) == 0:
            return
        print("selected_index",selected_index_list)

        new_index_list = []
        model = selected_index_list[0].model()
        if hasattr(model, 'mapToSource'):
            for index in selected_index_list:
                new_index = model.mapToSource(index)
                new_index_list.append(new_index)
        print("new_index_list",new_index_list)
        item_text_list = []
        for index in new_index_list:
            item = self.file_model.itemFromIndex(index)
            print("item_text:",item.text())
            item_text_list.append(item.text())
        filepath = item_text_list[1]
        filename = item_text_list[0]
        return filepath, filename

    def upload_file(self,fullpath):

        record = None
        print(fullpath)

        if fullpath in self.file_record_hash.keys():
            record = self.file_record_hash[fullpath]
        else:
            record = DolfinImageFile.get_or_none(path=fullpath)
            if record is None:
                return

        get_url = "http://127.0.0.1:8000/dolfinrest/dolfinimage_detail_md5hash/{}/{}/".format(record.md5hash,record.name)
        print(get_url)
        response = requests.get(get_url)
        print(response.status_code)
        if int( response.status_code / 100 ) == 2:
            print('retrieve success. returning.')
            return


        data_hash = {'filename':record.name,'md5hash':record.md5hash,'exifdatetime':record.exifdatetime}

        fd = open(fullpath, 'rb')
        file_hash = {'imagefile': fd}   
        #fields = {'title':'test','filename':item_text_list[1],'md5hash':hash_val,"imagefile": fd}
        #print(fields)

        #post_url = "http://222.233.253.74:8000/dolfinrest/dolfinimage_list/"
        post_url = "http://127.0.0.1:8000/dolfinrest/dolfinimage_list/"

        #print(requests.Request('POST', post_url, files=file_hash, data=data_hash).prepare().body)
        response = requests.post(post_url, files=file_hash,data=data_hash)
        
        #log = open("log.txt","w")
        #log.write(str(response.json()))
        #log.close()
        print(response)
        print(response.json())
        record.uploaded = True
        record.save()
        

    def btnReadTreeClicked(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)

        self.read_tree()

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
        self.upload_file(str_fullpath)

        QApplication.restoreOverrideCursor()

    def btnSendAllClicked(self):
        print("send all")
        #return

        QApplication.setOverrideCursor(Qt.WaitCursor)

        record_list = DolfinImageFile.filter(type='file',uploaded=False)
        print("record count:",len(record_list))
        total_count = len(record_list)
        #return
        for index, record in enumerate(record_list):
            fullpath = record.path
            self.upload_file(fullpath)

        QApplication.restoreOverrideCursor()


    def read_tree(self):
        print("reading tree", datetime.now())
        rootdir = self.data_folder
        self.setRootdir(rootdir)

        #fd = open("output.log","w")
        print("checking database", datetime.now())
        dir_hash = {}
        #rec_list = [ self.dir_list, ]
        with db.atomic() as txn:
            for list in [ self.dir_list, self.file_list ]:
                for f in list:
                    #print(f)
                    fullpath = Path(f['path'])
                    #stem = fullpath.stem
                    fname = fullpath.name
                    rec_image = DolfinImageFile.get_or_none( path=str(fullpath.as_posix()) )
                    if not rec_image:
                        #print("no such record"+str(f)+"\n")
                        #print(str(dir_hash))
                        #print(stem)
                        if str(fullpath.parent.as_posix()) in dir_hash.keys():
                            parent = dir_hash[str(fullpath.parent.as_posix())]
                            #print(fullpath.parent)
                        else:
                            #print("no key")
                            #print(dir_hash.keys(), fullpath.parent)
                            parent = None
                        rec_image = DolfinImageFile()
                        rec_image.path = str(fullpath.as_posix())
                        rec_image.type = f['type']
                        rec_image.name = fname
                        rec_image.file_created = f['file_created']
                        rec_image.file_modified = f['file_modified']
                        rec_image.size = f['size']
                        rec_image.md5hash = f['md5hash']
                        rec_image.uploaded = False
                        rec_image.exifdatetime = f['exifdatetime']
                        rec_image.parent=parent
                        rec_image.save()
                        if f['type'] == 'dir':
                            dir_hash[str(fullpath.as_posix())] = rec_image
                            #print(rec_image)
                            #print(dir_hash)
                        else:
                            self.file_record_hash[str(fullpath.as_posix())] = rec_image
                    else:
                        pass
        #fd.writepstr(dir_hash))
        #print(dir_hash)
                #print("already_exist", f)
            #print(stem, fname)
            #fd.write(str(f)+"\n")
        #fd.close()
        print("database done", datetime.now())
        #print(self.fs_list)

    def treeViewDoubleClicked(self):
        index = self.treeView.currentIndex()
        print(index)
        self.treeView.setCurrentIndex(index)
        #self.stackedWidget.setCurrentIndex(CLOSEUP_VIEW)
    
    def setRootdir(self,rootdir):
        #rootdir = 
        #rootpath = Path(rootdir).resolve()
        #stat_result = os.stat(rootpath)

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
                    fileinfo = self.get_file_info(filepath)
                    #print(file_path.suffix)#if file_path.suffix != 
                    #print(file_path, rootdir)
                    #rel_path = file_path.relative_to(Path(rootdir).resolve())
                    #self.file_list.append([str(filepath),'file',datetime.fromtimestamp(stat_result.st_ctime),datetime.fromtimestamp(stat_result.st_mtime),stat_result.st_size, exif_info['date']])
                    fileinfo_hash = {   'path': str(filepath), 
                                        'type': 'file', 
                                        'file_created':datetime.fromtimestamp(fileinfo['ctime']), 
                                        'file_modified':datetime.fromtimestamp(fileinfo['mtime']), 
                                        'size': fileinfo['size'],
                                        'md5hash': fileinfo['md5hash'],
                                        'exifdatetime': fileinfo['exifdatetime'],
                                    }           
                    self.file_list.append( fileinfo_hash )

            if jpg_count + len(dirs) > 0:
                dirpath = Path(root).resolve()
                dirinfo = self.get_file_info(dirpath)
                #stat_result = os.stat(dirpath)
                #print(dir_path, rootdir)
                #rel_path = dir_path.relative_to(Path(rootdir).resolve())
                #if str(rel_path) == ".":
                #    rel_path = Path(rootdir).resolve()
                dir_record = DolfinImageFile.get_or_none( path=str(dirpath.as_posix()) )
                if dir_record is None:

                    dirinfo_hash = {   'path': str(dirpath), 
                                        'type': 'dir', 
                                        'file_created':datetime.fromtimestamp(dirinfo['ctime']), 
                                        'file_modified':datetime.fromtimestamp(dirinfo['mtime']), 
                                        'size': jpg_count,
                                        'md5hash': '',
                                        'exifdatetime': datetime.fromtimestamp(dirinfo['ctime']),
                                    }           
                    self.dir_list.append( dirinfo_hash )

                #self.dir_list.append([str(dir_path),'dir',datetime.fromtimestamp(stat_result.st_ctime),datetime.fromtimestamp(stat_result.st_mtime),jpg_count,datetime.fromtimestamp(stat_result.st_ctime).strftime("%Y-%m-%d")])

    
    def closeEvent(self, event):
        #if self.mainview_dlg is not None:
        #    self.mainview_dlg.close()
        print("closing")
        self.write_settings()

    def write_settings(self):
        #print("write settings", str(self.data_folder))
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope,"DiploSoft", "DolfinID")

        settings.beginGroup("Defaults")
        settings.setValue("Server Address", self.server_address)
        settings.setValue("Data Folder", str(self.data_folder))
        settings.endGroup()

    def read_settings(self):
        #print("read settings")
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope,"DiploSoft", "DolfinID")

        settings.beginGroup("Defaults")
        self.server_address = settings.value("Server Address", "")
        self.data_folder = Path(settings.value("Data Folder", "./"))
        self.working_folder = self.data_folder
        settings.endGroup()


    def open_preferences(self):
        self.preferences_dialog = PreferencesDialog(self)
        self.preferences_dialog.parent = self
        self.preferences_dialog.show()

    def get_file_info(self, fullpath):

        file_info = {}

        ''' file stat '''
        stat_result = os.stat(fullpath)
        file_info['mtime'] = stat_result.st_mtime
        file_info['ctime'] = stat_result.st_ctime

        if os.path.isdir( fullpath ):
            return file_info

        file_info['size'] = stat_result.st_size

        # 나중에 md5 와 exif 를 합칠 것.

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
            str1 = time.ctime(os.path.getmtime(filename))
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
    myWindow = DolfinIDWindow()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
