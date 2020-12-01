# -*- coding: utf-8 -*-

import pywinauto,time

ss=2

class AutoHuatai():
    def __init__(self, exe_path, user, password, comm_password):
        """
        :param user: 用户名
        :param password: 密码
        :param exe_path: 客户端路径, 类似
        :param comm_password:
        :param kwargs:
        :return:
        """
        try:
            self._app = pywinauto.Application().connect(path=exe_path)
        except Exception:
            self._app = pywinauto.Application().start(exe_path)

            # wait login window ready
            while True:
                try:
                    self._app.top_window().Edit1.wait("ready")
                    break
                except RuntimeError:
                    pass
            self._app.top_window().Edit1.set_focus()
            self._app.top_window().Edit1.type_keys(user)
            self._app.top_window().Edit2.type_keys(password)

            self._app.top_window().Edit3.type_keys(comm_password)

            self._app.top_window().button0.click()

            self._app = pywinauto.Application().connect(path=exe_path)
        self._main = self._app.window(title="网上股票交易系统5.0")
        self._main.wait ( "exists enabled visible ready" , timeout=100 )
        self._close_prompt_windows ( )
        self._main_frame= self._app.window(class_name='AfxFrameOrView42s').child_window(class_name='AfxMDIFrame42s')

    def _close_prompt_windows(self):
        # self.wait(1)
        for window in self._app.windows(class_name="#32770", visible_only=True):
            title = window.window_text()
            if title != self._main.title:
                window.close()
                # self.wait(0.2)
        # self.wait(1)

    def change_menu(self,name):
        if name=='信用':
            tab=self._main_frame.child_window(class_name="CCustomTabCtrl",found_index=0)
            fw=tab.rectangle() # <RECT L817, T612, R1067, B652>
            tab.set_focus() 
            x=fw.left+int((fw.right-fw.left)/5)
            y=fw.bottom-int((fw.bottom-fw.top)/4)
            pywinauto.mouse.click(button='left', coords=(x, y))

    def balance(self):
        self._main_frame.type_keys('{F4}')
        return self._main_frame.child_window(class_name='Static',found_index=5).window_text()
        
    def credit_balance(self):
        self._main_frame.type_keys('{F4}')
        return self._main_frame.child_window(class_name='Static',found_index=42).window_text()
    
    def credit_buy(self,code,price,qty):
        self._main_frame.type_keys('{F1}')
        self._main_frame.child_window(class_name="Edit",found_index=0).set_text(code)
        time.sleep(ss) # 需停顿，否则可用还没反应出来
        can_buy=int(self._main_frame.child_window(class_name="Static",found_index=1).window_text())
        if qty>can_buy:# 超出可买份额
            return
        self._main_frame.child_window(class_name="Edit",found_index=1).set_text(price)
        if qty == 0:
            qty=can_buy
        self._main_frame.child_window(class_name="Edit",found_index=2).set_text(qty)
        self._main_frame.child_window(class_name="Button",title="确定[&B]").click() 
        self._app.top_window().type_keys('{ENTER}')
        print('buy:',code,price,qty)

    def credit_sell(self,code,price,qty):#卖，输入仓位,0为满仓
        self._main_frame.type_keys('{F2}')
        self._main_frame.child_window(class_name="Edit",found_index=0).set_text(code)
        time.sleep(ss)
        can_sell=int(self._main_frame.child_window(class_name="Static",found_index=1).window_text())
        self._main_frame.child_window(class_name="Edit",found_index=1).set_text(price)
        if qty == 0:
            qty=can_sell
        self._main_frame.child_window(class_name="Edit",found_index=2).set_text(qty)
        self._main_frame.child_window(class_name="Button",title="确定[&S]").click() 
        self._app.top_window().type_keys('{ENTER}')
        print('sell:',code,price,qty)

    def credit_holds(self):
        self._main_frame.type_keys("{F4}")
        grid=self._main_frame.child_window(class_name="CVirtualGridCtrl")
        grid.type_keys('^s') #保存为excel
        time.sleep(1)
        self._app.top_window().type_keys("{ENTER}")
        time.sleep(1)
        self._app.top_window().type_keys('{TAB}{ENTER}')
        # pywinauto.keyboard.send_keys("{TAB}{ENTER}")
