# 🚀 vLLM Local ChatGPT

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![vLLM](https://img.shields.io/badge/vLLM-0.11.0-orange.svg?style=for-the-badge)](https://docs.vllm.ai/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/Nginx-1.25-009639.svg?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0+-2496ED.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

Полноценный, изолированный сервис для общения с локальными LLM.

---

## ⚠️ Требования к железу (Hardware Requirements)

> **ВНИМАНИЕ:** Для работы этого проекта **обязательна видеокарта NVIDIA** с поддержкой CUDA. 
> 
> По умолчанию в конфигурации используется модель `Qwen/Qwen2.5-1.5B-Instruct`, которой достаточно **~4-5 ГБ видеопамяти (VRAM)**. Если вы планируете использовать модели на 7B-8B параметров, вам потребуется минимум **8-10 ГБ VRAM** (или использование квантизации).
> 
> На системе должен быть установлен [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) для проброса GPU в Docker.

---

## 🏗 Архитектура проекта

Проект построен по принципу **единой точки входа (Reverse Proxy)**. Наружу открыт только порт `80` (Nginx). Все остальные сервисы изолированы в приватной Docker-сети и недоступны из интернета.

1. **Nginx** принимает запросы на порту 80 и проксирует их.
2. **Streamlit** отдает фронтенд (чат-интерфейс).
3. **FastAPI** обрабатывает бизнес-логику, хранит историю и общается с vLLM.
4. **vLLM** (на базе Continuous Batching и PagedAttention) выполняет генерацию токенов.
5. **PostgreSQL** хранит сессии и историю сообщений.

---

## 🛠 Стек технологий

*   **Backend:** Python 3.12, FastAPI, Async SQLAlchemy, Alembic, httpx, Pydantic.
*   **LLM Engine:** vLLM.
*   **Frontend:** Streamlit.
*   **Database:** PostgreSQL 16 + pgAdmin.
*   **Infrastructure:** Docker, Docker Compose, Nginx.
*   **Package Manager:** uv.

---

## ⚙️ Переменные окружения (.env)

Перед запуском скопируйте шаблон `.env.example` в `.env`:
```bash
cp .env.example .env
```

### Настройка LLM и GPU:
*   `MODEL_NAME` — ID модели из HuggingFace (например, `meta-llama/Llama-3.2-1B-Instruct`, `Qwen/Qwen2.5-7B-Instruct-AWQ`).
*   `HF_TOKEN` — ваш токен HuggingFace.
*   `VLLM_URL` — внутренний адрес движка (по умолчанию `http://vllm:8000`).
*   `GPU_UTILIZATION` — процент видеопамяти от общего объема, который разрешено занимать vLLM. По умолчанию 0.7.
*   `VLLM_QUANTIZATION` — метод квантизация. Если переменная пустая, модель загружается в стандартном формате.

### Настройка базы данных:
*   `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` — креды для базы.
*   `POSTGRES_HOST` — имя сервиса в Docker (оставьте `postgres`).
*   `POSTGRES_PORT` — порт БД (по умолчанию `5432`).

### Настройка pgAdmin (Веб-интерфейс для БД):
*   `PGADMIN_DEFAULT_EMAIL`, `PGADMIN_DEFAULT_PASSWORD` — логин/пароль для входа в pgAdmin.

### Настройка фронтенда:
*   `BACKEND_URL` — адрес API для фронтенда (по умолчанию `http://backend:8081`).


## 🚀 Быстрый старт (Инструкция по запуску)

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/your-username/vllm-local-chat.git
cd vllm-local-chat

docker compose up -d --build
docker compose exec backend alembic -c app/alembic.ini upgrade head
```
### Опционально: Выбор другой модели

По умолчанию скачивается модель из файла `.env`. Если вы хотите быстро протестировать другую модель без изменения файлов, переопределите переменную окружения прямо при запуске:


```bash
MODEL_NAME="Qwen/Qwen2.5-7B-Instruct-AWQ" docker compose up --build
```