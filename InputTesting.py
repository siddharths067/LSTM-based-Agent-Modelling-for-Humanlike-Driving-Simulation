import pyautogui as pg
import time
import DirectInputRoutines as DIR

pg.hotkey("alt","tab")

for i in range(10):
    time.sleep(1)
    DIR.PressKey(DIR.W)
