import streamlit as st
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="댄스 연습 앱", page_icon="💃", layout="wide")
st.title("💃 댄스 연습 기록 & 랜덤 안무 아이디어 🕺")

# ---- 데이터 초기화 ----
if "records" not in st.session_state:
    st.session_state["records"] = []

# ---- 장르별 기본기 ----
dance_basics = {
    "힙합": {
        "초급": ["Bounce", "Step Touch", "Slide"],
        "중급": ["Body Roll", "Wave", "Isolations"],
        "고급": ["Knee Drop", "Harlem Shake", "Reverse Wave"]
    },
    "팝핀": {
        "초급": ["Hit", "Fresno", "Arm Wave"],
        "중급": ["Dime Stop", "Robot Walk", "Isolation Groove"],
        "고급": ["Boogaloo Roll", "Neck-o-flex", "Twist-o-flex"]
    },
    "락킹": {
        "초급": ["Point", "Wrist Roll", "Lock"],
        "중급": ["Scoobot", "Stop-and-Go", "Up Lock"],
        "고급": ["Funky Chicken", "Throwback", "Jazz Split"]
    },
    "걸리시": {
        "초급": ["Step Tap", "Shoulder Bounce", "Hip Roll"],
        "중급": ["Hair Whip", "Body Wave", "Chest Isolation"],
        "고급": ["Floor Work", "Drop Spin", "Back Arch"]
    },
    "하우스": {
        "초급": ["Two Step", "Side Walk", "Heel Toe"],
        "중급": ["Shuffle", "Stomp", "Jack"],
        "고급": ["Lofting", "Floor Spin", "Heel Jack"]
    }
}

# ---- 장르별 추천곡 ----
song_recommendations = {
    "힙합": ["Jay Park - All I Wanna Do", "Zico - Artist"],
    "팝핀": ["Michael Jackson - Billie Jean", "Usher - Yeah!"],
    "락킹": ["James Brown - Get Up Offa That Thing", "Bruno Mars - 24K Magic"],
    "걸리시": ["BLACKPINK - How You Like That", "Sunmi - Gashina"],
    "하우스": ["Disclosure - Latch", "Robin S - Show Me Love"]
}

# ---- 안무 랜덤 생성 ----
st.header("✨ 랜덤 기본기 안무 생성기 🎶")
genre = st.selectbox("🎵 장르 선택", list(dance_basics.keys()))
level = st.radio("🔥 난이도 선택", ["초급", "중급", "고급"])

if st.button("💡 안무 생성하기"):
    moves = dance_basics[genre][level]
    routine = random.sample(moves, k=min(3, len(moves)))
    st.session_state["current_routine"] = f"[{genre}/{level}] " + " → ".join(routine)

# ---- 안무 결과 + 곡 선택 ----
if "current_routine" in st.session_state:
    st.success(f"오늘의 안무 아이디어 💃🕺: {st.session_state['current_routine']}")
    
    # 곡 선택지 제공
    st.subheader("🎶 추천 곡 선택")
    song_choice = st.selectbox("마음에 드는 곡을 선택하세요", song_recommendations[genre])
    st.session_state["selected_song"] = song_choice

# ---- 연습 기록 ----
st.header("📒 연습 기록하기")
date = st.date_input("📅 연습 날짜", datetime.today())
minutes = st.number_input("⏱️ 연습 시간 (분)", min_value=5, max_value=300, step=5)

if st.button("✅ 연습 기록 저장"):
    st.session_state["records"].append({
        "date": date,
        "minutes": minutes,
        "routine": st.session_state.get("current_routine", "없음"),
        "genre": genre,
        "level": level,
        "song": st.session_state.get("selected_song", "선택 안 함")
    })
    st.success("✨ 연습 기록이 저장되었습니다!")

# ---- 기록 보기 ----
st.header("📊 나의 연습 기록")
if len(st.session_state["records"]) > 0:
    df = pd.DataFrame(st.session_state["records"])
    st.dataframe(df)

    st.line_chart(df.set_index("date")["minutes"])
else:
    st.info("아직 연습 기록이 없습니다. 먼저 기록을 남겨보세요!")

