import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time

# --- 1. 보안 설정 및 보이스 설정 ---
try:
    # 깃허브 Secrets에 등록된 키들을 가져옵니다.
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
    VOICE_ID = st.secrets.get("VOICE_ID", "EXAVITQu4vr4xnNLMQer") 
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception as e:
    st.error("Secrets 설정(API 키 등)을 확인해 주세요!")
    st.stop()

# --- 2. 뇌(LLM) 로직: Groq API ---
def get_llm_response(prompt, user_info, mode):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    # 메이킴님의 정보를 기억하는 로즈샘 페르소나
    persona = f"""
    당신은 한국어 튜터 '로즈샘'입니다. 사용자의 이름은 {user_info['name']}, 
    MBTI는 {user_info['mbti']}, 취미는 {user_info['hobby']}, 목적은 {user_info['goal']}입니다.
    {mode} 모드로 대화하며 '개꿀', '갓벽' 등의 표현을 섞어 쾌활하게 말하세요.
    사용자가 한국어 문법이나 받침을 틀리면 다정하게 교정해 주세요.
    """
    
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "system", "content": persona}, {"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()['choices'][0]['message']['content']

# --- 3. 음성 생성 함수 (소리 안 남 방지 보강) ---
def generate_audio(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.75}
    }
    
    res = requests.post(url, json=data, headers=headers)
    if res.status_code == 200:
        return res.content
    else:
        # 에러가 나면 화면에 작게 표시해서 디버깅을 도와줍니다.
        st.warning(f"음성 생성 실패: {res.status_code}")
        return None

# --- [이후 레이아웃 및 둥둥 떠있는 CSS 로직은 이전과 동일하게 고정합니다] ---
# (생략된 디자인 로직은 위에서 드린 '강제 중앙 정렬' 코드를 그대로 쓰시면 됩니다!)

# --- 채팅 및 실행 부분 ---
if st.session_state.get("is_thinking"):
    response = get_llm_response(st.session_state.last_prompt, st.session_state.user_info, st.session_state.mode)
    
    # 음성 생성 시도
    audio_bytes = generate_audio(response)
    
    if audio_bytes:
        # autoplay=True가 안 먹힐 때를 대비해 오디오 플레이어를 명시적으로 보여줍니다.
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.is_thinking = False
    st.rerun()
