import os
import re
import sqlite3

import cv2
import pymysql
from datetime import datetime
from json import load as json_load
from tinytag import TinyTag

dirInfo = ['name', 'type', 'path', 'modifyTime', 'createTime', 'accessTime', 'fatherPath', 'size', 'sizeUnit',
           'Tags']  # 数据库中，dir表的各项参数
dirBasicInfo = ['name', 'Tags', 'type', 'modifyTime', 'size', 'sizeUnit']
dirOtherInfo = ['path', 'createTime', 'accessTime', 'fatherPath']
musicInfo = ['name', 'album', 'mvPath', 'duration', 'bitRate', 'sampleRate', 'path', 'genre', 'year', 'fatherPath',
             'size', 'sizeUnit', 'Tags', 'type', 'modifyTime', 'createTime', 'accessTime', 'singer']
musicBasicInfo = ['name', 'Tags', 'type', 'modifyTime', 'size', 'sizeUnit']
musicOtherInfo = ['album', 'mvPath', 'duration', 'bitRate', 'sampleRate', 'path', 'genre', 'year', 'fatherPath',
                  'createTime', 'accessTime', 'singer']
videoInfo = ['name', 'Tags', 'type', 'modifyTime', 'size', 'sizeUnit', 'path', 'ext', 'createTime', 'accessTime',
             'fatherPath', 'duration', 'width', 'height', 'bitRate', 'fps']
videoBasicInfo = ['name', 'Tags', 'type', 'modifyTime', 'size', 'sizeUnit']
videoOtherInfo = ['path', 'ext', 'createTime', 'accessTime', 'fatherPath', 'duration', 'width', 'height', 'bitRate',
                  'fps']
imageInfo = ["name", "Tags", "type", "modifyTime", "size", "sizeUnit", "path", "ext", "createTime", "accessTime",
             "fatherPath", "width", "height"]
imageBasicInfo = ["name", "Tags", "type", "modifyTime", "size", "sizeUnit"]
imageOtherInfo = ["path", "ext", "createTime", "accessTime", "fatherPath", "width", "height"]
fileInfo = ['name', 'type', 'path', 'ext', 'size', 'sizeUnit', 'modifyTime', 'createTime', 'accessTime',
            'fatherPath', 'Tags']
fileBasicInfo = ['name', 'Tags', 'type', 'modifyTime', 'size', 'sizeUnit']
fileOtherInfo = ['path', 'ext', 'createTime', 'accessTime', 'fatherPath']


