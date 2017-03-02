#打包指令pyinstaller -F -w -p C:\Users\T440\AppData\Roaming\Python\Python35\site-packages\PyQt5\Qt\bin -i G:\TACHIAGARE\icon.ico C:\Users\T440\PycharmProjects\catcher\main.py
import sys
import os
import re
import requests
import time
import socket

from PyQt5 import QtCore, QtWidgets

from PyQt5.QtWidgets import QApplication , QMainWindow

socket.setdefaulttimeout(30)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(257, 60)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        MainWindow.setWindowOpacity(0.8)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit1.setGeometry(QtCore.QRect(50, 8, 121, 21))
        self.lineEdit1.setObjectName("lineEdit1")
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(180, 7, 71, 23))
        self.pushButton1.setObjectName("pushButton1")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(6, 13, 54, 12))
        self.label1.setObjectName("label1")
        self.lineEdit2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit2.setGeometry(QtCore.QRect(50, 33, 121, 21))
        self.lineEdit2.setObjectName("lineEdit2")
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(180, 32, 71, 23))
        self.pushButton2.setObjectName("pushButton2")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(6, 38, 54, 12))
        self.label2.setObjectName("label2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")

        self.retranslateUi(MainWindow)
        self.pushButton1.clicked.connect(self.getimage)
        self.pushButton2.clicked.connect(self.getillustor)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "P站图片抓取"))
        self.pushButton1.setText(_translate("MainWindow", "抓取"))
        self.label1.setText(_translate("MainWindow", "图片ID："))
        self.pushButton2.setText(_translate("MainWindow", "抓取"))
        self.label2.setText(_translate("MainWindow", "画师ID："))
        self.action.setText(_translate("MainWindow", "设置路径"))

    def login(self):
        try:
            PIXIV_PAGE_HEADERS = {
                'Host': 'accounts.pixiv.net',
                'Referer': 'http://www.pixiv.net/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/50.0.2661.102 Safari/537.36'
            }

            PIXIV_LOGIN_URL = "https://accounts.pixiv.net/api/login"
            PIXIV_LOGIN_KEY = "https://accounts.pixiv.net/login"

            r = s.get(PIXIV_LOGIN_KEY, headers=PIXIV_PAGE_HEADERS)
            if r.ok:
                logindata = r.content.decode('UTF-8')
                list = re.compile('post_key"\\svalue="(.*?)">')
                lodata = re.findall(list, logindata)
                post_key = lodata[0]
                print(post_key)
            postdata = {
                'pixiv_id': '237515611@qq.com',
                'password': '1248163264128',
                'post_key': post_key,
            }
            # 存储cookie
            s.post(PIXIV_LOGIN_URL, data=postdata, headers=PIXIV_PAGE_HEADERS)
            cookie = requests.utils.dict_from_cookiejar(s.cookies)
            print(cookie)
        except:
            QtWidgets.QMessageBox.information(self.pushButton1, "失败", "登陆P站失败，请检查网络连接")

    #获取单ID图片
    def getimage(self):
        id = self.lineEdit1.text()

        mainurl = "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + id
        try:
            maindata = s.get(mainurl, timeout=30).content
            strdata = maindata.decode('UTF-8')
            list = re.compile('data-src="(.*?img-original.*?)"')
            data = re.findall(list, strdata)
            if len(data)!=0:
                #单图
                try:
                    picurl = data[0].replace('\/', '/')
                    print(picurl)
                    PIXIV_PIC_HEADERS = {
                        'Host': picurl[7:19],
                        'Referer': 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + id,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/50.0.2661.102 Safari/537.36'
                    }
                    print(picurl[7:19])
                    picdata = s.get(picurl, headers=PIXIV_PIC_HEADERS, timeout=30).content
                    picpath = os.path.expanduser('~') + "/Pictures/" + id + "_0" + picurl[-4:]
                    open(picpath, 'wb').write(picdata)
                    QtWidgets.QMessageBox.information(self.pushButton1, "成功", "已保存至图库")
                except:
                    QtWidgets.QMessageBox.information(self.pushButton1, "失败", "该图片可能已被删除或暂时无法获取")
            else:
                #多图
                mangaurl="http://www.pixiv.net/member_illust.php?mode=manga&illust_id="+id
                print(mangaurl)
                PIXIV_PIC_HEADERS = {
                    'Host': 'www.pixiv.net',
                    'Referer': 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + id,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/50.0.2661.102 Safari/537.36'
                }
                mangadata = s.get(mangaurl, headers=PIXIV_PIC_HEADERS, timeout=30).content
                manstrdata = mangadata.decode('UTF-8')
                mangalist = re.compile('images\[\d*\]\\s=\\s"(.*?img-master.*?)"')
                mandata = re.findall(mangalist, manstrdata)
                point=0
                manurl=mandata[0].replace('\/', '/')
                PIXIV_MANPIC_HEADERS = {
                    'Host': manurl[7:19],
                    'Referer': 'http://www.pixiv.net/member_illust.php?mode=manga&illust_id=' + id,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/50.0.2661.102 Safari/537.36'
                }
                print(manurl[7:19])
                for i in range(len(mandata)):
                    try:
                        manpurl = mandata[i].replace('\/', '/')
                        print(manpurl)
                        picdata = s.get(manpurl, headers=PIXIV_MANPIC_HEADERS, timeout=30).content
                        picpath = os.path.expanduser('~') + "/Pictures/" + id + "_" + str(i) + manpurl[-4:]
                        open(picpath, 'wb').write(picdata)
                        if i==len(mandata)-1:
                            QtWidgets.QMessageBox.information(self.pushButton1, "成功", "已保存至图库")
                    except:
                        QtWidgets.QMessageBox.information(self.pushButton1, "失败", "该图片可能已被删除或暂时无法获取")
        except:
            QtWidgets.QMessageBox.information(self.pushButton1, "失败", "该图片可能已被删除或暂时无法获取")

    #获取画师单ID图片
    def getoneimage(self,illustor,id):
        mainurl = "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + id
        try:
            maindata = s.get(mainurl, timeout=30).content
            strdata = maindata.decode('UTF-8')
            list = re.compile('data-src="(.*?img-original.*?)"')
            data = re.findall(list, strdata)
            if len(data)!=0:
                #单图
                try:
                    picurl = data[0].replace('\/', '/')
                    print(picurl)
                    PIXIV_PIC_HEADERS = {
                        'Host': picurl[7:19],
                        'Referer': 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + id,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/50.0.2661.102 Safari/537.36'
                    }
                    print(picurl[7:19])
                    picdata = s.get(picurl, headers=PIXIV_PIC_HEADERS, timeout=30).content
                    picpath = os.path.expanduser('~') + "/Pictures/" + illustor + "/" +id + "_0" + picurl[-4:]
                    open(picpath, 'wb').write(picdata)
                    print("sucess")
                except:
                    QtWidgets.QMessageBox.information(self.pushButton2, "失败", "ID为" + str(id) + "的图片下载失败")
            else:
                #多图
                mangaurl="http://www.pixiv.net/member_illust.php?mode=manga&illust_id="+id
                print(mangaurl)
                PIXIV_PIC_HEADERS = {
                    'Host': 'www.pixiv.net',
                    'Referer': 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + id,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/50.0.2661.102 Safari/537.36'
                }
                mangadata = s.get(mangaurl, headers=PIXIV_PIC_HEADERS, timeout=30).content
                manstrdata = mangadata.decode('UTF-8')
                mangalist = re.compile('images\[\d*\]\\s=\\s"(.*?img-master.*?)"')
                mandata = re.findall(mangalist, manstrdata)
                point=0
                manurl=mandata[0].replace('\/', '/')
                PIXIV_MANPIC_HEADERS = {
                    'Host': manurl[7:19],
                    'Referer': 'http://www.pixiv.net/member_illust.php?mode=manga&illust_id=' + id,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/50.0.2661.102 Safari/537.36'
                }
                print(manurl[7:19])
                for i in range(len(mandata)):
                    try:
                        manpurl = mandata[i].replace('\/', '/')
                        print(manpurl)
                        picdata = s.get(manpurl, headers=PIXIV_MANPIC_HEADERS, timeout=30).content
                        picpath = os.path.expanduser('~') + "/Pictures/" + illustor + "/" + id + "_" + str(i) + manpurl[-4:]
                        open(picpath, 'wb').write(picdata)
                        if i==len(mandata)-1:
                            print("success")
                    except:
                        QtWidgets.QMessageBox.information(self.pushButton2, "失败", "ID为" + str(id) + "的第" + str(i+1) + "图片下载失败")
        except:
            QtWidgets.QMessageBox.information(self.pushButton2, "失败", "ID为" + str(id) + "的第" + str(i+1) + "图片下载失败")

    #获取画师所有作品
    def getillustor(self):
        id=self.lineEdit2.text()

        header1 = {
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': 'https://www.pixiv.net/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'
        }

        header2 = {
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Host': 'www.pixiv.net',
            'Referer': 'https://www.pixiv.net/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'
        }

        # 获取作品数
        try:
            numurl = "http://www.pixiv.net/member_illust.php?id=" + id
            r=s.get(numurl, headers=header1)
            numdata = r.content
            numlist = re.compile('count-badge">(\d*?)件<')
            nndata = numdata.decode('UTF-8')
            workdata = re.findall(numlist, nndata)
            num = int(workdata[0])
            print(num)
        except:
            QtWidgets.QMessageBox.information(self.pushButton2, "失败", "没有该画师")
            return
        if num == 0:
            QtWidgets.QMessageBox.information(self.pushButton2, "失败", "该画师没有作品")
            return


        # 创建画师路径
        dir = os.path.expanduser('~') + "/Pictures/" + id
        if(not os.path.exists(dir)):
            os.mkdir(dir)
            print(dir)
        print("s")

        #计算页面数
        page=int((int(num)-1)/20)+1
        print(page)

        #遍历所有图片
        for i in range(0,page):
            pageurl="http://www.pixiv.net/member_illust.php?id=" + id + "&type=all&p=" + str(i+1)
            pagedata=s.get(pageurl, headers=header2).content
            pagelist = re.compile('illust_id=(\d*?)"\\sclass')
            ppdata = pagedata.decode('UTF-8')
            pagepicdata = re.findall(pagelist, ppdata)
            print(len(pagepicdata))
            for j in range(0,len(pagepicdata)):
                pagenum=pagepicdata[j]
                self.getoneimage(id, pagenum)
                #设置间隔时间，防止抓图过快被封IP
                time.sleep(5)
        QtWidgets.QMessageBox.information(self.pushButton2, "完成", "下载完成")

#主运行界面
if __name__ == '__main__':
    # 设置爬虫网络线程
    s = requests.Session()
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    ui.login()
    mainWindow.show()
    sys.exit(app.exec_())