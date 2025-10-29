import azure.functions as func
import os, json, requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
        user_message = body.get("message", "")
        if not user_message:
            return func.HttpResponse(json.dumps({"error": "message 누락"}), status_code=400)

        OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
        OPENAI_KEY = os.getenv("OPENAI_KEY")
        OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT")

        url = f"{OPENAI_ENDPOINT}openai/deployments/{OPENAI_DEPLOYMENT}/chat/completions?api-version=2025-01-01-preview"
        headers = {"Content-Type": "application/json", "api-key": OPENAI_KEY}
        data = {
            "messages": [
                {"role": "system", "content": "너는 산업현장 안전보조 AI야. PPE 관련 질문에 친절하게 답해줘."},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 1000
        }
        resp = requests.post(url, headers=headers, json=data)
        reply = resp.json()["choices"][0]["message"]["content"]

        return func.HttpResponse(json.dumps({"reply": reply}, ensure_ascii=False), mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)
