import streamlit as st
from groq import Groq
import requests
import re
import base64

# [1] 디자인 (럭셔리 스타일 고정)
st.set_page_config(page_title="Jenny's VIP K-Academy", page_icon="🐆", layout="wide")
st.markdown("""
    <style>
    .stApp { 
        background-image: url('https://img.freepik.com/premium-photo/luxury-pink-gold-leopard-print-pattern-background_911061-163.jpg'); 
        background-size: cover; background-position: center; background-attachment: fixed; 
    }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.85) !important; border-radius: 15px; border: 2px solid #FFD700; }
    .english { color: #00BFFF !important; font-weight: bold !important; } 
    p, span, div { color: #000 !important; font-weight: 800 !important; }
    .hidden-audio { display: none; }
    </style>
    """, unsafe_allow_html=True)

# [2] API 연결
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"].strip()
    ELEVEN_KEY = st.secrets["ELEVENLABS_API_KEY"].strip()
    VOICE_ID = st.secrets["VOICE_ID"].strip()
    client = Groq(api_key=GROQ_KEY)
except Exception as e:
    st.error(f"🚨 Secrets Error: {e}"); st.stop()

# [3] 세션 초기화
if "messages" not in st.session_state: st.session_state.messages = []
if "learned_exps" not in st.session_state: st.session_state.learned_exps = []
if "summary_mode" not in st.session_state: st.session_state.summary_mode = False

# [4] 입학 신청서
if "user_info" not in st.session_state:
    st.title("🐆 Welcome to Jenny's VIP K-Academy")
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Name", value="maykim")
        role = st.selectbox("Your Goal", ["K-드라마 대사 배우기", "K-팝 가사 이해하기", "한국 여행 실전 회화", "비즈니스 한국어", "한국 친구와 수다 떨기"])
    with c2:
        level = st.select_slider("Korean Level", options=["Beginner", "Intermediate", "Advanced"])
        interest = st.text_area("Interests", placeholder="e.g. BTS, Squid Game, K-BBQ...")
    if st.button("Start Learning Korean! 🏄‍♀️"):
        if name and interest:
            st.session_state.user_info = {"name": name, "role": role, "level": level, "interest": interest}
            st.rerun()
    st.stop()

user = st.session_state.user_info

# ⭐ [요약 모드]
if st.session_state.summary_mode:
    st.balloons()
    st.title("🎓 Today's K-Study Recap")
    
    if not st.session_state.messages:
        st.warning("No conversation to summarize, Bestie! 😅")
    else:
        with st.spinner("Jenny is wrapping up your K-lesson... ✍️"):
            try:
                sum_res = client.chat.completions.create(
                    messages=[{"role": "system", "content": "너는 럭셔리 한국어 튜터 제니야. 오늘 배운 내용을 3줄의 영어 평서문으로 요약하고, 핵심 한국어 표현 3개를 '한국어 - 영어뜻' 형식으로 정리해줘. 한자/일어/특수태그 절대 금지."}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    model="llama-3.3-70b-versatile",
                )
                raw_summary = sum_res.choices[0].message.content
                clean_summary = re.sub(r'\[Slang:.*?\]|\[\[표현:.*?\]\]|<.*?>|[一-龥ぁ-ゔァ-ヶー]', '', raw_summary)
                
                st.success(f"You nailed Korean today, {user['name']}! 🥂")
                st.info(f"### 📝 Summary & Key Points\n{clean_summary}")
            except Exception as e:
                st.error(f"Summary Error: {e}")

    if st.button("Back to Chat 🏄‍♀️"):
        st.session_state.summary_mode = False
        st.rerun()
    st.stop()

# [5] 사이드바
with st.sidebar:
    st.title(f"🐆 {user['name']}'s Studio")
    v_speed = st.slider("🗣️ Voice Speed", 0.5, 2.0, 1.2, 0.1) # 한국어는 조금 천천히 1.2
    if st.button("🏁 수업 종료 및 요약하기"):
        st.session_state.summary_mode = True
        st.rerun()
    st.divider()
    st.subheader("📚 Today's K-Expressions")
    for e in list(dict.fromkeys(st.session_state.learned_exps)):
        st.write(f"✨ {e}")

# [6] 시스템 지침 (한국어 선생님 버전으로 교체)
JENNY_SYSTEM = f"""너는 24세 재미교포 출신 한국어 튜터 제니야. 한국어와 영어를 완벽하게 해.
학습자 레벨: {user['level']}. 목적: {user['role']}
[Rules]
1. 기본적으로 한국어로 대화하되, 학습자가 이해 못할 것 같으면 영어로 보충 설명해줘.
2. 'Bestie'라고 불러줘. 아주 친근하고 힙한 톤을 유지해.
3. 한국어 슬랭이나 유행어는 **굵게**, 끝에 [Slang: 단어 - <span class='english'>영어뜻</span>] 추가.
4. 핵심 표현은 [[표현: 한국어 - <span class='english'>영어뜻</span>]] 형식. 영어 뜻은 <span class='english'> </span> 태그 필수.
5. 한자/일어 사용 절대 금지. 오직 한글과 영어만 사용."""

# 로그 출력
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.markdown(m["display_content"], unsafe_allow_html=True)
            if m.get("audio_b64"): st.audio(base64.b64decode(m["audio_b64"]), format="audio/mp3")

# [7] 대화 로직
prompt = st.chat_input(f"Hi {user['name']}! Ready to learn Korean?")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt, "display_content": prompt})
    with st.chat_message("user"): st.write(prompt)

    try:
        with st.spinner("Jenny is thinking in Korean..."):
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": JENNY_SYSTEM}] + 
                         [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                model="llama-3.3-70b-versatile",
            )
            raw_ans = res.choices[0].message.content
            ans = re.sub(r'[一-龥ぁ-ゔァ-ヶー]', '', raw_ans) # 한자/일어 제거
            
            # 표현 추출 (한국어 표현)
            exps = re.findall(r'\[\[표현:\s*(.*?)\s*\]\]', ans)
            for e in exps:
                clean_e = re.sub(r'<.*?>|한국어\s*[:|-]\s*', '', e).strip()
                if clean_e and clean_e not in st.session_state.learned_exps:
                    st.session_state.learned_exps.append(clean_e)

            with st.chat_message("assistant"):
                display_ans = ans.replace("[[표현:", "⭐ **K-Exp**:").replace("]]", "")
                st.markdown(display_ans, unsafe_allow_html=True)
                
                # TTS는 이제 한국어를 읽어줌
                # 영어와 태그는 제외하고 한글 위주로 읽도록 정제
                v_text = re.sub(r'<.*?>|\[.*?\]|[a-zA-Z]+', '', ans).strip()
                audio_b64 = None
                if v_text:
                    v_res = requests.post(
                        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
                        headers={"xi-api-key": ELEVEN_KEY},
                        json={"text": v_text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5}}
                    )
                    if v_res.status_code == 200:
                        audio_data = v_res.content
                        audio_b64 = base64.b64encode(audio_data).decode()
                        st.audio(audio_data, format="audio/mp3")
                        md = f"""<audio id="ja" class="hidden-audio" autoplay><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>
                            <script>var a=document.getElementById('ja'); a.playbackRate={v_speed}; a.play();</script>"""
                        st.markdown(md, unsafe_allow_html=True)
            
            st.session_state.messages.append({"role": "assistant", "content": ans, "display_content": display_ans, "audio_b64": audio_b64})
    except Exception as e:
        st.error(f"🚨 Error: {e}")
