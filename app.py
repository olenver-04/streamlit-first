import streamlit as st


# =========================================================
# СТРАНИЦЫ
# =========================================================

home = st.Page(
    "home.py",
    title="AI Assistant",
    icon="🤖",
    default=True
)

code_mentor = st.Page(
    "pages/AI_CodeMentor.py",
    title="AI-CodeMentor",
    icon="💻"
)

friends = st.Page(
    "pages/2_Мои_любимки.py",
    title="Мои любимки <3",
    icon="❤️"
)


# =========================================================
# НАВИГАЦИЯ
# =========================================================

page = st.navigation(
    {
        "Проекты": [
            home,
            code_mentor
        ],

        "Для друзей ❤️": [
            friends
        ]
    }
)


page.run()
