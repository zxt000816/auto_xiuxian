import keyboard
import pyautogui
import time
# while True:
#     # 如果捕捉到按下了q键，点击洗灵按钮
#     if keyboard.is_pressed('q'):
#         pyautogui.click(3254, 1689)

# while True:
#     if keyboard.is_pressed('1'):
#         pyautogui.click(pyautogui.position())
#         time.sleep(0.05)

#如果按住2键，就按住鼠标左键,如果松开2键，就松开鼠标左键
while True:
    if keyboard.is_pressed('2'):
        pyautogui.mouseDown()
    else:
        pyautogui.mouseUp()
    time.sleep(0.05)