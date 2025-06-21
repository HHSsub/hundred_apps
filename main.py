# requirements.txt: streamlit, openai>=1.0.0
import os

with open("requirements.txt", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            os.system(f"pip install {line.strip()}")

import streamlit as st
from openai import OpenAI

# 🔑 OpenAI 키 입력
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # 또는 직접 문자열로 입력 가능

st.set_page_config(page_title="AI 세대차이 번역기", layout="centered")
st.title("🧠 AI 세대차이 번역기")
st.caption("자녀가 보낸 톡이 무슨 뜻인지 모르겠다면? 여기에 붙여넣으세요!")

user_input = st.text_area("📨 자녀 또는 MZ세대 문장을 입력하세요:", height=100)

if st.button("번역하기"):
    if not user_input.strip():
        st.warning("문장을 입력해주세요.")
    else:
        with st.spinner("GPT가 해석 중입니다..."):
            prompt = f"""
다음 문장은 한국의 MZ세대(10~30대)가 사용하는 표현이야.
아래 문장을 40~60대 부모님이 이해할 수 있게 설명해줘.

1. 무슨 뜻인지 쉬운 말로 해석
2. 어떤 감정이 담긴 말인지 분석
3. 이 말을 들었을 때 어떤 식으로 반응하면 좋을지 추천 대답 2개

문장: {user_input}
"""
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                st.success("✅ 해석 결과")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"에러 발생: {e}")
