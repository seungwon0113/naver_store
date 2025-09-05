from gemini.rag import build_index, rag_answer

def ai():
    embedder, store = build_index()

    while True:
        message = input("질문을 입력해 주세요 (종료하려면 exit): ")
        if message.lower() == "exit":
            break
        answer = rag_answer(message, embedder, store)
        print(answer)

if __name__ == "__main__":
    ai()
