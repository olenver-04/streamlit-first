import streamlit as st

# Настройки страницы
st.set_page_config(
    page_title="Denver Site",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Небольшой CSS для красоты
st.markdown("""
<style>
    .main-title {
        font-size: 55px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
    }

    .subtitle {
        font-size: 21px;
        text-align: center;
        color: gray;
        margin-bottom: 40px;
    }

    .card {
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #444;
        margin-bottom: 15px;
    }

    .card h3 {
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# БОКОВОЕ МЕНЮ
# -----------------------------

with st.sidebar:

    st.title("🚀 Denver Site")

    st.write("Навигация")

    page = st.radio(
        "Выберите страницу",
        [
            "🏠 Главная",
            "👨‍💻 Обо мне",
            "🛠 Возможности",
            "📩 Связаться"
        ]
    )

    st.divider()

    st.caption("Сделано на Python + Streamlit")


# -----------------------------
# ГЛАВНАЯ
# -----------------------------

if page == "🏠 Главная":

    st.markdown(
        '<div class="main-title">Добро пожаловать 🚀</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Мой первый полноценный сайт на Python и Streamlit</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <h3>🐍 Python</h3>
        <p>Весь сайт работает на языке Python.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h3>⚡ Streamlit</h3>
        <p>Интерфейс создаётся без сложного JavaScript.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <h3>☁️ Cloud</h3>
        <p>Позже опубликуем сайт в интернете.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.header("Попробуй сайт")

    name = st.text_input(
        "Введите ваше имя",
        placeholder="Например: Denver"
    )

    if st.button("Поздороваться", type="primary"):

        if name:
            st.success(f"Привет, {name}! Сайт работает 🎉")

        else:
            st.warning("Введите имя.")


# -----------------------------
# ОБО МНЕ
# -----------------------------

elif page == "👨‍💻 Обо мне":

    st.title("👨‍💻 Обо мне")

    col1, col2 = st.columns([1, 2])

    with col1:

        st.markdown("""
        ## 👤 Denver

        Начинающий разработчик.

        Изучаю:

        - Python
        - Java
        - Web-разработку
        - AI
        - Streamlit
        """)

    with col2:

        st.subheader("Мои навыки")

        st.write("Python")
        st.progress(70)

        st.write("Java")
        st.progress(60)

        st.write("HTML / CSS")
        st.progress(50)

        st.write("AI")
        st.progress(65)


# -----------------------------
# ВОЗМОЖНОСТИ
# -----------------------------

elif page == "🛠 Возможности":

    st.title("🛠 Что можно добавить на сайт")

    col1, col2 = st.columns(2)

    with col1:

        st.info("""
        🤖 AI-помощник

        Можно подключить API искусственного интеллекта
        и сделать чат прямо на сайте.
        """)

        st.info("""
        📊 Графики

        Streamlit отлично подходит для отображения
        статистики и аналитики.
        """)

    with col2:

        st.info("""
        📁 Загрузка файлов

        Пользователь сможет загружать PDF,
        изображения, Excel и другие файлы.
        """)

        st.info("""
        🗄 База данных

        Можно подключить SQLite,
        PostgreSQL или MySQL.
        """)

    st.divider()

    st.subheader("Пример статистики")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Посетители",
        "1 240",
        "+12%"
    )

    col2.metric(
        "Пользователи",
        "523",
        "+8%"
    )

    col3.metric(
        "Проекты",
        "14",
        "+3"
    )


# -----------------------------
# ОБРАТНАЯ СВЯЗЬ
# -----------------------------

elif page == "📩 Связаться":

    st.title("📩 Обратная связь")

    st.write("Заполните форму:")

    with st.form("contact_form"):

        name = st.text_input("Имя")

        email = st.text_input("Email")

        message = st.text_area(
            "Сообщение",
            height=150
        )

        submitted = st.form_submit_button(
            "Отправить",
            type="primary"
        )

        if submitted:

            if not name or not email or not message:

                st.warning(
                    "Заполните все поля."
                )

            else:

                st.success(
                    "Сообщение успешно отправлено!"
                )

                st.balloons()