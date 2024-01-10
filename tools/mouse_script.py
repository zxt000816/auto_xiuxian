import keyboard
import pyautogui
import time
# while True:
#     # 如果捕捉到按下了q键，点击洗灵按钮
#     if keyboard.is_pressed('q'):
#         pyautogui.click(3254, 1689)

while True:
    if keyboard.is_pressed('1'):
        pyautogui.click(pyautogui.position())
        time.sleep(0.05)
    
# pyautogui.mouseDown()