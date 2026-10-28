# %% 0
# 2장 1강: 오래 기억할 정보와 현재 대화에서만 쓸 정보를 나누어요.
from datetime import date, timedelta

# 실행 날짜가 달라도 만료 결과를 비교할 수 있게 기준일을 고정해요.
today = date(2026, 10, 8)
# 필드 값은 수업에서 직접 지정했어요. 자동 개인정보 탐지 결과가 아니에요.
# consent는 장기 재사용 여부를 설명하기 위한 값이에요. 인증을 대신하지 않아요.
# ttl_days는 보존할 일수예요. session과 secret에는 장기 저장 규칙을 적용하지 않아요.
candidates = [
    {"id": "m1", "text": "한국어로 간결한 답변을 선호합니다.",
     "kind": "preference", "consent": True, "ttl_days": 30},
    {"id": "m2", "text": "지금 비교하는 숙소는 A호텔입니다.",
     "kind": "session", "consent": False, "ttl_days": None},
    {"id": "m3", "text": "수업용 가상 비밀 값입니다.",
     "kind": "secret", "consent": True, "ttl_days": 30},
    {"id": "m4", "text": "앞으로 표로 설명해 주면 좋겠습니다.",
     "kind": "preference", "consent": False, "ttl_days": 30},
    {"id": "m5", "text": "짧은 답변을 선호합니다.",
     "kind": "preference", "consent": True, "ttl_days": 0},
]

# %% 1
def decide_memory(item):
    """저장 전에 정책을 적용하고, 결정과 이유를 함께 반환해요."""
    # 비밀 값은 동의 표시가 있어도 이 수업의 장기 기억에 저장하지 않아요.
    if item["kind"] == "secret":
        return "저장하지 않음", "비밀 정보"
    # 일시적인 작업 정보는 다음 세션의 선호로 승격하지 않아요.
    if item["kind"] == "session":
        return "현재 대화만", "일시적인 작업 상태"
    # 유형 또는 동의가 불명확하면 먼저 확인하도록 이유와 함께 반환해요.
    if item["kind"] != "preference" or not item["consent"]:
        return "확인 필요", "재사용 목적 또는 동의 확인"
    # bool은 Python에서 int의 하위 타입이므로 type으로 정확히 검사해요.
    ttl = item["ttl_days"]
    if type(ttl) is not int or not 1 <= ttl <= 180:
        return "확인 필요", "보존 기간 확인"
    return "장기 저장", "선호와 보존 기간 확인됨"


# %% 2
# 두 목록은 사용 범위를 분리해서 보여 줘요. 디스크에 저장하는 코드는 아니에요.
long_term = []
session_state = []
for item in candidates:
    # 반환된 튜플을 두 변수로 나누어, 결정은 분기에, 이유는 설명에 사용해요.
    decision, reason = decide_memory(item)
    print(item["id"], "->", decision, "/", reason)
    if decision == "장기 저장":
        # 원본 항목을 바꾸지 않고 필요한 필드만 새 기록에 담아요.
        # source_id는 후보와 연결하고, expires_on은 조회 시점의 만료 검사에 써요.
        long_term.append({
            "source_id": item["id"], "text": item["text"],
            "expires_on": (today + timedelta(days=item["ttl_days"])).isoformat(),
        })
    # 확인 필요와 저장 제외 항목은 어느 목록에도 추가하지 않아요.
    elif decision == "현재 대화만":
        session_state.append(item["text"])

print("장기 기억 수:", len(long_term))
print("세션 상태 수:", len(session_state))
print("장기 기억 만료일:", long_term[0]["expires_on"])

# %% 3
def active_memories(records, as_of):
    """조회 시점에도 만료를 확인해요. 만료일 당일부터 사용하지 않아요."""
    # 문자열을 날짜로 되돌려 비교해요. 만료일과 같은 날도 결과에서 빠져요.
    # 새 목록만 반환하므로 records의 원본 데이터는 그대로 남아요.
    return [record for record in records
            if date.fromisoformat(record["expires_on"]) > as_of]


# 만료 필터는 사용을 중단하는 처리예요. 저장소에서 지우는 삭제와는 달라요.
after_expiry = date(2026, 11, 7)
print("만료일의 조회 결과 수:", len(active_memories(long_term, after_expiry)))
