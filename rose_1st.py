import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time

# --- 1. 보안 설정 (GitHub Secrets 연동) ---
try:
    # 깃허브에 넣으신 이름과 정확히 일치해야 합니다.
    ELEVEN_API_KEY = st.secrets["ELEVENLABS_API"] 
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    VOICE_ID = st.secrets.get("VOICE_ID", "EXAVITQu4vr4xnNLMQer")
except Exception as e:
    st.error("Secrets 설정(API 키)을 다시 확인해주세요! 🌹")
    st.stop()

# --- 2. 뇌(LLM) 로직: 전문 한국어 강사 페르소나 주입 ---
def get_rose_ai_response(prompt, user_info, mode):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    # 한국어 강사로서의 정체성을 강력하게 심어줍니다.
    persona = f"""
    당신은 전문 한국어 강사 '로즈샘'입니다.
    사용자 정보: 이름 {user_info['name']}, MBTI {user_info['mbti']}, 취미 {user_info['hobby']}, 목적 {user_info['goal']}.
    성격: 쾌활하고 에너지가 넘치며, '개꿀', '갓벽' 등의 단어를 즐겨 사용합니다.
    대화 모드: {mode} 모드.
    
    [필수 임무]
    1. 사용자가 한국어 받침, 문법, 어휘를 틀리면 즉시 지적하고 친절하게 예시를 들어 교정해주세요.
    2. 답변 시작할 때 항상 사용자의 이름을 다정하게 불러주세요.
    3. 사용자의 MBTI나 취미를 대화 중간에 언급하며 공감해주세요.
    4. 한국어 학습 목적에 맞는 격려를 잊지 마세요.
    """
    
    data = {
        "model": "llama-3.3-70b-versatile", # 제니샘 프로젝트에서 쓴 고성능 모델
        "messages": [
            {"role": "system", "content": persona},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except:
        return f"{user_info['name']}님, 로즈샘 뇌에 잠깐 렉이 걸렸어요! 다시 말해줄래요? 🌹"

# --- 3. 음성 생성 함수 ---
def generate_audio(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVEN_API_KEY}
    data = {"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.4, "similarity_boost": 0.75}}
    try:
        res = requests.post(url, json=data, headers=headers)
        return res.content if res.status_code == 200 else None
    except: return None

# 핑크 점 Lottie (수정 완료)
LOTTIE_DATA = {"v":"5.9.0","fr":10,"ip":0,"op":90,"w":500,"h":500,"nm":"02","ddd":0,"assets":[],"layers":[{"ddd":0,"ind":1,"ty":4,"nm":"01","sr":1,"ks":{"o":{"a":0,"k":100,"ix":11},"r":{"a":0,"k":0,"ix":10},"p":{"a":0,"k":[250,250,0],"ix":2,"l":2},"a":{"a":0,"k":[0,0,0],"ix":1,"l":2},"s":{"a":1,"k":[{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":0,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":5,"s":[80,80,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":20,"s":[120,120,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":30,"s":[90,90,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.167,0.167,0.167],"y":[0,0,0]},"t":35,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":45,"s":[100,100,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":50,"s":[80,80,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":65,"s":[120,120,100]},{"i":{"x":[0.667,0.667,0.667],"y":[1,1,1]},"o":{"x":[0.333,0.333,0.333],"y":[0,0,0]},"t":75,"s":[90,90,100]},{"t":80,"s":[100,100,100]}],"ix":6,"l":2}},"ao":0,"shapes":[{"ty":"gr","it":[{"d":1,"ty":"el","s":{"a":0,"k":[500,500],"ix":2},"p":{"a":0,"k":[0,0],"ix":3},"nm":"æ¥•å††å½¢ãƒ‘ã‚¹ 1","mn":"ADBE Vector Shape - Ellipse","hd":False},{"ty":"fl","c":{"a":0,"k":[1,0.4,0.6,1],"ix":4},"o":{"a":0,"k":100,"ix":5},"r":1,"bm":0,"nm":"å¡—ã‚Š 1","mn":"ADBE Vector Graphic - Fill","hd":False},{"ty":"tr","p":{"a":0,"k":[0,0],"ix":2},"a":{"a":0,"k":[0,0],"ix":1},"s":{"a":0,"k":[37.53,37.53],"ix":3},"r":{"a":0,"k":0,"ix":6},"o":{"a":0,"k":100,"ix":7},"sk":{"a":0,"k":0,"ix":4},"sa":{"a":0,"k":0,"ix":5},"nm":"ãƒˆãƒ©ãƒ³ã‚¹ãƒ•ã‚©ãƒ¼ãƒ "}],"nm":"æ¥•å††å½¢ 1","np":3,"cix":2,"bm":0,"ix":1,"mn":"ADBE Vector Group","hd":False}],"ip":0,"op":90,"st":0,"bm":0}],"markers":[]}

# --- 4. 킹벽 디자인 (절대 중앙 정렬 & 둥둥 효과) ---
st.set_page_config(page_title="로즈샘 고민상담소", layout="centered")
st.markdown("""
    <style>
    .block-container { padding-top: 5rem !important; display: flex !important; flex-direction: column !important; align-items: center !important; }
    @keyframes floating { 0% { transform: translateY(0px); } 50% { transform: translateY(-25px); } 100% { transform: translateY(0px); } }
    .stImage { display: flex !important; justify-content: center !important; animation: floating 3s ease-in-out infinite !important; }
    .stChatInputContainer { max-width: 600px; margin: 0 auto; }
    .stButton>button { border-radius: 20px; width: 250px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. 세션 상태 관리 ---
if "page" not in st.session_state: st.session_state.page = "profile"
if "messages" not in st.session_state: st.session_state.messages = []
if "rose_state" not in st.session_state: st.session_state.rose_state = "rose_idle.png"

# --- 6. 프로필 설정 페이지 ---
if st.session_state.page == "profile":
    st.image("rose_happy.png", width=220)
    st.markdown("## 로즈샘이 널 더 알고 싶어! 🌹")
    with st.form("profile_form"):
        name = st.text_input("이름 (닉네임)")
        mbti = st.selectbox("MBTI", ["선택해줘", "INTJ", "ENFP", "INFJ", "ENTP", "기타"])
        hobby = st.text_input("취미")
        goal = st.text_input("학습 목적")
        if st.form_submit_button("로즈샘 만나러 가기 ✨"):
            st.session_state.user_info = {"name": name, "mbti": mbti, "hobby": hobby, "goal": goal}
            st.session_state.page = "mode_select"; st.rerun()

# --- 7. 모드 선택 페이지 ---
elif st.session_state.page == "mode_select":
    st.image("rose_smart.png", width=220)
    st.markdown(f"### {st.session_state.user_info['name']}님, 반가워!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌹 친근한 반말"): st.session_state.mode = "반말"; st.session_state.page = "chat"; st.rerun()
    with col2:
        if st.button("👑 정중한 존칭"): st.session_state.mode = "존칭"; st.session_state.page = "chat"; st.rerun()

# --- 8. 채팅 페이지 ---
elif st.session_state.page == "chat":
    st.image(st.session_state.rose_state, width=220)
    if st.session_state.get("is_thinking"): st_lottie(LOTTIE_DATA, height=60, key="loader")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    if prompt := st.chat_input("로즈샘에게 고민을 털어놔봐!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.rose_state = "rose_think.png"
        st.session_state.is_thinking = True
        st.rerun()

    if st.session_state.get("is_thinking"):
        response = get_rose_ai_response(prompt, st.session_state.user_info, st.session_state.mode)
        audio = generate_audio(response)
        if audio: st.audio(audio, format="audio/mp3", autoplay=True)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.rose_state = "rose_happy.png" if st.session_state.mode == "반말" else "rose_smart.png"
        st.session_state.is_thinking = False
        st.rerun()
