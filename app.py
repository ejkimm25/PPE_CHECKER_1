

import streamlit as st
import requests
import json
from io import BytesIO

st.set_page_config(page_title="👷 AI 기반 PPE 감지 & 대화", layout="centered")

st.title("👷 AI 기반 PPE 감지 시스템")
st.write(
    """
이 시스템은 **산업현장 근로자의 안전 장비(PPE)** 착용 여부를 AI로 분석합니다.  
또한 아래에서 **PPE 관련 질문을 직접 입력**하면 AI가 대화형으로 답변해드립니다.
"""
)

# Azure Function URL
url_check = "https://pro-ppe-checker-func.azurewebsites.net/api/ppe_check"
url_chat = "https://pro-ppe-checker-func.azurewebsites.net/api/ppe_chat"

# 탭 구성
tab1, tab2 = st.tabs(["📸 이미지 분석", "💬 대화형 질문"])

# ✅ --- 탭1: 이미지 분석 ---
with tab1:
    st.subheader("📸 PPE 이미지 분석")

    uploaded_file = st.file_uploader("이미지를 업로드하세요 (JPG/PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file and st.button("🔍 분석 시작"):
        try:
            files = {"file": uploaded_file.getvalue()}
            with st.spinner("AI가 이미지를 분석 중입니다..."):
                res = requests.post(url_check, files=files)

            if res.status_code == 200:
                data = res.json()

                # 이미지 미리보기
                st.image(uploaded_file, caption="", width=400)

                st.success("✅ 분석 완료!")

                st.subheader("📋 PPE 분석 결과")
                st.write(data.get("PPE_결과", "결과 없음"))

                st.subheader("🧠 AI 설명")

                # ✅ 줄바꿈 및 줄 간격 유지
                ai_text = data.get("AI_설명", "설명 없음")
                st.markdown(
                    f"<div style='white-space: pre-line; font-size: 1.05rem; line-height: 1.6;'>{ai_text}</div>",
                    unsafe_allow_html=True
                )

            else:
                st.error("⚠️ 서버 오류 발생")
                try:
                    st.json(res.json())
                except:
                    st.write(res.text)

        except Exception as e:
            st.error(f"에러 발생: {e}")

# ✅ --- 탭2: 대화형 질문 ---
with tab2:
    st.subheader("💬 PPE 관련 AI 상담")

    user_message = st.text_area("질문을 입력하세요 (예: 'PPE의 종류는 뭐야?', '안전모는 왜 써야 해?')")

    if st.button("🤖 AI에게 물어보기"):
        if not user_message.strip():
            st.warning("질문을 입력해주세요.")
        else:
            try:
                with st.spinner("AI가 답변 중입니다..."):
                    res = requests.post(url_chat, json={"message": user_message})
                
                if res.status_code == 200:
                    reply = res.json().get("reply", "AI 응답이 없습니다.")
                    st.markdown(f"**🧠 AI의 답변:**\n\n{reply}")
                else:
                    st.error("⚠️ 서버 오류 발생")
                    st.json(res.json())

            except Exception as e:
                st.error(f"에러 발생: {e}")
