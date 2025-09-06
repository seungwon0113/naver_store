import re
from google import genai
from envs import environments as env
from database import Databases
from gemini.embedding import Embedding
from gemini.vectorstore import VectorStore

def build_index(category: str):
    db = Databases()
    if category == "패션의류":
        rows = db.execute("SELECT id, rank, keyword, link FROM naver_fashion;")
    elif category == "생활/건강":
        rows = db.execute("SELECT id, rank, keyword, link FROM naver_health;")
    else:
        raise ValueError(f"알 수 없는 카테고리: {category}")

    db.close()

    texts = [f"{r[1]} | {r[2]} | {r[3]}" for r in rows]  # keyword | url | created_at

    embedder = Embedding()
    vectors = embedder.encode(texts)

    store = VectorStore(vectors.shape[1])
    store.add(vectors, texts)

    return embedder, store

def get_rank_from_db(rank: int, category: str):
    db = Databases()
    if category == "패션의류":
        rows = db.execute("SELECT rank, keyword, link FROM naver_fashion WHERE rank = %s;", (rank,))
    elif category == "생활/건강":
        rows = db.execute("SELECT rank, keyword, link FROM naver_health WHERE rank = %s;", (rank,))
    else:
        rows = []
    db.close()
    return rows

def rag_answer(query, embedder, store):
    '''
    TODO: 불필요한 대답 수정필요
    질문을 입력해 주세요 (종료하려면 exit): 너이름이 뭐야?
    [패션의류] 제공해주신 데이터는 '카디건', '원더브라' 등 패션의류 관련 검색어 목록입니다.

    이 데이터 목록에는 제 이름이 포함되어 있지 않습니다. 저는 OpenAI에서 개발한 대규모 언어 모델입니다.
    '''
    # 카테고리 분류
    if "패션" in query or "의류" in query:
        category = "패션의류"
    elif "생활" in query or "건강" in query:
        category = "생활/건강"
    else:
        category = "패션의류"  # 기본값

    # "n위는 뭔데?" 처리
    if re.search(r"\d+위", query):
        numbers = re.findall(r"\d+", query)
        if numbers:
            rank = int(numbers[0])
            row = get_rank_from_db(rank, category)
            if row:
                return f"{category} {rank}위는 {row[0][1]} 입니다. (링크: {row[0][2]})"
            else:
                return f"{category} {rank}위 데이터는 존재하지 않습니다."

    # 일반 RAG 검색
    client = genai.Client(api_key=env.GENAI_API_KEY)
    query_vec = embedder.encode([query])
    results = store.search(query_vec, top_k=5)

    context = "\n".join(results)
    prompt = f"""
다음은 {category} 데이터에서 검색된 정보입니다:

{context}

질문: {query}
위 데이터를 참고해서 답변해 주세요.
"""

    response = client.models.generate_content(
        model=env.GENAI_API_MODEL,
        contents=prompt,
    )
    return response.text
