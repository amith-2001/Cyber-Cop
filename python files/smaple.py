
import time

import pyautogui
import requests
# from selenium import webdriver

# driver = webdriver.Chrome('./chromedriver.exe')
url = 'https://www.media.io/editor/53f51604176f2921d11c473174ff3a94'


# driver.get(url)

def chrome():
    # pyautogui.moveTo(0,1079)
    pyautogui.click(4, 1079)
    pyautogui.typewrite('chrome')
    time.sleep(0.5)
    pyautogui.press('enter')


def urlopener():
    pyautogui.click(428, 70)
    pyautogui.typewrite(url)
    pyautogui.press('enter')


def detector():
    return pyautogui.locateOnScreen('img.png')


def uploading():
    pyautogui.click(318, 377)
    pyautogui.doubleClick(278, 189)
    time.sleep()


def downloader():
    time.sleep(0.5)
    pyautogui.click()  # pass position


if _name_ == '_main_':
    # chrome()
    # time.sleep(0.5)
    # urlopener()
    # downloader()
    if detector() != None:
        pyautogui.click(43, 511)  # subtitles
        time.sleep(0.5)
        pyautogui.click(402, 672)  # auto subtitles
        pyautogui.click(527, 679)  # download button
        pass