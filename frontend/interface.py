import streamlit as st
import httpx


st.set_page_config("Chat LLM", layout="wide")
st.title("Ask your question")


if st.button("Создать юзера", type="primary"):
    try:
        response = httpx.post("http://backend:8081/users/", timeout=5.0)
        response.raise_for_status()
        data = response.json()
        created_time = data.get("create_at", "err")
        st.success(f"Время создания: {created_time}")
        
    except httpx.HTTPStatusError as e:
        st.error(f"{e.response.text}")
    except httpx.RequestError as e:
        st.error(f"{e}")
    except Exception as e:
        st.error(f"{e}")