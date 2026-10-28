# %% 0
# 3장 1강: 전체 입력을 세고 최근의 연속된 대화 턴을 남겨요.
# 모델 가중치 없이 토크나이저와 대화 형식만 가져와요.
from transformers import AutoTokenizer

# 같은 토큰 수를 재현하도록 저장소의 특정 revision을 지정해요.
# 다른 모델이나 대화 형식을 사용하면 같은 문장도 토큰 수가 달라질 수 있어요.
tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen3-4B-Instruct-2507",
    revision="cdbee75f17c01a7cc42f958dc650907174af0554",
    trust_remote_code=False,
)


def count_tokens(messages):
    """본문뿐 아니라 역할과 답변 시작 표시까지 포함해 세어요."""
    # tokenize=True는 문자열 대신 토큰 ID를 돌려줘요. len은 그 개수를 세어요.
    # add_generation_prompt는 모델이 답변을 시작할 위치의 표시를 포함해요.
    return len(tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True,
    ))


# %% 1
system = {"role": "system", "content": "확인된 내용으로만 답하고 모르면 물어보세요."}
question = {"role": "user", "content": "현재 담당자와 마감일을 알려 주세요."}

# 한 턴에 질문과 답변을 함께 담아요. 순서는 오래된 대화부터예요.
pairs = [
    ("담당자는 김대리예요.", "담당자를 김대리로 기록했어요."),
    ("마감은 10월 15일이에요.", "마감일을 10월 15일로 기록했어요."),
    ("발표 자료는 한국어로 작성해요.", "한국어 자료를 준비할게요."),
    ("담당자가 이과장으로 바뀌었어요.", "이제 담당자는 이과장이에요."),
    ("마감도 10월 22일로 바뀌었어요.", "새 마감은 10월 22일이에요."),
    ("예산은 1억 2천만원이에요.", "예산을 1억 2천만원으로 기록했어요."),
]
# pairs의 각 튜플을 user와 assistant 메시지 두 개로 바꿔요.
# 질문만 남고 대응하는 답변이 사라지는 일을 줄이기 위해 한 묶음으로 다뤄요.
turns = [[{"role": "user", "content": user},
          {"role": "assistant", "content": assistant}] for user, assistant in pairs]


def make_messages(kept):
    # 선택된 턴의 내부 순서도 유지하고 현재 질문을 맨 뒤에 놓아요.
    # 바깥 목록은 턴, 안쪽 목록은 메시지이므로 두 번 순회해 평탄화해요.
    history = [message for turn in kept for message in turn]
    return [system, *history, question]


# %% 2
def select_recent(all_turns, input_budget):
    """예산에 들어오는 가장 최근의 연속 구간을 반환해요."""
    if count_tokens(make_messages([])) > input_budget:
        # 시스템 지시나 현재 질문을 몰래 자르지 않고, 입력 재구성을 요청해요.
        raise ValueError("고정 지시와 현재 질문만으로 입력 예산을 넘었어요.")
    kept = []
    for turn in reversed(all_turns):
        # 최신 턴부터 검사하되 앞에 붙여 최종 메시지는 시간순으로 유지해요.
        candidate = [turn, *kept]
        # 턴 본문만 더하지 않고 system과 현재 질문을 포함한 전체를 다시 세어요.
        if count_tokens(make_messages(candidate)) > input_budget:
            # 더 오래된 턴을 건너뛰어 끼워 넣지 않아요. 최근 연속 구간을 유지해요.
            break
        # 한도 안에 들어온 후보만 확정해요. 넘친 후보는 kept에 반영하지 않아요.
        kept = candidate
    return kept


# %% 3
# 아래 값은 수업에서 비교할 요청 한도예요. 모델의 최대 길이를 뜻하지 않아요.
# 출력과 여유 공간을 먼저 떼고, 남은 공간에 전체 입력을 넣어요.
for request_limit in (256, 512, 1024):
    output_reserve = 128
    margin = 32
    input_budget = request_limit - output_reserve - margin
    kept = select_recent(turns, input_budget)
    # 출력 예약량을 실제 생성한 토큰 수로 해석하지 않아요. 여기서는 모델을 호출하지 않아요.
    used = count_tokens(make_messages(kept))
    print(f"요청 한도={request_limit}, 입력 예산={input_budget}, 사용={used}, 남은 턴={len(kept)}")

print("안녕하세요 글자 수:", len("안녕하세요"))
print("안녕하세요 토큰 수:", len(tokenizer.encode("안녕하세요", add_special_tokens=False)))
