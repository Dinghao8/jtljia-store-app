# -*- encoding: utf-8 -*-
"""
@File    : logs
@Time    : 2023/3/8 21:25
@Author  : DING HAO
@Contact : 17826185420
@Version : 1.0
@License : Apache License Version 2.0, January 2021
@Desc    : None
-----------------------------------------------------
"""

import logzero
from tool import config, Path
import pathlib
import time



# 读取配置文件
file = path.parent_dir.joinpath('setup.cfg')
conf = config(file=file)
# 日志格式
fmt = conf.get_value('LOG', 'fmt')
# 日志日期格式
date_format = conf.get_value('LOG', 'date_format')
# 日志等级,当前为info
level = conf.get_value('LOG', 'level')
# 日志文件
date = time.strftime('%Y-%m-%d')
log_file = date+'.log'


class logs:

    def __init__(self):
        try:
            self.p = pathlib.WindowsPath(path.parent_dir, 'logs', log_file)
            if self.p.exists():
                # pathlib.WindowsPath(path.parent_dir, 'logs').mkdir(exist_ok=True)
                pass
            else:
                pathlib.WindowsPath(path.parent_dir, 'logs').mkdir(exist_ok=True)
                self.p.touch()
        except:
            raise FileExistsError('%s:文件已存在' % self.p)
        else:
            self.format = logzero.LogFormatter(fmt=fmt, datefmt=date)
            self.logger = logzero.setup_logger(logfile=self.p, level=level,formatter=self.format,
                                               maxBytes=10240,backupCount=3,disableStderrLogger=True)

    def debug(self, message):  # 打印debug级别的日志
        self.logger.debug(message)

    def info(self, message):  # 打印info级别的日志
        self.logger.info(message)

    def warn(self, message):  # 打印warn级别的日志
        self.logger.warning(message)

    def error(self, message):  # 打印error级别的日志
        self.logger.error(message)

    def critical(self, message):  # 打印critical级别的日志
        self.logger.critical(message)

