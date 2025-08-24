import streamlit as st
import random
import datetime
import pandas as pd

st.set_page_config(page_title="댄스 연습 기록 앱", layout="wide")

# 🌌 오로라 + 별 배경 CSS
page_bg = """
<style>
.stApp {
    background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
    color: white;
}
@keyframes aurora {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.aurora {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0; left: 0;
    background: linear-gradient(270deg, rgba(0,255,255,0.2), rgba(255,0,255,0.2), rgba(0,0,128,0.2));
    background-size: 600% 600%;
    animation: aurora 30s ease infinite;
    z-index: -1;
}
</style>
<div class="aurora"></div>
"""
st.markdown(page_bg, unsafe_allow_html=True)


# 🎵 장르별 추천곡 (곡명, 아티스트, 유튜브 링크)
recommendations = {
    "힙합": [
        ("Sicko Mode", "Travis Scott", "https://www.youtube.com/watch?v=6ONRf7h3Mdk"),
        ("Goosebumps", "Travis Scott", "https://www.youtube.com/watch?v=Dst9gZkq1a8"),
        ("DNA", "방탄소년단", "https://www.youtube.com/watch?v=MBdVXkSdhwU")
    ],
    "팝핀": [
        ("Billie Jean", "Michael Jackson", "https://www.youtube.com/watch?v=Zi_XLOBDo_Y"),
        ("Smooth Criminal", "Michael Jackson", "https://www.youtube.com/watch?v=h_D3VFfhvs4"),
        ("Dance Monkey", "Tones and I", "https://www.youtube.com/watch?v=q0hyYWKXF0Q")
    ],
    "하우스": [
        ("One More Time", "Daft Punk", "https://www.youtube.com/watch?v=FGBhQbmPwH8"),
        ("Turn Back Time", "Diplo & Sonny Fodera", "https://www.youtube.com/watch?v=R9gD7aVCBdg"),
        ("Show Me Love", "Robin S", "https://www.youtube.com/watch?v=Ps2Jc28tQrw")
    ],
    "걸스힙합": [
        ("Partition", "Beyoncé", "https://www.youtube.com/watch?v=pZ12_E5R3qc"),
        ("Savage", "Megan Thee Stallion", "https://www.youtube.com/watch?v=JvQcabZ1zrk"),
        ("Kill This Love", "BLACKPINK", "https://www.youtube.com/watch?v=2S24-y0Ij3Y")
    ],
    "K-Pop": [
        ("Hype Boy", "NewJeans", "https://www.youtube.com/watch?v=11cta61wi0g"),
        ("Sorry Sorry", "Super Junior", "https://www.youtube.com/watch?v=x6QA3m58DQw"),
        ("LOVE DIVE", "IVE", "https://www.youtube.com/watch?v=Y8JFxS1HlDo")
    ]
}

# 🎵 오늘 날짜 기반 추천곡 자동 선택
today = datetime.date.today()
random.seed(today.toordinal())  # 날짜별 고정 시드
daily_recommendations = {genre: random.sample(songs, k=2) for genre, songs in recommendations.items()}


