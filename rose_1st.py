import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time

# --- 1. 보안 설정 (키 이름 'ELEVENLABS_API' 적용) ---
try:
    # 깃허브 Secrets와 이름을 정확히 일치시켰습니다.
    API_KEY_ELEVEN = st.secrets["ELEVENLABS_API"] 
    API_KEY_GROQ = st.secrets["GROQ_API_KEY"]
    VOICE_ID = st.secrets.get("VOICE_ID", "EXAVITQu4vr4xnNLMQer")
except Exception as e:
    st.error(f"Secrets 설정 확인 필요: {e} 🌹")
    st.stop()

# --- 2. 뇌(LLM) 로직: 난이도 및 페르소나 정교화 ---
def get_rose_ai_response(prompt, user_info, mode):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY_GROQ}", "Content-Type": "application/json"}
    
    # 난이도별 가이드라인
    level_guide = {
        "초급": "쉬운 단어와 짧은 문장 위주로 말하고, 문법 설명을 아주 쉽게 해주세요.",
        "중급": "일반적인 대화 속도로 말하며, 유용한 표현과 관용구를 섞어주세요.",
        "고급": "전문적이고 깊이 있는 어휘를 사용하며, 문법의 미세한 뉘앙스 차이를 설명해주세요."
    }

    persona = f"""
    당신은 지적이고 쾌활한 전문 한국어 강사 '로즈샘'입니다.
    사용자: {user_info['name']}, MBTI: {user_info['mbti']}, 취미: {user_info['hobby']}, 목적: {user_info['goal']}.
    학습 난이도: {user_info['level']} ({level_guide[user_info['level']]})
    모드: {mode}.
    
    [핵심 가이드]
    1. 반드시 사용자의 이름을 부르며 시작하세요.
    2. 난이도에 딱 맞는 어휘와 속도로 대화하세요.
    3. 틀린 문법은 '선생님'답게 정확히 짚어주되, 맥락에 맞는 적절한 감탄사(개꿀, 갓벽 등)는 아주 가끔만 쓰세요.
    """
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": persona}, {"role": "user", "content": prompt}],
        "temperature": 0.5
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except:
        return f"{user_info['name']}님, 로즈샘 뇌가 잠시 정비 중이에요! 다시 말해줄래요? 🌹"

# --- 3. 음성 생성 함수 ---
def generate_audio(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": API_KEY_ELEVEN}
    data = {"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}}
    try:
        res = requests.post(url, json=data, headers=headers)
        return res.content if res.status_code == 200 else None
    except: return None

# --- 4. 초강력 중앙 정렬 & 둥둥 효과 CSS (그림 안 깨지게 수정) ---
st.set_page_config(page_title="로즈샘 고민상담소", layout="centered")

st.markdown("""
    <style>
    /* 1. 사이드바 제거 및 전체 여백 초기화 */
    [data-testid="stSidebar"] { display: none; }
    
    /* 2. 최상위 컨테이너 강제 중앙 정렬 */
    .stApp {
        display: flex;
        justify-content: center;
    }
    .main .block-container {
        max-width: 600px !important;
        margin: 0 auto !important;
        padding-top: 3rem !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        text-align: center !important;
    }

    /* 3. 이미지(로즈샘) 정중앙 고정 및 둥둥 애니메이션 */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        animation: float_rose 3s ease-in-out infinite !important;
    }
    
    [data-testid="stImage"] img {
        width: 220px !important;
    }

    @keyframes float_rose {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-25px); }
        100% { transform: translateY(0px); }
    }

    /* 4. 입력창 및 버튼 너비 조정 */
    .stChatInputContainer { margin: 0 auto !important; width: 100% !important; }
    .stButton > button { width: 100% !important; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. 세션 상태 관리 ---
if "page" not in st.session_state: st.session_state.page = "profile"
if "messages" not in st.session_state: st.session_state.messages = []
if "rose_state" not in st.session_state: st.session_state.rose_state = "rose_idle.png"

# --- 6. 프로필 설정 페이지 (MBTI & 난이도 추가) ---
if st.session_state.page == "profile":
    # st.image를 다시 사용해서 그림 깨짐 방지
    st.image("rose_happy.png", width=220)
    st.markdown("## 로즈샘이 널 더 알고 싶어! 🌹")
    
    with st.form("profile"):
        name = st.text_input("이름")
        
        # MBTI 16가지 전체 추가
        mbti_list = ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", 
                     "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]
        mbti = st.selectbox("MBTI", mbti_list)
        
        # 난이도 추가
        level = st.radio("학습 난이도", ["초급", "중급", "고급"], horizontal=True)
        
        hobby = st.text_input("취미")
        goal = st.text_input("학습 목적")
        
        if st.form_submit_button("로즈샘 만나러 가기 ✨"):
            st.session_state.user_info = {"name": name, "mbti": mbti, "hobby": hobby, "goal": goal, "level": level}
            st.session_state.page = "mode_select"; st.rerun()

# --- 7. 모드 선택 페이지 ---
elif st.session_state.page == "mode_select":
    # st.image 사용
    st.image("rose_smart.png", width=220)
    st.markdown(f"### {st.session_state.user_info['name']}님, 반가워!")
    
    if st.button("🌹 친근한 반말 모드"): st.session_state.mode = "반말"; st.session_state.page = "chat"; st.rerun()
    if st.button("👑 정중한 존칭 모드"): st.session_state.mode = "존칭"; st.session_state.page = "chat"; st.rerun()

# --- 8. 채팅 페이지 ---
elif st.session_state.page == "chat":
    # st.image 사용
    st.image(st.session_state.rose_state, width=220)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    if prompt := st.chat_input("로즈샘에게 궁금한 걸 물어봐!"):
        st.messages.append({"role": "user", "content": prompt})
        st.session_state.rose_state = "rose_think.png"
        st.session_state.is_thinking = True
        st.rerun()

    if st.session_state.get("is_thinking"):
        response = get_rose_ai_response(st.session_state.messages[-1]["content"], st.session_state.user_info, st.session_state.mode)
        
        audio = generate_audio(response)
        if audio: st.audio(audio, format="audio/mp3", autoplay=True)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.rose_state = "rose_happy.png" if st.session_state.mode == "반말" else "rose_smart.png"
        st.session_state.is_thinking = False
        st.rerun()
