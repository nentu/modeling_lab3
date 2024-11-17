import time

import pyautogui
import pyperclip


def get_current_text():
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    return pyperclip.paste()


def execute(code, iter_n):
    # create new file
    pyautogui.hotkey('ctrl', 'n')
    pyautogui.press('enter')

    # paste code
    pyperclip.copy(code)
    pyautogui.hotkey('ctrl', 'v')

    # execute
    pyautogui.hotkey('ctrl', 'alt', 's')

    # click start
    ## open tab
    pyautogui.moveTo(310, 50)
    pyautogui.click()

    ## choose START
    pyautogui.moveTo(340, 235)
    pyautogui.click()

    # print iter count
    pyautogui.press('backspace')
    pyautogui.typewrite(str(iter_n))

    # run
    pyautogui.press('enter')

    current_text = get_current_text()
    while 'Report' not in current_text:
        current_text = get_current_text()

    return current_text


if __name__ == '__main__':
    f = open('code.txt', 'r', encoding='utf8').read()
    time.sleep(2)
    print(
        execute(f, 1e6)
    )
