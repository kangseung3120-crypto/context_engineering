# %% 0
# 1장 2강: 사용할 수 있는 근거를 먼저 고르고 관련성 순으로 정렬해요.
from datetime import date

# 실행하는 날에 따라 결과가 달라지지 않도록 기준일을 고정해요.
today = date(2026, 10, 8)
current_user = "jihoon"
# owner와 status는 서비스가 확인한 값이라고 가정한 수업용 데이터예요.
# score는 임의로 정한 관련성 점수이며 사용 권한을 나타내지 않아요.
# expires=None은 별도 만료일이 없다는 뜻이며 현행 여부는 따로 검사해요.
documents = [
    {"id": "travel-old", "owner": "shared", "status": "retired",
     "expires": None, "score": 0.99, "text": "숙박 한도는 8만원입니다."},
    {"id": "travel-v2", "owner": "shared", "status": "current",
     "expires": None, "score": 0.90, "text": "숙박 한도는 12만원입니다."},
    {"id": "approval-rule", "owner": "shared", "status": "current",
     "expires": None, "score": 0.85, "text": "초과 시 예약 전 서면 승인이 필요합니다."},
    {"id": "other-memory", "owner": "mina", "status": "current",
     "expires": None, "score": 1.00, "text": "다른 사용자의 선호입니다."},
    {"id": "temporary-note", "owner": "jihoon", "status": "current",
     "expires": "2026-10-01", "score": 0.95, "text": "지난 예약의 임시 메모입니다."},
]

# %% 1
def exclusion_reason(doc, user_id, as_of):
    """제외할 이유가 있으면 문자열을, 사용할 수 있으면 None을 반환해요."""
    # 먼저 범위를 확인해요. 높은 관련성 점수가 열람 권한을 만들지는 않아요.
    if doc["owner"] not in {"shared", user_id}:
        return "사용자 범위 불일치"
    # 읽을 권한이 있어도 폐기된 규정이면 현재 답변의 근거에서 제외해요.
    if doc["status"] != "current":
        return "현행 문서 아님"
    # 이 예제는 만료일 당일부터 사용할 수 없다고 정해요.
    if doc["expires"] and date.fromisoformat(doc["expires"]) <= as_of:
        return "유효기간 만료"
    # 아무 제외 조건에도 걸리지 않았을 때만 다음 정렬 단계로 넘겨요.
    return None


# %% 2
selected = []
for doc in documents:
    # 결정과 이유를 한 번 계산해서 선택 결과와 로그에 같은 판단을 사용해요.
    reason = exclusion_reason(doc, current_user, today)
    if reason:
        # 제외된 원문은 출력하지 않아요. ID와 사유만으로 선택 과정을 설명해요.
        print(doc["id"], "->", reason)
    else:
        selected.append(doc)

# 사용할 수 있는 자료끼리만 순위를 비교해요. 점수는 예제에 주어진 값이에요.
# 같은 점수일 때는 ID로 정렬하여 출력 순서를 일정하게 유지해요.
# 기본 정렬은 오름차순이므로 score에 음수를 붙여 큰 점수가 앞서게 해요.
selected.sort(key=lambda doc: (-doc["score"], doc["id"]))
print("선택:", [doc["id"] for doc in selected])

# %% 3
# Skills는 작업별 절차 묶음이에요. 여기서는 짧은 목록에서 후보만 찾아요.
# 이 예제는 두 절차를 미리 준비해 선택 결과를 보여 줘요.
# 실제 파일을 필요할 때 읽는 지연 로딩까지 구현한 코드는 아니에요.
skills = [
    {"id": "travel", "keywords": ["출장", "숙박"],
     "procedure": "한도, 영수증, 초과 승인 여부를 차례로 확인한다."},
    {"id": "leave", "keywords": ["연차", "휴가"],
     "procedure": "잔여 일수와 신청 가능 기간을 확인한다."},
]
question = "출장 숙박 한도를 알려 주세요."
# any는 여러 키워드 중 하나라도 맞으면 참이에요. 같은 Skill은 한 번만 남아요.
chosen = [s for s in skills if any(word in question for word in s["keywords"])]
print("선택한 절차:", [s["id"] for s in chosen])
# 후보가 없으면 이 반복문은 실행되지 않아요. 관련 없는 절차를 임의로 쓰지 않아요.
for skill in chosen:
    print(skill["procedure"])
