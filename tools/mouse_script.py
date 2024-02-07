import keyboard
import pyautogui
import time

while True:
    if keyboard.is_pressed('1'):
        pyautogui.click(pyautogui.position())
        time.sleep(0.1)

    if keyboard.is_pressed('3'):
        pyautogui.mouseDown()