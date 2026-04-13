import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time

# --- 1. 보안 설정 (Streamlit Cloud용) ---
# 스트림릿 설정창의 Secrets에 등록한 API 키를 가져옵니다.
try:
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
except:
    ELEVENLABS_API_KEY = ""

VOICE_ID = "EXAVITQu4vr4xnNLMQer" # 로즈샘 추천 목소리 ID

# --- 2. 핑크 점 Lottie 데이터 (파이썬 문법에 맞게 False/True 수정 완료) ---
LOTTIE_DATA = {
    "v":"5.9.0","fr":10,"ip":0,"op":90,"w":500,"h":500,"nm":"02","ddd":0,"assets":[],
    "layers":[{"ddd":0,"ind":1,"ty":4,"nm":"01","sr":1,"ks":{"o":{"a":0,"k":100,"ix":11},"r":{"a":0,"k":0,"ix":10},"p":{"a":0,"k":[250,250,0],"ix":2,"l":2},"a":{"a":0,"k":[0,0,0],"ix":1,"l":2},"s":{"a":1,"k":[{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":0,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":5,"s":[80,80,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":20,"s":[120,120,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":30,"s":[90,90,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.167,0.167,0.167],"y":[0,0,0]},"t":35,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":45,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":50,"s":[80,80,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":65,"s":[120,120,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":75,"s":[90,90,100]},{"t":80,"s":[100,100,100]}],"ix":6,"l":2}},"ao":0,"shapes":[{"ty":"gr","it":[{"d":1,"ty":"el","s":{"a":0,"k":[500,500],"ix":2},"p":{"a":0,"k":[0,0],"ix":3},"nm":"æ¥•å††å½¢ãƒ‘ã‚¹ 1","mn":"ADBE Vector Shape - Ellipse","hd":False},{"ty":"fl","c":{"a":0,"k":[1,0.4,0.6,1],"ix":4},"o":{"a":0,"k":100,"ix":5},"r":1,"bm":0,"nm":"å¡—ã‚Š 1","mn":"ADBE Vector Graphic - Fill","hd":False},{"ty":"tr","p":{"a":0,"k":[0,0],"ix":2},"a":{"a":0,"k":[0,0],"ix":1},"s":{"a":0,"k":[37.53,37.53],"ix":3},"r":{"a":0,"k":0,"ix":6},"o":{"a":0,"k":100,"ix":7},"sk":{"a":0,"k":0,"ix":4},"sa":{"a":0,"k":0,"ix":5},"nm":"ãƒˆãƒ©ãƒ³ã‚¹ãƒ•ã‚©ãƒ¼ãƒ "}],"nm":"æ¥•å††å½¢ 1","np":3,"cix":2,"bm":0,"ix":1,"mn":"ADBE Vector Group","hd":False}],"ip":0,"op":90,"st":0,"bm":0}],"markers":[]}

# --- 3. 페이지 디자인 ---
st.set_page_config(page_title="로즈샘 고민상담소", layout="centered")

# 배경을 흰색으로 고정하는 CSS
st.markdown("""
    <style>
    .main { background-color: white; }
    .stApp { background-color: white; }
    .rose-container { display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. 세션 상태 관리 ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rose_state" not in st.session_state:
    st.session_state.rose_state = "rose_idle.png"

# --- 5. UI 렌더링 ---
st.markdown('<div class="rose-container">', unsafe_allow_html=True)

# 현재 상태의 로즈샘 이미지 표시
st.image(st.session_state.rose_state, width=280)

# 생각 중일 때 핑크 점 로더 표시
if st.session_state.get("is_thinking"):
    st_lottie(LOTTIE_DATA, height=80, key="loader")
st.markdown('</div>', unsafe_allow_html=True)

# 채팅 기록 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- 6. 대화 로직 ---
if prompt := st.chat_input("로즈샘에게 말을 걸어봐!"):
    # 1. 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2. 로즈샘 고민 시작 (한복 입은 생각 이미지로 변경)
    st.session_state.rose_state = "rose_think.png"
    st.session_state.is_thinking = True
    st.rerun()

# 로즈샘의 답변 생성 단계
if st.session_state.get("is_thinking"):
    # (여기에 향후 실제 API 연결)
    time.sleep(2) # 하찮게 고민하는 척 하는 시간
    
    response_text = f"자기야~ 방금 '{prompt}'라고 했어? 그건 진짜 개꿀이지! 🌹"
    
    # 3. 상태 업데이트 (환호 이미지로 변경!)
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.session_state.rose_state = "rose_happy.png"
    st.session_state.is_thinking = False
    
    # 4. 재실행해서 화면 갱신
    st.rerun()
