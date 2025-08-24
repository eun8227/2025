import streamlit as st
import pandas as pd
import random
from datetime import datetime, time

st.set_page_config(page_title="댄스 연습 앱", page_icon="💃", layout="wide")

# --- 🌌 오로라 배경 ---
page_bg = """
<style>
.stApp {
    background: linear-gradient(120deg, #1e3c72, #2a5298, #6dd5ed, #00c6ff, #ff758c, #ff7eb3);
    background-size: 600% 600%;
    animation: aurora 20s ease infinite;
}
@keyframes aurora {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
</style>
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
        "초급": [("Bounce", ["무릎 굽히며 박자 타기", "어깨 리듬"]), ("Step Touch", ["옆으로 발 내딛기", "손 반대방향 흔들기"])],
        "중급": [("Body Roll", ["가슴→배→골반 굴리기"]), ("Wave", ["손끝→팔꿈치→어깨→가슴→허리 이어가기"])],
        "고급": [("Knee Drop", ["무릎 굽히며 착지", "리듬 유지"]), ("Harlem Shake", ["어깨와 상체를 빠르게 흔들기"])]
    },
    "팝핀": {
        "초급": [("Hit", ["팔·다리 힘주며 박자"]), ("Fresno", ["좌우 이동하며 팝"])],
        "중급": [("Old Man", ["상체 숙이며 팝"]), ("Neck-o-flex", ["목을 기계적으로 꺾기"])],
        "고급": [("Boogaloo Roll", ["몸 전체 웨이브"]), ("Gliding", ["발을 미끄러지듯 이동"])]
    },
    "하우스": {
        "초급": [("Jack", ["상체를 업다운"]), ("Loose Leg", ["발 가볍게 튕기며 이동"])],
        "중급": [("Shuffle", ["발을 빠르게 비비며 이동"]), ("Cross Step", ["발 교차 스텝"])],
        "고급": [("Stomp", ["강한 박자 찍기"]), ("Heel Toe", ["발끝과 발뒤꿈치 교차 이동"])]
    },
    "걸스힙합": {
        "초급": [("Hip Swing", ["골반 좌우 리듬"]), ("Hair Flip", ["머리를 크게 돌리기"])],
        "중급": [("Chest Pump", ["가슴을 앞뒤로"]), ("Body Roll", ["전신 굴리기"])],
        "고급": [("Drop", ["빠르게 무릎 굽혀 앉기"]), ("Floor Move", ["바닥 동작"])],
    },
    "K-Pop": {
        "초급": [("Finger Point", ["손가락으로 포인트"]), ("Side Step", ["좌우 기본 스텝"])],
        "중급": [("Shoulder Dance", ["어깨 리듬"]), ("Hip Roll", ["골반 돌리기"])],
        "고급": [("Floor Wave", ["바닥 웨이브"]), ("Jump & Pose", ["점프 후 포즈"])]
    }
}

# --- 추천곡 (장르별, 유튜브 링크 포함) ---
song_recommendations = {
    "힙합": [
        ("Jay Park - All I Wanna Do", "https://youtu.be/w0PtbE8K6FQ"),
        ("Zico - Artist", "https://youtu.be/UuV2BmJ1p_I"),
        ("Epik High - Fly", "https://youtu.be/lS9VnS6tJqE"),
        ("Dynamic Duo - Ring My Bell", "https://youtu.be/vOhtFtzLGuQ"),
    ],
    "팝핀": [
        ("Michael Jackson - Billie Jean", "https://youtu.be/Zi_XLOBDo_Y"),
        ("Turbo - Love Is", "https://youtu.be/zB2C7tgpN6E"),
        ("Chris Brown - Fine China", "https://youtu.be/iGsV9gTXgXo"),
    ],
    "하우스": [
        ("Robin S - Show Me Love", "https://youtu.be/PSYxT9GM0fQ"),
        ("Crystal Waters - Gypsy Woman", "https://youtu.be/MK6TXMsvgQg"),
        ("Disclosure - Latch", "https://youtu.be/93ASUImTedo"),
    ],
    "걸스힙합": [
        ("Beyoncé - Run The World", "https://youtu.be/VBmMU_iwe6U"),
        ("Ariana Grande - 7 rings", "https://youtu.be/QYh6mYIJG2Y"),
        ("BLACKPINK - How You Like That", "https://youtu.be/ioNng23DkIM"),
    ],
    "K-Pop": [
        ("BTS - Dynamite", "https://youtu.be/gdZLi9oWNZg"),
        ("NewJeans - Super Shy", "https://youtu.be/ArmDp-zijuc"),
        ("SEVENTEEN - HOT", "https://youtu.be/gRnuFC4Ualw"),
        ("IVE - I AM", "https://youtu.be/6ZUIwj3FgUY"),
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

    # --- 오늘의 추천곡 (매일 자동 변경) ---
    st.subheader("🎶 오늘의 추천 곡")
    today = datetime.today().date()
    random.seed(str(today) + genre)  # 오늘 날짜 + 장르 기반 시드
    
    songs_today = random.sample(song_recommendations[genre], 
                                min(2, len(song_recommendations[genre])))  # 오늘 2곡 랜덤
    
    for title, link in songs_today:
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
        "level": level
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
