import streamlit as st

st.set_page_config(page_title="✨ MBTI 진로 탐색 ✨", layout="wide")

# --- Title ---
st.markdown(
    """
    <h1 style='text-align: center; color: #ff4b4b;'>
    🌈✨ MBTI 기반 진로 탐색 🎓🚀<br>🐼🐯🦊 동물 친구들과 함께해요! 🐧🦁🐰
    </h1>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

# --- 질문 ---
st.header("📝 MBTI 간단 검사 🔮")
st.markdown("👉 아래 질문에 솔직하게 답해주세요! 😆")

# E/I
q1 = st.radio("💬 사람들과 이야기할 때 에너지가 충전된다 🎉", ["🙋 그렇다", "🤔 아니다"])
q2 = st.radio("🏞️ 혼자만의 시간이 꼭 필요하다 🌙", ["🙋 그렇다", "🤔 아니다"])

# S/N
q3 = st.radio("🔍 구체적인 사실이 더 중요하다 📊", ["🙋 그렇다", "🤔 아니다"])
q4 = st.radio("💡 아이디어와 상상이 더 중요하다 🌌", ["🙋 그렇다", "🤔 아니다"])

# T/F
q5 = st.radio("⚖️ 논리와 분석으로 판단한다 🧠", ["🙋 그렇다", "🤔 아니다"])
q6 = st.radio("💞 감정과 관계를 고려한다 ❤️", ["🙋 그렇다", "🤔 아니다"])

# J/P
q7 = st.radio("📅 계획을 세우고 따르는 것을 좋아한다 ✅", ["🙋 그렇다", "🤔 아니다"])
q8 = st.radio("🎨 상황에 따라 유연하게 대처하는 편이다 🌊", ["🙋 그렇다", "🤔 아니다"])

# --- 결과 계산 ---
if st.button("🎯 결과 보기"):
    e_score = (q1 == "🙋 그렇다") - (q2 == "🙋 그렇다")
    s_score = (q3 == "🙋 그렇다") - (q4 == "🙋 그렇다")
    t_score = (q5 == "🙋 그렇다") - (q6 == "🙋 그렇다")
    j_score = (q7 == "🙋 그렇다") - (q8 == "🙋 그렇다")

    mbti = ""
    mbti += "E" if e_score >= 0 else "I"
    mbti += "S" if s_score >= 0 else "N"
    mbti += "T" if t_score >= 0 else "F"
    mbti += "J" if j_score >= 0 else "P"

    st.success(f"✨ 당신의 MBTI 유형은 **{mbti}** 입니다! 🎉💫")

    # MBTI 동물 + 진로 매핑
    mbti_animals = {
        "ISTJ": ("🐘 코끼리", ["📊 회계사", "⚙️ 엔지니어", "🏢 관리자"]),
        "ISFJ": ("🐢 거북이", ["🏥 간호사", "🤝 사회복지사", "👩‍🏫 교사"]),
        "INFJ": ("🦁 사자", ["💞 상담가", "✍️ 작가", "📚 교육자"]),
        "INTJ": ("🦉 올빼미", ["🔬 연구원", "💻 개발자", "📊 전략기획가"]),
        "ISTP": ("🐆 치타", ["✈️ 파일럿", "🔧 수리공", "⚙️ 엔지니어"]),
        "ISFP": ("🦋 나비", ["🎨 디자이너", "🎶 작곡가", "🎭 예술가"]),
        "INFP": ("🦄 유니콘", ["✍️ 작가", "🧠 심리학자", "💞 상담가"]),
        "INTP": ("🐱 고양이", ["🔬 과학자", "💻 프로그래머", "📖 철학자"]),
        "ESTP": ("🐅 호랑이", ["🏃 운동선수", "📈 기업가", "📢 마케팅"]),
        "ESFP": ("🐬 돌고래", ["🎤 연예인", "🎉 이벤트 플래너", "📸 크리에이터"]),
        "ENFP": ("🦊 여우", ["🎨 디자이너", "📢 마케터", "🚀 창업가"]),
        "ENTP": ("🐒 원숭이", ["💡 발명가", "📺 방송인", "🚀 벤처기업가"]),
        "ESTJ": ("🦅 독수리", ["⚖️ 판사", "🪖 군인", "🏢 관리자"]),
        "ESFJ": ("🐕 강아지", ["👩‍🏫 교사", "🏥 간호사", "🤝 HR 담당자"]),
        "ENFJ": ("🐼 판다", ["📚 교육자", "💞 상담가", "🌍 사회운동가"]),
        "ENTJ": ("🦍 고릴라", ["👔 CEO", "⚖️ 변호사", "🏢 경영자"]),
    }

    animal, careers = mbti_animals.get(mbti, ("🐼 판다", ["🌍 다양한 가능성이 있어요! 🚀"]))

    # --- 결과 카드 ---
    st.markdown(
        f"""
        <div style='background-color:#fff0f5; border-radius:20px; padding:20px; 
        text-align:center; box-shadow:2px 2px 15px rgba(0,0,0,0.15);'>
        <h2 style='color:#ff1493'>당신은 {animal} 타입! 🐾</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- 진로 추천 ---
    st.markdown("## 🌟 추천 진로 ✨")
    cols = st.columns(len(careers))
    for idx, c in enumerate(careers):
        with cols[idx]:
            st.markdown(
                f"""
                <div style='background-color:#f0fff0; border-radius:15px; padding:20px; 
                text-align:center; box-shadow:2px 2px 10px rgba(0,0,0,0.1);'>
                <h2 style='color:#32cd32'>{c}</h2>
                </div>
                """, 
                unsafe_allow_html=True
            )

    # --- 학습 스타일 ---
    st.markdown("## 📚 학습 스타일 🌟")
    if mbti.startswith("I"):
        st.info("🌙 혼자 탐구하고 깊이 몰입하는 학습에 강합니다! 🧠📖")
    else:
        st.info("🌞 함께 토론하고 활동적인 학습에서 에너지를 얻습니다! 🤝🎉")
