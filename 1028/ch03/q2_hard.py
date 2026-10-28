# -*- coding: utf-8 -*-
# 3장 2강 퀴즈: 담당자가 한 번 더 바뀌면 현재 값과 이전 값은? (Hard: TODO를 직접 완성해요)
# 이 폴더에서 uv run q2_hard.py로 실행해요.
# lesson_02.py를 먼저 실행해 events, missing_evidence를 준비해요. 그래서 강의 예제 출력이 먼저 나오는 게 정상이에요.

from lesson_02 import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# t7에서 담당자가 박부장으로 한 번 더 바뀌었어요. 같은 방식으로 상태를 다시 만들어요.
new_events = events + [{"source": "t7", "field": "담당자", "value": "박부장"}]
state = {}
replaced = []
# TODO: new_events를 시간순으로 읽으며, 같은 필드가 다시 나오면 기존 값을 replaced에 넣고 state를 새 값(복사본)으로 바꾸세요.
for event in new_events:
    field = event["field"]
    if field in state:
        replaced.append(state[field])
    state[field] = event.copy()


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
for field, event in state.items():
    print(f"{field}: {event['value']} (출처 {event['source']})")
print("이전 담당자 기록:", [(e["value"], e["source"]) for e in replaced if e["field"] == "담당자"])
assert state["담당자"] == {"source": "t7", "field": "담당자", "value": "박부장"}
assert len(replaced) == 4, "이전 값은 김대리, 2026-10-15, 1억원, 이과장 네 개예요"
assert [e["source"] for e in replaced if e["field"] == "담당자"] == ["t1", "t4"]
print("한도와 승인만 남길 때 누락:", missing_evidence(["p1", "p2"]))
print("\n✅ 정답이에요!")
print("생각해 보기:", "t7이 승인되지 않은 '제안'이었다면 이 코드로 처리해도 될까요? 교안의 '확인 필요' 원칙과 연결해 말해 보세요.")
