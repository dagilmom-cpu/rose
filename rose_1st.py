import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time

# --- 1. 보안 설정 및 보이스 설정 ---
try:
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
    VOICE_ID = st.secrets.get("VOICE_ID", "EXAVITQu4vr4xnNLMQer") 
except:
    ELEVENLABS_API_KEY = ""
    VOICE_ID = "EXAVITQu4vr4xnNLMQer"

# 핑크 점 Lottie 데이터 (수정 완료)
LOTTIE_DATA = {"v":"5.9.0","fr":10,"ip":0,"op":90,"w":500,"h":500,"nm":"02","ddd":0,"assets":[],"layers":[{"ddd":0,"ind":1,"ty":4,"nm":"01","sr":1,"ks":{"o":{"a":0,"k":100,"ix":11},"r":{"a":0,"k":0,"ix":10},"p":{"a":0,"k":[250,250,0],"ix":2,"l":2},"a":{"a":0,"k":[0,0,0],"ix":1,"l":2},"s":{"a":1,"k":[{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":0,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":5,"s":[80,80,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":20,"s":[120,120,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":30,"s":[90,90,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.167,0.167,0.167],"y":[0,0,0]},"t":35,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":45,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":50,"s":[80,80,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":65,"s":[120,120,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":75,"s":[90,90,100]},{"t":80,"s":[100,100,100]}],"ix":6,"l":2}},"ao":0,"shapes":[{"ty":"gr","it":[{"d":1,"ty":"el","s":{"a":0,"k":[500,500],"ix":2},"p":{"a":0,"k":[0,0],"ix":3},"nm":"æ¥•å††å½¢ãƒ‘ã‚¹ 1","mn":"ADBE Vector Shape - Ellipse","hd":False},{"ty":"fl","c":{"a":0,"k":[1,0.4,0.6,1],"ix":4},"o":{"a":0,"k":100,"ix":5},"r":1,"bm":0,"nm":"å¡—ã‚Š 1","mn":"ADBE Vector Graphic - Fill","hd":False},{"ty":"tr","p":{"a":0,"k":[0,0],"ix":2},"a":{"a":0,"k":[0,0],"ix":1},"s":{"a":0,"k":[37.53,37.53],"ix":3},"r":{"a":0,"k":0,"ix":6},"o":{"a":0,"k":100,"ix":7},"sk":{"a":0,"k":0,"ix":4},"sa":{"a":0,"k":0,"ix":5},"nm":"ãƒˆãƒ©ãƒ³ã‚¹ãƒ•ã‚©ãƒ¼ãƒ "}],"nm":"æ¥•å††å½¢ 1","np":3,"cix":2,"bm":0,"ix":1,"mn":"ADBE Vector Group","hd":False}],"ip":0,"op":90,"st":0,"bm":0}],"markers":[]}

# --- 2. 페이지 설정 및 디자인 (정중앙 정렬 CSS) ---
st.set_page_config(page_title="로즈샘 고민상담소", layout="centered")

st.markdown("""
    <style>
    /* 전체 화면 정중앙 정렬 */
    .stApp {
        background-color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .main .block-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
    }

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
        animation: floating 3s ease-in-out infinite;
        margin-bottom: 20px;
    }
    
    .stButton>button { border-radius: 20px; width: 250px; height: 50px; font-weight: bold; margin-bottom: 10px; }
    .stChatInputContainer { width: 100%; max-width: 600px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 세션 상태 관리 ---
if "page" not in st.session_state: st.session_state.page = "landing"
if "mode" not in st.session_state: st.session_state.mode = ""
if "messages" not in st.session_state: st.session_state.messages = []
if "rose_state" not in st.session_state: st.session_state.rose_state = "rose_idle.png"

# --- 4. 입장 페이지 ---
if st.session_state.page == "landing":
    st.markdown('<div class="rose-container">', unsafe_allow_html=True)
    st.image("rose_happy.png", width=250)
    st.markdown("<h2 style='text-align: center;'>로즈샘 고민상담소</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>오늘의 상담 컨셉을 골라봐!</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🌹 친근한 반말 모드"):
        st.session_state.mode = "반말"
        st.session_state.page = "chat"
        st.rerun()
    if st.button("👑 정중한 존칭 모드"):
        st.session_state.mode = "존칭"
        st.session_state.page = "chat"
        st.rerun()

# --- 5. 채팅 페이지 ---
elif st.session_state.page == "chat":
    st.markdown('<div class="rose-container">', unsafe_allow_html=True)
    st.image(st.session_state.rose_state, width=220)
    if st.session_state.get("is_thinking"):
        st_lottie(LOTTIE_DATA, height=60, key="loader")
    st.markdown('</div>', unsafe_allow_html=True)

    # 채팅 출력 영역 (최대 너비 제한)
    chat_box = st.container()
    with chat_box:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    if prompt := st.chat_input("로즈샘에게 고민을 털어놔봐!"):
        # 사용자 메시지 저장
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.last_prompt = prompt # None 방지를 위해 프롬프트 저장
        st.session_state.rose_state = "rose_think.png"
        st.session_state.is_thinking = True
        st.rerun()

    if st.session_state.get("is_thinking"):
        time.sleep(1.5)
        # 세션에 저장된 마지막 프롬프트 가져오기
        current_input = st.session_state.get("last_prompt", "반가워")
        
        # --- 페르소나 적용된 답변 로직 ---
        if st.session_state.mode == "반말":
            response = f"자기야~ 방금 '{current_input}'라고 했어? 그건 진짜 개꿀이지! 🌹 역시 갓벽한 생각이야!"
            st.session_state.rose_state = "rose_happy.png"
        else:
            response = f"메이킴님, 방금 말씀하신 '{current_input}'은 정말 탁월한 생각입니다. 👑 제가 정중히 응원할게요!"
            st.session_state.rose_state = "rose_smart.png"
            
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.is_thinking = False
        st.rerun()
