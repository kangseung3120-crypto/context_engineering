# 컨텍스트 엔지니어링 실습 자료 (1·2장 오전 · 3·4장 오후)

1장부터 4장까지 강의 8개의 예제 코드를 하나로 묶었어요. **uv 실행 환경은 이 폴더에 하나만 만들고 8개 강의가 함께 써요.** 그래서 처음에 한 번만 세팅하면 돼요.

## 폴더 구성

```
context_engineering/
├─ pyproject.toml      ← 8개 강의에 필요한 패키지 목록 (함께 씀)
├─ uv.lock             ← 패키지 버전 고정 (함께 씀)
├─ .python-version     ← Python 3.12 (함께 씀)
├─ ch01/  (오전)  lesson_01.py  1장 1강  입력의 종류와 메시지 역할
│                 lesson_02.py  1장 2강  근거 선택 · 우선순위 · Skills
├─ ch02/  (오전)  lesson_01.py  2장 1강  단기 메모리와 장기 메모리 설계
│                 lesson_02.py  2장 2강  Mem0로 저장부터 삭제까지
├─ ch03/  (오후)  lesson_01.py  3장 1강  토큰 예산과 Sliding Window
│                 lesson_02.py  3장 2강  Conversation Summary와 긴 문서 압축
└─ ch04/  (오후)  lesson_01.py  4장 1강  Prompt Caching과 정적 Prefix 설계
                  lesson_02.py  4장 2강  컨텍스트 오염 · Prompt Injection · 신뢰도 필터링
```

`lesson_0N.py`는 노션 교안의 장별 ZIP과 같아요. 강의마다 퀴즈 파일 3개(`qN_easy.py`, `qN_hard.py`, `qN_solution.py`)를 더했어요. `q1_…`은 1강, `q2_…`는 2강 퀴즈예요.

## 처음 한 번만: 세팅

1. **압축 풀기:** ZIP을 OneDrive와 동기화되지 않는 **짧은 경로**(예: `C:\ce`)에 풀어요. 바탕 화면이나 문서 폴더가 OneDrive와 동기화돼 있으면 설치 중에 오류가 날 수 있고, 경로가 너무 길면 Windows 경로 길이 제한에 걸려요.
2. **폴더 열기:** VS Code에서 **파일 → 폴더 열기**로 `context_engineering` 폴더를 열어요. `ch01` 같은 장 폴더가 아니라 이 루트 폴더를 열어요.
3. **터미널에서 설치:** **터미널 → 새 터미널**(PowerShell)을 열고 아래를 실행해요.

```powershell
uv --version
uv python install 3.12
uv sync --locked
```

`.venv` 폴더가 `context_engineering` 바로 아래에 하나 생기면 끝이에요.

4. **Ollama 임베딩 모델 (2장 2강만):** Ollama 앱을 실행하고, 모델이 없다면 한 번 내려받아요. 생성 모델은 호출하지 않으므로 따로 받을 필요가 없어요.

```powershell
ollama pull nomic-embed-text
```

- 3장 · 4장 1강은 첫 실행에 Qwen3 **토크나이저 파일만** 내려받아요(모델 가중치는 받지 않아요). 인터넷 연결이 필요해요.

> **교안의 "강의 예제 코드"와 다른 점:** 교안은 장마다 ZIP을 풀고 `uv sync --locked`를 하라고 안내해요. 이 묶음에서는 위의 `uv sync --locked` 한 번으로 대신하므로, **장 폴더 안에서 `uv init`이나 `uv sync`를 따로 실행하지 마세요.**

## 강의마다: 실행

uv가 상위 폴더의 환경을 자동으로 찾아 써요.

```powershell
# 예: 1장 1강
cd ch01
uv run lesson_01.py
uv run q1_easy.py

# 1장 2강은 같은 폴더에서
uv run lesson_02.py
uv run q2_easy.py

# 다음 장으로 갈 때
cd ..\ch02
uv run lesson_01.py
```

