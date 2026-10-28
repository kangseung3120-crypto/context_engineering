# -*- coding: utf-8 -*-
# 2장 1강 퀴즈: 보존 기간이 180일 · True인 후보는 어떻게 처리될까요? (Hard: TODO를 직접 완성해요)
# 이 폴더에서 uv run q1_hard.py로 실행해요.
# lesson_01.py를 먼저 실행해 today, decide_memory, active_memories를 준비해요. 그래서 강의 예제 출력이 먼저 나오는 게 정상이에요.

from lesson_01 import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 새 후보 두 개를 판단해요. m7의 ttl_days는 숫자가 아니라 True예요.
new_candidates = [
    {"id": "m6", "text": "예시 코드를 함께 보여 주면 좋겠습니다.",
     "kind": "preference", "consent": True, "ttl_days": 180},
    {"id": "m7", "text": "결론을 먼저 말해 주세요.",
     "kind": "preference", "consent": True, "ttl_days": True},
]
# TODO: 각 후보를 decide_memory로 판단해 (id, 결정) 목록 results를 만드세요.
# TODO: "장기 저장"인 후보만 source_id, text, expires_on(today + ttl_days일)으로 new_records에 담으세요.
results = []
new_records = []
for item in new_candidates:
    decision, reason = decide_memory(item)
    results.append((item["id"], decision))
    if decision == "장기 저장":
        new_records.append({
            "source_id": item["id"], "text": item["text"],
            "expires_on": (today + timedelta(days=item["ttl_days"])).isoformat(),
        })
# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
print("판단:", results)
assert results == [("m6", "장기 저장"), ("m7", "확인 필요")], "180일은 허용 범위, True는 int가 아니라서 확인 필요예요"
print("m6 만료일:", new_records[0]["expires_on"])
assert [r["source_id"] for r in new_records] == ["m6"] and new_records[0]["expires_on"] == "2027-04-06"
print("만료 하루 전 조회 수:", len(active_memories(new_records, date(2027, 4, 5))))
print("만료일 당일 조회 수:", len(active_memories(new_records, date(2027, 4, 6))))
assert len(active_memories(new_records, date(2027, 4, 6))) == 0, "만료일 당일부터 사용하지 않아요"
print("\n✅ 정답이에요!")
print("생각해 보기:", "m7을 isinstance(ttl, int)로 검사했다면 결과가 어떻게 달라졌을지, 그리고 그게 왜 문제인지 말해 보세요.")
