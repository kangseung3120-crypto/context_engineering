# %% 0
# 2장 2강: Mem0에 한 가지 선호를 저장하고 같은 ID로 수정·삭제해요.
import os
from pathlib import Path
from uuid import uuid4

# 설정은 mem0를 불러오기 전에 적용해요.
root = Path(__file__).resolve().parent
store = root / "local_store"
# 폴더가 이미 있어도 오류 없이 사용해요. 기존 데이터 전체를 지우지는 않아요.
store.mkdir(exist_ok=True)
os.environ["MEM0_TELEMETRY"] = "False"
os.environ["MEM0_DIR"] = str(store / "runtime")
from mem0 import Memory

# %% 1
# Qdrant는 이 폴더에 파일을 저장해요. 별도 Qdrant 서버는 필요하지 않아요.
# infer=False로 저장하므로 아래 LLM 설정은 이번 실행에서 생성에 사용하지 않아요.
# 임베딩 모델의 768차원과 컬렉션 차원을 맞춰요.
# 다른 모델로 바꾸면 같은 차원이더라도 기존 벡터를 그대로 섞지 않아요.
memory = Memory.from_config({
    "llm": {"provider": "ollama", "config": {
        "model": "qwen3:4b-instruct-2507-q4_K_M",
        "ollama_base_url": "http://localhost:11434"}},
    "embedder": {"provider": "ollama", "config": {
        "model": "nomic-embed-text:latest",
        "ollama_base_url": "http://localhost:11434"}},
    "vector_store": {"provider": "qdrant", "config": {
        "collection_name": "ce_lecture_memory",
        "path": str(store / "qdrant"), "embedding_model_dims": 768}},
    "history_db_path": str(store / "history.db"),
})

# 이전 실행과 섞이지 않도록 수업용 사용자 ID를 매번 새로 만들어요.
# 서비스에서는 로그인 결과로 확인한 사용자 ID를 사용해요.
user_id = "lecture-" + uuid4().hex[:12]
scope = {"user_id": user_id}

# %% 2
# 앞 강의에서 저장 가능하다고 판단한 선호 한 문장만 등록해요.
# infer=False는 추출 단계를 생략해 원문을 그대로 저장한다는 뜻이에요.
added = memory.add(
    "한국어로 짧은 답변을 선호합니다.", user_id=user_id, infer=False,
    metadata={"source": "turn-1", "purpose": "answer-style"},
)
# 실제로 ADD된 결과에서만 ID를 꺼내요. 검색 순위로 수정 대상을 추측하지 않아요.
new_ids = [row["id"] for row in added["results"] if row.get("event") == "ADD"]
# 예상과 다른 결과에서 아무 기억이나 선택하지 않도록 즉시 중단해요.
if len(new_ids) != 1:
    raise RuntimeError("등록한 기억 ID 하나를 확인할 수 없어요.")
target_id = new_ids[0]

# 목록 조회는 저장 여부, 검색은 질문과 관련된 기억을 찾을 때 사용해요.
rows = memory.get_all(filters=scope)["results"]
print("저장 수:", len(rows))
# threshold=0은 한 항목의 조회 흐름을 보여 주기 위한 설정이에요.
# 이 값으로 검색 품질이나 권한이 보장된다는 뜻은 아니에요.
found = memory.search("답변 선호", filters=scope, top_k=5, threshold=0)["results"]
print("등록한 기억 검색:", any(row["id"] == target_id for row in found))

# %% 3
def owned_record(memory_id):
    """수정·삭제하기 전에 조회한 기억의 사용자 범위를 확인해요."""
    # ID 조회 뒤 소유자를 검사하는 애플리케이션 예제예요.
    # 이 함수는 로그인 검증을 구현하지 않으며 user_id는 신뢰된 값이어야 해요.
    record = memory.get(memory_id)
    if not record or record.get("user_id") != user_id:
        raise PermissionError("현재 사용자의 기억이 아니에요.")
    return record


# 검색 결과의 첫 항목을 수정하면 다른 기억을 바꿀 수 있어요.
# add의 응답에서 받은 target_id를 끝까지 사용해 대상을 고정해요.
owned_record(target_id)
memory.update(target_id, text="한국어로 자세한 설명을 선호합니다.")
# 수정 응답만으로 성공을 판단하지 않고 저장된 현재 값을 다시 확인해요.
updated = owned_record(target_id)
print("수정 후:", updated["memory"])

# %% 4
owned_record(target_id)
memory.delete(target_id)
# 삭제 응답만 보는 대신, 현재 사용자의 활성 목록을 다시 조회해요.
remaining = memory.get_all(filters=scope)["results"]
print("활성 목록에서 삭제:", all(row["id"] != target_id for row in remaining))
# SQLite 이력은 별도로 남을 수 있어요. 모든 복사본을 지웠다는 뜻은 아니에요.
# 로컬 저장소 연결을 닫아 파일 잠금을 해제해요.
memory.vector_store.client.close()
