import streamlit as st
from openai import OpenAI

# --------------------------------
# НАСТРОЙКИ СТРАНИЦЫ
# --------------------------------

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)


# --------------------------------
# СТИЛЬ
# --------------------------------

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


# --------------------------------
# ПРОВЕРКА API-КЛЮЧА
# --------------------------------

if "OPENAI_API_KEY" not in st.secrets:

    st.error("API-ключ OpenAI не найден в Streamlit Secrets.")
    st.stop()


# --------------------------------
# OPENAI
# --------------------------------

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# --------------------------------
# ИСТОРИЯ ЧАТА
# --------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# --------------------------------
# БОКОВОЕ МЕНЮ
# --------------------------------

with st.sidebar:

    st.title("🤖 AI Assistant")

    st.write("""
    AI-помощник на базе:

    - Python
    - Streamlit
    - OpenAI API
    - GPT-6 Luna
    """)

    st.divider()

    if st.button(
        "🗑 Очистить чат",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption("AI Assistant v2.0")


# --------------------------------
# ЗАГОЛОВОК
# --------------------------------

st.title("🤖 AI Assistant")

st.markdown(
    '<div class="subtitle">'
    'Задайте любой вопрос'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------
# ПРИВЕТСТВИЕ
# --------------------------------

if len(st.session_state.messages) == 0:

    with st.chat_message("assistant"):

        st.write("""
        Привет! 👋

        Я AI Assistant.

        Можешь спросить меня о программировании,
        учёбе, технологиях или любой другой теме.
        """)


# --------------------------------
# ПОКАЗЫВАЕМ ИСТОРИЮ
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# --------------------------------
# ВВОД СООБЩЕНИЯ
# --------------------------------

prompt = st.chat_input(
    "Введите сообщение..."
)


# --------------------------------
# ЗАПРОС К AI
# --------------------------------

if prompt:

    # Сохраняем сообщение пользователя

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })


    # Показываем сообщение пользователя

    with st.chat_message("user"):

        st.markdown(prompt)


    # Ответ AI

    with st.chat_message("assistant"):

        with st.spinner("Думаю..."):

            try:

                response = client.responses.create(

                    model="gpt-6-luna",

                    reasoning={
                        "effort": "low"
                    },

                    instructions="""
                    Ты полезный AI-помощник.

                    Отвечай понятно и по существу.
                    Если пользователь спрашивает
                    о программировании, объясняй
                    код простыми словами и приводи
                    примеры.
                    """,

                    input=st.session_state.messages,

                    max_output_tokens=1500
                )


                answer = response.output_text

                st.markdown(answer)


                # Сохраняем ответ AI

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })


            except Exception as error:

                st.error(
                    "Не удалось получить ответ от OpenAI."
                )

                st.code(str(error))
