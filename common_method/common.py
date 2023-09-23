# -*- encoding: utf-8 -*-
"""
@File    : common
@Time    : 2023/2/20 20:51
@Author  : DING HAO
@Contact : 17826185420
@Version : 1.0
@License : Apache License Version 2.0, January 2021
@Desc    : 公共方法封装
-----------------------------------------------------
"""
import pathlib
import typing
from typing import Union, Any
import uiautomator2
from uiautomator2 import Device
from uiautomator2.exceptions import *
import logging
from tool import path
import os



class Base(Device):

    def __init__(self, device: Device) -> object:
        """
        初始化方法,继承Device类
        :param device: Device
        """
        super().__init__()
        self.ele = None
        self.d = device
        self.log = logging.getLogger(__name__)
        #self.wc = self.d.watch_context(autostart= True, builtin= False)

    def input(self, text, timeout=None, **kwargs):
        """
        输入方法
        :param text:输入内容
        :param timeout:等待时间
        :param kwargs:元素定位
        """
        self.ele = self.find_element(timeout, **kwargs)
        self.ele.clear_text()
        self.ele.set_text(text=text,timeout=timeout)
        self.log.info(f'方法:input,控件:{kwargs},text:{text}')

    def get_text(self, timeout = None, **kwargs):
        """
        获取元素的text
        :param timeout: 超时时间
        :param kwargs: 元素控件
        """
        return self.d(**kwargs).get_text(timeout=timeout)

    def click(self, timeout=None, offset=None, **kwargs):
        """
        点击方法
        :param timeout: 等待时间
        :param offset: (xoff, yoff) default (0.5, 0.5) -> center
        :param kwargs: 元素定位
        """
        self.ele = self.find_element(timeout,**kwargs)
        self.ele.click(timeout, offset)
        self.log.info(f'方法:click,控件:{kwargs}')

    def clear_text(self, **kwargs:Union[dict]):
        """
        清除输入框内容
        :param kwargs:元素定位
        """
        self.d(**kwargs).clear_text()

    def find_element(self,timeout:Union[int, float]=None,  **kwargs):
        """
        公共的元素定位方法
        :param timeout: 等待时间
        :param kwargs:  元素定位
        :return:  UiObject
        """
        if self.is_exist(timeout=timeout, **kwargs):
            self.logger.info(f'方法:find_element,控件:{kwargs}')
            return self.d(**kwargs)

    def is_exist(self,timeout=None, **kwargs):
        """
        判断元素是否存在
        :param timeout: 等待时间,默认为None
        :param kwargs: 元素定位
        :return: bool
        """
        return True if self.wait(timeout=timeout, **kwargs) else \
            UiObjectNotFoundError(
                {'code': -32002, "message": "不存在的控件" ,'data': kwargs},method='wait')

    def wait(self,exists= True, timeout:Union[int, float]=None, **kwargs):
        """
        等待元素出现或消失
        :param exists: bool,默认为True,表示需要等待元素出现,False表示等待元素消失
        :param timeout: 等待时间
        :param kwargs: 元素定位
        """
        return self.d(**kwargs).wait(exists, timeout)

    def app_current(self,key):
        """
        返回当前app的package_name,activity,pid
        :return: package/activity/pid
        """
        class dummy:
           package,activity,pid= [self.d.app_current().get(name,None) \
                                  for name in ['package', 'activity', 'pid']]
        return getattr(dummy,key)

    def sleep(self, seconds: float):
        """
        强制等待
        :param seconds: 秒
        """
        self.d.sleep(seconds=seconds)

    def assertion_equal(self, value, expect_value):
        """
        断言值是否相等
        :param value: 不能为空
        :param expect_value: 不能为空
        """
        if value and expect_value:
            assert f'{expect_value}'==f'{value}',f"{expect_value}!={value}"
        else:
            raise ValueError('值不能为空!')

    def screenshot(self, filename:str, format = 'pillow'):
        """
        截图,默认存放在screenshot文件夹下
        :param filename: 文件名
        """
        assert filename.endswith(('.jpg', '.jpeg', '.png')),'filename必须以.jpg/.png/.jpeg结尾'
        dir = path.mk_dir('screenshot/')
        _filename = os.path.split(filename)[-1]
        res = pathlib.WindowsPath(dir).joinpath(_filename)
        self.d.screenshot(filename = res, format =format)
        self.log.info(f'已截图,文件:{res}')

    def scroll_to(self, f:dict=None ,**kwargs):
        """
        滑动到所要定位的控件
        :param f: 初始控件
        :return: UiObject
        """
        if f is None:
            _from = self.d().scroll
        else:
            if not isinstance(f ,dict):
                raise TypeError(f'f必须为dict类型!,当前为{type(f)}')
            _from = self.d(**f).scroll
        _to = getattr(_from, 'to')(**kwargs)
        self.log.info(f'已滑动到控件:{kwargs}')
        return kwargs

    def fling(self, action,vertical = True, **kwargs):
        """
        水平/垂直快速滑动
        :param action: action (str): one of "forward", "backward", "toBeginning", "toEnd", "to"
        :param vertical: 默认True,垂直滑动,False,水平滑动
        :param kwargs:  当前位置

        """
        _from = self.d(**kwargs).fling
        _from.vertical = vertical
        res = getattr(_from, action, None)()
        self.log.info(f'已执行{action}操作')
        self.d.xpath.scroll_to()

    def watch_context_when(self, xpath: str):
        """
        当条件满足时,支持 .watch_context_when(..).watch_context_when(..) 的级联模式
        :param xpath: xpath
        :return: Base
        """
        self.wc.when(xpath= xpath)
        return self

    def watch_context_click(self):
        """
        目前只有点击操作
        """
        self.wc.click()
        self.log.info(f'已执行wc.click操作')

    def watch_context_call(self,func: typing.Callable):
        """
        support args (d: Device, el: Element)
        :param xpath: xpath
        :param func: function
        """
        # try:
        #     assert callable(func)
        # except:
        #     raise TypeError
        # else:
        self.wc.call(fn=func)

    def get_toast(self,time=10,cache_time=10,default=None):
        """
        获取toast
            wait_timeout: seconds of max wait time if toast now show right now
            cache_timeout: return immediately if toast showed in recent $cache_timeout
            default: default messsage to return when no toast show up
        """
        msg = self.d.toast.get_message(wait_timeout=time, cache_timeout=cache_time, default=default)
        self.log.info('已获取toast:%s' %msg)
        return msg

    def swipe(self, direction , steps=5, **kwargs):
        """
        UiObject滑动操作
            direction (str): one of ("left", "right", "up", "down")
            steps (int): move steps, one step is about 5ms
        """
        self.d(**kwargs).swipe(direction= direction , steps= steps)
        self.log.info(f'滑动方向:{direction},控件:{kwargs}')

    def drag_to(self, f:dict, *args, **kwargs):
        """
        拖动一个控件到另一个控件/坐标
        :param f: 初始控件
        :param args: 坐标(%/px)
        :param kwargs: 可以是包含x,y的字典,也可以是其他定位方式
        """
        if not isinstance(f,dict):
            raise TypeError
        else:
            self.d(**f).drag_to(*args, **kwargs)
            self.log.info(f'拖拽{f}控件到-->{args or kwargs}控件/坐标' )

    def count(self,**kwargs):
        """
        返回控件的数量
        :param kwargs: 控件
        """
        c = self.d(**kwargs).count
        self.log.info('{}控件的数量为{}'.format(kwargs,c))
        return c

    def get_item(self, index ,**kwargs):
        """
        支持索引选择控件
        :param index:  索引
        :param kwargs: 控件
        """
        count = self.count(**kwargs)
        assert 0 <= index <= count,f'{index}应该小于等于最大索引{count}'
        return self.d(**kwargs)[index]

    def center(self,offset=(0.5,0.5) , **kwargs):
        """
        返回中心点坐标(x,y)
        :param offset: 偏移量,默认(0.5,0.5)
        """
        x,y = self.d(**kwargs).center(offset=offset)
        self.log.info(f'{kwargs}控件的中心点坐标:{(x,y)}')
        return x,y

    def bounds(self, **kwargs):
        """
        返回元素的边界值
        :param kwargs: 元素控件
        :return: left_top_x, left_top_y, right_bottom_x, right_bottom_y
        """
        return self.d(**kwargs).bounds()

    def rect(self,**kwargs):
        """
        返回left_top_x, left_top_y, width, height
        :param kwargs:控件
        :return: (left_top_x, left_top_y, width, height)
        """
        lx,ly,rx,ry = self.bounds(**kwargs)
        return lx,ly,rx-lx,ry-ly



