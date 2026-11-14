import streamlit as st
import httpx
import uuid
import os


BASE_URL = "http://backend:8081"

st.set_page_config(page_title="Chat LLM", layout="wide")
st.title("🤖 Локальный ChatGPT")


if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []


def load_history(session_id: int):
    try:
        resp = httpx.get(f"{BASE_URL}/sessions/{session_id}/messages", timeout=5.0)
        resp.raise_for_status()
        st.session_state.messages = resp.json()
    except Exception as e:
        st.error(f"Ошибка загрузки: {e}")


with st.sidebar:
    st.header("Ваши чаты")
    
    if st.button("Новый чат", use_container_width=True, type="primary"):
        try:
            resp = httpx.post(
                f"{BASE_URL}/sessions", 
                json={"title": f"Chat {uuid.uuid4().hex[:4]}"},
                timeout=5.0
            )
            resp.raise_for_status()
            st.session_state.session_id = resp.json()["id"]
            st.session_state.messages = []
            st.rerun()
        except Exception as e:
            st.error(f"Ошибка создания: {e}")
            
    st.divider()


    try:
        sessions_resp = httpx.get(f"{BASE_URL}/sessions", timeout=5.0)
        sessions_resp.raise_for_status()
        sessions = sessions_resp.json()
        
        if not sessions:
            st.info("У вас пока нет чатов.")
        else:
            for s in sessions:
                sess_id = s["id"]
                sess_title = s["title"]
                is_current = (sess_id == st.session_state.session_id)
                
                btn_type = "primary" if is_current else "secondary"
                label = f"{sess_title}" if is_current else f"{sess_title}"
                
                if st.button(label, key=f"btn_{sess_id}", use_container_width=True, type=btn_type):
                    if not is_current:
                        st.session_state.session_id = sess_id
                        load_history(sess_id)
                        st.rerun()

    except Exception as e:
        st.error(f"Ошибка соединения с API: {e}")


if st.session_state.session_id is None:
    st.info("Создайте новый чат или выберите существующий в боковой панели.")
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Напишите сообщение..."):

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty() 
            full_response = ""
            
            try:
                with httpx.stream(
                    "POST", 
                    f"{BASE_URL}/chat/{st.session_state.session_id}", 
                    json={"prompt": prompt},
                    timeout=60.0
                ) as response:
                    
                    if response.status_code != 200:
                        st.error(f"Ошибка сервера: {response.read().decode()}")
                    else:
                        for chunk in response.iter_text():
                            if chunk:
                                full_response += chunk
                                placeholder.markdown(full_response + "▌")
                        
                        placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                        
            except Exception as e:
                st.error(f"Ошибка соединения: {e}")
