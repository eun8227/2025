import streamlit as st

st.set_page_config(page_title="MBTI 진로 교육", layout="wide")

st.title("MBTI 기반 진로 교육 웹앱 🎓")

# --- MBTI 테스트 ---
st.header("MBTI 간단 테스트")
q1 = st.radio("사람들과 함께하는 시간이 에너지를 준다.", ["그렇다", "아니다"])
q2 = st.radio("계획을 세우고 지키는 것을 선호한다.", ["그렇다", "아니다"])

if st.button("결과 보기"):
    # 단순 로직 예시
    e_or_i = "E" if q1 == "그렇다" else "I"
    j_or_p = "J" if q2 == "그렇다" else "P"
    result = e_or_i + "N" + "F" + j_or_p  # 예시: ENFJ
    
    st.success(f"당신의 MBTI 유형은 **{result}** 입니다!")

    # --- 진로 추천 ---
    career_dict = {
        "ENFJ": ["교사", "상담가", "교육 기획자"],
        "INTJ": ["연구원", "전략기획가", "프로그래머"],
        "ESFP": ["배우", "이벤트 기획자", "광고/홍보"],
    }
    
    st.subheader("추천 진로 ✨")
    careers = career_dict.get(result, ["다양한 가능성이 있어요!"])
    for c in careers:
        st.write(f"- {c}")
    
    # --- 학습 스타일 ---
    st.subheader("학습 스타일")
    if result == "ENFJ":
        st.write("🤝 협력적이고 사람 중심의 학습에 강점을 보입니다.")
    elif result == "INTJ":
        st.write("📚 자기주도적 학습과 장기적 목표 설정에 강합니다.")
    else:
        st.write("각 MBTI 유형마다 고유한 학습 강점이 있습니다.")
