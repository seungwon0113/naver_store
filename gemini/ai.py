from gemini.rag import build_index, rag_answer

def ai():
    # 두 카테고리를 모두 인덱싱
    fashion_embedder, fashion_store = build_index("패션의류")
    health_embedder, health_store = build_index("생활/건강")

    while True:
        message = input("질문을 입력해 주세요 (종료하려면 exit): ")
        if message.lower() == "exit":
            break

        # 질문에서 카테고리 분류
        if "패션" in message or "의류" in message:
            embedder, store, category = fashion_embedder, fashion_store, "패션의류"
        elif "생활" in message or "건강" in message:
            embedder, store, category = health_embedder, health_store, "생활/건강"
        else:
            embedder, store, category = fashion_embedder, fashion_store, "패션의류"  # 기본값

        # 카테고리 정보까지 넘겨줌
        answer = rag_answer(message, embedder, store)
        print(f"[{category}] {answer}")

if __name__ == "__main__":
    ai()