from PyQt5 import QtWidgets
from CourtNotifier import Ui_CourtNotifier

import email.message
import smtplib
from PyQt5 import QtTest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ctypes
from playsound import playsound

class MainWindowController (QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindowController, self).__init__()
        self.ui = Ui_CourtNotifier ()
        self.ui.setupUi (self)

        self.bExecuting = False
        self.chrome = None

    def GetWebElm(self, ByType, _str, _limitTime):
        if self.chrome == None:return None
        locator = (ByType, _str)
        try:
            elm = WebDriverWait (self.chrome, _limitTime).until (
                EC.presence_of_element_located (locator),
                "找不到指定元素 :" + _str
            )
            return elm
        except:return None

    def GetWebButton(self, ByType, _str, _limitTime):
        if self.chrome == None:return None
        locator = (ByType, _str)
        try:
            elm = WebDriverWait (self.chrome, _limitTime).until (
                EC.element_to_be_clickable (locator))
            return elm
        except:return None
    
    def GetMiniutesByDate(year, month, day):
        if type (year)  != int: year = 0
        if type (month) != int: month = 0
        if type (day)   != int: day = 0
        dayInMonth = 30 # TODO
        return (1440 * 365 * year) + (1440 * dayInMonth) + (1440 * day)
    
    def UISetup(self):
        self.ui.button_test.clicked.connect (self.onClickSendTestEmail)
        self.ui.button_start.clicked.connect (self.onStart)
        self.ui.button_cancel.clicked.connect (self.onCancel)

    def onStart(self):
        Intervalsecs = 10000
        try:Intervalsecs = float(self.ui.lineEdit_interval.text()) * 1000
        except:pass

        self.bExecuting = True
        driver_path = "./chromedriver"
        options = webdriver.ChromeOptions()
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        prefs = {'profile.default_content_setting_values':{'notifications':2 }}
        options.add_experimental_option("prefs", prefs)

        if self.chrome == None:
            self.chrome = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
            self.chrome.get("https://teamear.tixcraft.com/activity/game/22_CrowdSP") # 和泰產險試算網頁

        elm_order = None
        while True:
            elm_order = self.GetWebButton (By.XPATH, "//*[@id=\"gameList\"]/table/tbody/tr[2]/td[4]/input", 3)
            if elm_order == None:
                continue
            
            elm_order.click ()
            # if not elm_order.is_displayed ():
            #     playsound ("./notify.mp3")
            #     break

            QtTest.QTest.qWait (Intervalsecs)
    
    def onCancel(self):
        self.bExecuting = False

    def onSendEmail(self, subject, content):
        msg = email.message.EmailMessage()
        msg['From']     = self.ui.lineEdit_account.text()
        msg['To']       = self.ui.lineEdit_to.text()
        msg['Subject']  = subject
        msg.set_content(content)

        try:
            account = self.ui.lineEdit_account.text()
            password = self.ui.lineEdit_password.text()

            # 可到網路上搜尋gmail smtp server(公開的)
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(account, password)
            server.send_message(msg)
            server.close()
        except:
            ctypes.windll.user32.MessageBoxW(0, "資料格式輸入錯誤", "Warm", 1)

    def onClickSendTestEmail(self):
        self.onSendEmail ("爬蟲工具寄信測試", "測試")
