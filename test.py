import streamlit as st
import pandas as pd
import random
import datetime

st.set_page_config(page_title="댄스 연습 기록 앱", layout="wide")

# ===== CSS (오로라 + 별똥별 반짝임) =====
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #2E0854, #5B2C6F, #7D3C98, #2C3E50);
        background-size: 400% 400%;
        animation: aurora 20s ease infinite;
        color: white;
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
        height: 2px;
        background: white;
        border-radius: 50%;
        animation: twinkle 2s infinite ease-in-out;
    }

    @keyframes twinkle {
        0%, 100% {opacity: 0.2;}
        50% {opacity: 1;}
    }

    .shooting-star {
        position: absolute;
        width: 2px;
        height: 80px;
        background: linear-gradient(-45deg, white, transparent);
        animation: shooting 5s linear infinite;
        opacity: 0.8;
    }

    @keyframes shooting {
        0% {transform: translateX(0) translateY(0); opacity: 0;}
        10% {opacity: 1;}
        100% {transform: translateX(-800px) translateY(600px); opacity: 0;}
    }
    </style>

    <script>
    function createStars() {
        const body = document.querySelector("body");
        for (let i = 0; i < 150; i++) {
            let star = document.createElement("div");
            star.className = "star";
            star.style.top = Math.random() * window.innerHeight + "px";
            star.style.left = Math.random() * window.innerWidth + "px";
            star.style.animationDuration = 1 + Math.random() * 3 + "s";
            body.appendChild(star);
        }
        for (let i = 0; i < 5; i++) {
            let shooting = document.createElement("div");
            shooting.className = "shooting-star";
            shooting.style.top = Math.random() * window.innerHeight + "px";
            shooting.style.left = Math.random() * window.innerWidth + "px";
            shooting.style.animationDelay = Math.random() * 5 + "s";
            body.appendChild(shooting);
        }
    }
    window.onload = createStars;
    </script>
    """,
    unsafe_allow_html=True
)

# ===== 기본기 데이터 =====
dance_basics = {
    "HipHop": {
        "초급": [
            {"name": "Bounce 🐥", "desc": "무릎을 굽혔다 펴며 상체와 반동 주기", "link": "https://youtu.be/HDuXlV3t1Kg"},
            {"name": "Step Touch 🐰", "desc": "옆으로 발을 뻗고 다시 제자리로 가져오기", "link": "https://youtu.be/qKXK6rYxYh0"},
            {"name": "Slide 🌸", "desc": "발을 바닥에 밀듯이 옆으로 이동하기", "link": "https://youtu.be/s0t5lD8j5lU"}
        ],
        "중급": [
            {"name": "Kick Ball Change 🐾", "desc": "앞으로 찬 후 반대발로 교차 이동", "link": "https://youtu.be/ZQ2iXc8l8wA"},
            {"name": "Body Roll 🦋", "desc": "가슴부터 골반까지 웨이브", "link": "https://youtu.be/3QXhUJmWg7g"}
        ],
        "고급": [
            {"name": "Wave 🌊", "desc": "손끝부터 몸 전체로 물결 움직임", "link": "https://youtu.be/JVw-c4LJ2sY"},
            {"name": "Krump Arm Swing 🔥", "desc": "강렬한 팔 스윙과 상체 힘 강조", "link": "https://youtu.be/fcF7j7GhtI0"}
        ]
    },
    "KPop": {
        "초급": [
            {"name": "Two Step 🐾", "desc": "좌우로 두 발 이동 후 박자 맞추기", "link": "https://youtu.be/y7QjaG7xwPo"},
            {"name": "Clap 👏", "desc": "박자에 맞춰 손뼉치기", "link": "https://youtu.be/EHF7QZZb6U4"}
        ],
        "중급": [
            {"name": "Body Wave 🌊", "desc": "상체에서 하체로 흐르는 웨이브", "link": "https://youtu.be/6ArlKZydC2Y"}
        ],
        "고급": [
            {"name": "Isolation 🕺", "desc": "한 부위만 고립시켜 움직이기", "link": "https://youtu.be/z3ZFF0TNLr8"}
        ]
    }
}

# ===== 추천 곡 (하루마다 바뀜) =====
song_recommendations = {
    "HipHop": [
        {"title": "Jay Park - All I Wanna Do", "link": "https://youtu.be/JN0z9WZpVnM"},
        {"title": "Chris Brown - Fine China", "link": "https://youtu.be/iGs1gODLiSQ"},
    ],
    "KPop": [
        {"title": "BTS - Dynamite", "link": "https://youtu.be/gdZLi9oWNZg"},
        {"title": "BLACKPINK - How You Like That", "link": "https://youtu.be/ioNng23DkIM"},
    ]
}

# 날짜 기반 추천곡 선택
today = datetime.date.today()
def daily_song(genre):
    recs = song_recommendations[genre]
    idx = today.toordinal() % len(recs)
    return recs[idx]

# ===== 앱 UI =====
st.title("🐰💃 댄스 연습 기록 & 안무 아이디어 앱 ✨")

# 장르/난이도 선택
col1, col2 = st.columns(2)
with col1:
    genre = st.selectbox("장르 선택 🎶", list(dance_basics.keys()))
with col2:
    level = st.selectbox("난이도 선택 ⭐", list(dance_basics[genre].keys()))

# ===== 오늘의 안무 아이디어 =====
st.subheader("🌸 오늘의 랜덤 안무 아이디어 🌸")
selected_moves = random.sample(dance_basics[genre][level], k=min(2, len(dance_basics[genre][level])))
for move in selected_moves:
    st.markdown(f"**{move['name']}** → {move['desc']} 🎀  ")
    st.markdown(f"[예시 영상 보기]({move['link']}) 🎥")

# ===== 추천 곡 =====
st.subheader("🎵 오늘의 추천 곡 🎵")
song = daily_song(genre)
st.markdown(f"{song['title']} 💖 [듣기]({song['link']})")

# ===== 연습 기록 =====
st.subheader("📅 연습 기록하기")
if "records" not in st.session_state:
    st.session_state.records = []

date = st.date_input("연습 날짜")
start_time = st.time_input("시작 시간 ⏰")
end_time = st.time_input("종료 시간 ⏰")
duration = (datetime.datetime.combine(date, end_time) - datetime.datetime.combine(date, start_time)).seconds // 60

if st.button("기록 저장 ✨"):
    st.session_state.records.append({"날짜": date, "시작": str(start_time), "종료": str(end_time), "분": duration})
    st.success("연습 기록이 저장되었어요! 🐥")

if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.dataframe(df)
    st.line_chart(df.groupby("날짜")["분"].sum())
    st.download_button("CSV 다운로드 📂", df.to_csv(index=False), file_name="dance_records.csv")
