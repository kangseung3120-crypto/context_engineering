# %% 0
# 4장 1강: 고정 내용과 요청별 내용의 순서가 공통 앞부분에 미치는 영향을 봐요.
# 모델 가중치 없이 토크나이저와 대화 형식만 가져와요.
from transformers import AutoTokenizer

# 입력 배치만 비교하도록 같은 모델과 revision을 사용해요.
tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen3-4B-Instruct-2507",
    revision="cdbee75f17c01a7cc42f958dc650907174af0554",
    trust_remote_code=False,
)


# 수업에 필요한 정책만 사용해요. 캐시를 위해 불필요한 문장을 늘리지 않아요.
policy = (
    "제공된 출장 규정으로 답하세요. 숙박 한도는 1박당 12만원입니다. "
    "초과 시 예약 전 담당 임원의 서면 승인과 정산 영수증이 필요합니다. "
    "근거가 없으면 확인이 필요하다고 안내하세요."
)


def build_messages(mode, request_id, question, version="v2"):
    # mode는 아래 반복문에서 A 또는 B만 전달하는 수업용 선택값이에요.
    fixed = f"정책 버전: {version}\n{policy}"
    if mode == "A":
        # 요청마다 바뀌는 ID가 앞에 있어 초반부터 입력이 달라져요.
        system = f"요청 ID: {request_id}\n{fixed}"
        user = question
    else:
        # 고정 지시는 그대로 두고 동적인 ID와 질문을 뒤쪽에 배치해요.
        system = fixed
        user = f"요청 ID: {request_id}\n{question}"
    # 질문은 두 구조 모두 user 역할이에요.
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


# %% 1
def token_ids(messages):
    # 역할 구분과 답변 시작 표시까지 직렬화한 토큰 배열을 비교해요.
    return tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True,
    )


def common_prefix_length(left, right):
    """앞에서부터 연속으로 일치하는 토큰 수만 세어요."""
    count = 0
    # zip은 같은 위치의 두 토큰을 묶고, 더 짧은 배열의 끝에서 멈춰요.
    for a, b in zip(left, right):
        # 처음 달라진 뒤의 일치는 Prefix가 아니므로 더 세지 않아요.
        if a != b:
            break
        count += 1
    return count


# %% 2
question1 = "숙박 한도는 얼마인가요?"
question2 = "한도를 넘으면 어떤 승인이 필요한가요?"
# A와 B에 동일한 두 요청을 적용해야 배치 차이의 영향을 비교할 수 있어요.
for mode in ("A", "B"):
    first = token_ids(build_messages(mode, "request-001", question1))
    second = token_ids(build_messages(mode, "request-002", question2))
    print(mode, "공통 앞부분 토큰:", common_prefix_length(first, second))

# 정책을 바꾼 요청은 이전 정책과 같은 입력이 아니에요.
old = token_ids(build_messages("B", "request-001", question1, "v2"))
new = token_ids(build_messages("B", "request-002", question2, "v3"))
print("정책 버전 변경 후 공통 토큰:", common_prefix_length(old, new))

# %% 3
# 여기까지는 서버를 호출하지 않았어요. 캐시 적중이나 속도는 측정하지 않았어요.
# 아래 세 값은 지표를 읽는 방법을 설명하기 위해 직접 만든 예시예요.
def cache_observation(value):
    # None은 지표가 없다는 뜻이고, 숫자 0은 지표가 보고된 상태예요.
    # if not value로 두 경우를 합치면 이 차이가 사라져요.
    if value is None:
        return "캐시 사용량을 알 수 없음"
    if value == 0:
        return "캐시에서 읽은 토큰이 0개"
    return f"캐시에서 읽은 토큰 {value}개"


for example_value in (None, 0, 120):
    print("지표 해석 예:", cache_observation(example_value))
