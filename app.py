from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()
PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY")  # 환경변수 사용 권장

@app.post("/api/webhook")
async def kakao_webhook(req: Request):
    data = await req.json()
    user_message = data['userRequest']['utterance']

    # Perplexity API에 요청
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-medium-online",  # 원하는 모델명
        "messages": [
            {"role": "system", "content": "정확하고 간결하게 답변해 주세요."},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    response = requests.post(
        "https://api.perplexity.ai/chat/completions",
        headers=headers, json=payload
    )
    result = response.json()
    answer = result["choices"][0]["message"]["content"]

    # 카카오톡 챗봇 응답 포맷
    return {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {"text": answer}
            }]
        }
    }

@app.get("/api/test")
async def root():
    return {"message": "성공적인 테스트."}

@app.get("/api/hello/{name}")
async def say_hello(name: str):
    return {"message": f"반가워 {name}"}