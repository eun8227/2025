import streamlit as st
import pandas as pd
import random
from datetime import datetime, time

st.set_page_config(page_title="댄스 연습 앱", page_icon="💃", layout="wide")

st.title("💃 댄스 연습 기록 & 랜덤 안무 아이디어 🎶")

# 세션 상태 초기화
if "records" not in st.session_state:
    st.session_state["records"] = []

# --- 장르별 난이도별 기본기 데이터 (단계별 설명 포함) ---
dance_basics = {
    "힙합": {
        "초급": [
            ("Bounce", ["무릎을 살짝 굽히기", "상체를 편하게 흔들기", "리듬을 일정하게 유지"]),
            ("Step Touch", ["옆으로 한 발 내딛기", "반대발은 모으기", "박자에 맞춰 반복"]),
            ("Slide", ["발을 바닥에 밀듯 이동", "상체는 편하게 흐름 타기"])
        ],
        "중급": [
            ("Body Roll", ["가슴부터 아래로 흐르듯 굴리기", "허리까지 자연스럽게 연결"]),
            ("Wave", ["손끝부터 팔, 어깨, 몸통, 허리까지 순서대로 움직임"]),
            ("Isolations", ["머리/어깨/가슴/골반 중 한 부위만 따로 움직임"])
        ],
        "고급": [
            ("Knee Drop", ["무릎을 빠르게 꿇으며 리듬 유지", "상체는 흔들림 없이 잡기"]),
            ("Harlem Shake", ["어깨를 위아래로 흔들기", "몸 전체를 리드미컬하게 진동"]),
            ("Reverse Wave", ["Wave를 반대 방향(허리→팔끝)으로 연결"])
        ]
    },
    "팝핀": {
        "초급": [
            ("Hit", ["근육을 순간적으로 수축", "팝 사운드에 맞춰 타이밍 주기"]),
            ("Fresno", ["좌우 팔 벌리기", "다리를 번갈아 굽히며 이동"]),
            ("Arm Wave", ["손끝→팔꿈치→어깨 순으로 파도 만들기"])
        ],
        "중급": [
            ("Dime Stop", ["움직이다가 순간 정지", "정확한 박자에 멈추기"]),
            ("Isolation", ["머리/어깨/골반 한 부위만 움직이기"]),
            ("Tut", ["팔을 직각으로 꺾어 직선적인 그림 만들기"])
        ],
        "고급": [
            ("Boogaloo Roll", ["허리를 원형으로 돌리며 흐름 연결"]),
            ("Pop & Glide", ["팝 동작 후 발을 미끄러지듯 이동"]),
            ("Animation", ["프레임이 끊긴 듯 느리게 움직이기"])
        ]
    },
    "왁킹": {
        "초급": [
            ("Arm Swing", ["팔을 크게 원을 그리며 돌리기"]),
            ("Pose", ["박자에 맞춰 멈추고 포즈 취하기"]),
            ("Basic Step", ["앞뒤로 기본적인 이동 스텝"])
        ],
        "중급": [
            ("Turn & Pose", ["빠르게 회전 후 포즈로 마무리"]),
            ("Whip", ["팔을 채찍처럼 강하게 휘두르기"]),
            ("Groove Step", ["발을 구르며 리듬감 있게 이동"])
        ],
        "고급": [
            ("Double Whip", ["양팔을 동시에 빠르게 휘두르기"]),
            ("Arm Roll", ["팔을 원형으로 굴려 이어가기"]),
            ("Fast Spin", ["빠른 회전으로 강렬한 효과 주기"])
        ]
    },
    "하우스": {
        "초급": [
            ("Heel Toe", ["앞꿈치와 뒤꿈치로 리듬 밟기"]),
            ("Shuffle", ["발을 빠르게 끌며 리듬 타기"]),
            ("Jack", ["골반을 앞뒤로 밀며 그루브 타기"])
        ],
        "중급": [
            ("Lofting", ["공중을 날듯 가볍게 점프"]),
            ("Stomp", ["발을 바닥에 강하게 찍으며 리듬"]),
            ("Skate", ["미끄러지듯 옆으로 이동"])
        ],
        "고급": [
            ("Loose Legs", ["빠른 발놀림으로 흐름 유지"]),
            ("Floor Work", ["바닥에 손을 짚고 회전 동작"]),
            ("Cross Step", ["발을 교차하며 부드럽게 이동"])
        ]
    }
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
    ],
    "왁킹": [
        ("Madonna - Vogue", "https://youtu.be/GuJQSAiODqI"),
        ("Whitney Houston - I Wanna Dance With Somebody", "https://youtu.be/eH3giaIzONA"),
        ("Lady Gaga - Just Dance", "https://youtu.be/2Abk1jAONjw")
    ],
    "하우스": [
        ("Disclosure - Latch", "https://youtu.be/93ASUImTedo"),
        ("Robin S - Show Me Love", "https://youtu.be/PdzIS4oNP-4"),
        ("Calvin Harris - Summer", "https://youtu.be/ebXbLfLACGM")
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
        step_text = " → ".join(steps)
        formatted.append(f"{i}. {move} {emoji}\n   - {step_text}")
    
    st.session_state["current_routine"] = "\n".join(formatted)

if "current_routine" in st.session_state:
    st.success(f"오늘의 안무 아이디어 ({genre} - {level})")
    st.markdown(st.session_state["current_routine"])

    # 추천 곡 중 선택 (여러 개 가능)
    st.subheader("🎶 오늘의 추천 곡")
    song_list = [title for title, link in song_recommendations[genre]]
    selected_songs = st.multiselect("마음에 드는 곡을 고르세요", song_list)
    
    st.session_state["selected_songs"] = selected_songs

    # 선택된 곡 링크 보여주기
    if selected_songs:
        for title, link in song_recommendations[genre]:
            if title in selected_songs:
                st.markdown(f"👉 [{title}]({link})")

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
        "songs": st.session_state.get("selected_songs", [])
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
