from fastapi import FastAPI, Request
import os
import google.generativeai as genai

app = FastAPI()

# 환경변수 사용 권장
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

@app.post("/api/webhook")
async def kakao_webhook(req: Request):
    data = await req.json()
    user_message = data['userRequest']['utterance']

    # Gemini API에 요청
    response = model.generate_content(
        contents=[
            {"role": "user", "parts": [{"text": "정확하고 간결하게 답변해 주세요."}]},
            {"role": "model", "parts": [{"text": "네, 알겠습니다."}]},
            {"role": "user", "parts": [{"text": user_message}]}
        ],
        generation_config={
            "max_output_tokens": 500,
            "temperature": 0.7,
        }
    )
    answer = response.text

    # 카카오톡 챗봇 응답 포맷
    return {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {"text": answer}
            }]
        }
    }

@app.get("/key")
async def root():
    return {"message": GEMINI_API_KEY}

@app.get("/api/test")
async def test():
    return {"message": "성공적인 테스트."}

@app.get("/api/hello/{name}")
async def say_hello(name: str):
    return {"message": f"반가워 {name}"}