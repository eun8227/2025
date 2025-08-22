import streamlit as st
import random
import pandas as pd
from datetime import datetime, date

# =========================
# App Setup
# =========================
st.set_page_config(page_title="댄스 연습 앱", page_icon="💃", layout="wide")

# ---------- Cute styling (Gradient BG + Rounded cards) ----------
gradients = [
    "linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%)",
    "linear-gradient(135deg, #FFF1EB 0%, #ACE0F9 100%)",
    "linear-gradient(135deg, #F6D5F7 0%, #FBE9D7 100%)",
    "linear-gradient(135deg, #FAD0C4 0%, #FFD1FF 100%)",
    "linear-gradient(135deg, #D4FC79 0%, #96E6A1 100%)",
]
page_bg = f"""
<style>
.stApp {{
    background: {random.choice(gradients)};
    background-attachment: fixed;
    background-size: cover;
    font-family: "Pretendard", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
}}
.block-container {{
    background-color: rgba(255, 255, 255, 0.88);
    padding: 2rem 2rem 3rem 2rem;
    border-radius: 28px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.12);
}}
/* Titles */
h1, h2, h3 {{
    text-align: center;
    color: #ff4b9f;
    font-weight: 800;
}}
/* Buttons */
.stButton>button {{
    background: linear-gradient(90deg, #ff8c94, #ffaaa5, #ffd3b6);
    color: white;
    font-size: 18px;
    border-radius: 16px;
    padding: 0.6rem 1.4rem;
    border: 0;
    box-shadow: 2px 6px 14px rgba(0,0,0,0.18);
}}
.stButton>button:hover {{
    background: linear-gradient(90deg, #a8edea, #fed6e3);
    color: #222;
}}
/* Selects / Radios */
.stRadio>div>label, .stSelectbox>div>div>div, .stDateInput>div>div>input {{
    font-size: 15px;
}}
/* Dataframe */
.css-1xarl3l, .css-1y4p8pa {{
    border-radius: 16px !important;
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# =========================
# Emoji Packs
# =========================
cute = ["🐰","🐥","🐻","🐶","🐱","🍭","🍓","🍒","🌸","🌈","💖","🎀","✨","🎶","🎉","🫧","🧁","🍬"]
genre_emoji = {
    "힙합": "🎤",
    "팝핀": "🤖",
    "락킹": "🕺",
    "걸리시": "🌸",
    "하우스": "🏠",
}
level_emoji = {"초급": "🌱", "중급": "⚡", "고급": "🔥"}

st.title("💃✨ 댄스 연습 기록 & 랜덤 안무 아이디어 🕺🎶")
st.markdown("<div style='text-align:center;font-size:18px'>🌈 귀엽고 화려한 분위기에서 신나게 연습해요! " + random.choice(cute) + "</div>", unsafe_allow_html=True)

# =========================
# Session State
# =========================
if "records" not in st.session_state:
    st.session_state.records = []
if "current_routine" not in st.session_state:
    st.session_state.current_routine = None
if "selected_song" not in st.session_state:
    st.session_state.selected_song = None

# =========================
# Data: Basics & Songs
# =========================
dance_basics = {
    "힙합": {
        "초급": ["Bounce", "Step Touch", "Slide", "Clap", "Side Step"],
        "중급": ["Body Roll", "Wave", "Isolations", "Spin", "Kick Ball Change"],
        "고급": ["Knee Drop", "Harlem Shake", "Reverse Wave", "Footwork Mix", "Groove Switch"]
    },
    "팝핀": {
        "초급": ["Hit", "Fresno", "Arm Wave", "Robot", "Angle"] ,
        "중급": ["Dime Stop", "Robot Walk", "Isolation Groove", "Ticking", "Glide"],
        "고급": ["Boogaloo Roll", "Neck-o-flex", "Twist-o-flex", "Old Man", "Bracket"]
    },
    "락킹": {
        "초급": ["Point", "Wrist Roll", "Lock", "Basic Bounce", "Scoot"],
        "중급": ["Scoobot", "Stop-and-Go", "Up Lock", "Pacing", "Hitch Hike"],
        "고급": ["Funky Chicken", "Throwback", "Jazz Split", "Lock Drop", "Kick Walk"]
    },
    "걸리시": {
        "초급": ["Step Tap", "Shoulder Bounce", "Hip Roll", "Hair Touch", "Pose"],
        "중급": ["Hair Whip", "Body Wave", "Chest Isolation", "Walk Walk", "Snap Turn"],
        "고급": ["Floor Work", "Drop Spin", "Back Arch", "Body Line", "Cat Walk"]
    },
    "하우스": {
        "초급": ["Two Step", "Side Walk", "Heel Toe", "Pas de bourrée", "Loose Leg"],
        "중급": ["Shuffle", "Stomp", "Jack", "Skate", "Farmer"],
        "고급": ["Lofting", "Floor Spin", "Heel Jack", "Crossover", "Salsa Step"]
    }
}

song_recommendations = {
    "힙합": [
        "Jay Park - All I Wanna Do",
        "Zico - Artist",
        "Epik High - Fly",
        "Dynamic Duo - Ring My Bell",
        "Dok2 - On My Way",
        "BE'O - Counting Stars",
        "BIGBANG - BANG BANG BANG"
    ],
    "팝핀": [
        "Michael Jackson - Billie Jean",
        "Usher - Yeah!",
        "Bruno Mars - Treasure",
        "Chris Brown - Fine China",
        "Janet Jackson - Rhythm Nation"
    ],
    "락킹": [
        "James Brown - Get Up Offa That Thing",
        "Bruno Mars - 24K Magic",
        "Earth, Wind & Fire - September",
        "Bee Gees - Stayin' Alive",
        "Kool & The Gang - Celebration"
    ],
    "걸리시": [
        "BLACKPINK - How You Like That",
        "Sunmi - Gashina",
        "Chungha - Gotta Go",
        "TWICE - Fancy",
        "IVE - Love Dive",
        "LE SSERAFIM - Antifragile"
    ],
    "하우스": [
        "Disclosure - Latch",
        "Robin S - Show Me Love",
        "Calvin Harris - How Deep Is Your Love",
        "David Guetta - Titanium",
        "Swedish House Mafia - Don’t You Worry Child"
    ]
}

# =========================
# Sidebar Controls (advanced routine options)
# =========================
st.sidebar.header("⚙️ 안무 생성 옵션")
min_len = st.sidebar.slider("최소 동작 수", 3, 6, 3)
max_len = st.sidebar.slider("최대 동작 수", 4, 10, 6)
if max_len < min_len:
    max_len = min_len
use_sections = st.sidebar.checkbox("인트로/메인/아웃트로 구분", True)
allow_repeat = st.sidebar.checkbox("일부 동작 반복(x2) 허용", True)
add_details = st.sidebar.checkbox("방향/레벨/리듬 디테일 추가", True)

# Utility for details
directions = ["R", "L", "R→L", "L→R"]
levels = ["상체", "하체", "풀바디", "레벨다운", "레벨업"]
rhythms = ["x4", "x8", "1 Bar", "2 Bars", "& Count"]
transitions = ["Walk", "Turn", "Slide", "Groove", "Pose"]

# =========================
# Routine Generator
# =========================
def decorate_move(move: str) -> str:
    if not add_details:
        return move
    tags = []
    if random.random() < 0.7:
        tags.append(random.choice(directions))
    if random.random() < 0.6:
        tags.append(random.choice(levels))
    if random.random() < 0.7:
        tags.append(random.choice(rhythms))
    if tags:
        return f"{move} ({', '.join(tags)})"
    return move


def generate_sequence(pool: list, length: int) -> list:
    seq = [decorate_move(m) for m in random.choices(pool, k=length)]
    if allow_repeat and length >= 4 and random.random() > 0.5:
        i = random.randrange(0, len(seq))
        seq.insert(i+1, seq[i] + " x2")
    # occasional transition insert
    if random.random() > 0.6:
        j = random.randrange(1, len(seq))
        seq.insert(j, "→ Transition: " + random.choice(transitions))
    return seq


def generate_routine(genre: str, level: str) -> str:
    pool = dance_basics[genre][level]
    total_len = random.randint(min_len, max_len)

    if not use_sections:
        seq = generate_sequence(pool, total_len)
        return "\n".join([f"{idx+1}. {m} ✨" for idx, m in enumerate(seq)])

    # Sectioned routine
    intro_len = max(1, total_len // 4)
    outro_len = max(1, total_len // 5)
    main_len = max(1, total_len - intro_len - outro_len)

    intro = generate_sequence(pool, intro_len)
    main = generate_sequence(pool, main_len)
    outro = generate_sequence(pool, outro_len)

    parts = [
        f"**인트로 {random.choice(cute)}**\n" + "\n".join([f"• {m}" for m in intro]),
        f"\n**메인 {random.choice(cute)}**\n" + "\n".join([f"• {m}" for m in main]),
        f"\n**아웃트로 {random.choice(cute)}**\n" + "\n".join([f"• {m}" for m in outro])
    ]
    return "\n".join(parts)

# =========================
# UI: Routine + Recommendations
# =========================
st.header("✨ 랜덤 기본기 안무 생성기 " + random.choice(cute))
col1, col2, col3 = st.columns([1.2,1,1])
with col1:
    genre = st.selectbox("🎶 장르 선택", list(dance_basics.keys()))
with col2:
    level = st.radio("난이도", ["초급","중급","고급"], horizontal=True)
with col3:
    st.markdown("<div style='text-align:center;font-size:32px'>" + genre_emoji.get(genre, "🎵") + " " + level_emoji[level] + "</div>", unsafe_allow_html=True)

if st.button("💡 안무 생성하기"):
    st.session_state.current_routine = generate_routine(genre, level)

if st.session_state.current_routine:
    st.subheader("오늘의 안무 아이디어 " + random.choice(cute))
    st.markdown(st.session_state.current_routine)

    # Song selection + random pick
    st.subheader("🎶 추천 곡 선택 " + random.choice(cute))
    song_choice = st.selectbox("마음에 드는 곡을 골라요", song_recommendations[genre])
    st.session_state.selected_song = song_choice

    rand_song = random.choice(song_recommendations[genre])
    st.info(f"오늘의 랜덤 추천곡: **{rand_song}** {random.choice(cute)}")

    # Mood emojis
    mood = " ".join(random.sample(cute, 3))
    st.success(f"오늘의 댄스 무드: {mood}")

# =========================
# Practice Logging
# =========================
st.header("📒 연습 기록하기 " + random.choice(cute))
colA, colB, colC = st.columns([1,1,2])
with colA:
    d = st.date_input("📅 연습 날짜", value=date.today())
with colB:
    minutes = st.number_input("⏱ 연습 시간(분)", min_value=5, max_value=300, step=5, value=30)
with colC:
    note = st.text_input("📝 메모 (선택)", placeholder="느낌/포인트/이슈 등")

if st.button("✅ 연습 기록 저장"):
    st.session_state.records.append({
        "date": pd.to_datetime(d),
        "minutes": int(minutes),
        "genre": genre,
        "level": level,
        "routine": st.session_state.current_routine or "(생성 안 됨)",
        "song": st.session_state.selected_song or "(선택 안 함)",
        "note": note
    })
    st.success("🎉 기록이 저장되었습니다! 멋진 연습이었어요 ✨")

# =========================
# Records + Charts + Download
# =========================
st.header("📊 나의 연습 기록 " + random.choice(cute))
if len(st.session_state.records) > 0:
    df = pd.DataFrame(st.session_state.records)
    # Sort by date
    df = df.sort_values("date")
    st.dataframe(df, use_container_width=True)

    # Minutes by date chart (sum if multiple entries)
    sum_df = df.groupby(df["date"].dt.date)["minutes"].sum().reset_index()
    sum_df.rename(columns={"date": "Date", "minutes": "Minutes"}, inplace=True)
    sum_df = sum_df.set_index("Date")
    st.line_chart(sum_df["Minutes"])

    # CSV download
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="💾 CSV로 다운로드",
        data=csv,
        file_name="dance_practice_records.csv",
        mime="text/csv",
    )
else:
    st.info("아직 연습 기록이 없습니다. 안무를 생성하고 첫 기록을 남겨보세요! " + random.choice(cute))
