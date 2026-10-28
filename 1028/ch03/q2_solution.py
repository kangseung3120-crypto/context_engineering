# -*- coding: utf-8 -*-
# 3장 2강 퀴즈: 담당자가 한 번 더 바뀌면 현재 값과 이전 값은? (정답: 정답 코드예요)
# 이 폴더에서 uv run q2_solution.py로 실행해요.
# lesson_02.py를 먼저 실행해 events, missing_evidence를 준비해요. 그래서 강의 예제 출력이 먼저 나오는 게 정상이에요.

from lesson_02 import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 현재 값은 필드별 최신 하나만, 대체된 값은 출처와 함께 따로 남겨요.
new_events = events + [{"source": "t7", "field": "담당자", "value": "박부장"}]
state = {}
replaced = []
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
