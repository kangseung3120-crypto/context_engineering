# -*- coding: utf-8 -*-
# 3장 1강 퀴즈: 출력 예약을 64로 줄이면 담당자 정보가 들어올까요? (Hard: TODO를 직접 완성해요)
# 이 폴더에서 uv run q1_hard.py로 실행해요. 첫 실행이면 토크나이저를 내려받아요.
# lesson_01.py를 먼저 실행해 turns, select_recent, make_messages, count_tokens를 준비해요. 그래서 강의 예제 출력이 먼저 나오는 게 정상이에요.

from lesson_01 import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 요청 한도 256은 그대로 두고 출력 예약만 128에서 64로 줄여요. 여유분은 32예요.
request_limit = 256
output_reserve = 64
margin = 32
# TODO: 입력 예산 input_budget을 계산하세요.
input_budget = request_limit - output_reserve - margin
# TODO: select_recent로 kept를 고르고, 전체 메시지 토큰 수 used를 세세요.
kept = select_recent(turns, input_budget)
used = count_tokens(make_messages(kept))


# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
print(f"입력 예산={input_budget}, 사용={used}, 남은 턴={len(kept)}")
kept_text = " ".join(message["content"] for turn in kept for message in turn)
print("담당자 이과장 포함:", "이과장" in kept_text, "/ 마감 10월 22일 포함:", "10월 22일" in kept_text)
assert input_budget == 160 and len(kept) == 3 and used <= input_budget
assert "이과장" in kept_text and "10월 22일" in kept_text
print("\n✅ 정답이에요!")
print("생각해 보기:", "출력 예약을 64로 줄였을 때 답변이 길어지면 어떤 일이 생길까요? 한도를 늘리는 것과 비교해 보세요.")
