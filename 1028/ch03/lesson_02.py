# %% 0
# 3장 2강: 요약에 최신 값과 원문 출처를 함께 남겨요.
# 대화에서 사실을 추출하는 생성 단계는 생략하고, 확인된 변경 기록부터 읽어요.
# field가 같은 사건은 같은 항목의 변경이에요. source는 원문 턴의 식별자예요.
# 서로 다른 프로젝트나 미승인 제안을 이 목록에 섞지 않는다고 가정해요.
events = [
    {"source": "t1", "field": "담당자", "value": "김대리"},
    {"source": "t2", "field": "마감일", "value": "2026-10-15"},
    {"source": "t3", "field": "예산", "value": "1억원"},
    {"source": "t4", "field": "담당자", "value": "이과장"},
    {"source": "t5", "field": "마감일", "value": "2026-10-22"},
    {"source": "t6", "field": "예산", "value": "1억 2천만원"},
]

# %% 1
# current에는 항목별 최신 상태 하나만, previous에는 대체된 기록을 남겨요.
current = {}
previous = []
for event in events:
    # 담당자나 마감일 같은 필드 이름으로 현재 상태를 찾아요.
    field = event["field"]
    if field in current:
        # 바뀌기 전 값을 따로 남겨 변경 이유를 원문에서 추적할 수 있게 해요.
        previous.append(current[field])
    # 입력은 같은 프로젝트의 승인된 변경을 시간순으로 정렬한 목록이에요.
    # 모든 문서에서 뒤에 나온 문장을 무조건 채택하라는 규칙은 아니에요.
    # 새 딕셔너리를 저장해 이 예제의 원본 event를 나중에 함께 바꾸지 않도록 해요.
    current[field] = event.copy()

# 출력 순서는 필드가 처음 등록된 순서이고, 값은 마지막으로 확정한 값이에요.
for field, event in current.items():
    print(f"{field}: {event['value']} (출처 {event['source']})")
print("이전 값 수:", len(previous))

# %% 2
# 문서 압축에서는 조건을 쪼개다 빠뜨리지 않도록 원문 문장과 ID를 묶어요.
sentences = [
    {"id": "p1", "text": "숙박 한도는 1박당 12만원입니다.", "needed": True},
    {"id": "p2", "text": "초과 시 예약 전에 담당 임원의 서면 승인이 필요합니다.", "needed": True},
    {"id": "p3", "text": "승인 없는 초과 금액은 자동 정산되지 않습니다.", "needed": True},
    {"id": "p4", "text": "정산할 때 숙박 영수증을 첨부해야 합니다.", "needed": True},
    {"id": "p5", "text": "출장 규정 담당 부서는 매년 안내 문서를 배포합니다.", "needed": False},
]
# needed는 이번 질문에 필요한 근거를 사람이 지정한 학습용 표시예요.
# 실제 검색이나 LLM이 이 표시를 자동으로 알아낸다는 가정은 하지 않아요.
selected = [sentence for sentence in sentences if sentence["needed"]]
# 원문을 다시 쓰지 않고 ID와 문장을 함께 남기는 추출 방식의 압축이에요.
compressed = "\n".join(f"[{s['id']}] {s['text']}" for s in selected)
print("압축 후 근거:")
print(compressed)

# %% 3
def missing_evidence(chosen_ids):
    """필요한 원문 중 빠진 ID를 찾아요. 문장 의미 전체를 평가하는 함수는 아니에요."""
    # 집합의 차이로 필요한 ID 중 선택되지 않은 것을 찾고, 결과 순서를 고정해요.
    required = {s["id"] for s in sentences if s["needed"]}
    return sorted(required - set(chosen_ids))


# 한도 문장만 남긴 경우와 승인·영수증까지 남긴 경우를 비교해요.
print("한도만 남길 때 누락:", missing_evidence(["p1"]))
print("조건까지 남길 때 누락:", missing_evidence([s["id"] for s in selected]))
