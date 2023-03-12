import os.path
from json import load as json_load
import resource.interface.resource_rc
# import resource.interface.resource_rc # 这句不要删，是用于导入资源文件的，删了重新复制一下
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView
from pyqt5_plugins.examplebutton import QtWidgets
import file_db
from resource.interface.detailWindow import UI_DetailWindow
from resource.interface.mainWindow import UI_MainWindow


class Controller(QWidget):
    """
    该类协调前端和后端，以实现各项功能
    """

    def __init__(self):
        super().__init__()
        self.mainWindowUI = UI_MainWindow()  # 创建主窗口
        self.mainWindowUI.setupUi(self)  # 绘制默认UI
        self.detailWindowUI = UI_DetailWindow()  # 创建详细信息窗口
        self.detailWindowWidget = QtWidgets.QWidget()  # 创建详细信息窗口的widget
        self.detailWindowUI.setupUi(self.detailWindowWidget)  # 绘制详细信息窗口的UI
        self.detailWindowWidget.setWindowTitle("详细信息")
        self.setWindowTitle('SimpleResManager')  # 设置窗口标题
        self.pageHistory = []  # 页面历史队列，用于后退和前进，这个队列只可增长不可减少
        self.pageHistoryIndex = -1  # 当前索引，空的时候为-1，当非空时就从0开始了，配合pageHistory使用
        self.currentPage = None  # 当前页面
        self.currentPageItems = []  # 当前页面的所有子对象，类型为list(dict)
        self.selectionItem = {}  # 当前页面被选中的对象，类型为dict
        self.copyItem = {}  # 当前页面被复制的对象，类型为dict
        self.cutList = {}  # 当前页面被剪切的对象，类型为dict
        self._bind()  # 用于绑定各组件事件的函数
        with open("config.json", 'r', encoding='utf8') as conf:
            defaultPage = json_load(conf)["defaultPage"]
        # 每次在跳转时，一定要考虑对self.pageHistory、self.pageHistoryIndex和self.currentPage的调整
        self.currentPage = defaultPage
        self.pageHistory.append(self.currentPage)
        self.pageHistoryIndex += 1
        self.turnToPage(target=self.currentPage)  # 初始化界面

    def _bind(self):
        """绑定各个控件"""
        self.mainWindowUI.left.clicked.connect(self._buttonClicked)  # 绑定后退键
        self.mainWindowUI.right.clicked.connect(self._buttonClicked)  # 绑定前进键
        self.mainWindowUI.up.clicked.connect(self._buttonClicked)  # 绑定上级键
        self.mainWindowUI.refresh.clicked.connect(self._buttonClicked)  # 绑定刷新键
        self.mainWindowUI.info.clicked.connect(self._buttonClicked)  # 绑定详细信息窗口
        self.mainWindowUI.quick_jump.doubleClicked.connect(self._listClicked)  # 绑定左侧快速跳转列表
        self.mainWindowUI.main_widget.cellDoubleClicked.connect(self._mainTableDoubleClicked)  # 绑定主表格双击事件
        self.mainWindowUI.main_widget.cellClicked.connect(self._tableClicked)  # 绑定主表格单击事件
        self.mainWindowUI.main_widget.cellPressed.connect(self._tableClicked)  # 绑定主表格单击事件
        self.mainWindowUI.address.returnPressed.connect(self.turnToByInputAddress)  # 绑定状态栏

    def _buttonClicked(self):
        """监视各个按钮的点击"""
        sender = self.sender()
        if sender.objectName() == "left":
            self.backToLastPage()
        elif sender.objectName() == "right":
            self.forwardToNextPage()
        elif sender.objectName() == "up":
            self.goToParentPage()
        elif sender.objectName() == "refresh":
            self.refreshPage()
        elif sender.objectName() == "info":
            self.showDetailWindow()
        return sender

    def _listClicked(self, index):
        """监视左侧列表的点击"""
        index = index.row()
        with open("config.json", 'r', encoding='utf8') as conf:
            homePageQuickDirs = json_load(conf)['homePageQuickDirs']
        if index == 0:
            self.currentPage = "defaultPage"
        elif index == 1:
            self.currentPage = homePageQuickDirs['桌面']
        elif index == 2:
            self.currentPage = homePageQuickDirs['下载']
        elif index == 3:
            self.currentPage = homePageQuickDirs['图片']
        elif index == 4:
            self.currentPage = homePageQuickDirs['文档']
        elif index == 5:
            self.currentPage = homePageQuickDirs['视频']
        elif index == 6:
            self.currentPage = homePageQuickDirs['音乐']
        self.pageHistory.append(self.currentPage)
        self.pageHistoryIndex = len(self.pageHistory) - 1
        self.turnToPage(target=self.currentPage)
        print(index)

    def _mainTableDoubleClicked(self, row, col):
        """监视表格的双击（技术有限，只能监视到单个对象....）"""
        # 由于一个路径下，文件和文件夹的名称是不会重复的，所以可以用名称来唯一确定一个对象
        name = self.mainWindowUI.main_widget.item(row, 0).text()
        print('你双击了一个项目:', row, col, name)
        if self.selectionItem['basicInfo']['type'] == '文件夹':
            self.currentPage = self.selectionItem['otherInfo']["path"]
            self.pageHistory.append(self.currentPage)
            self.pageHistoryIndex = len(self.pageHistory) - 1
            self.turnToPage(target=self.currentPage)
        else:
            print('------' + self.selectionItem['basicInfo']['name'] + '------')
            for info in self.selectionItem['otherInfo']:
                print(info, ':', self.selectionItem['otherInfo'][info])

    def _tableClicked(self, row, col):
        """监视表格的单击"""
        # 由于一个路径下，文件和文件夹的名称是不会重复的，所以可以用名称来唯一确定一个对象
        name = self.mainWindowUI.main_widget.item(row, 0).text()
        for item in self.currentPageItems:
            if item['basicInfo']['name'] == name:
                self.selectionItem = item
                print('你选中了一个项目:', row, col, name)
                break

    def turnToByInputAddress(self):
        """根据地址栏输入的地址跳转"""
        inputAddress = self.mainWindowUI.address.text()
        inputAddress = inputAddress.replace('\\', '/')
        if os.path.exists(inputAddress):
            self.currentPage = inputAddress
            self.pageHistory.append(self.currentPage)
            self.pageHistoryIndex = len(self.pageHistory) - 1
            self.turnToPage(target=self.currentPage)

    def showDetailWindow(self):
        """显示详细信息窗口"""
        # 清空detailTable
        self.detailWindowUI.detailTable.clearContents()
        # 详细信息窗口的信息表格
        details = {**self.selectionItem['basicInfo'], **self.selectionItem['otherInfo']}
        self.detailWindowUI.detailTable.setRowCount(len(details))  # 设置行数
        self.detailWindowUI.detailTable.setColumnCount(2)  # 设置列数
        self.detailWindowUI.detailTable.setHorizontalHeaderLabels(['属性', '值'])  # 设置表头
        self.detailWindowUI.detailTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表头自适应
        for i, info in enumerate(details):
            self.detailWindowUI.detailTable.setItem(i, 0, QTableWidgetItem(info))
            self.detailWindowUI.detailTable.setItem(i, 1, QTableWidgetItem(str(details[info])))
            if info != 'Tags':
                # 设置item不可编辑
                self.detailWindowUI.detailTable.item(i, 0).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.detailWindowUI.detailTable.item(i, 1).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        # 详细信息窗口的确认与取消按钮
        self.detailWindowUI.saveModify.clicked.connect(self._saveDetailModify)
        self.detailWindowUI.close.clicked.connect(self._closeDetailWindow)
        self.detailWindowWidget.show()

    def _saveDetailModify(self):
        """保存详细信息窗口的修改"""
        tags = ''  # 获取tags的信息
        for i in range(self.detailWindowUI.detailTable.rowCount()):
            if self.detailWindowUI.detailTable.item(i, 0).text() == 'Tags':
                tags = self.detailWindowUI.detailTable.item(i, 1).text()
                break
        # 编辑数据
        data = self.selectionItem
        data['basicInfo']['Tags'] = tags
        # 写入数据库
        dbController = file_db.DBController()
        dbController.updateDB([data])
        self.detailWindowWidget.close()
        self.turnToPage(target=self.currentPage)  # 刷新页面

    def _closeDetailWindow(self):
        """关闭详细信息窗口"""
        self.detailWindowWidget.close()
        self.turnToPage(target=self.currentPage)  # 刷新页面

    def backToLastPage(self):
        """后退"""
        self.pageHistoryIndex -= 1
        if self.pageHistoryIndex >= 0:
            self.currentPage = self.pageHistory[self.pageHistoryIndex]
            self.pageHistory.append(self.currentPage)
            self.turnToPage(target=self.currentPage)

    def forwardToNextPage(self):
        """前进"""
        self.pageHistoryIndex += 1
        if self.pageHistoryIndex < len(self.pageHistory):
            self.currentPage = self.pageHistory[self.pageHistoryIndex]
            self.pageHistory.append(self.currentPage)
            self.turnToPage(target=self.currentPage)

    def goToParentPage(self):
        """前往父级菜单"""
        self.pageHistoryIndex += 1
        self.currentPage = "/".join(self.currentPage.split('/')[:-1])
        self.pageHistory.append(self.currentPage)
        self.turnToPage(target=self.currentPage)

    def refreshPage(self):
        """刷新当前页面，即强制请求使用文件系统更新数据库，并重新加载页面"""
        fileController = file_db.FileController()
        fileController.refreshItemsByFatherPath(self.currentPage)
        fileController.updateDB()
        self.turnToPage(target=self.currentPage)

    def turnToPage(self, target: str):
        """
        加载页面
        :param target: 目标页面，为文件夹路径或"defaultPage"(主页保留字)
        """
        # 获取数据
        if target == "defaultPage":  # “defaultPage”作为保留字，就是指向的主页
            # 获取主页的项目列表
            with open("config.json", 'r', encoding='utf8') as conf:
                homePageQuickDirs = json_load(conf)["homePageQuickDirs"]
            # 从文件系统中获取这些路径的信息
            fileController = file_db.FileController()
            res = []  # 结果
            for i in homePageQuickDirs:
                res.extend(fileController.getDirByPath(path=homePageQuickDirs[i]))
        else:  # 给定路径，显示该路径下的文件
            # 从数据库获取文件信息
            fileController = file_db.DBController()
            target = target[:-1] if target.endswith('/') else target
            res = fileController.getItemByFatherPath(target)
            if not res:  # 数据库中没有，则从实际文件系统获取文件信息，并以此更新数据库
                fileController = file_db.FileController()
                res = fileController.getItemsByFatherPath(target, updateDB=True)
        # 将res存入self.currentPageItems
        self.currentPageItems = res
        # 前端对应调整
        if target == "defaultPage":
            self.mainWindowUI.address.setText("主页")
        else:
            self.mainWindowUI.address.setText(target)
        self.mainWindowUI.main_widget.clearContents()  # 清空文件区
        self.mainWindowUI.main_widget.setRowCount(len(res))
        for i in range(len(res)):
            basicInfo = res[i]['basicInfo']
            self.mainWindowUI.main_widget.setItem(i, 0, QTableWidgetItem(basicInfo["name"]))
            self.mainWindowUI.main_widget.setItem(i, 1, QTableWidgetItem(basicInfo["Tags"]))
            self.mainWindowUI.main_widget.setItem(i, 2, QTableWidgetItem(basicInfo["type"]))
            self.mainWindowUI.main_widget.setItem(i, 3, QTableWidgetItem(basicInfo["modifyTime"]))
            self.mainWindowUI.main_widget.setItem(i, 4,
                                                  QTableWidgetItem('%.2f' % basicInfo["size"] + basicInfo["sizeUnit"]))