- 퀴즈 파일은 해당 `lesson_0N.py`를 먼저 실행한 뒤 문제를 풀어요. 그래서 강의 예제 출력이 먼저 나오는 게 정상이에요. 통과하면 `✅ 정답이에요!`가 나와요.
  - `qN_easy.py`: 빈칸(`____`)을 채워요
  - `qN_hard.py`: 같은 문제를 TODO로 직접 완성해요
  - `qN_solution.py`: 정답
- 교안에는 기본 실습 문제가 없어서, 퀴즈는 **교안 본문 · 코드 · 실행 결과 · 자주 묻는 질문에서 다룬 내용만으로** 새로 만들었어요.
- 2장 2강(`lesson_02.py`, `q2_*.py`)은 `ch02/local_store`에 Qdrant 데이터와 SQLite 이력을 만들어요. 실행할 때마다 새 사용자 ID를 쓰므로 이전 실행과 섞이지 않아요.

## VS Code 편집기 설정 (import 밑줄이 보일 때)

Ctrl+Shift+P → **Python: Select Interpreter** → `context_engineering\.venv\Scripts\python.exe`를 골라요. 8개 강의 모두 이 하나로 돼요.

## 막힐 때

| 증상 | 확인할 것 |
| --- | --- |
| `uv sync` 중 `os error 396` (하드 링크 오류) | OneDrive 동기화 폴더예요. `setx UV_LINK_MODE copy`를 실행하고 터미널을 새로 연 뒤 다시 `uv sync --locked` 해요. 동기화되지 않는 폴더에 다시 푸는 것도 방법이에요 |
| `.venv\Lib\site-packages\…py` 파일이 없다는 `FileNotFoundError` | 압축을 푼 경로가 너무 길어요(Windows 경로 260자 제한). `C:\ce`처럼 짧은 경로에 다시 풀고 `uv sync --locked` 해요 |
| 2장 2강에서 Connection refused | Ollama 앱이 실행 중인지 확인해요 (`ollama list`가 동작해야 해요) |
| 2장 2강에서 model not found | `ollama pull nomic-embed-text`를 실행해요 |
| spaCy · fastembed가 없다는 안내 | 이 예제에서 쓰지 않는 Mem0 추가 기능 안내예요. 실행 결과에는 영향이 없어요 |
| 2장 2강에서 저장소가 잠겨 있다는 오류 | 같은 `ch02`에서 다른 터미널이 `lesson_02.py`나 `q2_*.py`를 실행 중인지 확인하고, 끝난 뒤 다시 실행해요 |
| 3장 · 4장에서 토크나이저 다운로드 실패 | 인터넷 연결과 Hugging Face 접속을 확인해요. 한 번 받으면 다음부터는 다시 받지 않아요 |
| HF 토큰 · symlink 경고 | 파일을 받을 때 나오는 안내 문구예요. 실행 결과에는 영향이 없어요 |
| `ModuleNotFoundError` | `context_engineering` 폴더에서 `uv sync --locked`를 했는지, `uv run`으로 실행했는지 확인해요 |
| 장 폴더에 `pyproject.toml`이 생겼어요 | 실수로 `uv init`을 실행한 거예요. 그 장 폴더의 `pyproject.toml`, `.python-version`, `.venv`를 지우면 다시 공용 환경을 써요 |

## 검증 기록

- 2026-10-27 · Windows 11 · Python 3.12에서 확인했어요.
- 8개 강의의 `lesson_0N.py`를 공용 환경으로 실행한 결과가 교안의 실행 결과와 같았어요 (예: 1-2 선택 ['travel-v2', 'approval-rule'], 2-1 장기 기억 1 · 만료일 2026-11-07, 2-2 저장 1 · 수정 · 삭제 True, 3-1 한도 256 → 남은 턴 1 · 512 → 6, 3-2 이전 값 3 · 한도만 남길 때 누락 p2~p4, 4-1 공통 토큰 A 11 · B 94 · 버전 변경 8, 4-2 통과 ['current-policy', 'paraphrased-note']).
- 퀴즈 8개 모두 `qN_solution.py`가 통과하고, `qN_easy.py` 빈칸을 정답으로 채우면 통과하며, 원본 `qN_easy.py` · `qN_hard.py`는 통과하지 않는 것을 확인했어요.
