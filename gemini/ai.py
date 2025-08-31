from google import genai
from envs import environments as env

client = genai.Client(api_key=env.GENAI_API_KEY)
message = input("질문을 입력해 주세요: ")
response = client.models.generate_content(
    model=env.GENAI_API_MODEL,
    contents=message,
)

print(response.text)