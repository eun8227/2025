import streamlit as st
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="댄스 연습 앱", page_icon="💃", layout="wide")

# ---- 스타일 (오로라 배경 적용) ----
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 30%, #fbc2eb 60%, #a6c1ee 100%);
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💃 댄스 연습 기록 & 랜덤 안무 아이디어 🕺")

# ---- 데이터 초기화 ----
if "records" not in st.session_state:
    st.session_state["records"] = []

# ---- 장르별 기본기 + 유튜브 링크 ----
dance_basics = {
    "힙합": {
        "초급": [("Bounce", "https://youtu.be/9tKXPCZ0DJ8"), ("Step Touch", "https://youtu.be/mkcoXZ2J1uA"), ("Slide", "https://youtu.be/lRZL8u6L1xA")],
        "중급": [("Body Roll", "https://youtu.be/4ZPZkG7FZVE"), ("Wave", "https://youtu.be/f3OjN6B3sK0"), ("Isolations", "https://youtu.be/FpYHzqxeV5U")],
        "고급": [("Knee Drop", "https://youtu.be/2VVV4BWDVYg"), ("Harlem Shake", "https://youtu.be/8vJiSSAMNWw"), ("Reverse Wave", "https://youtu.be/DFPjXGbgZQ4")]
    },
    "팝핀": {
        "초급": [("Hit", "https://youtu.be/qb0w7sGzA5o"), ("Fresno", "https://youtu.be/nZn97VYjByM"), ("Arm Wave", "https://youtu.be/F3xG3dYgWn0")],
        "중급": [("Dime Stop", "https://youtu.be/2xVdQpTzGH4"), ("Robot Walk", "https://youtu.be/3oHdkG49Fh0"), ("Isolation Groove", "https://youtu.be/q3TSo-YwP5c")],
        "고급": [("Boogaloo Roll", "https://youtu.be/NNp0DQruM8Y"), ("Neck-o-flex", "https://youtu.be/gfQXb6H2v40"), ("Twist-o-flex", "https://youtu.be/3HRRkAkS-UE")]
    },
    "락킹": {
        "초급": [("Point", "https://youtu.be/H2mM9MMW4rY"), ("Wrist Roll", "https://youtu.be/mBx5CSQ87OE"), ("Lock", "https://youtu.be/EGxBPZ7hpNc")],
        "중급": [("Scoobot", "https://youtu.be/0qVddrzNRXk"), ("Stop-and-Go", "https://youtu.be/lSBo8J5x7Tk"), ("Up Lock", "https://youtu.be/nRYDdcsO7o0")],
        "고급": [("Funky Chicken", "https://youtu.be/cI-wd1X3X24"), ("Throwback", "https://youtu.be/2nC6t0oEWjY"), ("Jazz Split", "https://youtu.be/1xYClGdKqkg")]
    },
    "걸리시": {
        "초급": [("Step Tap", "https://youtu.be/k9mxbStkPgk"), ("Shoulder Bounce", "https://youtu.be/10FoGLwRoT8"), ("Hip Roll", "https://youtu.be/BZp1HczGQAU")],
        "중급": [("Hair Whip", "https://youtu.be/KMM9lWQHgCA"), ("Body Wave", "https://youtu.be/f3OjN6B3sK0"), ("Chest Isolation", "https://youtu.be/FpYHzqxeV5U")],
        "고급": [("Floor Work", "https://youtu.be/USlXq94E2Lc"), ("Drop Spin", "https://youtu.be/16OK7vhYrkU"), ("Back Arch", "https://youtu.be/-j4Y5xJYP5I")]
    },
    "하우스": {
        "초급": [("Two Step", "https://youtu.be/4y5m5wEJaqY"), ("Side Walk", "https://youtu.be/uX2qM1cQ03k"), ("Heel Toe", "https://youtu.be/E0lH6lSvZcE")],
        "중급": [("Shuffle", "https://youtu.be/6U2Ok6q6slo"), ("Stomp", "https://youtu.be/TgEz9fNty9Y"), ("Jack", "https://youtu.be/4oJc1K25CZM")],
        "고급": [("Lofting", "https://youtu.be/y6xBeqWsS1c"), ("Floor Spin", "https://youtu.be/5I9Pzfq5lHk"), ("Heel Jack", "https://youtu.be/b3slI1XCYJ4")]
    }
}

