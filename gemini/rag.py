from google import genai
from envs import environments as env
from database import Databases
from gemini.embedding import Embedding
from gemini.vectorstore import VectorStore

def build_index():
    db = Databases()
    rows = db.execute("SELECT id, rank, keyword, link FROM naver_fashion;")
    db.close()

    texts = [f"{r[1]} | {r[2]} | {r[3]}" for r in rows]  # keyword | url | created_at

    embedder = Embedding()
    vectors = embedder.encode(texts)

    store = VectorStore(vectors.shape[1])
    store.add(vectors, texts)

    return embedder, store

def rag_answer(query, embedder, store):
    client = genai.Client(api_key=env.GENAI_API_KEY)

    query_vec = embedder.encode([query])
    results = store.search(query_vec, top_k=5)

    context = "\n".join(results)
    prompt = f"""
다음은 naver_fashion 데이터에서 검색된 정보입니다:

{context}

질문: {query}
위 데이터를 참고해서 답변해 주세요.
"""

    response = client.models.generate_content(
        model=env.GENAI_API_MODEL,
        contents=prompt,
    )
    return response.text
