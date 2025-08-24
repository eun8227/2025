import streamlit as st
import pandas as pd
import random
import datetime

st.set_page_config(page_title="댄스 연습 앱", layout="wide")

# --- CSS: 오로라 + 별똥별 ---
st.markdown("""
<style>
body {
    margin: 0;
    height: 100vh;
    background: linear-gradient(270deg, #0f2027, #203a43, #2c5364);
    background-size: 600% 600%;
    animation: aurora 20s ease infinite;
    color: white;
}
@keyframes aurora {
    0% {background-position:0% 50%}
    50% {background-position:100% 50%}
    100% {background-position:0% 50%}
}
/* 별똥별 효과 */
.starry {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  top: 0;
  left: 0;
}
.star {
  position: absolute;
  width: 2px;
  height: 2px;
  background: white;
  animation: twinkle 2s infinite alternate;
}
@keyframes twinkle {
  from {opacity: 0.1;}
  to {opacity: 1;}
}
.shooting-star {
  position: absolute;
  width: 150px;
  height: 2px;
  background: linear-gradient(-45deg, white, rgba(0,0,255,0));
  animation: shooting 3s linear infinite;
}
@keyframes shooting {
  from {transform: translateX(0) translateY(0);}
  to {transform: translateX(-600px) translateY(600px);}
}
</style>
<div class="starry">
  """ + "".join([f'<div class="star" style="top:{random.randint(0,100)}%;left:{random.randint(0,100)}%"></div>' for _ in range(80)]) +
  "".join([f'<div class="shooting-star" style="top:{random.randint(0,100)}%;left:{random.randint(0,100)}%"></div>' for _ in range(5)]) +
  "</div>",
  unsafe_allow_html=True
)

# --- 기본기 데이터 ---
dance_moves = {
    "HipHop": {
        "초급": [
            ("Bounce 🐥", "무릎을 리드미컬하게 굽혔다 펴며 상체 반동 주기", "https://youtu.be/HDuXlV3t1Kg"),
            ("Step Touch 🐰", "옆으로 발을 뻗고 제자리로 가져오기", "https://youtu.be/qKXK6rYxYh0"),
        ],
        "중급": [
            ("Running Man 🏃", "발을 뒤로 빼면서 상체를 앞뒤로 움직이기", "https://youtu.be/n3-9Z5qA0rM"),
        ],
    },
    "K-Pop": {
        "초급": [
            ("Finger Heart 💖", "양손으로 하트를 만들어 리듬에 맞춰 흔들기", "https://youtu.be/4Q46xYqUwZQ"),
        ],
        "중급": [
            ("Body Wave 🌊", "상체를 물결처럼 이어서 움직이기", "https://youtu.be/OhmR4lFZx3o"),
        ],
    }
}

# --- 추천곡 데이터 (날짜별 랜덤) ---
songs = {
    "HipHop": [
        ("Lose Control - Missy Elliott", "https://youtu.be/dVL4azrBFoM"),
        ("Lean Back - Terror Squad", "https://youtu.be/ajmI1P3r1w4")
    ],
    "K-Pop": [
        ("SEVENTEEN - Super", "https://youtu.be/-GQg25oP0S4"),
        ("BLACKPINK - Pink Venom", "https://youtu.be/gQlMMD8auMs")
    ]
}

# --- 사이드바 ---
st.sidebar.title("📌 메뉴")
page = st.sidebar.radio("이동", ["오늘의 안무", "연습 기록"])

# --- 세션 상태 ---
if "records" not in st.session_state:
    st.session_state.records = []

# --- 오늘의 안무 페이지 ---
if page == "오늘의 안무":
    st.title("✨ 오늘의 안무 아이디어 ✨")

    genre = st.selectbox("장르 선택 🕺", list(dance_moves.keys()))
    level = st.selectbox("난이도 선택 🎚", list(dance_moves[genre].keys()))

    if st.button("랜덤 안무 생성 🎲"):
        moves = random.sample(dance_moves[genre][level], k=min(2, len(dance_moves[genre][level])))
        for move in moves:
            name, desc, link = move
            st.markdown(f"**{name}** - {desc}")
            st.video(link)

    # 오늘의 추천곡
    st.subheader("🎵 오늘의 추천곡")
    today = datetime.date.today().toordinal()
    for genre_name, genre_songs in songs.items():
        song = genre_songs[today % len(genre_songs)]
        st.markdown(f"**{genre_name}**: [{song[0]}]({song[1]})")

# --- 연습 기록 페이지 ---
elif page == "연습 기록":
    st.title("📊 연습 기록하기")
    date = st.date_input("연습 날짜 선택 📅", datetime.date.today())
    start_time = st.time_input("시작 시간 ⏰", datetime.datetime.now().time())
    end_time = st.time_input("종료 시간 🕒", (datetime.datetime.now() + datetime.timedelta(hours=1)).time())
    duration = (datetime.datetime.combine(datetime.date.today(), end_time) -
                datetime.datetime.combine(datetime.date.today(), start_time)).seconds / 60

    if st.button("기록 저장 ✍️"):
        st.session_state.records.append({"날짜": date, "시작": start_time, "종료": end_time, "분": duration})
        st.success("저장 완료! 🎉")

    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(df)
        st.line_chart(df.set_index("날짜")["분"])
        st.download_button("CSV 다운로드 📂", df.to_csv(index=False), "records.csv", "text/csv")
