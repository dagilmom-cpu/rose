import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time

# --- 1. 보안 설정 (Secrets 사용) ---
# 스트림릿 클라우드 설정창(Secrets)에 넣은 키를 가져옵니다.
try:
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
except:
    ELEVENLABS_API_KEY = "" # 키가 없을 경우 대비

VOICE_ID = "EXAVITQu4vr4xnNLMQer" # 로즈샘 추천 목소리 ID

# 핑크 점 Lottie 데이터
LOTTIE_DATA = {"v":"5.9.0","fr":10,"ip":0,"op":90,"w":500,"h":500,"nm":"02","ddd":0,"assets":[],"layers":[{"ddd":0,"ind":1,"ty":4,"nm":"01","sr":1,"ks":{"o":{"a":0,"k":100,"ix":11},"r":{"a":0,"k":0,"ix":10},"p":{"a":0,"k":[250,250,0],"ix":2,"l":2},"a":{"a":0,"k":[0,0,0],"ix":1,"l":2},"s":{"a":1,"k":[{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":0,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":5,"s":[80,80,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":20,"s":[120,120,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":30,"s":[90,90,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.167,0.167,0.167],"y":[0,0,0]},"t":35,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":45,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":50,"s":[80,80,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":65,"s":[120,120,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":75,"s":[90,90,100]},{"t":80,"s":[100,100,100]}],"ix":6,"l":2}},"ao":0,"shapes":[{"ty":"gr","it":[{"d":1,"ty":"el","s":{"a":0,"k":[500,500],"ix":2},"p":{"a":0,"k":[0,0],"ix":3},"nm":"æ¥•å††å½¢ãƒ‘ã‚¹ 1","mn":"ADBE Vector Shape - Ellipse","hd":False},{"ty":"fl","c":{"a":0,"k":[1,0.4,0.6,1],"ix":4},"o":{"a":0,"k":100,"ix":5},"r":1,"bm":0,"nm":"å¡—ã‚Š 1","mn":"ADBE Vector Graphic - Fill","hd":false},{"ty":"tr","p":{"a":0,"k":[0,0],"ix":2},"a":{"a":0,"k":[0,0],"ix":1},"s":{"a":0,"k":[37.53,37.53],"ix":3},"r":{"a":0,"k":0,"ix":6},"o":{"a":0,"k":100,"ix":7},"sk":{"a":0,"k":0,"ix":4},"sa":{"a":0,"k":0,"ix":5},"nm":"ãƒˆãƒ©ãƒ³ã‚¹ãƒ•ã‚©ãƒ¼ãƒ "}],"nm":"æ¥•å††å½¢ 1","np":3,"cix":2,"bm":0,"ix":1,"mn":"ADBE Vector Group","hd":false}],"ip":0,"op":90,"st":0,"bm":0}],"markers":[]}

# --- 2. 페이지 디자인 ---
st.set_page_config(page_title="로즈샘 고민상담소", layout="centered")

st.markdown("""
    <style>
    .main { background-color: white; }
    .stApp { background-color: white; }
    .rose-container { display: flex; flex-direction: column; align-items: center; padding-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 세션 상태 관리 ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rose_state" not in st.session_state:
    st.session_state.rose_state = "rose_idle.png"

# --- 4. 메인 UI ---
st.markdown('<div class="rose-container">', unsafe_allow_html=True)
st.image(st.session_state.rose_state, width=280)

if st.session_state.get("is_thinking"):
    st_lottie(LOTTIE_DATA, height=80, key="loader")
st.markdown('</div>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- 5. 대화 로직 ---
if prompt := st.chat_input("로즈샘에게 말을 걸어봐!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.rose_state = "rose_think.png"
    st.session_state.is_thinking = True
    st.rerun()

if st.session_state.get("is_thinking"):
    # 답변 생성 로직 (예시)
    time.sleep(2)
    response_text = f"자기야~ '{prompt}'? 그건 진짜 개꿀이지! 🌹"
    
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.session_state.rose_state = "rose_happy.png"
    st.session_state.is_thinking = False
    st.rerun()
