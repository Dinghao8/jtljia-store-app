# -*- encoding: utf-8 -*-
"""
@File    : demo
@Time    : 2022/11/27 14:26
@Author  : DINGHAO
@Contact : 17826185420
@Version : 1.0
@License : Apache License Version 2.0, January 2021
@Desc    : None
-----------------------------------------------------
"""
import os
import random
import subprocess
import sys
import time

import pytest
import uiautomator2 as u2
from uiautomator2.swipe import SwipeExt as se
from uiautomator2.watcher import XPathWatcher as xw
from collections import  OrderedDict
import typing

'''APPIUM
caps = {
    "appium:automationName": "UiAutomator2",
    "platformName": "android",
    "appium:platformVersion": "5.1.1",
    "appium:noReset": True,
    "appium:appPackage": "com.tencent.weread",
    "appium:appActivity": ".WeReadFragmentActivity"
}
# options = u2()
# options.load_capabilities(caps=caps)
# driver = wd.Remote(command_executor='http://127.0.0.1:4723/wd/hub', options=options)
# driver.find_element('class name', 'android.widget.TextView').click()
# time.sleep(3)
# driver.find_element('class name', 'android.widget.Button').click()
'''

'''
res = u2.connect()
res.app_start("com.goldmantis.appjia",stop=True)
res(resourceId='com.goldmantis.appjia:id/et_account').send_keys('N0065636')
res(resourceId='com.goldmantis.appjia:id/et_pwd').send_keys('Dh19970322')
# res.send_action('3')
res.implicitly_wait(5)
res(resourceId='com.goldmantis.appjia:id/btn_login').click()
time.sleep(2)
res(resourceId='com.goldmantis.appjia:id/tv_shop').click()
print(res.app_info(res.app_current().get('package')),res.current_ime(),res.app_list('-3'),sep='\n')
res.app_stop("com.goldmantis.appjia")
'''




def test_(device):
    d =device
    c = d.xpath.scroll_to('金螳螂家吴江公司')
    print(c)
    res = c.scroll_to('工程总监').click()






