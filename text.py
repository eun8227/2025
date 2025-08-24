import streamlit as st
import pandas as pd
import random
from datetime import datetime, time

st.set_page_config(page_title="댄스 연습 앱", page_icon="💃", layout="wide")

st.title("💃 댄스 연습 기록 & 랜덤 안무 아이디어 🎶")

# 세션 상태 초기화
if "records" not in st.session_state:
    st.session_state["records"] = []

# --- 장르별 난이도별 기본기 데이터 (더 자세한 단계별 설명) ---
dance_basics = {
    "힙합": {
        "초급": [
            ("Bounce", [
                "무릎을 가볍게 굽히며 박자를 타기",
                "상체는 편하게 두고 어깨로 리듬을 강조",
                "손은 자연스럽게 흔들며 균형 맞추기"
            ]),
            ("Step Touch", [
                "옆으로 한 발 내딛기",
                "반대발은 가볍게 붙이기",
                "손은 반대 방향으로 흔들며 리듬 타기"
            ]),
            ("Slide", [
                "발을 바닥에 밀듯이 옆으로 이동",
                "상체는 흐름에 맞게 부드럽게 흔들기",
                "발을 모아 리듬을 마무리하기"
            ])
        ],
        "중급": [
            ("Body Roll", [
                "가슴을 앞으로 내밀며 시작",
                "가슴→배→골반 순서로 파도처럼 굴리기",
                "상체가 자연스럽게 이어지도록 연결"
            ]),
            ("Wave", [
                "손끝에서부터 팔꿈치까지 흐름 주기",
                "어깨→가슴→허리로 이어주기",
                "허리에서 반대 팔로 연결하며 마무리"
            ]),
            ("Isolations", [
                "머리만 좌우로 움직이며 나머지는 고정",
                "어깨만 위아래로 리듬 주기",
                "골반만 원형으로 돌리기"
            ])
        ],
        "고급": [
            ("Knee Drop", [
                "무릎을 빠르게 구부리며 착지",
                "상체는 흔들림 없이 고정",
                "다시 일어나며 리듬을 이어가기"
            ]),
            ("Harlem Shake", [
                "어깨를 위아래로 빠르게 흔들기",
                "몸 전체가 진동하는 듯 리듬 유지",
                "팔과 머리도 자연스럽게 흔들기"
            ]),
            ("Reverse Wave", [
                "허리에서 시작해 가슴, 어깨, 팔로 전달",
                "손끝까지 흐름을 밀어내듯 표현",
                "부드럽게 마무리하며 제자리로 돌아오기"
            ])
        ]
    },
    "팝핀": {
        "초급": [
            ("Hit", [
                "근육을 순간적으로 수축하며 충격 주기",
                "팔꿈치와 어깨를 동시에 튕기기",
                "팝 사운드와 동작을 맞추기"
            ]),
            ("Fresno", [
                "팔을 좌우로 벌리며 리듬 맞추기",
                "무릎을 번갈아 굽히며 발을 구르기",
                "상체는 중심을 잡으며 부드럽게 이동"
            ]),
            ("Arm Wave", [
                "손끝에서 팔꿈치까지 파도 만들기",
                "어깨→반대 팔로 연결하기",
                "끝에서 자연스럽게 제스처 추가"
            ])
        ]
    }
    # 👉 다른 장르들도 같은 방식으로 확장 가능
}

# --- 장르별 추천 곡 (유튜브 링크 포함) ---
song_recommendations = {
    "힙합": [
        ("Jay Park - All I Wanna Do", "https://youtu.be/w0PtbE8K6FQ"),
        ("Zico - Artist", "https://youtu.be/UuV2BmJ1p_I"),
        ("Epik High - Fly", "https://youtu.be/lS9VnS6tJqE")
    ],
    "팝핀": [
        ("Michael Jackson - Billie Jean", "https://youtu.be/Zi_XLOBDo_Y"),
        ("Chris Brown - Forever", "https://youtu.be/5sMKX22BHeE"),
        ("Usher - Yeah!", "https://youtu.be/GxBSyx85Kp8")
    ]
}

# --- 랜덤 안무 아이디어 생성 ---
st.header("✨ 랜덤 안무 생성기")
genre = st.selectbox("장르를 선택하세요", list(dance_basics.keys()))
level = st.radio("난이도를 선택하세요", ["초급", "중급", "고급"])

if st.button("안무 아이디어 생성하기"):
    moves = dance_basics[genre][level]
    routine_length = random.randint(3, 5)
    routine = random.sample(moves, k=min(routine_length, len(moves)))
    
    cute_emojis = ["🌸", "🐥", "🐰", "🎀", "🍓", "💫"]
    formatted = []
    for i, (move, steps) in enumerate(routine, 1):
        emoji = random.choice(cute_emojis)
        step_text = "\n      - " + "\n      - ".join(steps)
        formatted.append(f"{i}. {move} {emoji}{step_text}")
    
    st.session_state["current_routine"] = "\n".join(formatted)

if "current_routine" in st.session_state:
    st.success(f"오늘의 안무 아이디어 ({genre} - {level})")
    st.markdown(st.session_state["current_routine"])

    # 추천 곡 선택 (여러 개 가능)
    st.subheader("🎶 오늘의 추천 곡")
    song_list = [title for title, link in song_recommendations[genre]]
    selected_songs = st.multiselect("마음에 드는 곡을 골라보세요 🎧", song_list)
    
    if selected_songs:
        for title, link in song_recommendations[genre]:
            if title in selected_songs:
                st.markdown(f"👉 {title} 🔗 [유튜브 바로가기]({link})")

# --- 연습 기록하기 ---
st.header("📝 연습 기록")
date = st.date_input("연습 날짜", datetime.today())
start_time = st.time_input("연습 시작 시각", time(18, 0))
end_time = st.time_input("연습 종료 시각", time(19, 0))

# 연습 시간 계산
duration = (datetime.combine(datetime.today(), end_time) - 
            datetime.combine(datetime.today(), start_time)).seconds / 3600

if st.button("기록 저장"):
    st.session_state["records"].append({
        "date": date,
        "hours": round(duration, 2),
        "routine": st.session_state.get("current_routine", "없음"),
        "genre": genre,
        "level": level,
        "songs": selected_songs
    })
    st.success("연습 기록이 저장되었습니다!")

# --- 기록 확인 ---
st.header("📊 연습 기록 보기")
if len(st.session_state["records"]) > 0:
    df = pd.DataFrame(st.session_state["records"])
    st.dataframe(df)
    st.line_chart(df.set_index("date")["hours"])
else:
    st.info("아직 기록이 없습니다. 위에서 연습 기록을 추가해보세요!")
