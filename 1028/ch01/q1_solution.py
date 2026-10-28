# -*- coding: utf-8 -*-
# 1장 1강 퀴즈: 영수증 질문에는 어떤 자료만 넣을까요? (정답: 정답 코드예요)
# 이 폴더에서 uv run q1_solution.py로 실행해요.
# lesson_01.py를 먼저 실행해 instruction, context, render_context를 준비해요. 그래서 강의 예제 출력이 먼저 나오는 게 정상이에요.

from lesson_01 import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 질문에 필요한 규정 문서만 남기고, 자료와 현재 질문을 표지로 나눠 조립해요.
new_question = "숙박비를 정산할 때 영수증이 필요한가요?"
docs = [item for item in context if item["kind"] == "document"]
new_messages = [
    {"role": "system", "content": instruction},
    {"role": "user", "content": (
        "참고 자료:\n" + render_context(docs) + "\n\n현재 질문:\n" + new_question
    )},
]


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
for message in new_messages:
    print(f"--- {message['role']} ---")
    print(message["content"])
assert [d["id"] for d in docs] == ["policy-v2"], "규정 문서 policy-v2 하나만 남아야 해요"
assert new_messages[0] == {"role": "system", "content": instruction}, "지시문은 system에 그대로 둬요"
user_text = new_messages[1]["content"]
assert "[policy-v2 / document / 출장 규정 v2]" in user_text, "render_context로 출처 표지를 붙여요"
assert "approval-17" not in user_text and "preference-1" not in user_text, "필요 없는 자료는 넣지 않아요"
assert user_text.endswith("현재 질문:\n" + new_question), "현재 질문은 자료 뒤 별도 표지에 둬요"
print("\n✅ 정답이에요!")
print("생각해 보기:", "질문이 '13만원 숙소 예약해도 되나요?'로 바뀌면 approval-17(승인 조회 결과)은 다시 필요할까요? 이유를 말해 보세요.")
