import os
import tempfile
from dotenv import load_dotenv
import streamlit as st
from gemini import generate_three_poems

# Load environment variables
load_dotenv()
if not os.getenv("Gemini_API_KEY"):
    st.error("`.env`에 Gemini_API_KEY를 설정해주세요.")
    st.stop()

# Streamlit page configuration
st.set_page_config(
    page_title="✨ 힌트 기반 시 생성기",
    layout="centered",
)

# Custom CSS for modern card styling
st.markdown(
    """
    <style>
    .poem-card {
        background-color: #f0f8ff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .poem-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .poem-body {
        white-space: pre-line;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App header and bilingual description
st.title("AI와 시 쓰기(Poem with AI)")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write(
    "당신의 세 가지 힌트를 바탕으로, 세 편의 시를 씁니다."
)
st.write(
    "Based on the three hints you provide, three distinct poems will be created individually."
)
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
# Hint inputs
st.write("")
# 첫 번째 힌트
col1, col2, col3 = st.columns([1,1,1])
with col1:
    hint1 = st.text_input(
        "첫 번째 힌트 (Hint 1)",
        max_chars=12,
   
    )
st.write("")  # 여백

# 두 번째 힌트
col1, col2, col3 = st.columns([1,1,1])
with col1:
    hint2 = st.text_input(
        "두 번째 힌트 (Hint 2)",
        max_chars=12,
  
    )
st.write("")  # 여백

# 세 번째 힌트
col1, col2, col3 = st.columns([1,1,1])
with col1:
    hint3 = st.text_input(
        "세 번째 힌트 (Hint 3)",
        max_chars=12,

    )
st.write("")

# Generate & Print button
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

if st.button("시 쓰기 / Write Poem"):
    if not (hint1 and hint2 and hint3):
        st.warning("세 개의 힌트를 모두 입력해주세요. / Please enter all three hints.")
    else:
        # Generate poems
        with st.spinner("당신의 시를 생성 중입니다... / Generating poems ..."):
            try:
                poems = generate_three_poems([hint1, hint2, hint3])
            except Exception as e:
                st.error(f"시 생성 오류: {e} / Error generating poems: {e}")
                st.stop()

        # Print each poem separately with number above title
        errors = []
        for idx, (title, body) in enumerate(poems, start=1):
            # Number on first line, then blank line, then title, then blank line, then body
            content = f"{idx}\n\n{title}\n\n{body}\n"
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=f"_v{idx}.txt", mode="w", encoding="utf-8") as tmp:
                    tmp.write(content)
                    path = tmp.name
                os.startfile(path, "print")
            except Exception as e:
                errors.append(f"{idx}번 인쇄 오류: {e} / Print error for poem {idx}: {e}")

        if errors:
            st.error("\n".join(errors))
        else:
            st.success("세 편의 시 중 마음에 드는 번호를 골라주세요! / Please choose the number of your favorite poem among the three!")
