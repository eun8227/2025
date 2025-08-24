import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="댄스 연습 앱", page_icon="💃", layout="wide")

st.title("💃 댄스 연습 기록 & 랜덤 안무 아이디어 🎶")

# 세션 상태 초기화
if "records" not in st.session_state:
    st.session_state["records"] = []

# --- 장르별 난이도별 기본기 데이터 (설명 포함) ---
dance_basics = {
    "힙합": {
        "초급": [("Bounce", "무릎 반동으로 리듬 잡기"),
                ("Step Touch", "옆으로 발을 뻗고 제자리로 가져오기"),
                ("Slide", "발을 바닥에 밀듯이 이동하기")],
        "중급": [("Body Roll", "상체를 위에서 아래로 굴리듯 움직이기"),
                ("Wave", "팔과 몸통을 물결처럼 연결하기"),
                ("Isolations", "몸의 특정 부위만 따로 움직이기")],
        "고급": [("Knee Drop", "무릎을 빠르게 바닥에 꿇으며 흐름 유지"),
                ("Harlem Shake", "어깨와 몸통을 흔들어 리듬 강조"),
                ("Reverse Wave", "Wave를 반대 방향으로 이어가기")]
    },
    "팝핀": {
        "초급": [("Hit", "근육을 순간적으로 수축하여 박자 강조"),
                ("Fresno", "팔과 다리를 좌우로 흔드는 기본 팝핀 동작"),
                ("Arm Wave", "팔을 통해 파도 흐르듯 움직이기")],
        "중급": [("Dime Stop", "갑작스러운 정지 동작"),
                ("Isolation", "한 부위만 고립해서 움직이기"),
                ("Tut", "각진 팔 동작을 직선으로 이어가기")],
        "고급": [("Boogaloo Roll", "허리와 몸통을 굴리듯 연결하기"),
                ("Pop & Glide", "팝과 미끄러짐을 결합하기"),
                ("Animation", "프레임이 끊긴 듯한 착각 주기")]
    },
    "왁킹": {
        "초급": [("Arm Swing", "팔을 크게 원형으로 휘두르기"),
                ("Pose", "리듬에 맞춰 순간 정지하기"),
                ("Basic Step", "기본적인 발 동작으로 이동하기")],
        "중급": [("Turn & Pose", "회전 후 포즈로 마무리"),
                ("Whip", "팔을 채찍처럼 빠르게 휘두르기"),
                ("Groove Step", "리듬에 맞춰 몸 전체를 흔들며 이동")],
        "고급": [("Double Whip", "양팔을 동시에 빠르게 휘두르기"),
                ("Arm Roll", "팔을 원형으로 굴려 이어가기"),
                ("Fast Spin", "빠른 회전으로 강렬한 효과 주기")]
    }
}

# --- 장르별 추천 곡 ---
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
    for i, (move, desc) in enumerate(routine, 1):
        emoji = random.choice(cute_emojis)
        formatted.append(f"{i}. {move} {emoji} → {desc}")
    
    st.session_state["current_routine"] = "\n".join(formatted)

if "current_routine" in st.session_state:
    st.success(f"오늘의 안무 아이디어 ({genre} - {level})")
    st.markdown(st.session_state["current_routine"])

    # 추천 곡 중 선택 (여러 개 가능)
    st.subheader("🎶 오늘의 추천 곡")
    song_list = [title for title, link in song_recommendations[genre]]
    selected_songs = st.multiselect("마음에 드는 곡을 고르세요 (여러 개 가능)", song_list)
    
    st.session_state["selected_songs"] = selected_songs

    # 선택된 곡 링크 보여주기
    if selected_songs:
        for title, link in song_recommendations[genre]:
            if title in selected_songs:
                st.markdown(f"👉 [{title}]({link})")

# --- 연습 기록하기 ---
st.header("📝 연습 기록")
date = st.date_input("연습 날짜", datetime.today())
minutes = st.number_input("연습 시간(분)", min_value=10, step=5)

if st.button("기록 저장"):
    st.session_state["records"].append({
        "date": date,
        "minutes": minutes,
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
    st.line_chart(df.set_index("date")["minutes"])
else:
    st.info("아직 기록이 없습니다. 위에서 연습 기록을 추가해보세요!")
