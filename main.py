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


def simulate_conversation(topic, rounds=3):
    """
    특정 주제(topic)에 대해 'rounds'번 대화를 나눈다.
    매 라운드마다:
      1) GPT가 "새로운 질문"을 생성 (질문자 역할)
      2) GPT가 "해당 질문에 대한 전문가 답변"을 생성 (답변자 역할)
      3) 각 메시지(질문/답변)를 카카오톡에 전송
      -> 이전 대화를 참고해 문맥을 유지.
    """

    # 시스템 메시지(초기 지시사항):
    # - 질문은 더욱 창의적, 구체적 (단 너무 길지 않게)
    # - 답변은 3~4문장 이내로 핵심만.
    # - 절대 마크다운 사용 금지
    system_msg = f"""
    당신은 '{topic}' 분야의 전문가이면서 동시에 질문자입니다.

    [질문자일 때]
    - 고민 중인 주제에 대해 창의적이고 구체적인 질문을 만드세요.
    - 질문은 간결하게, 핵심이 분명하도록 해주세요.
    - 공식적인 상담 느낌이지만, 너무 설명조로 쓰지 말고 자연스럽게 질문하세요.
    - "~에 대해 생각해보세요" 같은 표현을 쓰지 말고, 직접 묻는 형식으로 작성하세요.

    [답변자일 때]
    - 핵심 정보만 간략하게 정리하세요. 문장은 3~4문장 이내로 유지하세요.
    - 너무 장황하지 않게, 자연스러운 말투로 짧고 명확하게 답변하세요.
    - "~입니다" 같은 문어체 표현을 사용하지 말고, 자연스럽게 끝나는 말투를 사용하세요.
    - 나열식 리스트(1,2,3)보다는 문장형으로 답변하세요.

    절대 마크다운(##, *, - 등)을 사용하지 마세요.
    """

    messages = [{"role": "system", "content": system_msg}]

    # 해당 주제의 좌표 (카카오톡 입력창 위치)
    if topic not in TOPIC_COORDS:
        print(f"[ERROR] {topic} 주제에 해당하는 좌표가 없습니다.")
        return

    x_coord, y_coord = TOPIC_COORDS[topic]

    for i in range(1, rounds + 1):
        print(f"\n--- [대화 {i}회차] 주제: {topic} ---")

        # 1) 질문 생성 (user 역할)
        user_prompt = f"""
'{topic}'와 관련된 새로운 질문을 만들어 주세요.
질문은 조금 더 창의적이고 구체적으로 해주시되, 핵심을 벗어나지는 말아주세요.
절대 마크다운을 쓰지 말고, 약간의 상황이나 예시를 곁들여도 좋습니다.
"""
        # 이전 대화 + 새 요청을 합쳐서 GPT 호출
        tmp_messages = messages + [{"role": "user", "content": user_prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=tmp_messages,
            temperature=0.7,
        )
        question_text = response["choices"][0]["message"]["content"].strip()

        # 대화에 user(질문) 추가
        messages.append({"role": "user", "content": question_text})
        print(f"[Q{i}] {question_text}")

        # 카톡에 질문 전송
        send_to_kakao(question_text, x_coord, y_coord)
        time.sleep(1)

        # 2) 답변 생성 (assistant 역할)
        tmp_messages = messages
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=tmp_messages,
            temperature=0.7,
        )
        answer_text = response["choices"][0]["message"]["content"].strip()

        # 대화에 assistant(답변) 추가
        messages.append({"role": "assistant", "content": answer_text})
        print(f"[A{i}] {answer_text}")

        # 카톡에 답변 전송
        send_to_kakao(answer_text, x_coord, y_coord)
        time.sleep(1)

    print("\n대화 종료.")
    return messages


def main():
    # TEST: 3회 반복 (각 반복 시, 3번의 질의응답)
    topics = ["입시", "학업", "창업"]
    for attempt in range(1, 4):
        chosen_topic = random.choice(topics)
        print(f"\n========== [{attempt}번째 대화] 주제: {chosen_topic} ==========")
        simulate_conversation(chosen_topic, rounds=3)
        time.sleep(3)  # 각 대화 종료 후 잠깐 쉬기

if __name__ == "__main__":
    main()