def dict_factory(cursor, row):
    """该函数用以使Sqlite3请求的结果为字典，便于操作"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Dir:
    """文件夹类"""

    def __init__(self, path):
        self.path = path
        self.fatherPath = "/".join(path.split("/")[:-1])
        self.name = os.path.basename(path)
        self.size = self._getDirSize()
        self.sizeUnit = ''
        self.modifyTime = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
        self.createTime = datetime.fromtimestamp(os.path.getctime(path)).strftime('%Y-%m-%d %H:%M:%S')
        self.accessTime = datetime.fromtimestamp(os.path.getatime(path)).strftime('%Y-%m-%d %H:%M:%S')
        self.type = "文件夹"
        self.Tags = ''
        self._adjustSize()

    def _getDirSize(self):
        """获取文件夹大小"""
        totalSize = 0
        for dirpath, names, names in os.walk(self.path):
            for f in names:
                fp = os.path.join(dirpath, f)
                totalSize += os.path.getsize(fp)
        return totalSize  # Unit: Byte

    def _adjustSize(self):
        """调整大小及单位"""
        if self.size >= pow(1024, 3):
            self.sizeUnit = "GB"
            self.size = self.size / pow(1024, 3)
        elif self.size >= pow(1024, 2):
            self.sizeUnit = "MB"
            self.size = self.size / pow(1024, 2)
        elif self.size >= 1024:
            self.sizeUnit = "KB"
            self.size = self.size / 1024
        else:
            self.sizeUnit = "B"

    def getInfo(self):
        content = {'path': self.path, 'name': self.name, 'size': self.size, 'sizeUnit': self.sizeUnit,
                   'type': self.type, 'Tags': self.Tags, 'fatherPath': self.fatherPath, 'modifyTime': self.modifyTime,
                   'createTime': self.createTime, 'accessTime': self.accessTime}
        basicInfo = dict(zip(dirBasicInfo, [content[key] for key in dirBasicInfo]))
        otherInfo = dict(zip(dirOtherInfo, [content[key] for key in dirOtherInfo]))
        res = {'basicInfo': basicInfo, 'otherInfo': otherInfo}
        return res


class File:
    """
    这个类（及其子类）用于详细描述某文件的相关参数
    """

    def __init__(self, filePath, type=None):
        # 创建基本的文件参数
        self.path = filePath
        if not os.path.exists(self.path):
            return
        self.name = ''  # 文件名
        self.ext = ''  # 扩展名
        self.size = ''
        self.sizeUnit = ''
        self.modifyTime = ''
        self.createTime = ''
        self.accessTime = ''
        self.fatherPath = ''
        self.Tags = ''
        self.type = type if type else '文件'
        self.initial()

    def initial(self):
        self.name = os.path.split(self.path)[1]
        self.ext = os.path.splitext(self.path)[1]
        self._adjustSize()  # 调整大小及单位
        self.modifyTime = datetime.fromtimestamp(os.path.getmtime(self.path)).strftime('%Y-%m-%d %H:%M:%S')
        self.createTime = datetime.fromtimestamp(os.path.getctime(self.path)).strftime('%Y-%m-%d %H:%M:%S')
        self.accessTime = datetime.fromtimestamp(os.path.getatime(self.path)).strftime('%Y-%m-%d %H:%M:%S')
        self.fatherPath = "/".join(self.path.split("/")[:-1])

    def _adjustSize(self) -> None:
        """
        格式化文件大小
        :return: dict['size':float,'unit':str]
        """
        size = os.path.getsize(self.path)
        if size >= pow(1024, 3):
            self.sizeUnit = "GB"
            size = size / pow(1024, 3)
        elif size >= pow(1024, 2):
            self.sizeUnit = "MB"
            size = size / pow(1024, 2)
        elif size >= 1024:
            self.sizeUnit = "KB"
            size = size / 1024
        else:
            self.sizeUnit = "B"
        self.size = size

    def getInfo(self):
        res = {'path': self.path, 'name': self.name, 'ext': self.ext, 'size': self.size, 'fatherPath': self.fatherPath,
               'sizeUnit': self.sizeUnit, 'modifyTime': self.modifyTime, 'createTime': self.createTime,
               'accessTime': self.accessTime, 'type': self.type, 'Tags': self.Tags}
        basicInfo = dict(zip(fileBasicInfo, [res[key] for key in fileBasicInfo]))
        otherInfo = dict(zip(fileOtherInfo, [res[key] for key in fileOtherInfo]))
        res = {'basicInfo': basicInfo, 'otherInfo': otherInfo}
        return res


class Music(File):
    def __init__(self, filePath):
        """
        音乐文件类，继承自File类
        :param filePath:str:文件路径
        """
        self.name = ''  # 歌曲名
        self.album = ''  # 专辑名
        self.singer = ''  # 歌手名
        self.genre = ''  # 流派
        self.year = ''  # 年
        self.duration = ''  # 时长
        self.bitRate = ''  # 比特率
        self.sampleRate = ''  # 采样率
        super().__init__(filePath=filePath)

    def initial(self):
        super(Music, self).initial()
        self.type = "音乐"
        self._parseMusicInfo()

    def _parseMusicInfo(self):
        tagInfo = TinyTag.get(self.path)
        self.name = tagInfo.title
        self.album = tagInfo.album
        singers = re.split("[,;，；/]", tagInfo.artist)
        singers.sort()
        self.singer = ", ".join(singers)
        self.genre = tagInfo.genre if tagInfo.genre else ''  # 流派
        self.year = tagInfo.year if tagInfo.year else ''  # 年
        self.duration = str(int(tagInfo.duration / 60)) + ":" + str(int(tagInfo.duration % 60))
        self.bitRate = str(tagInfo.bitrate) + "Kbps"
        self.sampleRate = str(tagInfo.samplerate) + "Hz"

    def getInfo(self):
        res = super(Music, self).getInfo()
        res['basicInfo']['name'] = self.name
        res['otherInfo']['album'] = self.album
        res['otherInfo']['singer'] = self.singer
        res['otherInfo']['duration'] = self.duration
        res['otherInfo']['bitRate'] = self.bitRate
        res['otherInfo']['sampleRate'] = self.sampleRate
        res['otherInfo']['mvPath'] = ''
        res['otherInfo']['genre'] = self.genre
        res['otherInfo']['year'] = self.year
        return res


class Video(File):
    def __init__(self, filePath):
        """
        视频文件类，继承自File类
        :param filePath:str:文件路径
        """
        self.duration = ''  # 时长
        self.width = ''  # 宽
        self.height = ''  # 高
        self.bitRate = ''  # 比特率
        self.fps = ''  # 帧率
        super().__init__(filePath=filePath)

    def initial(self):
        super(Video, self).initial()
        self.type = "视频"
        self._parseVideoInfo()

    def _parseVideoInfo(self):
        video = cv2.VideoCapture(self.path)
        sec = int(video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS))
        self.duration = str(sec // 60).zfill(2) + ":" + str(sec % 60).zfill(2)
        self.width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = video.get(cv2.CAP_PROP_FPS)
        self._parseBitRate(video)

    def _parseBitRate(self, video):
        kbps = (os.path.getsize(self.path) * 8 / 1024) / (
                video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS))  # kbit/sec
        if kbps >= 1024:
            self.bitRate = str(round(kbps / 1024, 2)) + "Mbps"
        else:
            self.bitRate = str(round(kbps, 2)) + "Kbps"

    def getInfo(self):
        res = super(Video, self).getInfo()
        res['otherInfo']['duration'] = self.duration
        res['otherInfo']['width'] = self.width
        res['otherInfo']['height'] = self.height
        res['otherInfo']['bitRate'] = self.bitRate
        res['otherInfo']['fps'] = self.fps
        return res


class Image(File):
    def __init__(self, filePath):
        """
        图片文件类，继承自File类
        :param filePath:str:文件路径
        """
        self.width = 0  # 宽
        self.height = 0  # 高
        super().__init__(filePath=filePath)

    def initial(self):
        super(Image, self).initial()
        self.type = "图片"
        self._parseImageInfo()

    def _parseImageInfo(self):
        """获取图片的宽度和高度"""
        img = cv2.VideoCapture('D:/Desktop/1 编译.jpg')
        self.width = int(img.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(img.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def getInfo(self):
        res = super(Image, self).getInfo()
        res['otherInfo']['width'] = self.width
        res['otherInfo']['height'] = self.height
        return res


class FileController:
    def __init__(self):
        self.queryRes = []

    def refreshItemsByFatherPath(self, fatherPath) -> None:
        """
        根据父目录，从文件系统中获取查询文件（存在self.queryRes中）
        :param fatherPath: str: 父目录路径
        """
        for item in os.listdir(fatherPath + "/"):
            itemPath = fatherPath + "/" + item
            if os.path.isdir(itemPath):
                self.queryRes.append(Dir(path=itemPath).getInfo())
            elif os.path.isfile(itemPath):
                fileType = self._adjustFileType(itemPath)
                if fileType == "文件":
                    self.queryRes.append(File(filePath=itemPath).getInfo())
                elif fileType == "快捷方式":
                    self.queryRes.append(File(filePath=itemPath, type='快捷方式').getInfo())
                elif fileType == "软件":
                    self.queryRes.append(File(filePath=itemPath, type='软件').getInfo())
                elif fileType == "文档（不可读）":
                    self.queryRes.append(File(filePath=itemPath, type='文档（不可读）').getInfo())
                elif fileType == "音乐":
                    self.queryRes.append(Music(filePath=itemPath).getInfo())
                elif fileType == "视频":
                    self.queryRes.append(Video(filePath=itemPath).getInfo())
                elif fileType == "图片":
                    self.queryRes.append(Image(filePath=itemPath).getInfo())
            else:  # 既不是文件也不是文件夹，不知道该属于什么了，就忽略掉
                continue

    def getDirByPath(self, path, updateDB=False):
        self.queryRes=[Dir(path=path).getInfo()]
        if updateDB:
            self.updateDB()
        return self.queryRes
    def getItemsByFatherPath(self, fatherPath, updateDB=False):
        self.refreshItemsByFatherPath(fatherPath)
        if updateDB:
            self.updateDB()
        return self.queryRes

    def updateDB(self):
        dbController = DBController()
        dbController.updateDB(self.queryRes)

    @staticmethod
    def _adjustFileType(filePath):
        """
        用于判断文件属于哪种类型
        :param filePath: str:文件路径
        :return:str:文件类型
        """
        with open("config.json", 'r', encoding='utf8') as conf:
            fileExt = json_load(conf)['fileExt']  # 各类文件的扩展名
        for typeName in fileExt:
            ext = filePath.split('.')[-1]
            if ext.lower() in fileExt[typeName]:
                return typeName
        else:
            if os.path.exists(filePath):
                return "文件"
            else:
                return ''


class DBController:
    def __init__(self):
        with open("config.json", 'r', encoding='utf8') as conf:
            res = json_load(conf)
            self.dbType = res['dbType']
            SqlitePath = res['projectPath'] + res['SqlitePath']
            MySQLHost = res['MySQLHost']
            MySQLPort = res['MySQLPort']
            MySQLUser = res['MySQLUser']
            MySQLPassword = res['MySQLPassword']
            MySQLDatabase = res['MySQLDatabase']
        if self.dbType == 'Sqlite':
            self.SqlitePath = SqlitePath
            self.conn = sqlite3.connect(self.SqlitePath)
            self.conn.row_factory = dict_factory  # 设置按字典方式返回查询结果
            self.cursor = self.conn.cursor()
        elif self.dbType == 'MySQL':
            self.MySQLHost = MySQLHost
            self.MySQLPort = MySQLPort
            self.MySQLUser = MySQLUser
            self.MySQLPassword = MySQLPassword
            self.MySQLDatabase = MySQLDatabase
            self.conn = pymysql.connect(host=self.MySQLHost, port=self.MySQLPort, user=self.MySQLUser,
                                        database=self.MySQLDatabase, password=self.MySQLPassword)
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)  # 设置按字典方式返回查询结果

    def _splitQueryRes(self, queryList, queryType):
        """
        将查询结果分割出basicInfo和otherInfo

        :param queryList:list:查询结果
        :param queryType:str:查询对象
        """
        resList = []
        for fetch in queryList:
            if queryType == 'dir':
                basicInfo = dict(zip(dirBasicInfo, [fetch[key] for key in dirBasicInfo]))
                otherInfo = dict(zip(dirOtherInfo, [fetch[key] for key in dirOtherInfo]))
                res = {'basicInfo': basicInfo, 'otherInfo': otherInfo}
                resList.append(res)
            elif queryType == 'file':
                basicInfo = dict(zip(fileBasicInfo, [fetch[key] for key in fileBasicInfo]))
                otherInfo = dict(zip(fileOtherInfo, [fetch[key] for key in fileOtherInfo]))
                res = {'basicInfo': basicInfo, 'otherInfo': otherInfo}
                resList.append(res)
            elif queryType == 'music':
                basicInfo = dict(zip(musicBasicInfo, [fetch[key] for key in musicBasicInfo]))
                otherInfo = dict(zip(musicOtherInfo, [fetch[key] for key in musicOtherInfo]))
                res = {'basicInfo': basicInfo, 'otherInfo': otherInfo}
                resList.append(res)
            elif queryType == 'video':
                basicInfo = dict(zip(videoBasicInfo, [fetch[key] for key in videoBasicInfo]))
                otherInfo = dict(zip(videoOtherInfo, [fetch[key] for key in videoOtherInfo]))
                res = {'basicInfo': basicInfo, 'otherInfo': otherInfo}
                resList.append(res)
            elif queryType == 'image':
                basicInfo = dict(zip(imageBasicInfo, [fetch[key] for key in imageBasicInfo]))
                otherInfo = dict(zip(imageOtherInfo, [fetch[key] for key in imageOtherInfo]))
                res = {'basicInfo': basicInfo, 'otherInfo': otherInfo}
                resList.append(res)
        return resList

    def getMusicByName(self, name):
        """按标题获取数据库中音乐文件"""
        self.cursor.execute("SELECT * FROM music WHERE FIND_IN_SET('%s', name)" % name)
        fetchList = self.cursor.fetchall()
        return self._splitQueryRes(fetchList, 'music')

    def getMusicByFatherPath(self, fatherPath):
        """按父路径获取数据库中音乐文件"""
        self.cursor.execute("SELECT * FROM music WHERE fatherPath = '%s'" % fatherPath)
        fetchList = self.cursor.fetchall()
        return self._splitQueryRes(fetchList, 'music')

    def getVideoByFatherPath(self, fatherPath):
        """按父路径获取数据库中视频文件"""
        self.cursor.execute("SELECT * FROM video WHERE fatherPath = '%s'" % fatherPath)
        fetchList = self.cursor.fetchall()
        return self._splitQueryRes(fetchList, 'video')

    def getImageByFatherPath(self, fatherPath):
        """按父路径获取数据库中图片文件"""
        self.cursor.execute("SELECT * FROM image WHERE fatherPath = '%s'" % fatherPath)
        fetchList = self.cursor.fetchall()
        return self._splitQueryRes(fetchList, 'image')

    def getFileByName(self, name):
        """按文件名获取数据库中文件"""
        self.cursor.execute("SELECT * FROM file WHERE FIND_IN_SET('%s',name)" % name)
        fetchList = self.cursor.fetchall()
        return self._splitQueryRes(fetchList, 'file')

    def getFileByFatherPath(self, fatherPath) -> list:
        """获取数据库中某父目录下的所有文件"""
        self.cursor.execute("SELECT * FROM file WHERE fatherPath = '%s'" % fatherPath)
        fetchList = self.cursor.fetchall()
        return self._splitQueryRes(fetchList, 'file')

    def getFileByPath(self, path) -> list:
        """根据路径获取文件信息"""
        self.cursor.execute("SELECT * FROM file WHERE path = '%s'" % path)
        fetchList = self.cursor.fetchall()
        return self._splitQueryRes(fetchList, 'file')

    def getDirByName(self, name) -> list:
        """
        根据文件夹名获取文件夹信息
        需要注意，文件夹名可能不唯一，所以返回的是一个列表
        :param name:str:文件夹名
        """
        self.cursor.execute("SELECT * FROM dir WHERE name = '%s'" % name)
        fetchList = self.cursor.fetchall()
        return self._splitQueryRes(fetchList, 'dir')

    def getDirByFatherPath(self, fatherPath) -> list:
        """获取数据库中某父目录下的所有文件夹"""
        self.cursor.execute("SELECT * FROM dir WHERE fatherPath = '%s'" % fatherPath)
        fetchList = self.cursor.fetchall()
        return self._splitQueryRes(fetchList, 'dir')

    def getItemByName(self, name) -> list:
        """
        根据文件名获取对象信息

        :param name:str:文件路径
        """
        self.cursor.execute("SELECT * FROM file WHERE name = '%s'" % name)
        fetchList = self.cursor.fetchall()
        resList = self._splitQueryRes(fetchList, 'file')
        self.cursor.execute("SELECT * FROM dir WHERE name = '%s'" % name)
        fetchList = self.cursor.fetchall()
        resList.extend(self._splitQueryRes(fetchList, 'dir'))
        self.cursor.execute("SELECT * FROM music WHERE name = '%s'" % name)
        fetchList = self.cursor.fetchall()
        resList.extend(self._splitQueryRes(fetchList, 'music'))
        self.cursor.execute("SELECT * FROM video WHERE name = '%s'" % name)
        fetchList = self.cursor.fetchall()
        resList.extend(self._splitQueryRes(fetchList, 'video'))
        self.cursor.execute("SELECT * FROM image WHERE name = '%s'" % name)
        fetchList = self.cursor.fetchall()
        resList.extend(self._splitQueryRes(fetchList, 'image'))
        return resList

    def getItemByFatherPath(self, fatherPath) -> list:
        """
        根据文件父路径获取文件信息
        :param fatherPath:str:文件父路径
        """
        res = []
        res.extend(self.getDirByFatherPath(fatherPath))
        res.extend(self.getFileByFatherPath(fatherPath))
        res.extend(self.getMusicByFatherPath(fatherPath))
        res.extend(self.getVideoByFatherPath(fatherPath))
        res.extend(self.getImageByFatherPath(fatherPath))
        return res

    def updateDB(self, data: list[dict]):
        """
        更新数据库
        :param data:dict:数据
        """
        unique_key = 'path'
        for item in data:  # 对每个对象进行操作
            info = {**item['basicInfo'], **item['otherInfo']}  # 合并basicInfo和otherInfo
            key, value = zip(*info.items())
            key = list(key)
            value = list(value)
            if info['type'] in ('文件', '快捷方式', '软件', '文档（不可读）'):
                table = 'file'
            elif info['type'] == '音乐':
                table = 'music'
            elif info['type'] == '图片':
                table = 'image'
            elif info['type'] == '视频':
                table = 'video'
            elif info['type'] == '文件夹':
                table = 'dir'
            else:  # 未知类型，跳过
                continue
            # 更新数据库
            if info['type'] == '音乐':  # 一些前期检查，依次检查歌手和专辑是否存在记录，不存在则插入，然后再判断歌曲并插入/更新
                # 检查歌手
                singer = info['singer']
                self.cursor.execute("SELECT * FROM music_singer WHERE name = '%s'" % singer)
                fetch = self.cursor.fetchone()
                if not fetch:  # 如果不存在，则插入
                    self.cursor.execute(
                        "INSERT INTO music_singer (name) VALUES ('%s')" % singer)  # 因为从歌曲文件的tags中只能知道歌手名
                    self.conn.commit()
                # 检查专辑，差不多
                album = info['album']
                self.cursor.execute("SELECT * FROM music_album WHERE name = '%s'" % album)
                fetch = self.cursor.fetchone()
                if not fetch:  # 如果不存在，则插入
                    self.cursor.execute("INSERT INTO music_album (name) VALUES ('%s')" % album)
                    self.conn.commit()
            # 剩下的就是更新主表，因为文件/配置文件、文件夹都只有一个表，所以跳过前面那些复杂的准备工作
            # 先将旧记录删掉
            self.cursor.execute("DELETE FROM %s WHERE %s = '%s'" % (table, unique_key, info[unique_key]))
            self.conn.commit()
            # 然后插入新记录
            values = ', '.join(["'" + v + "'" if isinstance(v, str) else str(v) for v in value])
            self.cursor.execute("INSERT INTO %s (%s) VALUES (%s)" % (table, ','.join(key), values))
            self.conn.commit()
