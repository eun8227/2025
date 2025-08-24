import streamlit as st
import pandas as pd
import random
from datetime import datetime, time

st.set_page_config(page_title="댄스 연습 앱", page_icon="💃", layout="wide")

# --- 🌌 오로라 + 별똥별 CSS ---
page_bg = """
<style>
.stApp {
    background: linear-gradient(120deg, #1e3c72, #2a5298, #6dd5ed, #cc2b5e, #753a88);
    background-size: 400% 400%;
    animation: aurora 15s ease infinite;
    position: relative;
    overflow: hidden;
}
@keyframes aurora {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.star {
    position: absolute;
    width: 2px;
    height: 80px;
    background: linear-gradient(white, rgba(255,255,255,0));
    border-radius: 50%;
    animation: shooting 3s linear infinite;
    opacity: 0.8;
}
.star:nth-child(1) { top: 10%; left: 20%; animation-delay: 0s; }
.star:nth-child(2) { top: 30%; left: 70%; animation-delay: 1s; }
.star:nth-child(3) { top: 50%; left: 40%; animation-delay: 2s; }
.star:nth-child(4) { top: 80%; left: 60%; animation-delay: 1.5s; }
.star:nth-child(5) { top: 20%; left: 85%; animation-delay: 0.5s; }
.star:nth-child(6) { top: 60%; left: 15%; animation-delay: 2.5s; }
@keyframes shooting {
    0% {transform: translateX(0) translateY(0) rotate(45deg); opacity: 1;}
    100% {transform: translateX(-200px) translateY(200px) rotate(45deg); opacity: 0;}
}
</style>
<div class="star"></div><div class="star"></div><div class="star"></div>
<div class="star"></div><div class="star"></div><div class="star"></div>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("💃 댄스 연습 기록 & 랜덤 안무 아이디어 🌙✨")

# --- 세션 상태 초기화 ---
if "records" not in st.session_state:
    st.session_state["records"] = []
if "selected_songs" not in st.session_state:
    st.session_state["selected_songs"] = []

# --- 기본기 데이터 ---
dance_basics = {
    "힙합": {
        "초급": [
            ("Bounce", ["무릎 굽히며 박자 타기", "어깨 리듬", "손 자연스럽게 흔들기"]),
            ("Step Touch", ["옆으로 발 내딛기", "반대발 붙이기", "손 반대방향 흔들기"]),
            ("Slide", ["발을 밀듯 옆으로", "상체 부드럽게", "발 모으기"])
        ],
        "중급": [
            ("Body Roll", ["가슴 내밀기", "가슴→배→골반 굴리기", "부드럽게 연결"]),
            ("Wave", ["손끝→팔꿈치 파도", "어깨→가슴→허리 이어가기", "허리→반대팔"]),
            ("Isolations", ["머리만 좌우", "어깨 업다운", "골반 원형"])
        ],
        "고급": [
            ("Knee Drop", ["무릎 구부리며 착지", "상체 고정", "일어나며 리듬"]),
            ("Harlem Shake", ["어깨 빠르게 흔들기", "몸 전체 진동", "팔·머리 흔들기"]),
            ("Reverse Wave", ["허리→가슴→어깨→팔", "손끝까지 흐름", "부드럽게 원위치"])
        ]
    }
}

# --- 추천곡 ---
song_recommendations = {
    "힙합": [
        ("Jay Park - All I Wanna Do", "https://youtu.be/w0PtbE8K6FQ"),
        ("Zico - Artist", "https://youtu.be/UuV2BmJ1p_I"),
        ("Epik High - Fly", "https://youtu.be/lS9VnS6tJqE")
    ]
}

# --- 랜덤 안무 생성기 ---
st.header("🌸 랜덤 안무 생성기 🦋")
genre = st.selectbox("장르를 선택하세요 🎵", list(dance_basics.keys()))
level = st.radio("난이도를 선택하세요", list(dance_basics[genre].keys()))

if st.button("✨ 안무 아이디어 생성하기"):
    moves = dance_basics[genre][level]
    routine_length = random.randint(3, 5)
    routine = random.sample(moves, k=min(routine_length, len(moves)))
    
    cute_emojis = ["🌸", "🐰", "🦋", "🌙", "⭐", "💎", "🍀", "🔥", "🪽", "🪐"]
    formatted = []
    for i, (move, steps) in enumerate(routine, 1):
        emoji = random.choice(cute_emojis)
        step_text = "\n      - " + "\n      - ".join(steps)
        formatted.append(f"{i}. {move} {emoji}{step_text}")
    
    st.session_state["current_routine"] = "\n".join(formatted)

if "current_routine" in st.session_state:
    st.success(f"오늘의 안무 아이디어 ({genre} - {level}) 🌟")
    st.markdown(st.session_state["current_routine"])

    st.subheader("🎶 오늘의 추천 곡")
    song_list = [title for title, _ in song_recommendations[genre]]
    st.session_state["selected_songs"] = st.multiselect("곡을 골라보세요 🎧", song_list)

    for title, link in song_recommendations[genre]:
        if title in st.session_state["selected_songs"]:
            st.markdown(f"👉 {title} 🔗 [유튜브]({link})")

# --- 연습 기록 ---
st.header("📝 연습 기록")
date = st.date_input("연습 날짜", datetime.today())
start_time = st.time_input("시작 시각", time(18, 0))
end_time = st.time_input("종료 시각", time(19, 0))

duration = (datetime.combine(datetime.today(), end_time) - 
            datetime.combine(datetime.today(), start_time)).seconds / 3600

if st.button("기록 저장"):
    st.session_state["records"].append({
        "date": date,
        "hours": round(duration, 2),
        "routine": st.session_state.get("current_routine", "없음"),
        "genre": genre,
        "level": level,
        "songs": st.session_state["selected_songs"]
    })
    st.success("✅ 연습 기록이 저장되었습니다!")

# --- 기록 보기 ---
st.header("📊 연습 기록 보기")
if st.session_state["records"]:
    df = pd.DataFrame(st.session_state["records"])
    st.dataframe(df)
    st.line_chart(df.set_index("date")["hours"])
else:
    st.info("아직 기록이 없습니다 🐥")
