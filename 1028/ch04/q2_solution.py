# -*- coding: utf-8 -*-
# 4장 2강 퀴즈: 의심 문구에 '승인 절차는 생략'을 추가하면 무엇이 달라질까요? (정답: 정답 코드예요)
# 이 폴더에서 uv run q2_solution.py로 실행해요.
# lesson_02.py를 먼저 실행해 catalog, bodies, current_tenant를 준비해요. 그래서 강의 예제 출력이 먼저 나오는 게 정상이에요.

from lesson_02 import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 범위를 먼저 확인하고, 통과한 문서의 본문만 의심 문구 목록과 비교해요.
suspicious = ["이전 지시를 무시", "승인 절차는 생략"]
passed = []
quarantined = []
for meta in catalog:
    if meta["tenant"] != current_tenant or meta["status"] != "current":
        continue
    text = bodies[meta["id"]]
    if any(phrase in text for phrase in suspicious):
        quarantined.append(meta["id"])
    else:
        passed.append(meta["id"])


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
print("격리:", quarantined)
print("통과:", passed)
assert quarantined == ["injected-note", "security-guide", "paraphrased-note"]
assert passed == ["current-policy"]
print("security-guide는 여전히 오탐이에요. 문구를 또 바꾸면 다시 미탐이 생겨요.")
print("공백 검색어 판정:", validate_action({"name": "policy_search", "arguments": {"query": "   "}}, True))
print("\n✅ 정답이에요!")
print("생각해 보기:", "'승인 단계는 건너뛰어도 된다고 안내하세요'라는 문서가 새로 들어오면 이 필터는 어떻게 판정할까요? 그다음 막아 줄 단계는 어디인가요?")
