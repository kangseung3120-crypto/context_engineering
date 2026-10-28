# -*- coding: utf-8 -*-
# 1장 2강 퀴즈: 기준일이 9월 30일이면 어떤 자료가 선택될까요? (Easy: 빈칸(____)을 채워요)
# 이 폴더에서 uv run q2_easy.py로 실행해요.
# lesson_02.py를 먼저 실행해 documents, current_user, exclusion_reason를 준비해요. 그래서 강의 예제 출력이 먼저 나오는 게 정상이에요.

from lesson_02 import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 같은 자료를 기준일 2026-09-30으로 다시 골라요. temporary-note의 만료일은 2026-10-01이에요.
# 제외 사유가 없는 자료만 남긴 뒤, 점수가 높은 순(같으면 ID 순)으로 정렬하세요.
as_of = date(2026, 9, 30)
picked = [doc for doc in documents if exclusion_reason(doc, current_user, as_of) is None]
picked.sort(key=lambda doc: (-doc["score"], doc["id"]))


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
print("9월 30일 기준 선택:", [doc["id"] for doc in picked])
assert [doc["id"] for doc in picked] == ["temporary-note", "travel-v2", "approval-rule"], \
    "만료 전이면 temporary-note도 쓸 수 있고, 점수 순으로 맨 앞에 와요"
print("other-memory:", exclusion_reason(documents[3], current_user, as_of))
print("travel-old:", exclusion_reason(documents[0], current_user, as_of))
print("\n✅ 정답이에요!")
print("생각해 보기:", "temporary-note가 맨 앞에 오는데, '지난 예약의 임시 메모'가 숙박 한도 질문에 정말 필요한지 관련성 관점에서 말해 보세요.")
