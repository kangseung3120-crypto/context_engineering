# -*- coding: utf-8 -*-
# 4장 1강 퀴즈: 똑같은 입력이면 공통 앞부분은? 서버 지표는 어떻게 읽을까요? (Hard: TODO를 직접 완성해요)
# 이 폴더에서 uv run q1_hard.py로 실행해요. 첫 실행이면 토크나이저를 내려받아요.
# lesson_01.py를 먼저 실행해 build_messages, token_ids, common_prefix_length, cache_observation를 준비해요. 그래서 강의 예제 출력이 먼저 나오는 게 정상이에요.

from lesson_01 import *

print("\n" + "=" * 20, "퀴즈", "=" * 20)

# 1) B 구조로 완전히 같은 요청(같은 ID, 같은 질문)을 두 번 만들어 공통 앞부분 길이를 재요.
# 2) 서버 응답 예시 세 개에서 prompt_eval_cached_count를 읽어 해석해요. 필드가 없는 응답도 있어요.
first = token_ids(build_messages("B", "request-001", question1))
second = token_ids(build_messages("B", "request-001", question1))
responses = [
    {"prompt_eval_count": 120},
    {"prompt_eval_count": 120, "prompt_eval_cached_count": 0},
    {"prompt_eval_count": 120, "prompt_eval_cached_count": 96},
]
# TODO: first와 second의 공통 앞부분 길이를 same에 담으세요.
same = common_prefix_length(first, second)
# TODO: 각 응답의 prompt_eval_cached_count를 (없으면 None으로) cache_observation에 넣어 readings 목록을 만드세요.
readings = [cache_observation(response.get("prompt_eval_cached_count")) for response in responses]

# ---------- 실행과 확인 (이 아래는 고치지 마세요) ----------
print("같은 입력의 공통 앞부분:", same, "/ 전체 길이:", len(first))
assert same == len(first), "완전히 같은 입력이면 끝까지 일치해요"
for reading in readings:
    print("지표 해석:", reading)
assert readings == ["캐시 사용량을 알 수 없음", "캐시에서 읽은 토큰이 0개", "캐시에서 읽은 토큰 96개"]
print("공통 길이가 전체여도 실제 재사용 여부는 서버 지표로만 확인해요")
print("\n✅ 정답이에요!")
print("생각해 보기:", "응답 예시 세 개가 실제로 같은 입력에 대한 연속 요청이라면, 첫 번째 응답에 필드가 없는 이유로 무엇을 의심해 볼 수 있을까요?")
