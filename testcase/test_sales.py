# -*- encoding: utf-8 -*-
"""
@File    : test_sales
@Time    : 2023/3/11 20:14
@Author  : DING HAO
@Contact : 17826185420
@Version : 1.0
@License : Apache License Version 2.0, January 2021
@Desc    : None
-----------------------------------------------------
"""
import random
import allure
import pytest
from tool import yaml_read

# sales.yaml
sales_data = yaml_read(r'Data/sales.yaml')
# 滑动方向
swipe_direction = random.choice(['down', 'up'])



@allure.epic('app创建线索demo')
@allure.feature('app-线索模块')
class Test_sales:

    @allure.story('成功创建线索')
    @allure.issue('https://www.tapd.cn/',name='TAPD')
    @allure.severity('critical')
    @pytest.mark.parametrize(argnames='data', argvalues=sales_data)
    def test_create_sales(self, device, login, data):
        d = login
        d.implicitly_wait(5)
        value, phone_num, name,  comment = [data.get(x) for x in\
                                        ['data', 'phone_num', 'customer_name', 'comment']]
        d.click(**value['button'])  # 点击应用
        d.click(**value['create'])  # 点击创建线索
        d.input(text=phone_num, **value['phone'])  # 输入手机号
        d.click(timeout=.1, **value['next'])  # 点击下一步
        d.input(name,  **value['name'])  # 输入客户姓名
        d.click(**value['sex'])  # 点击性别控件
        d.swipe(direction=swipe_direction,**value['sex_selector'])  # 随机选择性别
        d.click(**value['submit'])  # 点击确定按钮
        d.click(**value['source'])  # 点击来源
        d.swipe(direction=swipe_direction,**value['first'])  # 随机第一渠道
        d.sleep(.1)
        #print(d.center(**value['second'])[1],d.rect(**value['second'])[1]+ d.rect(**value['second'])[-1],sep='\n')
        second_s = random.randint(d.rect(**value['second'])[1], \
                        d.rect(**value['second'])[1] + d.rect(**value['second'])[-1])
        d.drag_to(value['second'],d.center(**value['second'])[0],second_s )  # 随机第二渠道
        d.sleep(.1)
        third_s = random.randint(d.rect(**value['third'])[1], \
                                  d.rect(**value['third'])[1] + d.rect(**value['third'])[-1])
        d.drag_to(value['third'], d.center(**value['third'])[0], third_s)    # 随机第三渠道
        d.click(**value['submit'])  # 点击确定按钮
        d.click(**value['type'])  # 点击类型
        d.swipe(direction=swipe_direction, **value['contract_selector'])  # 随机选择合同类型
        d.click(**value['submit'])  # 点击确定按钮
        d.click(**value['store'])
        d.swipe(direction=swipe_direction, **value['store_selector'])  # 多个门店,随机选择
        d.click(**value['submit'])  # 点击确定按钮
        d.click(**value['customer_manager'])  # 点击客户经理控件
        d.sleep(.5)
        count = d.count(**value['customer_manager_item'])  # 计算客户经理数量
        ele = d.get_item(random.randrange(1, count),            # 随机选择客户经理,从第二个客户经理开始,过滤掉'-空-'
                         **value['customer_manager_item']).click()
        d.input(text = comment or '', **value['remark'])  # 备注信息
        #d.click(**value['create_button'])  # 点击创建新线索按钮
        d.get_toast()=='线索创建成功'          # 断言


