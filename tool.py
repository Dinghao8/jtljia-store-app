# -*- encoding: utf-8 -*-
"""
@File    : tool
@Time    : 2023/2/12 20:21
@Author  : DING HAO
@Contact : 17826185420
@Version : 1.0
@License : Apache License Version 2.0, January 2021
@Desc    : 常用工具模块
-----------------------------------------------------
"""
import os.path
from configparser import ConfigParser, \
    NoSectionError, NoOptionError, BasicInterpolation, ExtendedInterpolation
import pathlib
import yaml
from yaml import YAMLError



class config(ConfigParser):
    def __init__(self, file):
        self.data = None
        self.file = file
        super(config, self).__init__()
        super(config, self).read(filenames=self.file, encoding='utf-8')

    def get_value(self, section: str, option: str):
        """根据section和option获取值"""
        try:
            data = super(config, self).get(section=section, option=option)
            return data
        except :
             raise

    def add_section(self, section):
        """新增节点section"""
        if section:
            new_section = str(section).upper()
        else:
            raise ValueError('section不能为空!')
        super(config, self).add_section(section=new_section)
        with open(file=self.file, mode='w+', encoding='utf-8') as _file:
            super(config, self).write(fp=_file)
            _file.close()

    def has_section(self, section: str) -> bool:
        """布尔值,true代表有节点,false代表无此节点"""
        _ = super().has_section(section=section)
        return _

    def has_option(self, section: str, option: str) -> bool:
        """布尔值,true代表有选项,false代表无此选项"""
        _res = super(config, self).has_option(section=section, option=option)
        return _res

    def add_option(self, section, option, value=None):
        """给节点新增选项和值"""
        try:
            if super(config, self).has_section(section=section):
                pass
        except:
            raise
        else:
            super().set(section=section, option=option, value=value)
            with open(file=self.file, mode='w+', encoding='utf-8') as _file:
                super().write(fp=_file)
                _file.close()

    def remove_section(self, section: str) -> bool:
        """返回布尔值,删除section"""
        _res = super(config, self).remove_section(section=section)
        return _res

    def remove_option(self, section: str, option: str) -> bool:
        """返回布尔值,删除option"""
        _res = super(config, self).remove_option(section=section, option=option)
        return _res

    def options(self, section: str) -> list[str]:
        """返回所有的options"""
        _res = super(config, self).options(section=section)
        return _res

    def sections(self):
        """返回所有的sections"""
        return super(config, self).sections()

class Path:

    def __init__(self):
        self.p = pathlib.WindowsPath()

    @property
    def current_dir(self):
        """返回当前的工作目录"""
        self.c = self.p.cwd()
        return self.c

    @property
    def parent_dir(self):
        """返回上一级目录"""
        self.pd = self.current_dir.parent
        return self.pd

    @staticmethod
    def mk_dir(dir):
        """
        创建目录,如果存在则返回,不存在创建后仍然返回
        :param p: 要创建的目录
        """
        _dir =pathlib.WindowsPath(dir).absolute()
        if not _dir.exists():
            pathlib.WindowsPath.mkdir(_dir,exist_ok=False)
            return _dir
        else:
            return _dir
path = Path()

def yaml_read(file: str):
    if pathlib.WindowsPath(file).exists():
        try:
            with open(file=file, mode='r+', encoding='utf-8') as file:
                data = yaml.safe_load(stream=file)
                return data
        except YAMLError as e:
            raise e
    else:
        raise FileNotFoundError(file)


