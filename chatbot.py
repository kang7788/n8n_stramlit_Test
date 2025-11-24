import streamlit as st
import requests

# n8n Webhook URL
N8N_URL = "https://khg6975.app.n8n.cloud/webhook/14046dd1-6fc9-4299-ab22-b565e626c351"

st.set_page_config(page_title="n8n 챗봇", page_icon="🤖")
st.title("🤖 n8n Webhook 기반 챗봇")

# 세션 저장소 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 채팅 입력창
user_input = st.chat_input("메시지를 입력하세요")

if user_input:
    # 사용자 질문을 화면에 표시
    st.session_state.chat_history.append(("user", user_input))

    try:
        params = {"chatInput": user_input, "sessionId": "abc"}
        r = requests.get(N8N_URL, params=params, timeout=60)
        data = r.json()

        # output 필드 체크
        if "output" in data:
            bot_reply = data["output"]
        else:
            bot_reply = f"⚠️ 응답에 'output' 키가 없습니다.\n\n받은 데이터: {data}"

    except Exception as e:
        bot_reply = f"❌ 오류 발생: {e}"

    # 챗봇 응답 표시
    st.session_state.chat_history.append(("bot", bot_reply))

# 채팅 UI 렌더링
for role, msg in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user"):
            st.write(msg)
    else:
        with st.chat_message("assistant"):
            st.write(msg)
