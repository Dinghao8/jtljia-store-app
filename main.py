# -*- encoding: utf-8 -*-
"""
@File    : main
@Time    : 2023/3/22 14:58
@Author  : DING HAO
@Contact : 17826185420
@Version : 1.0
@License : Apache License Version 2.0, January 2021
@Desc    : None
-----------------------------------------------------
"""

import os
import pytest
import shutil

if __name__ == '__main__':
    pytest.main()
    # 复制environment.properties至allure_report目录
    shutil.copy('./environment.properties', './allure_report')
    # 在生成报告前删除已存在的报告文件夹
    os.system('allure generate ./allure_report -o ./allure_report/html -c ')
    # 执行allure serve命令打开报告
    # os.system('allure serve ./allure_report/html')
