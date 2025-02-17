import time
import random
import openai
import pyautogui
import pyperclip

# OpenAI API 키 설정
openai.api_key = ""

TOPIC_COORDS = {
    "학업": (263, 666),
    "창업": (742, 666),
    "입시": (1200, 666)
}

# 카카오톡 실행 대기 시간 (윈도우 부팅 후 프로그램 실행 대기)
BOOT_WAIT_TIME = 30  # 30초 대기 (필요 시 조정)


def wait_for_boot():
    print("[INFO] 시스템 부팅 대기 중...")
    time.sleep(BOOT_WAIT_TIME)


def login_kakaotalk(password1, password2, loc1, loc2):
    """
    두 개의 카카오톡 창을 실행하고 각각 로그인 수행
    """
    print("[INFO] 카카오톡 자동 로그인 시작")

    for idx, (password, loc) in enumerate([(password1, loc1), (password2, loc2)]):
        print(f"[INFO] 카카오톡 {idx + 1} 로그인 중...")
        pyautogui.click(*loc)  # 비밀번호 입력 위치 클릭
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.3)
        pyautogui.hotkey("ctrl", "c")  # 비밀번호 복사
        time.sleep(0.3)
        pyautogui.click(*loc)  # 비밀번호 입력 창 클릭
        time.sleep(0.3)
        pyautogui.hotkey("ctrl", "v")  # 비밀번호 붙여넣기
        time.sleep(0.3)
        pyautogui.press("enter")  # 로그인 시도
        time.sleep(5)  # 로그인 대기


def open_chat_rooms(chat_locs):
    """
    로그인 후 지정된 위치의 채팅방 실행 (각각 3번 클릭)
    """
    print("[INFO] 채팅방 자동 실행 중...")
    for idx, loc in enumerate(chat_locs):
        print(f"[INFO] 채팅방 {idx + 1} 실행 중...")
        for _ in range(3):  # 더블클릭 3번
            pyautogui.click(*loc)
            time.sleep(0.5)


def send_to_kakao(text, x, y):
    """
    (x, y) 좌표를 클릭 후,
    'text'를 클립보드 복사해서 Ctrl+V 붙여넣기 → Enter로 전송
    """
    pyautogui.click(x, y)
    time.sleep(0.5)
    pyperclip.copy(text)
    time.sleep(0.3)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.3)
    pyautogui.press("enter")
    time.sleep(0.5)


def simulate_conversation(topic):
    """
    특정 주제(topic)에 대해 무작위 시간 간격으로 대화를 무한 반복
    """
    system_msg = f"""
    당신은 '{topic}' 분야의 전문가이면서 동시에 질문자입니다.
    질문과 답변을 창의적이고 구체적으로 작성하세요.
    """
    messages = [{"role": "system", "content": system_msg}]

    if topic not in TOPIC_COORDS:
        print(f"[ERROR] {topic} 주제에 해당하는 좌표가 없습니다.")
        return

    x_coord, y_coord = TOPIC_COORDS[topic]

    while True:
        user_prompt = f"'{topic}'에 대한 창의적인 질문을 작성하세요."
        tmp_messages = messages + [{"role": "user", "content": user_prompt}]
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=tmp_messages, temperature=0.7)
        question_text = response["choices"][0]["message"]["content"].strip()

        messages.append({"role": "user", "content": question_text})
        send_to_kakao(question_text, x_coord, y_coord)
        time.sleep(1)

        tmp_messages = messages
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=tmp_messages, temperature=0.7)
        answer_text = response["choices"][0]["message"]["content"].strip()

        messages.append({"role": "assistant", "content": answer_text})
        send_to_kakao(answer_text, x_coord, y_coord)

        wait_time = random.randint(900, 1800)  # 15~30분 랜덤 대기 (초 단위)
        print(f"[INFO] 다음 대화까지 {wait_time // 60}분 대기...")
        time.sleep(wait_time)


def main():
    wait_for_boot()
    login_kakaotalk("password1", "password2", (500, 500), (1000, 500))
    open_chat_rooms([(600, 700), (1100, 700)])
    topics = ["입시", "학업", "창업"]
    while True:
        chosen_topic = random.choice(topics)
        print(f"[INFO] '{chosen_topic}' 주제로 대화 시작")
        simulate_conversation(chosen_topic)


if __name__ == "__main__":
    main()
