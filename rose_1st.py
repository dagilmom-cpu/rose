import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time

# --- 1. 보안 설정 및 보이스 설정 ---
try:
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
    # 시크릿에 넣어두신 VOICE_ID를 가져옵니다. 
    # 만약 시크릿에 VOICE_ID가 없다면 기본값을 사용합니다.
    VOICE_ID = st.secrets.get("VOICE_ID", "EXAVITQu4vr4xnNLMQer") 
except:
    ELEVENLABS_API_KEY = ""
    VOICE_ID = "EXAVITQu4vr4xnNLMQer"

# 핑크 점 Lottie 데이터
LOTTIE_DATA = {"v":"5.9.0","fr":10,"ip":0,"op":90,"w":500,"h":500,"nm":"02","ddd":0,"assets":[],"layers":[{"ddd":0,"ind":1,"ty":4,"nm":"01","sr":1,"ks":{"o":{"a":0,"k":100,"ix":11},"r":{"a":0,"k":0,"ix":10},"p":{"a":0,"k":[250,250,0],"ix":2,"l":2},"a":{"a":0,"k":[0,0,0],"ix":1,"l":2},"s":{"a":1,"k":[{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":0,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":5,"s":[80,80,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":20,"s":[120,120,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":30,"s":[90,90,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.167,0.167,0.167],"y":[0,0,0]},"t":35,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":45,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":50,"s":[80,80,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":65,"s":[120,120,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":75,"s":[90,90,100]},{"t":80,"s":[100,100,100]}],"ix":6,"l":2}},"ao":0,"shapes":[{"ty":"gr","it":[{"d":1,"ty":"el","s":{"a":0,"k":[500,500],"ix":2},"p":{"a":0,"k":[0,0],"ix":3},"nm":"æ¥•å††å½¢ãƒ‘ã‚¹ 1","mn":"ADBE Vector Shape - Ellipse","hd":False},{"ty":"fl","c":{"a":0,"k":[1,0.4,0.6,1],"ix":4},"o":{"a":0,"k":100,"ix":5},"r":1,"bm":0,"nm":"å¡—ã‚Š 1","mn":"ADBE Vector Graphic - Fill","hd":False},{"ty":"tr","p":{"a":0,"k":[0,0],"ix":2},"a":{"a":0,"k":[0,0],"ix":1},"s":{"a":0,"k":[37.53,37.53],"ix":3},"r":{"a":0,"k":0,"ix":6},"o":{"a":0,"k":100,"ix":7},"sk":{"a":0,"k":0,"ix":4},"sa":{"a":0,"k":0,"ix":5},"nm":"ãƒˆãƒ©ãƒ³ã‚¹ãƒ•ã‚©ãƒ¼ãƒ "}],"nm":"æ¥•å††å½¢ 1","np":3,"cix":2,"bm":0,"ix":1,"mn":"ADBE Vector Group","hd":False}],"ip":0,"op":90,"st":0,"bm":0}],"markers":[]}

# --- 2. 페이지 설정 및 디자인 (둥실둥실 애니메이션 추가) ---
st.set_page_config(page_title="로즈샘 고민상담소", layout="centered")

st.markdown("""
    <style>
    .main { background-color: white; }
    .stApp { background-color: white; }
    
    /* 로즈샘 둥실둥실 애니메이션 */
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    .rose-container { 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        padding-top: 30px;
        animation: floating 3s ease-in-out infinite; 
    }
    .stButton>button { border-radius: 20px; width: 100%; height: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 세션 상태 관리 ---
if "page" not in st.session_state:
    st.session_state.page = "landing" # 첫 화면 상태
if "mode" not in st.session_state:
    st.session_state.mode = "" # 반말/존칭 모드 저장
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rose_state" not in st.session_state:
    st.session_state.rose_state = "rose_idle.png"

# --- 4. 입장 페이지 (Landing Page) ---
if st.session_state.page == "landing":
    st.markdown('<div class="rose-container">', unsafe_allow_html=True)
    st.image("rose_happy.png", width=250)
    st.markdown("<h2 style='text-align: center;'>로즈샘 고민상담소</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>상담 모드를 선택해줘!</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌹 친근한 반말 모드"):
            st.session_state.mode = "반말"
            st.session_state.page = "chat"
            st.rerun()
    with col2:
        if st.button("👑 정중한 존칭 모드"):
            st.session_state.mode = "존칭"
            st.session_state.page = "chat"
            st.rerun()

# --- 5. 채팅 페이지 (Main Chat) ---
elif st.session_state.page == "chat":
    # 상단 로즈샘 로고 느낌의 레이아웃
    st.markdown('<div class="rose-container">', unsafe_allow_html=True)
    st.image(st.session_state.rose_state, width=220)
    
    if st.session_state.get("is_thinking"):
        st_lottie(LOTTIE_DATA, height=60, key="loader")
    st.markdown('</div>', unsafe_allow_html=True)

    # 채팅 기록
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 입력창
    if prompt := st.chat_input("로즈샘에게 궁금한 걸 물어봐!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.rose_state = "rose_think.png"
        st.session_state.is_thinking = True
        st.rerun()

    # 답변 생성 로직
    if st.session_state.get("is_thinking"):
        time.sleep(2)
        
        # 모드에 따른 로즈샘의 말투 변화
        if st.session_state.mode == "반말":
            response_text = f"자기야~ 방금 '{prompt}'라고 했어? 그건 진짜 개꿀이지! 🌹"
            st.session_state.rose_state = "rose_happy.png"
        else:
            response_text = f"메이킴님, 문의하신 '{prompt}'에 대해 고민해 보았습니다. 아주 훌륭한 아이디어네요! 👑"
            st.session_state.rose_state = "rose_smart.png" # 존칭 모드에선 갓 쓴 로즈샘!
            
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.session_state.is_thinking = False
        st.rerun()
