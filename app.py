import streamlit as st

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

page = st.navigation(
    {
        "Проекты": [
            home,
            code_mentor
        ]
    }
)

page.run()
