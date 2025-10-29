import azure.functions as func
import os
import json
import base64
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # === 파일 확인 ===
        file = req.files.get("file")
        if not file:
            return func.HttpResponse(
                json.dumps({"error": "파일이 제공되지 않았습니다."}, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )

        # === 환경 변수 ===
        OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT", "").rstrip("/") + "/"
        OPENAI_KEY = os.getenv("OPENAI_KEY", "")
        OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT", "")

        # === 이미지 base64 인코딩 ===
        img_bytes = file.stream.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        # === OpenAI Vision 호출 ===
        openai_url = (
            f"{OPENAI_ENDPOINT}openai/deployments/{OPENAI_DEPLOYMENT}/chat/completions"
            "?api-version=2024-08-01-preview"
        )

        headers = {"Content-Type": "application/json", "api-key": OPENAI_KEY}

        # 📋 GPT가 결과를 직접 작성하도록 지시
        body = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "너는 산업현장 안전점검을 수행하는 AI야. "
                        "사진 속 인물의 PPE 착용 상태를 분석해서 반드시 아래 형식으로만 답변해:\n\n"
                        "📋 PPE 분석 결과\n✅ 안전모 / ⚠️ 조끼 / ✅ 방독면\n\n"
                        "🧠 AI 설명\n"
                        "사진의 상황과 PPE 착용 이유를 간단히 한국어로 설명해.\n\n"
                        "⚠️ 절대 다른 문구(예: 결과 없음, 분석 완료, 설명 없음)는 넣지 마."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "이 사진의 PPE 착용 상태를 분석해줘."},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{img_base64}"}
                        },
                    ],
                },
            ],
            "max_tokens": 800,
            "temperature": 0.3,
        }

        response = requests.post(openai_url, headers=headers, json=body, timeout=60)
        data = response.json()

        # === GPT 응답 추출 ===
        ai_message = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )

        # GPT가 아무 응답도 안 줬을 경우 예외 처리
        if not ai_message:
            ai_message = "⚠️ AI 분석 결과를 가져오지 못했습니다."

        # ✅ 결과 분리 처리: “📋 PPE 분석 결과” 이후 첫 줄을 PPE 결과로, 나머지는 설명으로 구분
        ppe_result, ai_explanation = "", ""

        if "🧠 AI 설명" in ai_message:
            parts = ai_message.split("🧠 AI 설명", 1)
            ppe_result = parts[0].replace("📋 PPE 분석 결과", "").strip()
            ai_explanation = "🧠" + parts[1].strip()
            
        else:
            ai_explanation = ai_message.strip()

        # === 최종 응답 ===
        return func.HttpResponse(
            json.dumps(
                {
                    "PPE_결과": ppe_result or "⚠️ PPE 분석 실패",
                    "AI_설명": ai_explanation or "⚠️ AI 설명 생성 실패",
                },
                ensure_ascii=False,
                indent=2,
            ),
            mimetype="application/json",
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}, ensure_ascii=False),
            status_code=500,
            mimetype="application/json",
        )
