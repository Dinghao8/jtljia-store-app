# -*- encoding: utf-8 -*-
"""
@File    : common
@Time    : 2023/2/9 20:33
@Author  : DING HAO
@Contact : 17826185420
@Version : 1.0
@License : Apache License Version 2.0, January 2021
@Desc    : None
-----------------------------------------------------
"""
import logging
import uiautomator2
import time
import pytest
import allure
from tool import config,yaml_read,path
from uiautomator2 import exceptions, Device
from common_method.common import Base

# setting
data = config(r'setup.cfg')['APP']
# 被测app,直接在配置文件里配置
app = data['app']
# activity
activity = data['activity'] or None
# addr
addr = data['addr'] or None
# package
package = data['package']  or None
# wait
wait = data['wait'] or False
# stop
stop = data['stop'] or False
# login.yaml登录数据
file = config(r'setup.cfg')['LOGIN']['file']
login_file = path.current_dir.joinpath('Data', file)
# wait_timeout等待时间
wait_time = 8
# 日志
logger = logging.getLogger(__name__)


@allure.title(f'启动被测app:{app}')
@allure.severity('normal')
@pytest.fixture(scope='session', name='device')
def test_device(package_name = app, activity = activity, addr: str = addr,\
                package = package, wait = wait, stop = stop):
    """连接设备,并返回测试的app"""
    try:
        _device: Device = uiautomator2.connect(addr=addr)      #连接设备
        logger.info(f'正在连接:{_device}...')
        if package:
            _device.app_install(data=package)              #如果需要,先安装app
        _device.app_start(package_name=package_name, \
                          activity=activity, wait=wait, stop=stop)   #启动app
        logger.info('成功启动:%s' %package_name)
        return _device
    except:
        logger.error('未能连接到:%s' % app)
        raise exceptions.ConnectError('未能连接到:%s' % app)


@allure.title('登录门店app')
@allure.severity('critical')
@pytest.fixture(scope='function',name='login')
def test_login(device, login_data):
    """登录操作"""
    data, account, pwd, activity = login_data.values()
    res = Base(device)                                 # 实例化base
    res.implicitly_wait(wait_time)
    while time.time()<time.time() +10:
        time.sleep(3)
        if res.app_current('activity')==activity:   #打开app,如果当前页面是金螳螂家页面,则无需登录
            logger.info('当前页面:%s,无需登录' %activity)
            return res
            break
        else:
            with allure.step('输入工号:%s' %account):
                res.input(text=account, **data['account_ele'])    #输入工号
            with allure.step(f'输入密码:%s' %pwd):
                res.input(text=pwd,**data['pwd_ele'])         #输入密码
            with allure.step('点击登录按钮'):
                res.click(.1,**data['login_btn_ele'])         #登录按钮
            with allure.step('定位:{}元素,选择角色:{}'.format(*data['store_ele']['to'].keys(),
                                                      *data['store_ele']['to'].values())):
                ele = res.scroll_to(f = data['store_ele']['from'],
                                **data['store_ele']['to'])      #选择角色
            with allure.step('点击选中的角色'):
                res.click(.1,**ele)                                        #点击角色
            res.sleep(1.5)
            # 断言当前页面是否为com.goldmantis.appjia.splash.MainActivity
            with allure.step('断言操作'):
                res.assertion_equal(res.app_current('activity'),activity)
            with allure.step('登录成功并截图'):
                res.screenshot('MainActivity.jpg')
                allure.attach.file(r'./screenshot/MainActivity.jpg',attachment_type=allure.attachment_type.JPG)
            logger.info('登录成功!')
            return res
            break

@allure.title('读取login.yaml数据')
@pytest.fixture(params=yaml_read(file = login_file),name='login_data')
def test_data(request):
    """全局读取yaml数据"""
    return request.param


@allure.title('执行teardown')
@allure.severity('normal')
@pytest.fixture(scope='session', name='finalizer')
def test_finalizer(device, request):
    """teardown函数,所有测试用例执行完后执行"""
    logger.info('正在关闭:%s...' % device)
    def func():
        _d = device
        _d.app_stop(package_name=app)
    request.addfinalizer(func)

def pytest_addoption(parser):
    """
    添加命令行/ini参数
    """
    parser.addini('log_file',help='日志文件',type='string' ,\
                  default='log/'+time.strftime('%Y-%m-%d')+'.log')