# ---- 곡 추천 (유튜브 링크 포함) ----
song_recommendations = {
    "힙합": [
        ("Jay Park - All I Wanna Do", "https://youtu.be/kfQJNe8J2nw"),
        ("Zico - Artist", "https://youtu.be/UuV2BmJ1p_I"),
        ("Epik High - Fly", "https://youtu.be/8JpqFIdL5wM"),
        ("Dynamic Duo - Ring My Bell", "https://youtu.be/Z1-1pQFqad8"),
        ("Dok2 - On My Way", "https://youtu.be/BZp1HczGQAU")
    ],
    "팝핀": [
        ("Michael Jackson - Billie Jean", "https://youtu.be/Zi_XLOBDo_Y"),
        ("Usher - Yeah!", "https://youtu.be/GxBSyx85Kp8"),
        ("Bruno Mars - Treasure", "https://youtu.be/nPvuNsRccVw"),
        ("Chris Brown - Fine China", "https://youtu.be/iGs1gODLiSQ"),
        ("Janet Jackson - Rhythm Nation", "https://youtu.be/n54bEMc0lDU")
    ],
    "락킹": [
        ("James Brown - Get Up Offa That Thing", "https://youtu.be/Qbqgx2ZpR2U"),
        ("Bruno Mars - 24K Magic", "https://youtu.be/UqyT8IEBkvY"),
        ("Earth, Wind & Fire - September", "https://youtu.be/Gs069dndIYk"),
        ("Bee Gees - Stayin' Alive", "https://youtu.be/I_izvAbhExY"),
        ("Kool & The Gang - Celebration", "https://youtu.be/3GwjfUFyY6M")
    ],
    "걸리시": [
        ("BLACKPINK - How You Like That", "https://youtu.be/ioNng23DkIM"),
        ("Sunmi - Gashina", "https://youtu.be/OrHKZ3bY9J0"),
        ("Chungha - Gotta Go", "https://youtu.be/N4IhWJ8r7_0"),
        ("TWICE - Fancy", "https://youtu.be/kOHB85vDuow"),
        ("IVE - Love Dive", "https://youtu.be/Y8JFxS1HlDo")
    ],
    "하우스": [
        ("Disclosure - Latch", "https://youtu.be/93ASUImTedo"),
        ("Robin S - Show Me Love", "https://youtu.be/PXkQnSpgCj0"),
        ("Calvin Harris - How Deep Is Your Love", "https://youtu.be/7F37r50VUTQ"),
        ("David Guetta - Titanium", "https://youtu.be/JRfuAukYTKg"),
        ("Swedish House Mafia - Don’t You Worry Child", "https://youtu.be/1y6smkh6c-0")
    ]
}

# ---- 랜덤 안무 생성 함수 ----
def generate_routine(genre, level):
    moves = dance_basics[genre][level]
    routine_length = random.randint(3, 6)
    routine = random.choices(moves, k=routine_length)

    formatted = []
    for i, (move, link) in enumerate(routine, 1):
        formatted.append(f"{i}. {move} ✨ [예시 영상]({link})")
    return "\n".join(formatted)

# ---- 안무 랜덤 생성 ----
st.header("✨ 랜덤 기본기 안무 생성기 🎶")
genre = st.selectbox("🎵 장르 선택", list(dance_basics.keys()))
level = st.radio("🔥 난이도 선택", ["초급", "중급", "고급"])

if st.button("💡 안무 생성하기"):
    routine = generate_routine(genre, level)
    st.session_state["current_routine"] = routine

# ---- 안무 결과 + 곡 선택 ----
if "current_routine" in st.session_state:
    st.subheader("오늘의 안무 아이디어 💃🕺")
    st.markdown(st.session_state["current_routine"])

    st.subheader("🎶 추천 곡 선택")
    song_choice = st.selectbox(
        "마음에 드는 곡을 선택하세요",
        [f"{title} 🎵 [듣기]({link})" for title, link in song_recommendations[genre]]
    )
    st.session_state["selected_song"] = song_choice

    random_song = random.choice(song_recommendations[genre])
    st.info(f"오늘의 랜덤 추천곡 🎵: **{random_song[0]}** [듣기]({random_song[1]})")

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
