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
        "초급": [
            ("Bounce", ["무릎을 굽히며 리듬 타기", "어깨로 상체 리듬"]),
            ("Step Touch", ["옆으로 발 내딛기", "반대 손 흔들기"]),
            ("Clap", ["박자에 맞춰 손뼉 치기"]),
            ("Slide", ["발을 옆으로 미끄러지듯 이동"])
        ],
        "중급": [
            ("Body Roll", ["가슴→배→골반 굴리기"]),
            ("Wave", ["손끝→팔꿈치→어깨→가슴→허리"]),
            ("Kick Step", ["앞으로 발차기 후 리듬"]),
            ("Groove", ["상체로 전체적인 리듬 타기"])
        ],
        "고급": [
            ("Knee Drop", ["무릎 굽혀 착지"]),
            ("Harlem Shake", ["어깨·상체를 빠르게 흔들기"]),
            ("Air Walk", ["발이 떠 있는 듯 착시"]),
            ("Freeze Pose", ["박자에 맞춰 순간 정지"])
        ]
    },
    "팝핀": {
        "초급": [
            ("Hit", ["팔·다리에 힘주며 박자"]),
            ("Fresno", ["좌우 이동하며 팝"]),
            ("Toyman", ["로봇 인형처럼 팔 꺾기"])
        ],
        "중급": [
            ("Old Man", ["상체 숙이며 팝"]),
            ("Neck-o-flex", ["목을 기계적으로 꺾기"]),
            ("Twist-o-flex", ["상체를 나누어 꺾으며 이동"])
        ],
        "고급": [
            ("Boogaloo Roll", ["몸 전체 웨이브"]),
            ("Gliding", ["발을 미끄러지듯 이동"]),
            ("Animation Walk", ["만화처럼 부드럽게 걷기"])
        ]
    },
    "하우스": {
        "초급": [
            ("Jack", ["상체 업다운"]),
            ("Loose Leg", ["발을 튕기며 이동"]),
            ("Pas de bourrée", ["기본 발 교차 스텝"])
        ],
        "중급": [
            ("Shuffle", ["발 비비며 빠르게 이동"]),
            ("Cross Step", ["발 교차"]),
            ("Skate", ["스케이트 타듯 미끄러지기"])
        ],
        "고급": [
            ("Stomp", ["강한 박자 찍기"]),
            ("Heel Toe", ["발끝·뒤꿈치 교차"]),
            ("Floor Jack", ["바닥에 가까이 웨이브"])
        ]
    },
    "걸스힙합": {
        "초급": [
            ("Hip Swing", ["골반 좌우 리듬"]),
            ("Hair Flip", ["머리를 크게 돌리기"]),
            ("Hand Wave", ["손으로 웨이브"])
        ],
        "중급": [
            ("Chest Pump", ["가슴 앞뒤"]),
            ("Body Roll", ["전신 굴리기"]),
            ("Hip Circle", ["골반을 크게 원 그리기"])
        ],
        "고급": [
            ("Drop", ["빠르게 앉기"]),
            ("Floor Move", ["바닥 동작"]),
            ("Pose Change", ["연속된 포즈 전환"])
        ]
    },
    "K-Pop": {
        "초급": [
            ("Finger Point", ["손가락 포인트"]),
            ("Side Step", ["좌우 스텝"]),
            ("Clap Wave", ["손뼉 치며 웨이브"])
        ],
        "중급": [
            ("Shoulder Dance", ["어깨 리듬"]),
            ("Hip Roll", ["골반 돌리기"]),
            ("Spin & Point", ["회전 후 포즈"])
        ],
        "고급": [
            ("Floor Wave", ["바닥 웨이브"]),
            ("Jump & Pose", ["점프 후 포즈"]),
            ("Freeze Kick", ["발차기 후 정지"])
        ]
    }
}

