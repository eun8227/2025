import streamlit as st
import random
import pandas as pd
from datetime import datetime, time

st.set_page_config(page_title="댄스 연습 앱", page_icon="💃", layout="wide")

# ---- 스타일 (오로라 배경 + 무지개빛 반짝이는 효과) ----
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
        position: relative;
        overflow: hidden;
        color: white;
    }

    @keyframes sparkle {
        0% { opacity: 0; transform: scale(0.5) translateY(0); }
        50% { opacity: 1; transform: scale(1.2) translateY(-30px); }
        100% { opacity: 0; transform: scale(0.5) translateY(0); }
    }

    .sparkle {
        position: absolute;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        animation: sparkle 3s infinite;
    }
    </style>
    <script>
    function createSparkles(){
        const colors = ["#ff99cc", "#ffcc99", "#ffff99", "#ccff99", "#99ccff", "#cc99ff"];
        for(let i=0; i<100; i++){
            let s = document.createElement("div");
            s.className = "sparkle";
            s.style.top = Math.random()*100+"%";
            s.style.left = Math.random()*100+"%";
            s.style.background = colors[Math.floor(Math.random()*colors.length)];
            s.style.animationDelay = (Math.random()*5)+"s";
            s.style.opacity = 0;
            document.body.appendChild(s);
        }
    }
    createSparkles();
    </script>
    """,
    unsafe_allow_html=True
)

st.title("🌌✨ 댄스 연습 기록 & 랜덤 안무 아이디어 ✨🌌")

# ---- 데이터 초기화 ----
if "records" not in st.session_state:
    st.session_state["records"] = []

# ---- 장르별 기본기 (설명 포함) ----
dance_basics = {
    "힙합": {
        "초급": [("Bounce", "무릎을 리드미컬하게 굽혔다 펴며 상체와 함께 반동 주기"),
                ("Step Touch", "옆으로 발을 뻗고 다시 제자리로 가져오기"),
                ("Slide", "발을 바닥에 밀듯이 옆으로 이동하기")],
        "중급": [("Body Roll", "상체를 위에서 아래로 굴리듯 움직이기"),
                ("Wave", "팔과 몸통을 물결처럼 연결해서 흐르게 하기"),
                ("Isolations", "몸의 특정 부위만 따로 움직이는 연습")],
        "고급": [("Knee Drop", "무릎을 빠르게 바닥에 꿇으며 흐름을 유지하기"),
                ("Harlem Shake", "어깨와 몸통을 흔들어 리듬 강조하기"),
                ("Reverse Wave", "Wave를 반대 방향으로 부드럽게 이어가기")]
    }
}

# ---- 곡 추천 (유튜브 링크 포함) ----
song_recommendations = {
    "힙합": [
        ("Jay Park - All I Wanna Do", "https://youtu.be/w0PtbE8K6FQ"),
        ("Zico - Artist", "https://youtu.be/UuV2BmJ1p_I"),
        ("Epik High - Fly", "https://youtu.be/lS9VnS6tJqE"),
        ("Dynamic Duo - AEAO", "https://youtu.be/j3YcW1n4i7s"),
        ("Crush - Oasis", "https://youtu.be/cpE6oC2FZ94")
    ]
}

# ---- 랜덤 안무 생성 함수 ----
def generate_routine(genre, level):
    moves = dance_basics[genre][level]
    routine_length = random.randint(3, 5)
    routine = random.choices(moves, k=routine_length)

    formatted = []
    cute_emojis = ["🌸", "🐥", "🐰", "🎀", "🍓", "💫"]
    for i, (move, desc) in enumerate(routine, 1):
        emoji = random.choice(cute_emojis)
        formatted.append(f"{i}. {move} {emoji} → {desc}")
    return "\n".join(formatted)

# ---- 오늘의 곡 추천 (날짜에 따라 자동 변경) ----
def get_daily_song(genre):
    today = datetime.today().date()
    idx = today.toordinal() % len(song_recommendations[genre])
    return song_recommendations[genre][idx]

# ---- 안무 랜덤 생성 ----
st.header("🌈 랜덤 기본기 안무 생성기 🐰")
genre = st.selectbox("🎵 장르 선택", list(dance_basics.keys()))
level = st.radio("🔥 난이도 선택", ["초급", "중급", "고급"])

if st.button("💡 안무 생성하기"):
    routine = generate_routine(genre, level)
    st.session_state["current_routine"] = routine

# ---- 안무 결과 + 곡 선택 ----
if "current_routine" in st.session_state:
    st.subheader("오늘의 안무 아이디어 🎀✨")
    st.markdown(st.session_state["current_routine"])

    st.subheader("🎶 오늘의 추천 곡")
    daily_song = get_daily_song(genre)
    st.markdown(f"{daily_song[0]} 🎵 [듣기]({daily_song[1]})")
    st.session_state["selected_song"] = daily_song[0]

# ---- 연습 기록 ----
st.header("📒 연습 기록하기 🐥")
date = st.date_input("📅 연습 날짜", datetime.today())
start_time = st.time_input("⏰ 시작 시간", value=time(18, 0))
end_time = st.time_input("🏁 종료 시간", value=time(19, 0))
minutes = (datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds // 60

if st.button("✅ 연습 기록 저장 🎀"):
    st.session_state["records"].append({
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "minutes": minutes,
        "routine": st.session_state.get("current_routine", "없음"),
        "genre": genre,
        "level": level,
        "song": st.session_state.get("selected_song", "선택 안 함")
    })
    st.success("✨ 연습 기록이 저장되었습니다! 🌸")

# ---- 기록 보기 ----
st.header("📊 나의 연습 기록 🐰")
if len(st.session_state["records"]) > 0:
    df = pd.DataFrame(st.session_state["records"])
    st.dataframe(df)
    st.line_chart(df.set_index("date")["minutes"])
else:
    st.info("아직 연습 기록이 없습니다. 먼저 기록을 남겨보세요! 🐥")