# 💃 장르별 기본기 동작 (확장판)
dance_basics = {
    "힙합": {
        "초급": [
            ("Bounce", ["무릎을 리듬에 맞춰 굽혔다 펴며 상체와 함께 튕기기", "어깨를 위아래로 흔들며 그루브 살리기"]),
            ("Step Touch", ["오른발을 옆으로 내딛고 왼발을 모으며 손을 옆으로 흔들기", "좌우 교대로 반복"]),
        ],
        "중급": [
            ("Body Roll", ["가슴→배→골반 순으로 굴리며 상체를 뒤로 젖혀 마무리"]),
            ("Wave", ["손끝→팔꿈치→어깨→가슴→허리까지 물결처럼 연결"]),
        ],
        "고급": [
            ("Knee Drop", ["한쪽 무릎을 바닥에 닿듯 착지 후 반대 다리로 연결"]),
            ("Freeze Pose", ["박자에 맞춰 순간적으로 멈춰 포즈 유지"]),
        ]
    },
    "팝핀": {
        "초급": [
            ("Hit", ["근육에 순간적으로 힘을 줘서 튕기기", "팔/가슴/다리 동시에 Pop"]),
            ("Arm Wave", ["손끝→팔꿈치→어깨까지 파도처럼 연결"]),
        ],
        "중급": [
            ("Tut", ["팔꿈치와 손목을 직각으로 꺾어 도형 만들기", "마디마다 Pop으로 리듬감 살리기"]),
        ],
        "고급": [
            ("Animation Walk", ["걸음마다 Pop을 넣으며 애니메이션처럼 끊기"]),
        ]
    },
    "하우스": {
        "초급": [
            ("Shuffle Step", ["발을 빠르게 앞으로 미는 듯 이동", "무릎을 굽히며 바운스 유지"]),
        ],
        "중급": [
            ("Jack", ["허리를 중심으로 상체와 골반을 앞뒤로 리듬감 있게"]),
        ],
        "고급": [
            ("Spin Kick", ["회전하며 발을 차올려 착지", "Groove로 연결"]),
        ]
    },
    "걸스힙합": {
        "초급": [
            ("Hip Sway", ["골반을 좌우로 흔들며 리듬 타기", "손은 허리나 머리에 두기"]),
        ],
        "중급": [
            ("Chest Pump", ["가슴을 앞으로 강하게 내밀며 반복", "손과 어깨로 파워 강조"]),
        ],
        "고급": [
            ("Attitude Walk", ["천천히 걸으며 골반과 손동작 강조", "눈빛과 표정 활용"]),
        ]
    },
    "K-Pop": {
        "초급": [
            ("Finger Heart", ["손가락으로 하트 만들며 스텝과 함께 어필"]),
        ],
        "중급": [
            ("Formation Change", ["앞뒤/좌우로 이동하며 포메이션 바꾸기"]),
        ],
        "고급": [
            ("Sync Dance", ["여러 사람이 동시에 완벽히 맞춰 동작 수행"]),
        ]
    }
}


# 📊 연습 기록 저장용 DataFrame
if "records" not in st.session_state:
    st.session_state["records"] = pd.DataFrame(columns=["날짜", "장르", "동작", "연습 시간(시)", "연습 시간(분)", "추천곡"])


st.title("✨ 댄스 연습 기록 앱 ✨")
st.markdown("🐰💃 연습을 기록하고 랜덤 안무 아이디어와 추천곡을 받아보세요!")

# 🎶 장르 선택
genre = st.selectbox("연습할 장르를 선택하세요 🎵", list(dance_basics.keys()))

# 🏷️ 난이도 선택
level = st.radio("난이도를 선택하세요 🌟", ["초급", "중급", "고급"])

# 🎵 추천곡 제시 + 선택
st.subheader("오늘의 추천곡 🎶")
song_choices = daily_recommendations[genre]
song_option = st.selectbox(
    "마음에 드는 곡을 선택하세요:",
    [f"{title} - {artist}" for title, artist, link in song_choices]
)
song_link = [link for title, artist, link in song_choices if f"{title} - {artist}" == song_option][0]
st.markdown(f"👉 [YouTube에서 듣기 🎧]({song_link})")

# 💃 랜덤 안무 아이디어 생성
if st.button("랜덤 안무 아이디어 생성 🎲"):
    moves = random.sample(dance_basics[genre][level], k=min(2, len(dance_basics[genre][level])))
    st.write("✨ 오늘의 안무 아이디어 ✨")
    for move, details in moves:
        st.markdown(f"**{move}**")
        for step in details:
            st.markdown(f"- {step}")

# 🕒 연습 시간 기록
st.subheader("연습 시간 기록 📊")
hours = st.number_input("연습 시간 (시)", min_value=0, max_value=10, step=1)
minutes = st.number_input("연습 시간 (분)", min_value=0, max_value=59, step=5)

if st.button("연습 기록 저장 📝"):
    new_record = {
        "날짜": datetime.date.today(),
        "장르": genre,
        "동작": song_option,
        "연습 시간(시)": hours,
        "연습 시간(분)": minutes,
        "추천곡": song_option
    }
    st.session_state["records"] = pd.concat([st.session_state["records"], pd.DataFrame([new_record])], ignore_index=True)
    st.success("연습 기록이 저장되었습니다! 🎉")

# 📊 기록 확인
st.subheader("📖 나의 연습 기록")
st.dataframe(st.session_state["records"])