# --- 추천곡 (장르별, 유튜브 링크) ---
song_recommendations = {
    "힙합": [
        ("Jay Park - All I Wanna Do", "https://youtu.be/w0PtbE8K6FQ"),
        ("Zico - Artist", "https://youtu.be/UuV2BmJ1p_I"),
        ("Epik High - Fly", "https://youtu.be/lS9VnS6tJqE"),
        ("Dynamic Duo - Ring My Bell", "https://youtu.be/vOhtFtzLGuQ"),
        ("Dok2 - On My Way", "https://youtu.be/tvUAVSUZKjE"),
        ("Crush - Oasis", "https://youtu.be/14iHRRa3F-c")
    ],
    "팝핀": [
        ("Michael Jackson - Billie Jean", "https://youtu.be/Zi_XLOBDo_Y"),
        ("Turbo - Love Is", "https://youtu.be/zB2C7tgpN6E"),
        ("Chris Brown - Fine China", "https://youtu.be/iGsV9gTXgXo"),
        ("Usher - Yeah!", "https://youtu.be/GxBSyx85Kp8")
    ],
    "하우스": [
        ("Robin S - Show Me Love", "https://youtu.be/PSYxT9GM0fQ"),
        ("Crystal Waters - Gypsy Woman", "https://youtu.be/MK6TXMsvgQg"),
        ("Disclosure - Latch", "https://youtu.be/93ASUImTedo"),
        ("Avicii - Levels", "https://youtu.be/_ovdm2yX4MA")
    ],
    "걸스힙합": [
        ("Beyoncé - Run The World", "https://youtu.be/VBmMU_iwe6U"),
        ("Ariana Grande - 7 rings", "https://youtu.be/QYh6mYIJG2Y"),
        ("BLACKPINK - How You Like That", "https://youtu.be/ioNng23DkIM"),
        ("Jessie J - Bang Bang", "https://youtu.be/0HDdjwpPM3Y")
    ],
    "K-Pop": [
        ("BTS - Dynamite", "https://youtu.be/gdZLi9oWNZg"),
        ("NewJeans - Super Shy", "https://youtu.be/ArmDp-zijuc"),
        ("SEVENTEEN - HOT", "https://youtu.be/gRnuFC4Ualw"),
        ("IVE - I AM", "https://youtu.be/6ZUIwj3FgUY"),
        ("LE SSERAFIM - ANTIFRAGILE", "https://youtu.be/pyf8cbqyfPs"),
        ("TWICE - Feel Special", "https://youtu.be/3ymwOvzhwHs")
    ]
}

# --- 랜덤 안무 생성기 ---
st.header("🌸 랜덤 안무 생성기 🦋")
genre = st.selectbox("장르를 선택하세요 🎵", list(dance_basics.keys()))
level = st.radio("난이도를 선택하세요", list(dance_basics[genre].keys()))

if st.button("✨ 안무 아이디어 생성하기"):
    moves = dance_basics[genre][level]
    routine_length = random.randint(5, 7)  # 더 많은 아이디어!
    routine = random.sample(moves, k=min(routine_length, len(moves)))
    
    cute_emojis = ["🌸", "🐰", "🦋", "🌙", "⭐", "💎", "🍀", "🔥", "🪽", "🪐", "🌈", "💫"]
    formatted = []
    for i, (move, steps) in enumerate(routine, 1):
        emoji = random.choice(cute_emojis)
        step_text = "\n      - " + "\n      - ".join(steps)
        formatted.append(f"{i}. {move} {emoji}{step_text}")
    
    st.session_state["current_routine"] = "\n".join(formatted)

if "current_routine" in st.session_state:
    st.success(f"오늘의 안무 아이디어 ({genre} - {level}) 🌟")
    st.markdown(st.session_state["current_routine"])

    # --- 오늘의 추천곡 (사용자가 직접 선택) ---
    st.subheader("🎶 오늘의 추천 곡 선택")
    options = [f"{title} 🔗 [유튜브]({link})" for title, link in song_recommendations[genre]]
    selected = st.multiselect("원하는 곡을 선택하세요 🎵", options)
    st.session_state["selected_songs"] = selected

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
        "songs": st.session_state.get("selected_songs", [])
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
