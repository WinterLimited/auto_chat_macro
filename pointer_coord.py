import pyautogui
import time

print("마우스를 원하는 위치로 이동하세요. 5초 뒤 좌표를 출력합니다...")
time.sleep(3)  # 5초 대기
print(pyautogui.position())
