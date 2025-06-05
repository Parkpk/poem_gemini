import streamlit as st
from gemini import generate_poem

st.set_page_config(page_title="AI 시 챗봇", layout="centered")
st.title("✨ Gemini 기반 현대 시 챗봇 ✨")
st.write("세 칸에 각각 키워드를 입력하면, 세 키워드를 모두 반영하되 제목에는 절대 키워드가 포함되지 않는 서로 다른 버전의 시 3편을 생성하여 보여줍니다.")

# ====== 키워드 입력란 (max_chars=10) ======
col1, col2, col3 = st.columns(3)

with col1:
    kw1 = st.text_input("첫 번째 키워드", key="kw1", max_chars=10, placeholder="최대 10자")
with col2:
    kw2 = st.text_input("두 번째 키워드", key="kw2", max_chars=10, placeholder="최대 10자")
with col3:
    kw3 = st.text_input("세 번째 키워드", key="kw3", max_chars=10, placeholder="최대 10자")

# ====== 시 생성 버튼 ======
if st.button("키워드 3개로 시 3편 생성하기"):
    # 세 칸 모두 입력되었는지 확인
    if not (kw1.strip() and kw2.strip() and kw3.strip()):
        st.error("세 개의 키워드를 모두 입력해주세요.")
    else:
        keywords = [kw1.strip(), kw2.strip(), kw3.strip()]
        poems = []

        with st.spinner("세 편의 시를 생성 중입니다..."):
            for version in range(1, 4):
                try:
                    title, poem = generate_poem(keywords)
                    poems.append((version, title, poem))
                except Exception as e:
                    st.error(f"버전 {version} 생성 중 오류 발생: {e}")
                    st.stop()

        # 생성된 시 3편을 화면에 순서대로 출력
        for version, title, poem in poems:
            st.markdown("---")
           
            if title:
                st.markdown(f"### {title}")
            else:
                st.markdown("### (제목 생성 실패)")
            # 시 본문은 개행을 그대로 보여주기 위해 st.text 사용
            st.text(poem)
