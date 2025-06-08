import streamlit as st
from gemini import generate_three_poems

st.set_page_config(page_title="AI 시 챗봇", layout="centered")
st.title("✨ Gemini 기반 현대 시 챗봇 ✨")
st.write("세 칸에 키워드를 입력하면, 세 키워드를 모두 반영하되 제목이 서로 다른 시 3편을 한 번에 생성합니다.")

col1, col2, col3 = st.columns(3)
with col1:
    kw1 = st.text_input("첫 번째 키워드", key="kw1", max_chars=10, placeholder="최대 10자")
with col2:
    kw2 = st.text_input("두 번째 키워드", key="kw2", max_chars=10, placeholder="최대 10자")
with col3:
    kw3 = st.text_input("세 번째 키워드", key="kw3", max_chars=10, placeholder="최대 10자")

if st.button("키워드 3개로 시 3편 생성하기"):
    if not (kw1.strip() and kw2.strip() and kw3.strip()):
        st.error("세 개의 키워드를 모두 입력해주세요.")
    else:
        keywords = [kw1.strip(), kw2.strip(), kw3.strip()]
        try:
            with st.spinner("시를 생성 중입니다..."):
                poems = generate_three_poems(keywords)
        except Exception as e:
            st.error(f"시 생성 중 오류 발생: {e}")
            st.stop()

        # 결과 출력
        for idx, (title, poem) in enumerate(poems, start=1):
            st.markdown("---")
            st.markdown(f"{title}")
            st.text(poem)
