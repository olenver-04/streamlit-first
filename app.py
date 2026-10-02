import streamlit as st

# -----------------------------
# НАСТРОЙКИ СТРАНИЦЫ
# -----------------------------

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)


# -----------------------------
# СТИЛИ
# -----------------------------

st.markdown("""
<style>

.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

h1 {
    text-align: center;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# БОКОВАЯ ПАНЕЛЬ
# -----------------------------

with st.sidebar:

    st.title("🤖 AI Assistant")

    st.write("""
    Простой AI-чат, созданный на:

    - Python
    - Streamlit
    - OpenAI API
    """)

    st.divider()

    if st.button("🗑 Очистить чат", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Версия 1.0")


# -----------------------------
# ЗАГОЛОВОК
# -----------------------------

st.title("🤖 AI Assistant")

st.markdown(
    '<div class="subtitle">Ваш персональный AI-помощник</div>',
    unsafe_allow_html=True
)


# -----------------------------
# ИСТОРИЯ СООБЩЕНИЙ
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# Приветственное сообщение
if len(st.session_state.messages) == 0:

    with st.chat_message("assistant"):
        st.write(
            "Привет! 👋 Я AI Assistant. "
            "Напиши мне сообщение."
        )


# Показываем историю сообщений
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# ПОЛЕ ВВОДА
# -----------------------------

prompt = st.chat_input(
    "Введите сообщение..."
)


# -----------------------------
# ОБРАБОТКА СООБЩЕНИЯ
# -----------------------------

if prompt:

    # Сохраняем сообщение пользователя
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Показываем сообщение пользователя
    with st.chat_message("user"):
        st.markdown(prompt)


    # Пока тестовый ответ
    answer = (
        f"Вы написали: **{prompt}**\n\n"
        "Сейчас я работаю в тестовом режиме. "
        "На следующем этапе мы подключим настоящий AI."
    )


    # Показываем ответ
    with st.chat_message("assistant"):
        st.markdown(answer)


    # Сохраняем ответ
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
