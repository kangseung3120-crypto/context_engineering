# -*- coding: utf-8 -*-
# 2장 2강 퀴즈: 기억 두 개를 저장하고 첫 번째만 정확히 삭제하기 (정답: 정답 코드예요)
# 이 폴더에서 uv run q2_solution.py로 실행해요. Ollama가 실행 중이어야 해요.
# lesson_02.py를 먼저 실행해 memory, user_id, scope, owned_record를 준비해요. 그래서 강의 예제 출력이 먼저 나오는 게 정상이에요.

from lesson_02 import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# lesson_02.py가 마지막에 저장소 연결을 닫으므로 같은 폴더로 다시 열어요.
from qdrant_client import QdrantClient
memory.vector_store.client = QdrantClient(path=str(store / "qdrant"))

# add 응답에서 받은 ID로 대상을 고정하고, 범위를 확인한 뒤 삭제해요.
first = memory.add("표로 정리한 답변을 선호합니다.", user_id=user_id, infer=False)
second = memory.add("영어 용어는 괄호로 함께 적어 주세요.", user_id=user_id, infer=False)
first_id = [row["id"] for row in first["results"] if row.get("event") == "ADD"][0]
second_id = [row["id"] for row in second["results"] if row.get("event") == "ADD"][0]
owned_record(first_id)
memory.delete(first_id)


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
remaining = [row["id"] for row in memory.get_all(filters=scope)["results"]]
print("남은 기억 수:", len(remaining))
assert first_id not in remaining, "첫 번째 기억이 활성 목록에서 사라져야 해요"
assert remaining == [second_id], "두 번째 기억은 그대로 남아야 해요"
other = memory.add("다른 사용자의 선호입니다.", user_id="lecture-other-" + user_id[-6:], infer=False)
other_id = [row["id"] for row in other["results"] if row.get("event") == "ADD"][0]
try:
    owned_record(other_id)
    raise AssertionError("다른 사용자의 기억은 수정 · 삭제 전에 막혀야 해요")
except PermissionError as error:
    print("다른 사용자 기억:", error)
memory.delete(second_id)
memory.delete(other_id)
memory.vector_store.client.close()
print("\n✅ 정답이에요!")
print("생각해 보기:", "삭제 뒤에도 history.db에는 이력이 남을 수 있어요. 사용자가 '완전히 지워 달라'고 하면 어디까지 확인해야 할지 말해 보세요.")
