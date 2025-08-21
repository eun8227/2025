import streamlit as st

st.set_page_config(page_title="✨ MBTI 진로 탐색 ✨", layout="wide")

# --- Title ---
st.markdown(
    """
    <h1 style='text-align: center; color: #ff4b4b;'>
    🌈✨ MBTI 기반 진로 탐색 🎓🚀
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# --- Test Section ---
st.header("📝 MBTI 간단 테스트 🔮")

q1 = st.radio("💡 사람들과 함께하는 시간이 에너지를 준다 🎉", ["🙋‍♂️ 그렇다", "🤔 아니다"])
q2 = st.radio("📅 계획을 세우고 따르는 걸 좋아한다 ✅", ["👍 그렇다", "🙅‍♀️ 아니다"])

if st.button("🎯 결과 보기"):
    e_or_i = "E" if "그렇다" in q1 else "I"
    j_or_p = "J" if "그렇다" in q2 else "P"
    result = e_or_i + "N" + "F" + j_or_p
    
    st.success(f"✨ 당신의 MBTI 유형은 **{result}** 입니다! 🎉💫")

    # 직업 추천 DB
    career_dict = {
        "ENFJ": ["👩‍🏫 교사", "🧑‍💼 상담가", "📚 교육 기획자"],
        "INTJ": ["🔬 연구원", "📊 전략기획가", "💻 프로그래머"],
        "ESFP": ["🎭 배우", "🎉 이벤트 기획자", "📢 광고/홍보"],
    }

    st.markdown("## 🌟 추천 진로 ✨")

    careers = career_dict.get(result, ["🌍 다양한 가능성이 있어요! 🚀"])
    cols = st.columns(len(careers))

    for idx, c in enumerate(careers):
        with cols[idx]:
            st.markdown(
                f"""
                <div style='background-color:#f9f9f9; border-radius:15px; padding:20px; 
                text-align:center; box-shadow:2px 2px 10px rgba(0,0,0,0.1);'>
                <h2 style='color:#ff7f50'>{c}</h2>
                </div>
                """, 
                unsafe_allow_html=True
            )

    # 학습 스타일
    st.markdown("## 📚 학습 스타일 🌟")
    if result == "ENFJ":
        st.info("🤝 협력적이고 팀워크 중심의 학습에 강점을 보입니다! 🌍✨")
    elif result == "INTJ":
        st.info("📖 자기주도 학습 + 장기적 목표 설정에 최강입니다! 🚀")
    else:
        st.info("🎨 당신만의 특별한 학습 스타일이 있습니다! 🌈🔥")
