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

# --- 2. 한국어 교정 로직 ---
GRAMMAR_DB = {
    "돼어": {"correct": "되어(돼)", "msg": "이건 '해어'랑 똑같은 거야! '되어'가 갓벽해! ✨"},
    "않해": {"correct": "안 해", "msg": "부정할 때는 '안'! 이건 무조건 외우기야! 🌹"},
    "어떻해": {"correct": "어떡해", "msg": "받침 'ㅎ'은 '어떻게'에만 써! 👑"},
    "맜있어": {"correct": "맛있어", "msg": "맛은 그냥 '맛'! 받침 하나만 빼자! 💖"}
}

def check_grammar(text):
    for wrong, data in GRAMMAR_DB.items():
        if wrong in text: return {"wrong": wrong, **data}
    return None

# --- 3. 음성 생성 함수 ---
def generate_audio(text):
    if not ELEVENLABS_API_KEY: return None
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVENLABS_API_KEY}
    data = {"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.4, "similarity_boost": 0.75}}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200: return response.content
    except: return None
    return None

# 핑크 점 Lottie 데이터 (파이썬 문법 수정됨)
LOTTIE_DATA = {"v":"5.9.0","fr":10,"ip":0,"op":90,"w":500,"h":500,"nm":"02","ddd":0,"assets":[],"layers":[{"ddd":0,"ind":1,"ty":4,"nm":"01","sr":1,"ks":{"o":{"a":0,"k":100,"ix":11},"r":{"a":0,"k":0,"ix":10},"p":{"a":0,"k":[250,250,0],"ix":2,"l":2},"a":{"a":0,"k":[0,0,0],"ix":1,"l":2},"s":{"a":1,"k":[{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":0,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":5,"s":[80,80,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":20,"s":[120,120,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":30,"s":[90,90,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.167,0.167,0.167],"y":[0,0,0]},"t":35,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":45,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":50,"s":[80,80,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":65,"s":[120,120,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":75,"s":[90,90,100]},{"t":80,"s":[100,100,100]}],"ix":6,"l":2}},"ao":0,"shapes":[{"ty":"gr","it":[{"d":1,"ty":"el","s":{"a":0,"k":[500,500],"ix":2},"p":{"a":0,"k":[0,0],"ix":3},"nm":"æ¥•å††å½¢ãƒ‘ã‚¹ 1","mn":"ADBE Vector Shape - Ellipse","hd":False},{"ty":"fl","c":{"a":0,"k":[1,0.4,0.6,1],"ix":4},"o":{"a":0,"k":100,"ix":5},"r":1,"bm":0,"nm":"å¡—ã‚Š 1","mn":"ADBE Vector Graphic - Fill","hd":False},{"ty":"tr","p":{"a":0,"k":[0,0],"ix":2},"a":{"a":0,"k":[0,0],"ix":1},"s":{"a":0,"k":[37.53,37.53],"ix":3},"r":{"a":0,"k":0,"ix":6},"o":{"a":0,"k":100,"ix":7},"sk":{"a":0,"k":0,"ix":4},"sa":{"a":0,"k":0,"ix":5},"nm":"ãƒˆãƒ©ãƒ³ã‚¹ãƒ•ã‚©ãƒ¼ãƒ "}],"nm":"æ¥•å††å½¢ 1","np":3,"cix":2,"bm":0,"ix":1,"mn":"ADBE Vector Group","hd":False}],"ip":0,"op":90,"st":0,"bm":0}],"markers":[]}

# --- 4. 페이지 디자인 ---
st.set_page_config(page_title="로즈샘 고민상담소", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: white; display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .main .block-container { display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 80vh; }
    @keyframes floating { 0% { transform: translateY(0px); } 50% { transform: translateY(-15px); } 100% { transform: translateY(0px); } }
    .rose-container { display: flex; flex-direction: column; align-items: center; justify-content: center; animation: floating 3s ease-in-out infinite; margin-bottom: 10px; }
    .stButton>button { border-radius: 20px; width: 250px; font-weight: bold; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. 세션 상태 관리 ---
if "page" not in st.session_state: st.session_state.page = "profile"
if "user_info" not in st.session_state: st.session_state.user_info = {}
if "messages" not in st.session_state: st.session_state.messages = []
if "rose_state" not in st.session_state: st.session_state.rose_state = "rose_idle.png"

# --- 6. 프로필 설정 페이지 ---
if st.session_state.page == "profile":
    st.markdown('<div class="rose-container">', unsafe_allow_html=True)
    st.image("rose_happy.png", width=200)
    st.markdown("<h2 style='text-align: center;'>로즈샘이 널 더 알고 싶어! 🌹</h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.form("profile_form"):
        name = st.text_input("이름 (어떻게 불러줄까?)", placeholder="예: 메이킴")
        mbti = st.selectbox("MBTI는 뭐야?", ["선택해줘", "INTJ", "ENFP", "INFJ", "ENTP", "기타"])
        hobby = st.text_input("취미가 뭐야?", placeholder="예: 코딩, 그림 그리기")
        goal = st.text_input("한국어 공부 목적이 뭐야?", placeholder="예: 한국인 친구 사귀기")
        
        submitted = st.form_submit_button("로즈샘 만나러 가기 ✨")
        if submitted:
            if name:
                st.session_state.user_info = {"name": name, "mbti": mbti, "hobby": hobby, "goal": goal}
                st.session_state.page = "mode_select"
                st.rerun()
            else: st.warning("이름은 꼭 알려줘야지! 💖")

# --- 7. 모드 선택 페이지 ---
elif st.session_state.page == "mode_select":
    st.markdown(f"<h3 style='text-align: center;'>{st.session_state.user_info['name']}님, 반가워!</h3>", unsafe_allow_html=True)
    st.markdown('<div class="rose-container">', unsafe_allow_html=True)
    st.image("rose_smart.png", width=200)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🌹 친근한 반말 모드"): st.session_state.mode = "반말"; st.session_state.page = "chat"; st.rerun()
    if st.button("👑 정중한 존칭 모드"): st.session_state.mode = "존칭"; st.session_state.page = "chat"; st.rerun()

# --- 8. 채팅 페이지 ---
elif st.session_state.page == "chat":
    st.markdown('<div class="rose-container">', unsafe_allow_html=True)
    st.image(st.session_state.rose_state, width=200)
    if st.session_state.get("is_thinking"): st_lottie(LOTTIE_DATA, height=60, key="loader")
    st.markdown('</div>', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    if prompt := st.chat_input("로즈샘에게 고민을 털어놔봐!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.last_prompt = prompt
        st.session_state.is_thinking = True
        st.rerun()

    if st.session_state.get("is_thinking"):
        time.sleep(1.5)
        user = st.session_state.user_info
        current_input = st.session_state.get("last_prompt", "")
        grammar = check_grammar(current_input)
        
        if grammar:
            response = f"{user['name']}님! 잠깐만~ 방금 '{grammar['wrong']}'라고 썼지? " \
                       f"그건 '{grammar['correct']}'가 맞아! {grammar['msg']}"
            st.session_state.rose_state = "rose_think.png"
        else:
            if st.session_state.mode == "반말":
                response = f"{user['name']}아! {user['hobby']} 좋아하는구나? MBTI가 {user['mbti']}라서 그런지 '{current_input}' 생각도 아주 갓벽해! 🌹"
                st.session_state.rose_state = "rose_happy.png"
            else:
                response = f"{user['name']}님, {user['goal']}을(를) 위해 한국어를 공부하시는 모습이 멋집니다. '{current_input}'에 대해 정중히 응원할게요! 👑"
                st.session_state.rose_state = "rose_smart.png"
            
        audio_content = generate_audio(response)
        if audio_content: st.audio(audio_content, format="audio/mp3", autoplay=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.is_thinking = False
        st.rerun()
