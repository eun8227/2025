import streamlit as st
import random
import pandas as pd
from datetime import datetime, time

st.set_page_config(page_title="댄스 연습 앱", page_icon="💃", layout="wide")

# ---- 스타일 (오로라 배경 적용) ----
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 30%, #fad0c4 30%, #fbc2eb 60%, #a6c1ee 100%);
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

# ---- 장르별 기본기 (예시 영상 포함) ----
dance_basics = {
    "힙합": {
        "초급": [("Bounce", "https://youtu.be/9QxkYwWqU0Y"), ("Step Touch", "https://youtu.be/xvFZjo5PgG0"), ("Slide", "https://youtu.be/Y3w5Lvy9kuw")],
        "중급": [("Body Roll", "https://youtu.be/RbGJkpKYNps"), ("Wave", "https://youtu.be/Y2V2xKQeMxM"), ("Isolations", "https://youtu.be/k1xN5S9h4dI")],
        "고급": [("Knee Drop", "https://youtu.be/N8iP7y0sS6E"), ("Harlem Shake", "https://youtu.be/8vJiSSAMNWw"), ("Reverse Wave", "https://youtu.be/fHdVRC9vGgA")]
    },
    "팝핀": {
        "초급": [("Hit", "https://youtu.be/4CjzA8x8asA"), ("Fresno", "https://youtu.be/JqFL0cDN06I"), ("Arm Wave", "https://youtu.be/6Z7fPjvUMls")],
        "중급": [("Dime Stop", "https://youtu.be/m0-g_Aeibfg"), ("Robot Walk", "https://youtu.be/BdU7Yb6o5fM"), ("Isolation Groove", "https://youtu.be/5j5Y_KcW5E0")],
        "고급": [("Boogaloo Roll", "https://youtu.be/8TnP6vhf-Sc"), ("Neck-o-flex", "https://youtu.be/X2JxCzI8zvM"), ("Twist-o-flex", "https://youtu.be/lMWvHdQWZB8")]
    },
    "락킹": {
        "초급": [("Point", "https://youtu.be/lhR41sz4D5U"), ("Wrist Roll", "https://youtu.be/2ClbAOy3OUM"), ("Lock", "https://youtu.be/lAmUJX6wX6w")],
        "중급": [("Scoobot", "https://youtu.be/Ny7cZ6bM3jQ"), ("Stop-and-Go", "https://youtu.be/-sxbFzNw2KQ"), ("Up Lock", "https://youtu.be/4h0jw3Lw5xM")],
        "고급": [("Funky Chicken", "https://youtu.be/_5O1jR7Jp9M"), ("Throwback", "https://youtu.be/-qGgvN5xk1c"), ("Jazz Split", "https://youtu.be/tyN8W5K4T08")]
    },
    "걸리시": {
        "초급": [("Step Tap", "https://youtu.be/DF4L3cTtJr8"), ("Shoulder Bounce", "https://youtu.be/I9FgJRMU8lw"), ("Hip Roll", "https://youtu.be/fyCgRjz_6ec")],
        "중급": [("Hair Whip", "https://youtu.be/I9wV4E3Cr1A"), ("Body Wave", "https://youtu.be/5F_4g4X7tZQ"), ("Chest Isolation", "https://youtu.be/p0rFvRbYOqc")],
        "고급": [("Floor Work", "https://youtu.be/Kcb1qnQqkZ0"), ("Drop Spin", "https://youtu.be/hl5o9MiF7nU"), ("Back Arch", "https://youtu.be/oUUR8AaADaE")]
    },
    "하우스": {
        "초급": [("Two Step", "https://youtu.be/wnT4yZCzXtk"), ("Side Walk", "https://youtu.be/fJgh9Up9nAE"), ("Heel Toe", "https://youtu.be/J-qFcHfQ5XQ")],
        "중급": [("Shuffle", "https://youtu.be/vuJgE1Z8W9w"), ("Stomp", "https://youtu.be/RqjvXh-SkZg"), ("Jack", "https://youtu.be/gXTS3utpoTg")],
        "고급": [("Lofting", "https://youtu.be/kArf2uQfwJY"), ("Floor Spin", "https://youtu.be/SsKcGZbB3vI"), ("Heel Jack", "https://youtu.be/dtVvUlJY5BM")]
    }
}

# ---- 곡 추천 (유튜브 링크 포함) ----
song_recommendations = {
    "힙합": [
        ("Jay Park - All I Wanna Do", "https://youtu.be/0pU4z4mIU6A"),
        ("Zico - Artist", "https://youtu.be/UuV2BmJ1p_I"),
        ("Epik High - Fly", "https://youtu.be/nCtz4trJrOw"),
        ("Dynamic Duo - Ring My Bell", "https://youtu.be/8xZttJcSkOY"),
        ("Dok2 - On My Way", "https://youtu.be/EgD74mAvR3M")
    ],
    "팝핀": [
        ("Michael Jackson - Billie Jean", "https://youtu.be/Zi_XLOBDo_Y"),
        ("Usher - Yeah!", "https://youtu.be/GxBSyx85Kp8"),
        ("Bruno Mars - Treasure", "https://youtu.be/nPvuNsRccVw"),
        ("Chris Brown - Fine China", "https://youtu.be/iGs1gODLiSQ"),
        ("Janet Jackson - Rhythm Nation", "https://youtu.be/LvdLovAaYzM")
    ],
    "락킹": [
        ("James Brown - Get Up Offa That Thing", "https://youtu.be/Q9sF0QJ8yEY"),
        ("Bruno Mars - 24K Magic", "https://youtu.be/UqyT8IEBkvY"),
        ("Earth, Wind & Fire - September", "https://youtu.be/Gs069dndIYk"),
        ("Bee Gees - Stayin' Alive", "https://youtu.be/I_izvAbhExY"),
        ("Kool & The Gang - Celebration", "https://youtu.be/3GwjfUFyY6M")
    ],
    "걸리시": [
        ("BLACKPINK - How You Like That", "https://youtu.be/ioNng23DkIM"),
        ("Sunmi - Gashina", "https://youtu.be/9G9b8xZ8xHg"),
        ("Chungha - Gotta Go", "https://youtu.be/2NqPJM9t8zE"),
        ("TWICE - Fancy", "https://youtu.be/kOHB85vDuow"),
        ("IVE - Love Dive", "https://youtu.be/Y8JFxS1HlDo")
    ],
    "하우스": [
        ("Disclosure - Latch", "https://youtu.be/93ASUImTedo"),
        ("Robin S - Show Me Love", "https://youtu.be/PWgvGjAhvIw"),
        ("Calvin Harris - How Deep Is Your Love", "https://youtu.be/Yhnl3-rLyr8"),
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
start_time = st.time_input("⏰ 시작 시간", value=time(18, 0))
end_time = st.time_input("⏰ 종료 시간", value=time(19, 0))

minutes = int((datetime.combine(date, end_time) - datetime.combine(date, start_time)).total_seconds() // 60)

if st.button("✅ 연습 기록 저장"):
    st.session_state["records"].append({
        "date": date,
        "start_time": start_time.strftime("%H:%M"),
        "end_time": end_time.strftime("%H:%M"),
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
