FROM python:3.12-slim

WORKDIR /frontend

COPY interface.py ./

RUN pip install streamlit httpx
EXPOSE 8051

CMD [ "streamlit", "run", "interface.py", "--server.port=8051", "--server.address=0.0.0.0"]